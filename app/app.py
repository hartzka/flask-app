from flask import Flask, render_template
import tablib
import os

app = Flask(__name__, template_folder="templates")
dataset = tablib.Dataset()
with open(os.path.join(os.path.dirname(__file__),'data/weather.csv')) as f:
    dataset.csv = f.read()

@app.route("/")
def index():
    return "Hello, this is the mainpage!"

@app.route("/info")
def infopage():
    return "Info page"

@app.route("/weather")
def hello():
    data = dataset.html
    return render_template("weather.html", data=data)

@app.route("/test")
def test():
    return "Test"

app.run(host='0.0.0.0', port=5000)
