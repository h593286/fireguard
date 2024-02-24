from src.data.apihandler.apihandler import FrostClient
#Check if correct import
from src.data.apihandler.METClient import METClient

# Extracts the wanted data from the observations and forecasts.
# Same format for storage
class DataExtractor:
    def __init__(self):
        self.FrostClient = FrostClient()
        self.METClient = METClient()

    def extractObservation(self, observation, long, lat):
        # Take out the nessecary elements from the observation and return it
        #not sure what "observations" was supposed to do
        response = FrostClient().sendObservationRequest(long, lat)
        data = response.json()['data'][0]
        observations = data['observations']
        returnJson = {'sourceId': data['sourceId'], 'referenceTime': data['referenceTime'], 'air_temperature': observations[0]['value'], 'relative_humidity': observations[1]['value']}
        return returnJson

    def extractForecast(self, forecast, long, lat):
        # Take out the nessecary elements from the forecast and return it
        response = METClient().sendForecastRequest(long, lat)
        data = response.json()

        return data
