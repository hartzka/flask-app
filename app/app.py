from flask import Flask, render_template
import pandas as pd

app = Flask(__name__, template_folder="templates")
df = pd.read_csv("data/weather.csv")
dataset = df.to_html("detail.html")

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
