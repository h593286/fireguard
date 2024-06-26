import os
import requests
from dotenv import load_dotenv

from src.data.dataTypes import Location

load_dotenv()


# Frostclient, simple contact point for frost
# Only gets the observation, does not format it
class FrostClient:
    def __init__(self):
        self.FROST_CLIENT_ID = os.getenv('FROST_CLIENT_ID', '')
        self.FROST_CLIENT_SECRET = os.getenv('FROST_CLIENT_SECRET', '')
        self.observationEndpoint = 'https://frost.met.no/observations/v0.jsonld'
        self.sourcesEndpoint = 'https://frost.met.no/sources/v0.jsonld'

    def sendObservationRequest(self, location: Location, time='latest'):
        source = self.nearestStation(location)

        parameters = {
            'sources': source,
            'referencetime': time,
            'elements': 'air_temperature,relative_humidity,wind_speed'}

        response = requests.get(self.observationEndpoint,
                                params=parameters,
                                auth=(self.FROST_CLIENT_ID, self.FROST_CLIENT_SECRET))

        return response

    def nearestStation(self, location: Location):
        parameters = {
            'types': 'SensorSystem',
            'elements': 'air_temperature,relative_humidity,wind_speed',
            'geometry': f'nearest(POINT({location.longitude} {location.latitude}))'}

        response = requests.get(self.sourcesEndpoint,
                                params=parameters,
                                auth=(self.FROST_CLIENT_ID, self.FROST_CLIENT_SECRET))

        json = response.json()
        stationId = json['data'][0]['id']
        return stationId
