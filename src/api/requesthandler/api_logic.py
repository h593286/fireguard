from pydantic import BaseModel, ConfigDict
from datetime import datetime,UTC
from typing import Optional

from src.service.frcapi import FireRiskModelAPI, FireRiskPrediction, Location




class FireLogic(BaseModel):
    """The FireLogic class is a pydantic model that is used to represent the logic of the fireguard service."""

    #constructor for the FireLogic class
    model_config = ConfigDict(arbitrary_types_allowed=True,extra="allow")
    
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
    
    def get_firerisk_by_city(self, city: str, time_from: datetime | None = None, time_to: datetime | None = None)-> FireRiskPrediction:
        city_json = self.read_city(city)

        if time_from is not None:
            time_from = time_from.astimezone(UTC)
        
        if time_to is not None:
            time_to = time_to.astimezone(UTC)

        if city_json is not None:
            latitude = city_json["lat"]
            longitude = city_json["lng"]
        
        location = Location(latitude=latitude, longitude=longitude)

        if time_to is None and time_from is None:
            prediction = self.modelApi.compute(location)

        elif time_from is None and isinstance(time_to, datetime):
            if datetime.now(UTC) > time_to:
                #TODO: fetch firerisk directly from DB if implemented
                raise ValueError("time_to must be larger than datetime.now()")
            else:
                time_to_delta = time_to-datetime.now(UTC)
                prediction = self.modelApi.compute_now_period(location, time_to_delta)

        #TODO: could return same as modelApi.compute(location), but limited by time_from. 
        elif isinstance(time_from, datetime) and time_to is None: 
            raise ValueError("time_to must be specified")
            #prediction = self.modelApi.compute_period_now(location, time_from)
        
        elif isinstance(time_from, datetime) and isinstance(time_to, datetime):
            if time_from > time_to:
                raise ValueError('"from date" must be before "to date"')
            elif datetime.now(UTC) > time_to: #TODO: fetch firerisk directly from DB if implemented
                raise ValueError("time_to must be larger than datetime.now()")
            else:
                prediction = self.modelApi.compute_period(location, time_from, time_to)

        else:
            raise TypeError("time_from and time_to are wrong types")

        return prediction


    def get_firerisk_by_coordinates(self, latitude: float, longitude: float, ts: Optional[datetime] = None) -> FireRiskPrediction:

        #TODO: use code in get_firerisk_by_city to add ts functionality

        location = Location(latitude=latitude, longitude=longitude)
        prediction = self.modelApi.compute(location)

        return prediction    



