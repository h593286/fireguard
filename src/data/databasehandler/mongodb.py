import os
from typing import Any, Collection
from datetime import datetime, UTC, timedelta
from pymongo import MongoClient

from src.data.dataTypes import Forecast, Location, Observations, WeatherDataPoint
from src.data.databasehandler.databaseHandler import DatabaseHandler
from src.helpers.annotations import overrides

class MongoDbHandler(DatabaseHandler):
    def __init__(self, mongo_client: MongoClient | None = None):
        super().__init__()
        if mongo_client is None:
            connection_string = os.getenv("MONGO_DB_CONNECTION_STRING")
            mongo_client = MongoClient(connection_string)
        self.client = mongo_client
        print("connected to mongo db")

    @overrides(DatabaseHandler)
    def getObservation(self, location : Location, time: datetime):

        time_str = _create_str_key(time)
        
        database = self.client.get_database("observations")
        observations = database.get_collection(str(location))
        observation = observations.find_one({'timestamp': time_str})

        print("fetching", observation, time_str)

        if observation is None:
            return None
        else:
            time = _parse_str_key(observation['timestamp'])
            point = WeatherDataPoint(timestamp=time, temperature=observation['temperature'], humidity=observation['humidity'], wind_speed=observation['wind_speed'])
            return Observations(location=location, data=[point], source="_")
    
    @overrides(DatabaseHandler)
    def getObservations(self, location: Location, from_date: datetime, to_date: datetime) -> Observations | None    :
        from_str = _create_str_key(from_date)
        to_str = _create_str_key(to_date)

        database = self.client.get_database("observations")
        observation_list = database.get_collection(str(location))

        query = {
            'timestamp': {
                '$gte': from_str,
                '$lte': to_str
            }
        }

        observations = observation_list.find(query)
        points = list(map(_to_weather_data_point, observations))
        if len(points) == 0:
            return None
        else:
            return Observations(source="_", location=location, data=points)
    
    @overrides(DatabaseHandler)
    def storeObservations(self, location: Location, observations: list[WeatherDataPoint]):
        data = list(map(_to_mongodb_entry, observations))

        database = self.client.get_database("observations")
        observation_list = database.get_collection(str(location))
        return observation_list.insert_many(data).acknowledged
    
    @overrides(DatabaseHandler)
    def getForecast(self, location: Location, to_date: datetime | None) -> Forecast | None:
        from_date = datetime.now(UTC)
        if to_date is None:
            to_date = from_date + timedelta(days=14)
        forecasts = self._query_date_range("forecasts", location, from_date, to_date)

        points = list(map(_to_weather_data_point, forecasts))
        if len(points) == 0:
            return None
        else:
            return Forecast(location=location, data=points)

    @overrides(DatabaseHandler)
    def storeForecast(self, forecast: Forecast) -> bool:
        points = map(_to_mongodb_entry, forecast.data)

        database = self.client.get_database("forecasts")
        forecast_list = database.get_collection(str(forecast.location))
        return forecast_list.insert_many(points).acknowledged

    def _query_date_range(self, db_name: str, location: Location, from_date: datetime, to_date: datetime) -> Collection[dict[str, Any]]:
        database = self.client.get_database(db_name)
        collection = database.get_collection(str(location))
        query = {
            'timestamp': {
                '$gte': _create_str_key(from_date),
                '$lte': _create_str_key(to_date)
            }
        }
        return list(collection.find(query))



def _create_str_key(timetamp: datetime) -> str:
    return f'{timetamp.year:04}|{timetamp.month:02}|{timetamp.day:02}|{timetamp.hour:02}'

def _parse_str_key(key: str) -> datetime:
    year = int(key[0:4])
    month = int(key[5:7])
    day = int(key[8:10])
    hour = int(key[11:13])
    return datetime(year=year, month=month, day=day, hour=hour, tzinfo=UTC)


def _to_mongodb_entry(point: WeatherDataPoint) -> dict[str,Any]:
    return {
        'timestamp': _create_str_key(point.timestamp),
        'temperature': point.temperature,
        'humidity': point.humidity,
        'wind_speed': point.wind_speed
    }

def _to_weather_data_point(dict: dict[str, Any]):
    return WeatherDataPoint(
        timestamp=_parse_str_key(dict['timestamp']),
        temperature=dict['temperature'],
        humidity=dict['humidity'],
        wind_speed=dict['wind_speed']
    )