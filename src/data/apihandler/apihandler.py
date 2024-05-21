from datetime import date, datetime

from src.data.apihandler.frostClient import FrostClient
from src.data.apihandler.METClient import METClient
from src.data.dataTypes import Location
from src.data.apihandler import util



# Responsible for getting observations from the different weather clients and handling potenial errors
class APIHandler:
    def __init__(self):
        self.frostClient = FrostClient()
        self.metClient = METClient()


    def getObservation(self, location: Location, time:  list[datetime | date] | datetime | date | None = None):


        print("time", time, type(time))

        # Default value
        formatted_time = 'latest'

        # single value
        if is_date(time):
            formatted_time = util.format_date(time) # type: ignore

        # Time series
        elif is_list_of_dates(time): # type: ignore
            start: datetime | date
            end: datetime | datetime

            start, end = time  # type: ignore

            formatted_time = util.format_period(start, end)
        else:
            raise ValueError(
                "Invalid time argument. Must be 'latest', a datetime object, or an iterable of two datetime objects.")
        
        return self.frostClient.sendObservationRequest(location, formatted_time)

    def getForecast(self, location: Location):
        return self.metClient.sendForecastRequest(location)


def is_list_of_dates(item: list[datetime | date] | None) -> bool:
    return isinstance(item, list) and len(item) == 2 and all(map(is_date, item))

def is_date(item: list[datetime | date] | datetime | date | None) -> bool:
    return isinstance(item, (datetime, date))