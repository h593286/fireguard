from fastapi import FastAPI, Response, status
from src.api.requesthandler.buildFireguardAPI import Build_Fireguard


api_server_ = Build_Fireguard() # Calls function that builds the fireguard API server

app = FastAPI() # Creates a FastAPI instance

# ==============================================================================
# Fireguard API server endpoints
# ==============================================================================


@app.get("/")
def read_root():
    return {"message": "Welcome to this awesome page!"}
# app.mount("/welcome", StaticFiles(directory="static"), name="static") #static files for later


def create_response(body, response: Response, status_code):

    if body:
        return body
    
    response.status_code = status_code

    return None

@app.get("/fire_risk")
def root():
    return {"message": "Hello World"}

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






