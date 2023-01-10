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
db_collection= 'CpParameterProvisioning'

@router.get("/{scsAsId}/subscriptions", response_model=List[schemas.CpInfo])
def read_active_subscriptions(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Read all active subscriptions
    """ 
    db_mongo = client.fastapi
    retrieved_docs = crud_mongo.read_all(db_mongo, db_collection, current_user.id)

    #Check if there are any active subscriptions
    if not retrieved_docs:
        raise HTTPException(status_code=404, detail="There are no active subscriptions")
    
    http_response = JSONResponse(content=retrieved_docs, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

@router.post("/{scsAsId}/subscriptions", responses={201: {"model" : schemas.CpInfo}})
def create_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    db: Session = Depends(deps.get_db),
    item_in: schemas.CpInfoCreate,
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

@router.get("/{scsAsId}/subscriptions/{subscriptionId}", response_model=schemas.CpInfo)
def read_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
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
    if not retrieved_doc:
        raise HTTPException(status_code=404, detail="Subscription not found")
    #If the document exists then validate the owner
    if not user.is_superuser(current_user) and (retrieved_doc['owner_id'] != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    
    retrieved_doc.pop("owner_id")
    http_response = JSONResponse(content=retrieved_doc, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

@router.put("/{scsAsId}/subscriptions/{subscriptionId}", response_model=schemas.CpInfo)
def update_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.CpInfoCreate,
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

@router.delete("/{scsAsId}/subscriptions/{subscriptionId}", response_model=schemas.CpInfo)
def delete_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
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

@router.get("/{scsAsId}/subscriptions/{subscriptionId}/cpSets/{setId}", response_model=schemas.CpParameterSet)
def read_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    setId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Get cp parameter set by id
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
    
    parameterSet = None
    
    for cpParameterSet in retrieved_doc.get('cpParameterSets'):
        if cpParameterSet.get('setId') == setId:
            parameterSet = cpParameterSet
            break
    
    if parameterSet == None:
        raise HTTPException(status_code=404, detail="Cp Parameter Set not found")

    http_response = JSONResponse(content=parameterSet, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

@router.put("/{scsAsId}/subscriptions/{subscriptionId}/cpSets/{setId}", response_model=schemas.CpParameterSet)
def update_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    setId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.CpParameterSetCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    """
    Update/Replace an existing cp parameter set by id
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

    parameterSet = None
    parameterSets = []
    
    for cpParameterSet in retrieved_doc.get('cpParameterSets'):
        if cpParameterSet.get('setId') != setId:
            parameterSets.append(cpParameterSet)
        else:
            parameterSet = cpParameterSet
            json_data = jsonable_encoder(item_in)
            parameterSets.append(json_data)
    
    if parameterSet == None:
        raise HTTPException(status_code=404, detail="Cp Parameter Set not found")

    #Update the document
    data = jsonable_encoder({"cpParameterSets": parameterSets})
    crud_mongo.update_new_field(db_mongo, db_collection, subscriptionId, data)

    #Retrieve the updated document | UpdateResult is not a dict
    updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)

    for cpParameterSet in updated_doc.get('cpParameterSets'):
        if cpParameterSet.get('setId') == setId:
            parameterSet = cpParameterSet
            break

    http_response = JSONResponse(content=parameterSet, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response

@router.delete("/{scsAsId}/subscriptions/{subscriptionId}/cpSets/{setId}", response_model=schemas.CpParameterSet)
def delete_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    setId: str = Path(..., title="Identifier of the subscription resource"),
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
    
    parameterSet = None
    parameterSets = []
    
    for cpParameterSet in retrieved_doc.get('cpParameterSets'):
        if cpParameterSet.get('setId') != setId:
            parameterSets.append(cpParameterSet)
        else:
            parameterSet = cpParameterSet
    
    if parameterSet == None:
        raise HTTPException(status_code=404, detail="Cp Parameter Set not found")

    #Update the document
    data = jsonable_encoder({"cpParameterSets": parameterSets})
    crud_mongo.update_new_field(db_mongo, db_collection, subscriptionId, data)

    #Retrieve the updated document | UpdateResult is not a dict
    updated_doc = crud_mongo.read_uuid(db_mongo, db_collection, subscriptionId)

    parameterSet = {}

    for cpParameterSet in updated_doc.get('cpParameterSets'):
        if cpParameterSet.get('setId') == setId:
            parameterSet = cpParameterSet
            break

    http_response = JSONResponse(content=parameterSet, status_code=200)
    add_notifications(http_request, http_response, False)
    return http_response