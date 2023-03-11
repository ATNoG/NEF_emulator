from typing import Any, List
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, FileResponse
from app import models
from app.api import deps
from app import tools

router = APIRouter()

@router.post("/report")
def read_subscription(
    *,
    # scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    # subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    tools.reports.create_report()
    return JSONResponse(content="OK",status_code=200)


@router.get("/report")
def read_subscription(
    *,
    # scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    # subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    report_path = tools.reports.get_report_path()
    return FileResponse(report_path,filename="report.json")


@router.delete("/report")
def read_subscription(
    *,
    # scsAsId: str = Path(..., title="The ID of the Netapp that creates a subscription", example="myNetapp"),
    # subscriptionId: str = Path(..., title="Identifier of the subscription resource"),
    current_user: models.User = Depends(deps.get_current_active_user),
    http_request: Request
) -> Any:
    tools.reports.delete_report()
    return JSONResponse(content="OK",status_code=200)