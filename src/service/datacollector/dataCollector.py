from datetime import datetime, UTC
from src.data.apihandler.apihandler import APIHandler
from src.data.databasehandler.databaseHandler import DatabaseHandler
from src.data.databasehandler.mongodb import MongoDbHandler
from src.data.dataextractor.dataExtractor import DataExtractor
from src.data.dataTypes import Location


# Responsible for the flow of data.
# Uses apihandler to get new observation and forecasts
# Uses the database handler to check if data allready exists and to store new data
# Uses the dataextractor to get the correct format from the observations and prepare it for return + storing

class DataCollector:
    def __init__(self):
        self.apiHandler = APIHandler()
        self.databaseHandler: DatabaseHandler = MongoDbHandler()
        self.dataExtractor = DataExtractor()


    def collectObservation(self, location : Location, time: datetime | None = None):
        
        if time is None:
            time = datetime.now(UTC)

        # ToDo
        if (observation := self.databaseHandler.getObservation(location,time)) is not None:
            print("cache hit obs")
            return observation

        else:
            observation = self.apiHandler.getObservation(location,time)
            observation = self.dataExtractor.extractObservation(observation, location)
            print('SLIK SER OBSERVATION UT:', observation.data)
            self.databaseHandler.storeObservations(location, observation.data) #Stores the 'unseen' observation for potential later use
            observation = self.databaseHandler.getObservation(location,time) # Henter observationen fra databasen til riktig tidspunkt

        return observation

    def collectForecast(self, location : Location, time: datetime | None = None):

        if (forecast := self.databaseHandler.getForecast(location, time)) is not None:
            print("cache hit fore")
            return forecast
        else:
            forecast = self.apiHandler.getForecast(location)
            forecast = self.dataExtractor.extractForecast(forecast) 
            self.databaseHandler.storeForecast(forecast)
            #forecast = self.databaseHandler.getForecast(location, time) # Henter forecasten fra databasen til riktig tidspunkt

        return forecast
