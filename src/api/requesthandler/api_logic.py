from pydantic import BaseModel, ConfigDict
import datetime 
from src.service.datacollector.dataCollector import *
from src.service.frcapi import *



# from fireguard.data.dataextractor.dataExtractor import Location

class FireLogic(BaseModel):
    """The FireLogic class is a pydantic model that is used to represent the logic of the fireguard service."""
    
    #constructor for the FireLogic class
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str
    cities: list[dict] 
    modelApi: FireRiskModelAPI

    #class Config is used to allow arbitrary types to be used in the class
    

    # ==============================================================================
    # fireguard logic functions
    # ==============================================================================
    
    
    def read_city(self, city: str) -> dict | None:

        for c in self.cities:
            if c["city"] == city:
                return c
            
        return None # Return None?

    def read_city_by_coordinates(self, latitude: float, longitude: float) -> dict | None:
        
        for c in self.cities:
            if round(float(c["lat"]),4) == round(latitude,4) and round(float(c["lng"]),4) == round(longitude,4):
                return c

        return None # Return None?
    
    def get_firerisk_by_city(self, city: str)-> FireRiskPrediction:
        
        city_json = self.read_city(city)

        #TODO: make code robust (add error handling)

        if city_json is not None:
            latitude = city_json["lat"]
            longitude = city_json["lng"]
        
        location = Location(latitude=latitude, longitude=longitude)
        prediction = self.modelApi.compute(location)
        return prediction


    def get_firerisk_by_coordinates(self, latitude: float, longitude: float) -> FireRiskPrediction:

        location = Location(latitude=latitude, longitude=longitude)
        prediction = self.modelApi.compute(location)
        #print(prediction)
        return prediction
    
    
'''    def get_firerisk_by_coordinates_now(self, latitude: float, longitude: float):
        location = Location(latitude=latitude, longitude=longitude)

        obs_delta =  datetime.timedelta(days=2)
        prediction = self.model_api.compute_now(location, obs_delta)

        return prediction'''

    



