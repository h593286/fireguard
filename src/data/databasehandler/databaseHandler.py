from datetime import datetime

from src.data.dataTypes import Forecast, Location, Observations, WeatherDataPoint


class DatabaseHandler:
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

    def getObservation(self, location : Location, time: datetime) -> Observations | None:
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


    def storeObservations(self, location: Location, observations: list[WeatherDataPoint]):
        """Stores a list of observations to the database

        Args:
        ----
            observations (list[WeatherDataPoint]): The observations to store

        Returns:
        -------
            (bool): wether the store operation was successfull
        """
        raise BaseException("storeObservations is not implemented")

    def getForecast(self,  location : Location, time: datetime | None = None) -> Forecast | None:
        # ToDo
        raise BaseException("getForecast is not implemented")

    def storeForecast(self, forecast: Forecast) -> bool:
        # ToDo
        return False

