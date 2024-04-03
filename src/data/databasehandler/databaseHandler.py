from datetime import datetime
from typing_extensions import deprecated
from src.data.dataTypes import Location, WeatherDataPoint


class DatabaseHandler:
    #def __init__(self):

    @deprecated("Use `getObservation` to check for value existence")
    def checkObservation(self, location : Location, time):
        #ToDo
        return False

    def getObservations(self, location: Location, from_date: datetime, to_date: datetime) -> list[WeatherDataPoint]:
        """Retrieves a range of observations between `from_date` and `to_date`

        Args
        ----
            location (Location): The location of the observations
            from_date (datetime): the start of the date range
            to_date (datetime): the end of the date range

        Returns
        -------
            list[WeatherDataPoint]: the weather data points found in this range. 
            The range is not garantueed to be exaustive, meaning further api calls might be necessary to get the entire range requested
        """
        raise NotImplementedError("getObservations is not implemented")

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
        raise NotImplementedError("getObservation is not implemented")


    def storeObservations(self, location: Location, observatins: list[WeatherDataPoint]):
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

