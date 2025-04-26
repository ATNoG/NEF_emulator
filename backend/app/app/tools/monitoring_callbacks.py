import json

import requests

from app.schemas.monitoringevent import (
    GeographicalCoordinates,
    LocationInfo,
    MonitoringEventReport,
    MonitoringNotification,
    MonitoringType,
    Point,
    SupportedGADShapes,
)


def location_callback(ue, callbackurl, subscription):
    url = callbackurl

    notification = MonitoringNotification(
        subscription=subscription,
        monitoringEventReports=[
            MonitoringEventReport(
                externalId=ue.get("external_identifier"),
                monitoringType=MonitoringType.LOCATION_REPORTING,
                locationInfo=LocationInfo(
                    cellId=ue.get("cell_id_hex"),
                    enodeBId=ue.get("gnb_id_hex"),
                    geographicArea=Point(
                        shape=SupportedGADShapes.POINT,
                        point=GeographicalCoordinates(
                            lat=ue.get("latitude"),
                            lon=ue.get("longitude"),
                        ),
                    ),
                ),
            )
        ],
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Timeout values according to https://docs.python-requests.org/en/master/user/advanced/#timeouts
    # First value of the tuple "3.05" corresponds to connect and second "27" to read timeouts
    # (i.e., connect timeout means that the server is unreachable and read that the server is reachable but the client does not receive a response within 27 seconds)

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=notification.json(exclude_unset=True),
        timeout=(3.05, 27),
    )

    return response


def loss_of_connectivity_callback(ue, callbackurl, subscription):
    url = callbackurl

    payload = json.dumps(
        {
            "externalId": ue.get("external_identifier"),
            "ipv4Addr": ue.get("ip_address_v4"),
            "subscription": subscription,
            "monitoringType": "LOSS_OF_CONNECTIVITY",
            "lossOfConnectReason": 7,
        }
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Timeout values according to https://docs.python-requests.org/en/master/user/advanced/#timeouts
    # First value of the tuple "3.05" corresponds to connect and second "27" to read timeouts
    # (i.e., connect timeout means that the server is unreachable and read that the server is reachable but the client does not receive a response within 27 seconds)

    response = requests.request(
        "POST", url, headers=headers, data=payload, timeout=(3.05, 27)
    )

    return response


def ue_reachability_callback(ue, callbackurl, subscription, reachabilityType):
    url = callbackurl

    payload = json.dumps(
        {
            "externalId": ue.get("external_identifier"),
            "ipv4Addr": ue.get("ip_address_v4"),
            "subscription": subscription,
            "monitoringType": "UE_REACHABILITY",
            "reachabilityType": reachabilityType,
        }
    )
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    # Timeout values according to https://docs.python-requests.org/en/master/user/advanced/#timeouts
    # First value of the tuple "3.05" corresponds to connect and second "27" to read timeouts
    # (i.e., connect timeout means that the server is unreachable and read that the server is reachable but the client does not receive a response within 27 seconds)

    response = requests.request(
        "POST", url, headers=headers, data=payload, timeout=(3.05, 27)
    )

    return response
