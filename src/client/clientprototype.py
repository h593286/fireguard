from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/<path:path>")
def files(path: str):
    print(path)
    return send_from_directory("../../static",path)

app.run()