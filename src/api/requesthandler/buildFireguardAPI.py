from src.api.requesthandler.api_logic import FireLogic
import json
from src.service.datacollector.dataCollector import DataCollector
from src.service.frcapi import FireRiskModelAPI

# load cities from json file
def load_cities() -> list:
    with open('./src/api/requesthandler/cities.json','r') as json_raw:
        json_data = json.load(json_raw)


    return json_data

# Build the Fireguard API server
def Build_Fireguard():

    json_data = load_cities()
    service_data = DataCollector()

    #cities = [item['city'] for item in json_data]
    frc_model_api = FireRiskModelAPI(service_data) # maybe remove this line and strictly use the DataCollector class
    api_server_ = FireLogic(name = "Fireguard", cities=json_data, modelApi=frc_model_api)
    

    return api_server_