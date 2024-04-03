from datetime import datetime
import os
from src.data.dataTypes import Location, WeatherDataPoint
from src.data.databasehandler.databaseHandler import DatabaseHandler
from pymongo import MongoClient

from src.helpers.annotations import overrides

class MongoDbHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()
        connection_string = os.getenv("MONGO_DB_CONNECTION_STRING")
        self.client = MongoClient(connection_string)
        print("connected to mongo db")

    @overrides(DatabaseHandler)
    def getObservation(self, location : Location, time: datetime):

        time_str = _create_str_key(time)
        
        database = self.client.get_database("observations")
        observations = database.get_collection(str(location))

        observation = observations.find_one(time_str)
        if observation is None:
            return None
        else:
            time = _parse_str_key(observation['_id'])
            return WeatherDataPoint(timestamp=time, temperature=observation['temperature'], humidity=observation['humidity'], wind_speed=observation['wind_speed'])
        
    @overrides(DatabaseHandler)
    def getObservations(self, location: Location, from_date: datetime, to_date: datetime) -> list[WeatherDataPoint]:
        from_str = _create_str_key(from_date)
        to_str = _create_str_key(to_date)

        database = self.client.get_database("observations")
        observation_list = database.get_collection(str(location))

        raise NotImplementedError("todo")
def _create_str_key(timetamp: datetime) -> str:
    return f'{timetamp.year:04}|{timetamp.month:02}|{timetamp.day:02}|{timetamp.hour:02}'

def _parse_str_key(key: str) -> datetime:
    year = int(key[0:4])
    month = int(key[5:7])
    day = int(key[8:10])
    hour = int(key[11:13])
    return datetime(year=year, month=month, day=day, hour=hour)