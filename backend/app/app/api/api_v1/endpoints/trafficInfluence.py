import logging
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo.database import Database
from sqlalchemy.orm import Session
from app import models, schemas
from app.api import deps
from app.crud import crud_mongo, user, ue
from app.db.session import client
from .utils import add_notifications
from app.core.config import trafficInfluenceSettings


router = APIRouter()
db_collection= 'TrafficInfluence'

@router.get("/{afId}/subscriptions", response_model=List[schemas.TrafficInfluSub])
def read_active_subscriptions(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Read all active subscriptions
    """ 
    db_mongo = client.fastapi
    
    # Filter the subscriptions related with the afID
    retrieved_docs = [
        doc
        for doc
        in crud_mongo.read_all(db_mongo, db_collection, current_user.id)
        if doc["afId"] == afId
    ]
    
    #Check if there are any active subscriptions
    if not retrieved_docs:
        raise HTTPException(status_code=404, detail="There are no active subscriptions")
    
    http_response = JSONResponse(content=retrieved_docs, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

#Callback 

trafficInf_callback_router = APIRouter()

@trafficInf_callback_router.post("{$request.body.notificationDestination}",response_class=Response)
def trafficInf_notification(body: schemas.EventNotification):
    pass

@router.post("/{afId}/subscriptions", responses={201: {"model" : schemas.TrafficInfluSub}}, callbacks=trafficInf_callback_router.routes)
def create_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    db: Session = Depends(deps.get_db),
    item_in: schemas.TrafficInfluSubCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Create new subscription.
    """
    db_mongo = client.fastapi
    
    json_data = jsonable_encoder(item_in)
    json_data.update({'owner_id' : current_user.id})
    json_data.update({'afId' : afId})
    
    inserted_doc = crud_mongo.create(db_mongo, db_collection, json_data)
    
    #Create the reference resource and location header
    link = str(http_request.url.path) + '/' + str(inserted_doc.inserted_id)
    response_header = {"location" : link}

    #Update the subscription with the new resource (link) and return the response (+response header)
    crud_mongo.update_new_field(
        db_mongo,
        db_collection,
        inserted_doc.inserted_id,
        {
            "link" : link,
            "id": str(inserted_doc.inserted_id)
        }
    )
    
    #Retrieve the updated document | UpdateResult is not a dict
    updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, inserted_doc.inserted_id)
    updated_doc.pop("owner_id") #Remove owner_id from the response
    
    # Dynamic Slicing
    if item_in.snssai and item_in.trafficFilters:
        sst = item_in.snssai.sst
        flowd_id = item_in.trafficFilters[0].flowId
        
        # Select the Profile
        traffic_filters = trafficInfluenceSettings\
            .traffic_influence_characteristics["traffic_filters_mapping"]
        slice_profile = traffic_filters[f"sst-{sst}:flowid-{flowd_id}"]
        
        print(f"Will Apply the slice profile {slice_profile}")
        
        # Todo: Make Request to Network Slice
        
        # if everything went accordingly and the slicing api returns a 200
        updated_doc["sliceProfileApplied"] = True
        

    http_response = JSONResponse(content=updated_doc, status_code=201, headers=response_header)
    add_notifications(http_request, http_response, False)

    return http_response

@router.get("/{afId}/subscriptions/{subscriptionId}", response_model=schemas.TrafficInfluSub)
def read_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Get subscription by id
    """
    db_mongo = client.fastapi
    

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    except Exception as ex:
        raise HTTPException(status_code=400, detail='Please enter a valid uuid (24-character hex string)')
    
    #Check if the document exists
    if not retrieved_doc or retrieved_doc['afId'] != afId:
        raise HTTPException(status_code=404, detail="Subscription not found")
    #If the document exists then validate the owner
    if not user.is_superuser(current_user) and (retrieved_doc['owner_id'] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    retrieved_doc.pop("owner_id")
    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response


@router.put("/{afId}/subscriptions/{subscriptionId}", response_model=schemas.TrafficInfluSub)
def update_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.TrafficInfluSubCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Update/Replace an existing subscription resource by id
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    except Exception as ex:
        raise HTTPException(status_code=400, detail='Please enter a valid uuid (24-character hex string)')
    
    #Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Subscription not found")
    #If the document exists then validate the owner
    if not user.is_superuser(current_user) and (retrieved_doc['owner_id'] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    #Update the document
    json_data = jsonable_encoder(item_in)
    crud_mongo.update_new_field(db_mongo, db_collection, subscriptionId, json_data)

    #Retrieve the updated document | UpdateResult is not a dict
    updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    updated_doc.pop("owner_id")
    
    http_response = JSONResponse(content=updated_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response


@router.delete("/{afId}/subscriptions/{subscriptionId}", response_model=schemas.TrafficInfluSub)
def delete_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Delete a subscription
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)
    except Exception as ex:
        raise HTTPException(status_code=400, detail='Please enter a valid uuid (24-character hex string)')


    #Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Subscription not found")
    #If the document exists then validate the owner
    if not user.is_superuser(current_user) and (retrieved_doc['owner_id'] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    crud_mongo.delete_by_uuid(db_mongo, db_collection, subscriptionId)
    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response