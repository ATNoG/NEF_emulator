from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Path, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import models, schemas, tools
from app.api import deps
from app.api.api_v1.endpoints.utils import add_notifications
from app.crud import crud_mongo, ue, user
from app.db.session import client
from app.schemas.monitoringevent import MonitoringType
from ue_movement import (
    handle_location_report_callback,
    handle_ue_reachability_callback,
    handle_loss_connectivity_callback,
)

from .ue_movement import (
    handle_location_report_callback,
    handle_loss_connectivity_callback,
    handle_ue_reachability_callback,
)
from .utils import ReportLogging

router = APIRouter()
router.route_class = ReportLogging
db_collection = "MonitoringEvent"


@router.get(
    "/{scsAsId}/subscriptions",
    response_model=List[schemas.MonitoringEventSubscription],
    responses={204: {"model": None}},
)
def read_active_subscriptions(
    *,
    scsAsId: str = Path(
        ...,
        title="The ID of the Netapp that read all the subscriptions",
        example="myNetapp",
    ),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:
    """
    Read all active subscriptions
    """
    db_mongo = client.fastapi

    retrieved_docs = crud_mongo.read_all(db_mongo, db_collection, current_user.id)
    temp_json_subs = (
        retrieved_docs.copy()
    )  # Create copy of the list (json_subs) -> you cannot remove items from a list while you iterating the list.

    for sub in temp_json_subs:
        sub_validate_time = tools.check_expiration_time(
            expire_time=sub.get("monitorExpireTime")
        )
        if not sub_validate_time:
            crud_mongo.delete_by_item(
                db_mongo, db_collection, "externalId", sub.get("externalId")
            )
            retrieved_docs.remove(sub)

    temp_json_subs.clear()

    if retrieved_docs:
        http_response = JSONResponse(content=retrieved_docs, status_code=200)
        add_notifications(http_request, http_response, False)
        return http_response

    return Response(status_code=204)


# Callback

monitoring_callback_router = APIRouter()


@monitoring_callback_router.post(
    "{$request.body.notificationDestination}",
    response_model=schemas.MonitoringEventReportReceived,
    status_code=200,
    response_class=Response,
)
def monitoring_notification(body: schemas.MonitoringNotification):
    pass


@router.post(
    "/{scsAsId}/subscriptions",
    response_model=schemas.MonitoringEventSubscription,
    responses={201: {"model": schemas.MonitoringEventSubscription}},
    callbacks=monitoring_callback_router.routes,
)
def create_subscription(
    *,
    scsAsId: str = Path(
        ...,
        title="The ID of the Netapp that creates a subscription",
        example="myNetapp",
    ),
    db: Session = Depends(deps.get_db),
    item_in: schemas.MonitoringEventSubscription,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:
    """
    Create new subscription.
    """
    db_mongo = client.fastapi

    UE = None
    if item_in.externalId:
        UE = ue.get_externalId(
            db=db, externalId=item_in.externalId.__root__, owner_id=current_user.id
        )

    # Because item_in puts default values to externalId and msisdn, even if none are specified.
    # Therefore we need to check if we already have the UE
    if not UE and item_in.msisdn:
        UE = ue.get_supi(db=db, supi=item_in.msisdn.__root__)

    if not UE:
        raise HTTPException(
            status_code=404, detail="UE with this external identifier doesn't exist"
        )

    isByMaxReports = item_in.maximumNumberOfReports

    isByExpireTime = item_in.monitorExpireTime is not None

    if not (isByExpireTime or isByMaxReports):
        raise HTTPException(
            status_code=400,
            detail="The request must contain either a maximumNumberOfReports or a monitorExpireTime",
        )

    # One time request
    if item_in.maximumNumberOfReports == 1:
        if item_in.monitoringType == MonitoringType.LOCATION_REPORTING:

            json_compatible_item_data = {}
            json_compatible_item_data["monitoringType"] = item_in.monitoringType
            json_compatible_item_data["externalId"] = (
                item_in.externalId and item_in.externalId.__root__
            )
            json_compatible_item_data["ipv4Addr"] = UE.ip_address_v4

            if UE.Cell:
                json_compatible_item_data["locationInfo"] = {
                    "cellId": UE.Cell.cell_id,
                    "gNBId": UE.Cell.gNB.gNB_id,
                }
            else:
                json_compatible_item_data["locationInfo"] = {
                    "cellId": None,
                    "gNBId": None,
                }

            http_response = JSONResponse(
                content=json_compatible_item_data, status_code=200
            )
            add_notifications(http_request, http_response, False)

            return http_response

        if (
            item_in.monitoringType == MonitoringType.LOSS_OF_CONNECTIVITY
            or item_in.monitoringType == MonitoringType.UE_REACHABILITY
        ):
            return JSONResponse(
                content=jsonable_encoder(
                    {
                        "title": "The requested parameters are out of range",
                        "invalidParams": {
                            "param": "maximumNumberOfReports",
                            "reason": '"maximumNumberOfReports" should be greater than 1 in case of LOSS_OF_CONNECTIVITY event',
                        },
                    }
                ),
                status_code=403,
            )

    # Subscription
    elif isByMaxReports or isByExpireTime:
        if item_in.monitoringType == MonitoringType.LOCATION_REPORTING:

            json_data = jsonable_encoder(item_in.dict(exclude_unset=True))
            json_data.update(
                {"owner_id": current_user.id, "ipv4Addr": UE.ip_address_v4}
            )

            inserted_doc = crud_mongo.create(db_mongo, db_collection, json_data)

            # Create the reference resource and location header
            link = str(http_request.url) + "/" + str(inserted_doc.inserted_id)
            response_header = {"location": link}

            # Update the subscription with the new resource (link) and return the response (+response header)
            crud_mongo.update_new_field(
                db_mongo, db_collection, inserted_doc.inserted_id, {"link": link}
            )

            # Retrieve the updated document | UpdateResult is not a dict
            updated_doc = crud_mongo.read_uuid(
                db_mongo, db_collection, inserted_doc.inserted_id
            )
            updated_doc.pop("owner_id")

            if item_in.immediateRep:
                handle_location_report_callback(updated_doc, UE)

            http_response = JSONResponse(
                content=updated_doc, status_code=201, headers=response_header
            )
            add_notifications(http_request, http_response, False)

            return http_response
        if (
            item_in.monitoringType == MonitoringType.LOSS_OF_CONNECTIVITY
            or item_in.monitoringType == MonitoringType.UE_REACHABILITY
        ):
            # Check if subscription with externalid && monitoringType exists
            if crud_mongo.read_by_multiple_pairs(
                db_mongo,
                db_collection,
                externalId=item_in.externalId and item_in.externalId.__root__,
                monitoringType=item_in.monitoringType,
            ):
                raise HTTPException(
                    status_code=409,
                    detail=f"There is already an active subscription for UE with external id {item_in.externalId} - Monitoring Type = {item_in.monitoringType}",
                )

            json_data = jsonable_encoder(item_in.dict(exclude_unset=True))
            json_data.update(
                {"owner_id": current_user.id, "ipv4Addr": UE.ip_address_v4}
            )

            inserted_doc = crud_mongo.create(db_mongo, db_collection, json_data)

            if (
                item_in.immediateRep
                and item_in.monitoringType == MonitoringType.LOSS_OF_CONNECTIVITY
            ):
                handle_loss_connectivity_callback(inserted_doc, UE)

            elif (
                item_in.immediateRep
                and item_in.monitoringType == MonitoringType.UE_REACHABILITY
            ):
                handle_ue_reachability_callback(inserted_doc, UE)

            # Create the reference resource and location header
            link = str(http_request.url) + "/" + str(inserted_doc.inserted_id)
            response_header = {"location": link}

            # Update the subscription with the new resource (link) and return the response (+response header)
            crud_mongo.update_new_field(
                db_mongo, db_collection, inserted_doc.inserted_id, {"link": link}
            )

            # Retrieve the updated document | UpdateResult is not a dict
            updated_doc = crud_mongo.read_uuid(
                db_mongo, db_collection, inserted_doc.inserted_id
            )
            updated_doc.pop("owner_id")

            http_response = JSONResponse(
                content=updated_doc, status_code=201, headers=response_header
            )
            add_notifications(http_request, http_response, False)

            return http_response


@router.put(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    response_model=schemas.MonitoringEventSubscription,
)
def update_subscription(
    *,
    scsAsId: str = Path(
        ...,
        title="The ID of the Netapp that creates a subscription",
        example="myNetapp",
    ),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.MonitoringEventSubscriptionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:
    """
    Update/Replace an existing subscription resource
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid uuid (24-character hex string)",
        )

    # Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Subscription not found")
    # If the document exists then validate the owner
    if not user.is_superuser(current_user) and (
        retrieved_doc["owner_id"] != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    sub_validate_time = tools.check_expiration_time(
        expire_time=retrieved_doc.get("monitorExpireTime")
    )

    if sub_validate_time:
        # Update the document
        json_data = jsonable_encoder(item_in)
        crud_mongo.update_new_field(db_mongo, db_collection, subscriptionId, json_data)

        # Retrieve the updated document | UpdateResult is not a dict
        updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
        updated_doc.pop("owner_id")

        http_response = JSONResponse(content=updated_doc, status_code=200)
        add_notifications(http_request, http_response, False)
        return http_response
    else:
        crud_mongo.delete_by_uuid(db_mongo, db_collection, subscriptionId)
        raise HTTPException(status_code=403, detail="Subscription has expired")


@router.get(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    response_model=schemas.MonitoringEventSubscription,
)
def read_subscription(
    *,
    scsAsId: str = Path(
        ...,
        title="The ID of the Netapp that creates a subscription",
        example="myNetapp",
    ),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:
    """
    Get subscription by id
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid uuid (24-character hex string)",
        )

    # Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Subscription not found")
    # If the document exists then validate the owner
    if not user.is_superuser(current_user) and (
        retrieved_doc["owner_id"] != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    sub_validate_time = tools.check_expiration_time(
        expire_time=retrieved_doc.get("monitorExpireTime")
    )

    if sub_validate_time:
        retrieved_doc.pop("owner_id")
        http_response = JSONResponse(content=retrieved_doc, status_code=200)

        add_notifications(http_request, http_response, False)
        return http_response
    else:
        crud_mongo.delete_by_uuid(db_mongo, db_collection, subscriptionId)
        raise HTTPException(status_code=403, detail="Subscription has expired")


@router.delete(
    "/{scsAsId}/subscriptions/{subscriptionId}",
    response_model=schemas.MonitoringEventSubscription,
)
def delete_subscription(
    *,
    scsAsId: str = Path(
        ...,
        title="The ID of the Netapp that creates a subscription",
        example="myNetapp",
    ),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:
    """
    Delete a subscription
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    except Exception as ex:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid uuid (24-character hex string)",
        )

    # Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Subscription not found")
    # If the document exists then validate the owner
    if not user.is_superuser(current_user) and (
        retrieved_doc["owner_id"] != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    crud_mongo.delete_by_uuid(db_mongo, db_collection, subscriptionId)
    retrieved_doc.pop("owner_id")

    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response
