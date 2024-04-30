# This file has been modified from its original version
# This file is part of a project licensed under the GNU LGPLv3. See the LICENSE file in the root directory for license terms.

from datetime import timedelta, datetime
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

        obs_fetch = time()
        print("data fetching time: ", obs_fetch - start)
        wd = WeatherData(created=datetime.now(), observations=obs, forecast=fct)
        value = computeTTF.compute(wd)
        computation = time()
        print("computation time: ", computation - obs_fetch)
        return value
''' 
    def compute_now(self, location: Location, obs_delta: datetime.timedelta) -> FireRiskPrediction:

        time_now = datetime.datetime.now()
        start_time = time_now - obs_delta

        observations = self.client.fetch_observations(location, start=start_time, end=time_now)

        print(observations)

        forecast = self.client.fetch_forecast(location)

        print(forecast)

        wd = WeatherData(created=time_now, observations=observations, forecast=forecast)

        print(wd.to_json())

        prediction = self.compute(wd, location)

        return prediction
'''
'''
    def compute_now_period(self, location: Location, obs_delta: datetime.timedelta, fct_delta: datetime.timedelta):
        pass

    def compute_period(self, location: Location, start: datetime, end: datetime) -> FireRiskPrediction:
        pass

    def compute_period_delta(self, location: Location, start: datetime, delta: datetime.timedelta) -> FireRiskPrediction:
        pass

'''