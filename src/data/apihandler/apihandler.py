from src.data.apihandler.frostClient import FrostClient


class APIHandler:
    def __init__(self):
        self.frostClient = FrostClient()


    def getObservation(self, long, lat, time='latest'):

        #ToDo: Needs error handling

        return self.frostClient.sendObservationRequest(long,lat, time)
