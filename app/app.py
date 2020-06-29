from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, this is the mainpage!"

@app.route("/info")
def infopage():
    return "Infopage"

@app.route("/hello")
def hello():
    return "Hello"

app.run(host='0.0.0.0', port=5000)
