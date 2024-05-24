from os import getenv
from fastapi import FastAPI, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.api.authentication.auth import verify_user_role
from src.api.requesthandler.buildFireguardAPI import Build_Fireguard
from src.data.dataTypes import Location



api_server_ = Build_Fireguard() # Calls function that builds the fireguard API server

origins = [
    "http://127.0.0.1:5000",
    "http://localhost:5000",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8081",
]
 
app = FastAPI() # Creates a FastAPI instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# Fireguard API server endpoints
# ==============================================================================

def create_response(body, response: Response, status_code):
    
    if body:
        return body

    response.status_code = status_code


    return None

class GetFireRiskRequest(BaseModel):
    location: Location

@app.get("/cities/{city}")
def city(city: str, response: Response):

    city_json = api_server_.read_city(city)
    return create_response(city_json, response, status.HTTP_404_NOT_FOUND)

@app.get("cities/{latitude}/{longitude}")
def city_from_coordinates(latitude: float, longitude: float, response: Response, user: bool = Depends(verify_user_role)):

    city_json = api_server_.read_city_by_coordinates(latitude, longitude)
    return create_response(city_json, response, status.HTTP_404_NOT_FOUND)

@app.get("/fire_risk/city/{city}")
def fire_risk_city(city: str, response: Response, ts_from: Optional[datetime] = None, ts_to: Optional[datetime] = None, user: bool = Depends(verify_user_role)):

    firerisk = api_server_.get_firerisk_by_city(city, ts_from, ts_to)
    return create_response(firerisk, response, status.HTTP_404_NOT_FOUND)

@app.get("/fire_risk/{latitude}/{longitude}")
def fire_risk_lat_long(latitude: float, longitude: float, response: Response, ts: Optional[datetime] = None, user: bool = Depends(verify_user_role)):
    firerisk = api_server_.get_firerisk_by_coordinates(latitude, longitude, ts)
    return create_response(firerisk, response, status.HTTP_404_NOT_FOUND)


print("startin api in", getenv("ENVIRONMENT"), "mode", sep=" ")