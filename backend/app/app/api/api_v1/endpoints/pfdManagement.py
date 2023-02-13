import logging
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Path, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo.database import Database
from sqlalchemy.orm import Session
from app import models, schemas, tools
from app.api import deps
from app.crud import crud_mongo, user, ue
from app.db.session import client
from .utils import add_notifications

router = APIRouter()
db_collection= 'PfdManagement'

@router.get("/{scsAsId}/transactions", response_model=List[schemas.PfdManagement])
def read_active_subscriptions(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "GET")
    pass

#Callback 

pfdManagement_callback_router = APIRouter()
#TODO: checkar isto aqui da notificação
@pfdManagement_callback_router.post("{$request.body.notificationDestination}",response_class=Response)
def chargParty_notification(body: schemas.EventNotification):
    pass

@router.post("/{scsAsId}/transactions", responses={201: {"model" : schemas.PfdManagement}}, callbacks=pfdManagement_callback_router.routes)
def create_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    db: Session = Depends(deps.get_db),
    item_in: schemas.PfdManagementCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(scsAsId, endpoint, "POST", json_item)
    pass

@router.get("/{scsAsId}/transactions/{transactionId}", response_model=schemas.PfdManagement)
def read_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    transactionId: str = Path(..., title="Identifier of the transaction"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "GET", trans_id=transactionId)
    pass

@router.put("/{scsAsId}/transactions/{transactionId}", response_model=schemas.PfdManagement)
def update_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    transactionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.PfdManagementCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(scsAsId, endpoint, "PUT", json_item, trans_id=transactionId)
    pass

@router.delete("/{scsAsId}/transactions/{transactionId}", response_model=schemas.PfdManagement)
def delete_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    transactionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "DELETE", trans_id=transactionId)
    pass