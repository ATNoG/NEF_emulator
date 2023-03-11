import json
import os

def create_report():
    if not os.path.exists('report.json'):
        with open('report.json', 'x') as jsonFile:
            data = {}
            data["requests"] = []
            json.dump(data, jsonFile)
    pass

def get_report_path():
    return os.path.abspath('report.json')

def update_report(scsAsId, endpoint, method, json_item=None, subs_id=-1,set_id=-1,trans_id=-1,conf_id=-1,provs_id=-1):
    with open("report.json", "r") as jsonFile:
            data = json.load(jsonFile)
            request_count = len(data["requests"])
            json_data = {}
            json_data.update({"id" : request_count, "scsAsId" : scsAsId, "endpoint" : endpoint, "method" : method})
            if subs_id != -1:
                json_data.update({"subscriptionId" : subs_id})
            if set_id != -1:
                json_data.update({"setId" : set_id})
            if set_id != -1:
                json_data.update({"transactionId" : trans_id})
            if set_id != -1:
                json_data.update({"configurationId" : conf_id})
            if set_id != -1:
                json_data.update({"provisioningId" : provs_id})
            if json_item != None:
                json_data.update(json_item)
            
            data["requests"].append(json_data)

    with open("report.json", "w") as jsonFile:
        json.dump(data, jsonFile)
    pass

def delete_report():
    if os.path.exists('report.json'):
        os.remove('report.json')
    pass