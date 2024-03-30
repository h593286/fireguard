from uvicorn import run
from os import getenv



if __name__ == "__main__":
    run("src.api.requesthandler.api_server:app", port=80, host="0.0.0.0", reload=getenv("Environment") == "Development")