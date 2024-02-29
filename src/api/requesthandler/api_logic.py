from pydantic import BaseModel
import datetime 
from src.service.datacollector.dataCollector import *
from src.service.frcapi import *



# from fireguard.data.dataextractor.dataExtractor import Location

class FireLogic(BaseModel):
    """The FireLogic class is a pydantic model that is used to represent the logic of the fireguard service."""
    
    #constructor for the FireLogic class
    name: str
    cities: list[dict] 
    model_api: FireRiskModelAPI

    #class Config is used to allow arbitrary types to be used in the class
    class Config:
        arbitrary_types_allowed = True

    # ==============================================================================
    # fireguard logic functions
    # ==============================================================================
        
    def read_city(self, city: str):

        for c in self.cities:
            if c["city"] == city:
                return c
            
        return None # Return None?

    def read_city_by_coordinates(self, latitude: float, longitude: float) -> dict | None:
        
        for c in self.cities:
            if c["latitude"] == latitude and c["longitude"] == longitude:
                return c
        
        return None # Return None?
    
    def get_firerisk_by_city(self, city: str):#    city: Location
        
        city_ = self.read_city(city)

        #TODO: make code robust

        if city_ is not None:
            latitude = city_["latitude"]
            longitude = city_["longitude"]
            return self.get_firerisk_by_coordinates(latitude, longitude)


    def get_firerisk_by_coordinates(self, latitude: float, longitude: float):

        location = Location(latitude=latitude, longitude=longitude)

        '''
        obs_delta =  datetime.timedelta(days=2)

        # TODO: Get weatherdata (observations and forecast) from service layer

        wd = WeatherData(created=datetime.datetime.now(), observations=Observations(
            source="test", location=location, data=[WeatherDataPoint(temperature=34,humidity=4,wind_speed=2,timestamp=datetime.datetime.now())]), 
            forecast=Forecast(location=location, data=[WeatherDataPoint(temperature=34,humidity=4,wind_speed=2,timestamp=datetime.datetime.now())]))
        '''
        prediction = self.model_api.compute(self.model_api.client,location=location)
        print(prediction)
        return prediction
    
'''    def get_firerisk_by_coordinates_now(self, latitude: float, longitude: float):
        location = Location(latitude=latitude, longitude=longitude)

        obs_delta =  datetime.timedelta(days=2)
        prediction = self.model_api.compute_now(location, obs_delta)

        return prediction'''

    
        


