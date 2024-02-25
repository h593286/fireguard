from fastapi import FastAPI, Response, status

from typing import Union

from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles


# Without Pydantic's BaseModel
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# With Pydantic's BaseModel
        
class User(BaseModel):
    name: str
    age: int

app = FastAPI()


# endpoints for the API 

@app.get("/")
def hello_world():
    return "Hello, world!"

@app.get("/user")
def get_user():
    return User(name = "Magnus",age = 22)

"""@app.get("/weather/bergen")
def get_weather_bergen() -> str:
    return "sunny"

@app.get("/weather/oslo")
def get_weather_oslo():
    return "rainy"""

@app.get("/weather")
def get_weather(location: Optional[str] = None) -> str:

    if location == "bergen":
        return "sunny"
    elif location == "oslo":
        return "rainy"
    else:
        return "unknown location"


app.mount("/static", StaticFiles(directory="static"), name="static")



