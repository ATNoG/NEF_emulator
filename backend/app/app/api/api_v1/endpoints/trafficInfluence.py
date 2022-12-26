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
db_collection= 'TrafficInfluence'

@router.get("/{afId}/subscriptions")
def read_active_subscriptions(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(afId, endpoint, "GET")
    pass

#Callback 

trafficInf_callback_router = APIRouter()

@trafficInf_callback_router.post("{$request.body.notificationDestination}",response_class=Response)
def trafficInf_notification(body: schemas.EventNotification):
    pass

@router.post("/{afId}/subscriptions")
def create_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    db: Session = Depends(deps.get_db),
    item_in: schemas.TrafficInfluSubCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(afId, endpoint, "POST", json_item)
    pass

@router.put("/{afId}/subscriptions/{subscriptionId}", response_model=schemas.TrafficInfluSub)
def update_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.TrafficInfluSubCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(afId, endpoint, "PUT", json_item, subscriptionId)
    pass

@router.get("/{afId}/subscriptions/{subscriptionId}")
def read_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(afId, endpoint, "GET", subs_id=subscriptionId)
    pass

@router.delete("/{afId}/subscriptions/{subscriptionId}")
def delete_subscription(
    *,
    afId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(afId, endpoint, "DELETE", subs_id=subscriptionId)
    pass
