from src.data.apihandler.apihandler import FrostClient
from src.data.dataTypes import *
import numpy as np
import dateutil.parser


#Check if correct import
from src.data.apihandler.METClient import METClient

# Extracts the wanted data from the observations and forecasts.
# Same format for storage
class DataExtractor:
    def __init__(self):
        self.FrostClient = FrostClient()
        self.METClient = METClient()

    def extractObservation(self, location: Location):
        # Take out the nessecary elements from the observation and return it

        response = FrostClient().sendObservationRequest(location)

        data_list = response.json()['data']

        weatherdatapoints = list()

        source_id = None

        if len(data_list) >= 1:

            source_id = data_list[0]['sourceId']

            for data in data_list:

                reference_time = dateutil.parser.parse(data['referenceTime'])
                station_observations = data['observations']

                temperature = np.nan
                relative_humidity = np.nan
                wind_speed = np.nan

                for station_observation in station_observations:

                    # string to datatime object required
                    timestamp = reference_time  # assume that observations have the same time stamp

                    # TODO: rewrite to use a switch
                    if station_observation['elementId'] == 'air_temperature':
                        temperature = station_observation['value']
                    elif station_observation['elementId'] == 'relative_humidity':
                        relative_humidity = station_observation['value']
                    elif station_observation['elementId'] == 'wind_speed':
                        wind_speed = station_observation['value']

                wd_point = WeatherDataPoint(temperature=temperature,
                                            humidity=relative_humidity,
                                            wind_speed=wind_speed,
                                            timestamp=timestamp
                                            )

                weatherdatapoints.append(wd_point)

        # TODO: maybe also source as part of the parameters - or extract weather data function instead
        observations = Observations(source=source_id, location=location, data=weatherdatapoints)
        print(observations)
        return observations
    def extractForecast(self, forecast, long, lat):
        # Take out the nessecary elements from the forecast and return it
        response = METClient().sendForecastRequest(long, lat)
        data = response.json()

        return data
