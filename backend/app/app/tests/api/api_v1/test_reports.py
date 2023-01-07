from requests.structures import CaseInsensitiveDict
import requests
import json


def get_token(url, user_pass):

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Content-Type"] = "application/x-www-form-urlencoded"

    data = {

        "grant_type": "",

        "username": user_pass["username"],

        "password": user_pass["password"],

        "scope": "",

        "client_id": "",

        "client_secret": ""
    }

    resp = requests.post(url, headers=headers, data=data)

    resp_content = resp.json()

    token = resp_content["access_token"]

    return token


def test_token(base_url, key):

    token_test_url = base_url + '/api/v1/login/test-token'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    data = {""}

    resp = requests.post(token_test_url, headers=headers, data=data)

    resp_content = resp.json()

    return resp_content


def create_report(base_url, key):

    token_test_url = base_url + '/nef/api/v1/test-report/v1/report'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    resp = requests.post(token_test_url, headers=headers)

    resp_content = resp.json()

    return resp_content


def delete_report(base_url, key):

    token_test_url = base_url + '/nef/api/v1/test-report/v1/report'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    resp = requests.delete(token_test_url, headers=headers)

    resp_content = resp.json()

    return resp_content


def create_monitoring_subscription(base_url, key, netApp_id):

    scsAsId = netApp_id

    token_test_url = base_url + '/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    data ={
    "externalId": "123456789@domain.com",
    "notificationDestination": "http://localhost:80/api/v1/utils/monitoring/callback",
    "monitoringType": "LOCATION_REPORTING",
    "maximumNumberOfReports": 1,
    "monitorExpireTime": "2022-12-23T14:59:00.967Z",
    "maximumDetectionTime": 1,
    "reachabilityType": "DATA"
    }

    resp = requests.post(token_test_url, headers=headers, data=json.dumps(data))

    resp_content = resp.json()

    return resp_content


def get_monitoring_subscriptions(base_url, key, netApp_id):

    scsAsId = netApp_id

    token_test_url = base_url + '/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    resp = requests.get(token_test_url, headers=headers)

    resp_content = resp.json()

    return resp_content


def get_monitoring_subscription_by_id(base_url, key, netApp_id, sub_id):

    scsAsId = netApp_id

    subscriptionId = sub_id

    token_test_url = base_url + '/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions/1'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    resp = requests.get(token_test_url, headers=headers)

    resp_content = resp.json()

    return resp_content


def create_qos_subscription(base_url, key, netApp_id):

    scsAsId = netApp_id

    token_test_url = base_url + '/nef/api/v1/3gpp-as-session-with-qos/v1/netapp/subscriptions'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    data ={
    "ipv4Addr": "10.0.0.0",
    "ipv6Addr": "0:0:0:0:0:0:0:0",
    "macAddr": "22-00-00-00-00-00",
    "notificationDestination": "http://localhost:80/api/v1/utils/session-with-qos/callback",
    "snssai": {
        "sst": 1,
        "sd": "000001"
    },
    "dnn": "province1.mnc01.mcc202.gprs",
    "qosReference": 9,
    "altQoSReferences": [
        0
    ],
    "usageThreshold": {
        "duration": 0,
        "totalVolume": 0,
        "downlinkVolume": 0,
        "uplinkVolume": 0
    },
    "qosMonInfo": {
        "reqQosMonParams": [
        "DOWNLINK"
        ],
        "repFreqs": [
        "EVENT_TRIGGERED"
        ],
        "latThreshDl": 0,
        "latThreshUl": 0,
        "latThreshRp": 0,
        "waitTime": 0,
        "repPeriod": 0
    }
    }

    resp = requests.post(token_test_url, headers=headers, data=json.dumps(data))

    resp_content = resp.json()

    return resp_content


def get_qos_subscriptions(base_url, key, netApp_id):

    scsAsId = netApp_id

    token_test_url = base_url + '/nef/api/v1/3gpp-as-session-with-qos/v1/netapp/subscriptions'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    resp = requests.get(token_test_url, headers=headers)

    resp_content = resp.json()

    return resp_content


def get_qos_subscription_by_id(base_url, key, netApp_id, sub_id):

    scsAsId = netApp_id

    subscriptionId = sub_id

    token_test_url = base_url + '/nef/api/v1/3gpp-as-session-with-qos/v1/netapp/subscriptions/1'

    headers = CaseInsensitiveDict()

    headers["accept"] = "application/json"

    headers["Authorization"] = "Bearer " + key

    headers["Content-Type"] = "application/json"

    resp = requests.get(token_test_url, headers=headers)

    resp_content = resp.json()

    return resp_content



if __name__ == "__main__":

    base_url = "http://10.0.12.95:8888"

    url = base_url + "/api/v1/login/access-token"

    user_pass = {

        "username": "admin@my-email.com",

        "password": "pass"

    }

    key = get_token(url, user_pass)

    print(key)

    tested_token = test_token(base_url, key)

    print(tested_token)

    create_report(base_url, key)

    create_monitoring_subscription(base_url, key, "netAppTest")

    get_monitoring_subscriptions(base_url, key, "netAppTest")

    create_qos_subscription(base_url, key, "netAppTest")
    
    get_qos_subscriptions(base_url,key, "netAppTest")

    # delete_report(base_url, key)

