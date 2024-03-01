from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from src.api.requesthandler.buildFireguardAPI import Build_Fireguard
from pydantic import BaseModel
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


# @app.get("/")
# def read_root():
#     return {"message": "Welcome to this awesome page!"}
# # app.mount("/welcome", StaticFiles(directory="static"), name="static") #static files for later

def create_response(body, response: Response, status_code):

    if body:
        return body
    
    response.status_code = status_code

    return None

class GetFireRiskRequest(BaseModel):
    location: Location

@app.post("/fire_risk")
def root(body: GetFireRiskRequest, response: Response):
    city = api_server_.get_firerisk_by_coordinates(body.location.latitude, body.location.longitude)
    return create_response(city, response, status.HTTP_404_NOT_FOUND)


@app.get("/{location}")
def fire_risk(location: str, response: Response):

    city = api_server_.read_city(location)

    return create_response(city, response, status.HTTP_404_NOT_FOUND)

@app.get("/fire_risk/{latitude}/{longitude}")
def fire_risk_lat_long(longitude: float, latitude: float, response: Response):

    city = api_server_.get_firerisk_by_coordinates(latitude, longitude)
    return create_response(city, response, status.HTTP_404_NOT_FOUND)

"""@app.get("/fire_risk/{latitude}/{longitude}")
def fire_risk_lat_long(longitude: float, latitude: float, response: Response):
    pass"""