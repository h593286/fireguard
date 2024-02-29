import uvicorn
import sys



if __name__ == "__main__":
    uvicorn.run("src.api.requesthandler.api_server:app", port=80, host="0.0.0.0", reload=True)