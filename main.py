import src.test as t
from flask import Flask
app = Flask(__name__)

@app.route("/")
def test():
    return t.get_some_magic()

app.run("0.0.0.0", 80)