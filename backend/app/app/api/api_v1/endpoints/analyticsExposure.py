from typing import Any, List

from requests import status_codes
from app.schemas.analyticsExposure import (
    LocationArea5G,
    UeLocationInfo,
    AnalyticsEvent,
    UeMobilityExposure,
    AnalyticsData,
)
from app.schemas.monitoringevent import GeographicArea, GeographicalCoordinates, Point
from fastapi import APIRouter, Depends, HTTPException, Path, Response, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pymongo.database import Database
from app import models, schemas
from app.crud import crud_mongo, user, ue
from app.api import deps
from app import tools
from app.db.session import client
from app.api.api_v1.endpoints.utils import add_notifications

router = APIRouter()
db_collection = "AnalyticsExposure"


@router.get(
    "/{afId}/subscriptions",
    response_model=List[schemas.AnalyticsExposureSubsc],
    responses={204: {"model": None}},
)
def read_active_subscriptions(
    *,
    afId: str = Path(
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

    # Check if there are any active subscriptions
    if not retrieved_docs:
        raise HTTPException(status_code=404, detail="There are no active subscriptions")

    http_response = JSONResponse(content=retrieved_docs, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response


# #Callback

# analytics_exposure_callback_router = APIRouter()

# @analytics_exposure_callback_router.post("{$request.body.notificationDestination}", response_model=schemas.MonitoringEventReportReceived, status_code=200, response_class=Response)
# def analytics_exposure_notification(body: schemas.AnalyticsEventNotification):
#     pass


@router.post(
    "/{afId}/subscriptions",
    response_model=schemas.AnalyticsExposureSubsc,
    responses={201: {"model": schemas.AnalyticsExposureSubsc}},
)
def create_subscription(
    *,
    afId: str = Path(
        ...,
        title="The ID of the Netapp that creates a subscription",
        example="myNetapp",
    ),
    db: Session = Depends(deps.get_db),
    item_in: schemas.AnalyticsExposureSubscCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:
    """
    Create new subscription.
    """
    db_mongo = client.fastapi
    json_data = jsonable_encoder(item_in)
    json_data.update({"owner_id": current_user.id})

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

    updated_doc.pop("owner_id")  # Remove owner_id from the response

    http_response = JSONResponse(
        content=updated_doc, status_code=201, headers=response_header
    )
    add_notifications(http_request, http_response, False)

    return http_response


@router.put(
    "/{afId}/subscriptions/{subscriptionId}",
    response_model=schemas.AnalyticsExposureSubsc,
)
def update_subscription(
    *,
    afId: str = Path(
        ...,
        title="The ID of the Netapp that creates a subscription",
        example="myNetapp",
    ),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.AnalyticsExposureSubscCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:
    """
    Update/Replace an existing subscription resource by id
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

    # Update the document
    json_data = jsonable_encoder(item_in)
    crud_mongo.update_new_field(db_mongo, db_collection, subscriptionId, json_data)

    # Retrieve the updated document | UpdateResult is not a dict
    updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    updated_doc.pop("owner_id")
    http_response = JSONResponse(content=updated_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response


@router.get(
    "/{afId}/subscriptions/{subscriptionId}",
    response_model=schemas.MonitoringEventSubscription,
)
def read_subscription(
    *,
    afId: str = Path(
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

    retrieved_doc.pop("owner_id")
    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response


@router.delete(
    "/{afId}/subscriptions/{subscriptionId}",
    response_model=schemas.AnalyticsExposureSubsc,
)
def delete_subscription(
    *,
    afId: str = Path(
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
    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response


@router.post("/{afId}/fetch")
def fetch_analytics(
    *,
    db: Session = Depends(deps.get_db),
    afId: str = Path(
        ..., title="The ID of the Netapp that is fetching analytics", example="myNetapp"
    ),
    item_in: schemas.analyticsExposure.AnalyticsRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request,
) -> Any:

    db_mongo = client.fastapi

    if item_in.analyEvent != AnalyticsEvent.ueMobility:
        raise HTTPException(
            status_code=501, detail="This Analytics Event has not been implemented"
        )

    if not (
        item_in.tgtUe
        and any(
            [item_in.tgtUe.gpsi, item_in.tgtUe.anyUeInd, item_in.tgtUe.exterGroupId]
        )
    ):
        raise HTTPException(status_code=404, detail="No Target UE Specified")

    if not item_in.tgtUe.gpsi:
        raise HTTPException(status_code=501, detail="Not Implemented")

    user_equipment = None
    try:
        tgtUe: str = item_in.tgtUe.gpsi
        if tgtUe.startswith("msisdn-"):
            user_equipment = ue.get_supi(db, supi=tgtUe.split("msisdn-")[1])

        elif tgtUe.startswith("extid-"):
            user_equipment = ue.get_externalId(
                db, externalId=tgtUe.split("extid-")[1], owner_id=current_user.id
            )

    except Exception as ex:
        raise HTTPException(status_code=404, detail="The current device was not found")

    if user_equipment is None:
        raise HTTPException(status_code=404, detail="The current device was not found")

    point = Point(
        shape="POINT",
        point=GeographicalCoordinates(
            lat=user_equipment.latitude, lon=user_equipment.longitude
        ),
    )
    loc = LocationArea5G(geographicAreas=[point])
    locInfo = UeLocationInfo(loc=loc)
    mobilityExposure = UeMobilityExposure(
        locInfo=[locInfo],
    )
    response = AnalyticsData(ueMobilityInfos=[mobilityExposure], suppFeat="")
    return response
