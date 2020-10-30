from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, this is the mainpage!"

@app.route("/info")
def infopage():
    return "Info page"

@app.route("/weather")
def hello():
    return "Weatherdata:"

@app.route("/test")
def test():
    return "Test"

app.run(host='0.0.0.0', port=5000)
