# This file has been modified from its original version
# This file is part of a project licensed under the GNU LGPLv3. See the LICENSE file in the root directory for license terms.

from datetime import timedelta, datetime, UTC
from time import time
import src.service.TTFmodel.compute as computeTTF


from src.service.datacollector.dataCollector import DataCollector
from src.data.dataTypes import Location, FireRiskPrediction, Observations, Forecast, WeatherData



class FireRiskModelAPI:

    def __init__(self, client: DataCollector) -> None:
        self.client = client
        self.timedelta_ok = timedelta(days=1)
        self.interpolate_distance = 720

    def compute(self, location: Location) -> FireRiskPrediction:
        # Get the fire risk prediction
        start = time()
        observations=self.client.collectObservation(location)
        forecast=self.client.collectForecast(location)

        if isinstance(observations, Observations):
            obs = observations

        if isinstance(forecast, Forecast):
            fct = forecast
                
        print('OBSERVATION',observations)
        print('FORECAST', forecast)
        obs_fetch = time()
        print("data fetching time: ", obs_fetch - start)
        wd = WeatherData(created=datetime.now(), observations=obs, forecast=fct)
        value = computeTTF.compute(wd)
        computation = time()
        print("computation time: ", computation - obs_fetch)
        return value

    # compute firerisk from a timestamp to another timestamp
    def compute_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:

        #TODO: add logic for handling start being after datetime.now() and end being before datetime.now()
        #TODO: add error handling for start being after end

        observations=self.client.collectObservation(location, start) 
        forecast=self.client.collectForecast(location, end)

        wd = WeatherData(created=datetime.now(UTC), observations=observations, forecast=forecast)

        print(wd.to_json())

        prediction = computeTTF.compute(wd)

        return prediction

    # compute firerisk from now to a timestamp
    def compute_now_period(self, location: Location, fct_delta: timedelta):
        time_now = datetime.now(UTC)
        time_to = time_now + fct_delta

        observations=self.client.collectObservation(location, None)
        forecast=self.client.collectForecast(location, time_to)

        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)

        prediction = computeTTF.compute(wd) # TODO: get firerisk from straight from database instead of calculating each time?
        print(prediction)
        return prediction