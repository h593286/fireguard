import requests
from dotenv import load_dotenv
from src.data.dataTypes import *
import os

load_dotenv()

# METclient, simple contact point for MET(forecast)
# Only gets the observation, does not format it
class METClient:
    def __init__(self):
        self.FROST_CLIENT_ID = os.getenv('FROST_CLIENT_ID')
        self.FROST_CLIENT_SECRET = os.getenv('FROST_CLIENT_SECRET')
        self.forecastEndpoint = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'

    def sendForecastRequest(self,  location: Location):

        parameters = {
            'lat': location.latitude,
            'lon': location.longitude}

        #User-Agent needs to be changed, it requires the user agent not to be a python script, acts as an identifire(needs to be unique)
        headers = {
            'User-Agent': 'Test'
        }
        #auth is not used
        response = requests.get(self.forecastEndpoint,
                                params=parameters,
                                headers=headers,
                                auth=(self.FROST_CLIENT_ID, self.FROST_CLIENT_SECRET))
        return response
