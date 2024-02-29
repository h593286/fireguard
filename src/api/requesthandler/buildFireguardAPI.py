from src.api.requesthandler.api_logic import FireLogic
import json
from src.service.datacollector.dataCollector import DataCollector
from src.service.frcapi import FireRiskModelAPI


# Build the Fireguard API server
def Build_Fireguard():
    json_raw = open('/Users/Magnus1/Documents/GitHub/fireguard/src/api/requesthandler/cities.json','r')
    json_data = json.load(json_raw)

    service_data = DataCollector()

    #cities = [item['city'] for item in json_data]
    frc_model_api = FireRiskModelAPI(service_data)
    api_server_ = FireLogic(name = "Fireguard", cities=json_data, model_api=frc_model_api)
    

    return api_server_