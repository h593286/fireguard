import json
import requests
from flask import Flask, request, send_from_directory
from flask import Flask, request

app = Flask(__name__)

@app.route("/<path:path>")
def files(path: str):
    print(path)
    return send_from_directory("../../static",path)