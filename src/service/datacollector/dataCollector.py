from src.data.apihandler.apihandler import APIHandler
from src.data.databasehandler.databaseHandler import DatabaseHandler
from src.data.dataextractor.dataExtractor import DataExtractor
from src.data.dataTypes import Location


# Responsible for the flow of data.
# Uses apihandler to get new observation and forecasts
# Uses the database handler to check if data allready exists and to store new data
# Uses the dataextractor to get the correct format from the observations and prepare it for return + storing

class DataCollector:
    def __init__(self):
        self.apiHandler = APIHandler()
        self.databaseHandler = DatabaseHandler()
        self.dataExtractor = DataExtractor()


    def collectObservation(self, location : Location, time='latest'):

        # ToDo
        if self.databaseHandler.checkObservation(location,time):
            observation = self.databaseHandler.getObservation(location,time)

        else:
            observation = self.apiHandler.getObservation(location,time)
            observation = self.dataExtractor.extractObservation(observation, location)

            self.databaseHandler.storeObservation(observation) #Stores the 'unseen' observation for potential later use

        return observation

    def collectForecast(self, location : Location):

        if self.databaseHandler.checkForecast(location):
            forecast = self.databaseHandler.getForecast(
                location
            )
        else:
            forecast = self.apiHandler.getForecast(location)
            forecast = self.dataExtractor.extractForecast(forecast)

        return forecast
