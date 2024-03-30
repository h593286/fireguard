from datetime import datetime
from typing_extensions import deprecated
from src.data.dataTypes import Location, WeatherDataPoint


class DatabaseHandler:
    #def __init__(self):

    @deprecated("Use `getObservations` to check for value existence")
    def checkObservation(self, location : Location, time):
        #ToDo
        return False

    def getObservation(self, location : Location, time: datetime) -> WeatherDataPoint | None:
        """Retrieves an observation if it's present in the database

        Args:
        ----
            location (Location): The location of the observation
            time (datetime): the timestamp of the observation

        Returns:
        -------
            (WeatherDataPoint)
        """
        # ToDo
        return None


    def storeObservations(self, observatins: list[WeatherDataPoint]):
        """Stores a list of observations to the database

        Args:
        ----
            observatins (list[WeatherDataPoint]): The observations to store
        """
        raise BaseException("Not implemented exception")

    def storeObservation(self, observation: WeatherDataPoint):
        # ToDo
        return False


    def checkForecast(self,  location : Location):
        # ToDo
        return False

    def getForecast(self,  location : Location):
        # ToDo
        return False

    def storeForecast(self, forecast):
        # ToDo
        return False

