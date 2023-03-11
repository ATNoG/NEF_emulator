import cherrypy
import os
import requests
from requests.structures import CaseInsensitiveDict
from dotenv import load_dotenv
import json
load_dotenv()

class TestNEF(object):
    def __init__(self):
        self.REPORT_API_IP = None 
        self.REPORT_API_PORT = None 
        self.REPORT_FILE_NAME = None 
        self.NEF_IP = None
        self.NEF_PORT = None 
        self.USERNAME = None 
        self.PASSWORD = None 
        self.NEF_BASE_URL = None
        self.read_env_variables()
        
    def read_env_variables(self):
        self.REPORT_API_IP = os.getenv('REPORT_API_IP')
        self.REPORT_API_PORT = os.getenv('REPORT_API_PORT')
        self.REPORT_FILE_NAME = os.getenv('REPORT_FILE_NAME')
        self.NEF_IP = os.getenv('NEF_IP')
        self.NEF_PORT = os.getenv('NEF_PORT')
        self.USERNAME = os.getenv('EMAIL')
        self.PASSWORD = os.getenv('PASS')
        self.NEF_BASE_URL = f"http://{self.NEF_IP}:{self.NEF_PORT}"
        self.REPORT_BASE_URL = f"http://{self.REPORT_API_IP}:{self.REPORT_API_PORT}"
    
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def create_report(self):
        report_api_url = f"{self.REPORT_BASE_URL}/report/"
        try:
            r = requests.post(report_api_url, params={"filename":self.REPORT_FILE_NAME})
        
            if r.status_code != 200:
                print("Error Publishing")
                return f"There was an error creating report: {r.text}"
            else:
                return "Success Creating report"
        except Exception as e:
            return f"Could not Create Report: {e}"

    def get_token(self, user_pass):
    
        try:
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
            url = f"{self.NEF_BASE_URL}/api/v1/login/access-token"
            
            resp = requests.post(url, headers=headers, data=data)

            resp_content = resp.json()

            token = resp_content["access_token"]

            return token
        
        except Exception as e:
            print(f"An error occured. Exception {e}")
            return 4, f"An error occured. Exception {e}"

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def make_subscription(self):
        subscription_path = "/nef/api/v1/3gpp-monitoring-event/v1/netapp/subscriptions"
        monitoring_payload = {
            "externalId": "123456789@domain.com",
            "notificationDestination": "http://localhost:80/api/v1/utils/monitoring/callback",
            "monitoringType": "LOCATION_REPORTING",
            "maximumNumberOfReports": 1,
            "monitorExpireTime": "2024-03-09T13:18:19.495Z",
            "maximumDetectionTime": 1,
            "reachabilityType": "DATA"
        }
        user_pass = {
            "username": self.USERNAME,
            "password": self.PASSWORD
        }
        try:
            key = self.get_token(user_pass)

            headers = CaseInsensitiveDict()
            headers["accept"] = "application/json"
            headers["Authorization"] = "Bearer " + key
            headers["Content-Type"] = "application/json"
            res = requests.post(
                f"{self.NEF_BASE_URL}{subscription_path}",
                headers=headers,
                data=json.dumps(monitoring_payload))
            if res.status_code != 200:
                raise Exception("Failed to Create Subscrition.")
        
            cherrypy.response.status = 201
            return "Success creating Subscription"
        except Exception as e:
            cherrypy.response.status = 400
            return f"An error occured: {e}"

    @cherrypy.expose
    def get_report(self):
        report_api_url = f"{self.REPORT_BASE_URL}/report/"

        response = requests.get(
        report_api_url,
        params={"filename":self.REPORT_FILE_NAME})

        if response.status_code == 404:
            print(f"Report named{self.REPORT_FILE_NAME} does not exist")
            cherrypy.response.status = 404
            return f"Report named{self.REPORT_FILE_NAME} does not exist"

        report = response.json()
        return json.dumps(report
        )
    @cherrypy.expose
    def index(self):
        return "Hello, World!"

if __name__ == '__main__':
    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(TestNEF())
