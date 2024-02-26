from src.data.apihandler.frostClient import FrostClient
from datetime import date, datetime
from collections.abc import Iterable
from src.data.apihandler import util
from src.data.dataTypes import Location


# Responsible for getting observations from the different weather clients and handling potenial errors
class APIHandler:
    def __init__(self):
        self.frostClient = FrostClient()


    def getObservation(self, long, lat, time ='latest'):

        # Default value
        if time == 'latest':
            formatted_time = time

        # single value
        elif isinstance(time, (datetime, date)):
            formatted_time = util.format_date(time)

        # Time series
        elif isinstance(time, Iterable) and len(time) == 2 and all(
                isinstance(t, (datetime, date)) for t in time):
            start, end = time
            formatted_time = util.format_period(start, end)
        else:
            raise ValueError(
                "Invalid time argument. Must be 'latest', a datetime object, or an iterable of two datetime objects.")

        return self.frostClient.sendObservationRequest(Location(latitude=lat, longitude=long), formatted_time)



