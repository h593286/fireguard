from src.data.dataTypes import Location
from src.data.databasehandler.observationHandler import ObservationHandler
from src.data.databasehandler.TTFhandler import TTFhandler


class DatabaseHandler:
    def __init__(self):
        self.obsHandler = ObservationHandler()
        self.TTFhandler = TTFhandler()


    def getTTF(self, location: Location, time):
        #Todo
        #if self.TTFhandler.checkTFF(location, time):
        #    return self.TTFhandler.getTTF(location, time)
        #else:
        #    return False

        return False

    def getObservation(self, location: Location, time):
        return False
        #TODO
        #if todays date > time
        #    return self.obsHandler.getObservation(location, time)
        #
        #else:
        #    return self.obsHandler.getForcast(location, time)



