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
db_collection= 'NetStatReport'

@router.get("/{scsAsId}/subscriptions", response_model=List[schemas.AsSessionWithQoSSubscription])
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

netStatReport_callback_router = APIRouter()

@netStatReport_callback_router.post("{$request.body.notificationDestination}",response_class=Response)
def netStatReport_notification(body: schemas.NetworkStatusReportingNotification):
    pass

@router.post("/{scsAsId}/subscriptions", responses={201: {"model" : schemas.NetworkStatusReportingSubscription}})
def create_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    db: Session = Depends(deps.get_db),
    item_in: schemas.NetworkStatusReportingSubscriptionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(scsAsId, endpoint, "POST", json_item)
    pass

@router.get("/{scsAsId}/subscriptions/{subscriptionId}", response_model=schemas.NetworkStatusReportingSubscription)
def read_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "GET", subs_id=subscriptionId)
    pass

@router.put("/{scsAsId}/subscriptions/{subscriptionId}", response_model=schemas.NetworkStatusReportingSubscription)
def update_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    item_in: schemas.MonitoringEventSubscriptionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(scsAsId, endpoint, "PUT", json_item, subscriptionId)
    pass

@router.delete("/{scsAsId}/subscriptions/{subscriptionId}", response_model=schemas.NetworkStatusReportingSubscription)
def delete_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "DELETE", subs_id=subscriptionId)
    pass