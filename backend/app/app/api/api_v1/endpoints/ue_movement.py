import threading, logging, time, requests
from app.models.UE import UE
from fastapi import APIRouter, Path, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Any, Literal, Optional
from fastapi import APIRouter, Path, Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from typing import Any
from app import crud, tools, models
from app.crud import crud_mongo
from app.tools.distance import check_distance
from app.tools.rsrp_calculation import check_rsrp, check_path_loss
from app.tools import qos_callback
from app.db.session import SessionLocal, client
from app.api import deps
from app.crud import crud_mongo
from app.db.session import SessionLocal, client
from app.models.UE import UE
from app.schemas import Msg
from app.schemas.monitoringevent import (
    MonitoringEventReport,
    MonitoringNotification,
    MonitoringType,
    LocationInfo,
    Point,
    ReachabilityType,
    SupportedGADShapes,
    GeographicalCoordinates,
)
from app.schemas.afSessionWithQos import AsSessionWithQoSSubscription
from app.tools import monitoring_callbacks, timer

# Dictionary holding threads that are running per user id.
threads = {}

# Dictionary holding UEs' information
ues = {}

# Dictionary holding UEs' distances to cells
distances = {}

# Dictionary holding UEs' path losses in reference to cells
path_losses = {}

# Dictionary holding UEs' path losses in reference to cells
rsrps = {}

handovers = {}

# API
router = APIRouter()

moving_devices = dict()

Speed = Literal["HIGH", "LOW"]


def increment_position(speed: Speed) -> int:
    if speed == "LOW":
        return 1

    if speed == "HIGH":
        return 10


def validate_ue(*, ue: Optional[UE], user: models.User, db) -> Optional[UE]:
    if not ue:
        logging.warning("UE not found")
        return None

    if ue.owner_id != user.id:
        logging.warning("Not enough permissions")
        return None

    path = crud.path.get(db=db, id=ue.path_id)
    if not path:
        logging.warning("Path not found")
        return None

    if path.owner_id != user.id:
        logging.warning("Not enough permissions")
        return None

    return ue


async def movement_loop(supi: str, user: models.User):
    db = SessionLocal()
    ue = validate_ue(ue=crud.ue.get_supi(db=db, supi=supi), user=user, db=db)

    if ue is None:
        moving_devices.pop(supi)
        return

    points = crud.points.get_points(db=db, path_id=ue.path_id)

    # Assume end of path
    current_position_index = -1
    cells = jsonable_encoder(crud.cell.get_multi_by_owner(db=db, owner_id=user.id))

    # Find current position if one exists
    for index, point in enumerate(points):
        if (ue.latitude == point.latitude) and (ue.longitude == point.longitude):
            current_position_index = index
            break

    while True:
        if supi not in moving_devices:
            break

        current_position_index = (
            increment_position(ue.speed) + current_position_index
        ) % len(points)
        point = points[current_position_index]

        cell_now, cell_distances = check_distance(
            point.latitude, point.longitude, cells
        )

        ue = crud.ue.update_coordinates(
            db=db, lat=point.latitude, long=point.longitude, db_obj=ue
        )

        logging.info("The current cell is %d", cell_now)
        if cell_now and ue.Cell_id != cell_now.get("id"):
            ue.Cell_id = cell_now.get("id")
            crud.ue.update(
                db=db,
                db_obj=ue,
                obj_in={"Cell_id": ue.Cell_id},
            )

        await location_notification(
            ue, ue.Cell_id, cell_now.get("id") if cell_now else None
        )

        await asyncio.sleep(1)


async def location_notification(
    ue: UE, old_cell_id: Optional[int], current_cell_id: Optional[int]
):
    db_mongo = client.fastapi
    subscriptions = crud_mongo.read_all_by_multiple_pairs(
        db_mongo,
        "MonitoringEvent",
        externalId=ue.external_identifier,
    )

    for sub in subscriptions:
        sub_validate_time = tools.check_expiration_time(
            expire_time=sub.get("monitorExpireTime")
        )

        sub_validate_number_of_reports = tools.check_numberOfReports(
            sub.get("maximumNumberOfReports")
        )

        if not sub_validate_time or not sub_validate_number_of_reports:
            crud_mongo.delete_by_uuid(db_mongo, "MonitoringEvent", sub.get("_id"))
            continue

        if monitoringType == "LOCATION_REPORTING":
            await handle_location_report_callback(sub, ue)

        elif monitoringType == "LOSS_OF_CONNECTIVITY":
            asyncio.create_task(
                handle_loss_connectivity_callback(sub, ue, old_cell_id, current_cell_id)
            )

        elif monitoringType == "UE_REACHABILITY":
            await handle_ue_reachability_callback(sub, ue, old_cell_id, current_cell_id)


async def handle_location_report_callback(location_reporting_sub, ue: UE):
    db_mongo = client.fastapi
    logging.info(
        "Attempting to send the callback to %d",
        location_reporting_sub.get("notificationDestination"),
    )
    print(
        f"Attempting to send the callback to {location_reporting_sub.get('notificationDestination')}"
    )

    notification = MonitoringNotification(
        subscription=location_reporting_sub.get("link"),
        monitoringEventReports=[
            MonitoringEventReport(
                externalId=ue.external_identifier,
                monitoringType=MonitoringType.LOCATION_REPORTING,
                locationInfo=LocationInfo(
                    cellId=ue.Cell_id,
                    enodeBId=None,
                    geographicArea=Point(
                        shape=SupportedGADShapes.POINT,
                        point=GeographicalCoordinates(
                            lat=ue.latitude,
                            lon=ue.longitude,
                        ),
                    ),
                ),
            )
        ],
    )

    await notification_responder.send_notification(
        location_reporting_sub.get("notificationDestination"), notification
    )

    maxReports = location_reporting_sub.get("maximumNumberOfReports")

    if maxReports:
        location_reporting_sub.update({"maximumNumberOfReports": maxReports - 1})
        crud_mongo.update(
            db_mongo,
            "MonitoringEvent",
            location_reporting_sub.get("_id"),
            location_reporting_sub,
        )


async def handle_loss_connectivity_callback(
    loss_of_connectivity_sub,
    ue: UE,
    old_cell_id: Optional[int],
    current_cell_id: Optional[int],
):
    if old_cell_id and not current_cell_id:
        await asyncio.sleep(loss_of_connectivity_sub.get("maximumDurationTime"))
        db = SessionLocal()
        new_ue = crud.ue.get_supi(db=db, supi=ue.supi)
        if new_ue and not new_ue.Cell_id:
            notification = MonitoringNotification(
                subscription=loss_of_connectivity_sub.get("link"),
                monitoringEventReports=[
                    MonitoringEventReport(
                        externalId=ue.external_identifier,
                        monitoringType=MonitoringType.LOSS_OF_CONNECTIVITY,
                        lossOfConnectReason=2,
                    )
                ],
            )

            await notification_responder.send_notification(
                loss_of_connectivity_sub.get("notificationDestination"), notification
            )

    logging.info("There was an attempt at calling the connectivity callback")


async def handle_ue_reachability_callback(
    subscription, ue: UE, old_cell_id: Optional[int], current_cell_id: Optional[int]
):
    if current_cell_id and not old_cell_id:
        notification = MonitoringNotification(
            subscription=subscription.get("link"),
            monitoringEventReports=[
                MonitoringEventReport(
                    externalId=ue.external_identifier,
                    monitoringType=MonitoringType.UE_REACHABILITY,
                    reachabilityType=ReachabilityType.DATA,
                )
            ],
        )

        await notification_responder.send_notification(
            subscription.get("notificationDestination"), notification
        )


@router.post("/update_location/{supi}", status_code=200)
def update_location(
    *,
    supi: str = Path(...),
    new_location: Point,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db = SessionLocal()
    ue = crud.ue.get_supi(db, supi)

    if not ue:
        raise HTTPException(
            status_code=404,
            detail="No device found",
        )

    ue = crud.ue.update_coordinates(
        db,
        lat=new_location.point.lat,
        long=new_location.point.lon,
        db_obj=ue,
    )

    background_tasks.add_task(location_notification, ue)

    return {"msg": "Location updated"}


moving_devices = dict()

Speed = Literal["HIGH", "LOW"]


def increment_position(speed: Speed) -> int:
    if speed == "LOW":
        return 1

    if speed == "HIGH":
        return 10


def validate_ue(*, ue: Optional[UE], user: models.User, db) -> Optional[UE]:
    if not ue:
        logging.warning("UE not found")
        return None

    if ue.owner_id != user.id:
        logging.warning("Not enough permissions")
        return None

    path = crud.path.get(db=db, id=ue.path_id)
    if not path:
        logging.warning("Path not found")
        return None

    if path.owner_id != user.id:
        logging.warning("Not enough permissions")
        return None

    return ue


def movement_loop(supi: str, user: models.User):
    db = SessionLocal()
    ue = validate_ue(ue=crud.ue.get_supi(db=db, supi=supi), user=user, db=db)

    if ue is None:
        moving_devices.pop(supi)
        return

    points = crud.points.get_points(db=db, path_id=ue.path_id)

    # Assume end of path
    current_position_index = -1

    # Find current position if one exists
    for index, point in enumerate(points):
        if (ue.latitude == point.latitude) and (ue.longitude == point.longitude):
            current_position_index = index
            break

    while True:
        if supi not in moving_devices:
            break

        current_position_index += increment_position(ue.speed) % len(points)
        point = points[current_position_index]

        ue = crud.ue.update_coordinates(
            db=db, lat=point.latitude, long=point.longitude, db_obj=ue
        )

        location_notification(ue)

        time.sleep(1)


def location_notification(ue: UE):
    db_mongo = client.fastapi
    subscriptions = crud_mongo.read_all_by_multiple_pairs(
        db_mongo,
        "MonitoringEvent",
        externalId=ue.external_identifier,
    )

    for sub in subscriptions:
        sub_validate_time = tools.check_expiration_time(
            expire_time=sub.get("monitorExpireTime")
        )

        sub_validate_number_of_reports = tools.check_numberOfReports(
            sub.get("maximumNumberOfReports")
        )

        if not sub_validate_time or not sub_validate_number_of_reports:
            crud_mongo.delete_by_uuid(db_mongo, "MonitoringEvent", sub.get("_id"))
            continue

        monitoringType = sub["monitoringType"]

        if monitoringType == "LOCATION_REPORTING":
            handle_location_report_callback(sub, ue)

        elif monitoringType == "LOSS_OF_CONNECTIVITY":
            handle_loss_connectivity_callback(sub, ue)

        elif monitoringType == "UE_REACHABILITY":
            handle_ue_reachability_callback(sub, ue)


def handle_location_report_callback(location_reporting_sub, ue: UE):
    db_mongo = client.fastapi
    try:
        logging.info(
            "Attempting to send the callback to %d",
            location_reporting_sub.get("notificationDestination"),
        )
        print(
            f"Attempting to send the callback to {location_reporting_sub.get('notificationDestination')}"
        )
        monitoring_callbacks.location_callback(
            jsonable_encoder(ue),
            location_reporting_sub.get("notificationDestination"),
            location_reporting_sub.get("link"),
        )
        location_reporting_sub.update(
            {
                "maximumNumberOfReports": location_reporting_sub.get(
                    "maximumNumberOfReports"
                )
                - 1
            }
        )
        crud_mongo.update(
            db_mongo,
            "MonitoringEvent",
            location_reporting_sub.get("_id"),
            location_reporting_sub,
        )

    except requests.exceptions.ConnectionError as ex:
        logging.warning("Failed to send the callback request with error %d", ex)


def handle_loss_connectivity_callback(loss_of_connectivity_sub, ue: UE):
    logging.error("There was an attempt at calling the connectivity callback")


def handle_ue_reachability_callback(subscription, ue: UE):
    logging.error("There was an attempt at calling the reachability callback")


@router.post("/update_location/{supi}", status_code=200)
def update_location(
    *,
    supi: str = Path(...),
    new_location: Point,
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    db = SessionLocal()
    ue = crud.ue.get_supi(db, supi)

    if not ue:
        raise HTTPException(
            status_code=404,
            detail="No device found",
        )

    ue = crud.ue.update_coordinates(
        db,
        lat=new_location.point.lat,
        long=new_location.point.lon,
        db_obj=ue,
    )

    # TODO: Send notifications related to location update
    background_tasks.add_task(location_notification, ue)

    return {"msg": "Location updated"}


@router.post("/start-loop", status_code=200)
def initiate_movement(
    *,
    msg: Msg,
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Start the loop.
    """
    if msg.supi in moving_devices:
        raise HTTPException(
            status_code=409,
            detail=f"There is a thread already running for this supi:{msg.supi}",
        )

    moving_devices[msg.supi] = current_user.id
    background_tasks.add_task(movement_loop, msg.supi, current_user)

    return {"msg": "Loop started"}


@router.post("/stop-loop", status_code=200)
def terminate_movement(
    *,
    msg: Msg,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Stop the loop.
    """
    try:
        moving_devices.pop(msg.supi)
        return {"msg": "Loop ended"}
    except KeyError as ke:
        print("Key Not Found in Threads Dictionary:", ke)
        raise HTTPException(
            status_code=409,
            detail="There is no generator running for this SUPI",
        )


@router.get("/state-loop/{supi}", status_code=200)
def state_movement(
    *,
    supi: str = Path(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the state
    """
    return {"running": retrieve_ue_state(supi, current_user.id)}


@router.get("/state-ues", status_code=200)
def state_ues(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the state
    """
    return crud.ue.get_multi_by_owner(SessionLocal(), owner_id=current_user.id)


# Functions
def retrieve_ue_state(supi: str, user_id: int) -> bool:
    try:
        return threads[f"{supi}"][f"{user_id}"].is_alive()
    except KeyError as ke:
        print("Key Not Found in Threads Dictionary:", ke)
        return False


def retrieve_ues() -> dict:
    return crud.ue.get_multi_by_owner(SessionLocal(), owner_id=current_user.id)


def retrieve_ue(supi: str) -> dict:
    return crud.ue.get_supi(SessionLocal(), supi)


def retrieve_ue_distances(supi: str, user_id: int) -> dict:
    db = SessionLocal()
    ue = crud.ue.get_supi(db, supi)
    if ue is None:
        return {}

    cells = jsonable_encoder(crud.cell.get_multi_by_owner(db=db, owner_id=user_id))
    _, distances = check_distance(ue.latitude, ue.longitude, cells)
    return distances


def retrieve_ue_path_losses(supi: str) -> dict:
    return path_losses.get(supi)


def retrieve_ue_rsrps(supi: str) -> dict:
    return rsrps.get(supi)


def retrieve_ue_handovers(supi: str) -> dict:
    result = handovers.get(supi)
    if result != None:
        return handovers.get(supi)
    return []


def monitoring_event_sub_validation(
    sub: dict, is_superuser: bool, current_user_id: int, owner_id
) -> bool:

    if not is_superuser and (owner_id != current_user_id):
        # logging.warning("Not enough permissions")
        return False
    else:
        sub_validate_time = tools.check_expiration_time(
            expire_time=sub.get("monitorExpireTime")
        )
        sub_validate_number_of_reports = tools.check_numberOfReports(
            sub.get("maximumNumberOfReports")
        )
        if sub_validate_time and sub_validate_number_of_reports:
            return True
        else:
