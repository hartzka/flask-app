from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return "Hello, this is the mainpage!"

@app.route("/info")
def infopage():
    return "Info page"

@app.route("/weather")
def hello():
    return render_template("weather.html")

@app.route("/test")
def test():
    return "Test"

app.run(host='0.0.0.0', port=5000)
