from flask import Flask, request, render_template
import pandas as pd
import datetime
import os
from fmiopendata.wfs import download_stored_query

app = Flask(__name__, template_folder="templates")
df = pd.read_csv(os.path.join(os.path.dirname(__file__),'data/weather.csv'))
row = df.loc[(df["m"]==10) & (df["d"]==30) & (df["Time"]==22) & (df["Year"]==2019)]
current_temperature = row["Air temperature (degC)"].iloc[0]

end_time = datetime.datetime.utcnow()
start_time = end_time - datetime.timedelta(hours=1)
start_time = start_time.isoformat(timespec="seconds") + "Z"
end_time = end_time.isoformat(timespec="seconds") + "Z"
obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=["bbox=18,55,35,75",
                                  "starttime=" + start_time,
                                  "endtime=" + end_time])

time_of_day = max(obs.data.keys())
weather_station = list(obs.data[time_of_day].keys())[0]
print(weather_station)

data = obs.data[time_of_day][weather_station]
rain = data['Precipitation amount']['value']
celcius = data['Air temperature']['value']
windGustSpeed = data['Gust speed']['value']
windSpeed = data['Wind speed']['value']

current_weather = [rain, celcius, windGustSpeed, windSpeed, weather_station, time_of_day]
current_temperature = celcius

years = {2017, 2018, 2019}
months = {1,2,3,4,5,6,7,8,9,10,11,12}
days = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/info")
def infopage():
    return "Info page"

@app.route("/weather")
def weather():
    return render_template("weather.html")

@app.route("/current")
def current():
    return render_template("forecast.html", weather=current_weather, date=end_time, temperature=current_temperature, years=years, months=months, days=days)

@app.route("/forecast", methods=['POST'])
def forecast():
    inputs = [int(x) for x in request.form.values()]
    year = inputs[0]
    month = inputs[1]
    day = inputs[2]
    date = "{}.{}.{}".format(day, month, year)
    row = df.loc[(df["m"]==month) & (df["d"]==day) & (df["Time"]==13) & (df["Year"]==year)]
    temperature = row["Air temperature (degC)"].iloc[0]
    return render_template("forecast.html", date=date, temperature=temperature, years=years, months=months, days=days)

app.run(host='0.0.0.0', port=5000, debug=True)
