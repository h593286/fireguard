import datetime

import src.service.TTFmodel.compute as computeTTF


from src.service.datacollector.dataCollector import *
from src.data.dataTypes import *

class FireRiskModelAPI:

    def __init__(self, client: DataCollector) -> None:
        self.client = client
        self.timedelta_ok = datetime.timedelta(days=1)
        self.interpolate_distance = 720

    def compute(self, data: DataCollector, location: Location) -> FireRiskPrediction:
        # Get the fire risk prediction
        observations=data.collectObservation(location)
        forecast=data.collectForecast(location)

        if isinstance(observations, Observations):
            obs = observations

        if isinstance(forecast, Forecast):
            fct = forecast

        wd = WeatherData(created=datetime.datetime.now(), observations=obs, forecast=fct)
        return computeTTF.compute(wd)
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