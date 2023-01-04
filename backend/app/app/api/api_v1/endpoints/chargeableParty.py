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

router = APIRouter()
db_collection= 'ChargeableParty'

@router.get("/{scsAsId}/transactions", response_model=List[schemas.ChargeableParty])
def read_active_subscriptions(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Read all active transactions
    """ 
    db_mongo = client.fastapi
    retrieved_docs = crud_mongo.read_all(db_mongo, db_collection, current_user.id)

    #Check if there are any active transactions
    if not retrieved_docs:
        raise HTTPException(status_code=404, detail="There are no active transactions")
    
    http_response = JSONResponse(content=retrieved_docs, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

#Callback 

chargParty_callback_router = APIRouter()
#TODO: checkar isto aqui da notificação
@chargParty_callback_router.post("{$request.body.notificationDestination}",response_class=Response)
def chargParty_notification(body: schemas.EventNotification):
    pass

@router.post("/{scsAsId}/transactions", responses={201: {"model" : schemas.ChargeableParty}}, callbacks=chargParty_callback_router.routes)
def create_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    db: Session = Depends(deps.get_db),
    item_in: schemas.ChargeablePartyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Create new subscription.
    """
    db_mongo = client.fastapi
    json_data = jsonable_encoder(item_in)
    json_data.update({'owner_id' : current_user.id})

    inserted_doc = crud_mongo.create(db_mongo, db_collection, json_data)

    #Create the reference resource and location header
    link = str(http_request.url) + '/' + str(inserted_doc.inserted_id)
    response_header = {"location" : link}

    #Update the subscription with the new resource (link) and return the response (+response header)
    crud_mongo.update_new_field(db_mongo, db_collection, inserted_doc.inserted_id, {"link" : link})
    
    #Retrieve the updated document | UpdateResult is not a dict
    updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, inserted_doc.inserted_id)

    updated_doc.pop("owner_id") #Remove owner_id from the response

    http_response = JSONResponse(content=updated_doc, status_code=201, headers=response_header)
    add_notifications(http_request, http_response, False)

    return http_response

@router.get("/{scsAsId}/transactions/{transactionId}", response_model=schemas.ChargeableParty)
def read_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    transactionId: str = Path(..., title="Identifier of the transaction"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Get transaction by id
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, transactionId)
    except Exception as ex:
        raise HTTPException(status_code=400, detail='Please enter a valid uuid (24-character hex string)')
    
    #Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Transaction not found")
    #If the document exists then validate the owner
    if not user.is_superuser(current_user) and (retrieved_doc['owner_id'] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    retrieved_doc.pop("owner_id")
    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

@router.put("/{scsAsId}/transactions/{transactionId}", response_model=schemas.ChargeableParty)
def update_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    transactionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.TrafficInfluSubCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Update/Replace an existing transaction resource by id
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, transactionId)
    except Exception as ex:
        raise HTTPException(status_code=400, detail='Please enter a valid uuid (24-character hex string)')
    
    #Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Transaction not found")
    #If the document exists then validate the owner
    if not user.is_superuser(current_user) and (retrieved_doc['owner_id'] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    #Update the document
    json_data = jsonable_encoder(item_in)
    crud_mongo.update_new_field(db_mongo, db_collection, transactionId, json_data)

    #Retrieve the updated document | UpdateResult is not a dict
    updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, transactionId)
    updated_doc.pop("owner_id")
    http_response = JSONResponse(content=updated_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

@router.delete("/{scsAsId}/transactions/{transactionId}", response_model=schemas.ChargeableParty)
def delete_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    transactionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Delete a subscription
    """
    db_mongo = client.fastapi

    try:
        retrieved_doc = crud_mongo.read_uuid(db_mongo, db_collection, transactionId)
    except Exception as ex:
        raise HTTPException(status_code=400, detail='Please enter a valid uuid (24-character hex string)')


    #Check if the document exists
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Transaction not found")
    #If the document exists then validate the owner
    if not user.is_superuser(current_user) and (retrieved_doc['owner_id'] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    crud_mongo.delete_by_uuid(db_mongo, db_collection, transactionId)
    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response