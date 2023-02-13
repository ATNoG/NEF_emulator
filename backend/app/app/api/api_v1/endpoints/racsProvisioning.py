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
db_collection= 'RacsProvisioning'

@router.get("/{scsAsId}/provisionings", response_model=List[schemas.RacsProvisioningData])
def read_active_subscriptions(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a provisioning", example="myNetapp"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "GET")
    pass

#Callback 

racsProvisioning_callback_router = APIRouter()

@racsProvisioning_callback_router.post("{$request.body.notificationDestination}",response_class=Response)
def racsProvisioning_notification(body: schemas.ExNotification):
    pass

@router.post("/{scsAsId}/provisionings", responses={201: {"model" : schemas.RacsProvisioningData}}, callbacks=racsProvisioning_callback_router.routes)
def create_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a provisioning", example="myNetapp"),
    db: Session = Depends(deps.get_db),
    item_in: schemas.RacsProvisioningDataCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(scsAsId, endpoint, "POST", json_item)
    pass

@router.get("/{scsAsId}/provisionings/{provisioningId}", response_model=schemas.RacsProvisioningData)
def read_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a provisioning", example="myNetapp"),
    provisioningId: str = Path(..., title="Identifier of the provisioning resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "GET", provs_id=provisioningId)
    pass

@router.put("/{scsAsId}/provisionings/{provisioningId}", response_model=schemas.RacsProvisioningData)
def update_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a provisioning", example="myNetapp"),
    provisioningId: str = Path(..., title="Identifier of the provisioning resource"),
    item_in: schemas.RacsProvisioningDataCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    json_item = jsonable_encoder(item_in)
    tools.reports.update_report(scsAsId, endpoint, "PUT", json_item, provs_id=provisioningId)
    pass

@router.delete("/{scsAsId}/provisionings/{provisioningId}", response_model=schemas.RacsProvisioningData)
def delete_subscription(
    *,
    scsAsId: str = Path(..., title="The ID of the Netapp that creates a provisioning", example="myNetapp"),
    provisioningId: str = Path(..., title="Identifier of the provisioning resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    endpoint = http_request.scope['route'].path 
    tools.reports.update_report(scsAsId, endpoint, "DELETE", provs_id=provisioningId)
    pass