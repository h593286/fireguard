from src.data.apihandler.apihandler import APIHandler
from src.data.databasehandler.databaseHandler import DatabaseHandler
from src.data.dataextractor.dataExtractor import DataExtractor

# Responsible for the flow of data.
# Uses apihandler to get new observation and forecasts
# Uses the database handler to check if data allready exists and to store new data
# Uses the dataextractor to get the correct format from the observations and prepare it for return + storing

class DataCollector:
    def __init__(self):
        self.apiHandler = APIHandler()
        self.databaseHandler = DatabaseHandler()
        self.dataExtractor = DataExtractor()


    def collectObservation(self, long,lat, time=None):

        # ToDo
        if self.databaseHandler.checkObservation(long,lat,time):
            observation = self.databaseHandler.getObservation(long,lat,time)

        else:
            observation = self.apiHandler.getObservation(long,lat,time)
            observation = self.dataExtractor.extractObservation(observation)

            self.databaseHandler.storeObservation(observation) #Stores the 'unseen' observation for potential later use

        return observation