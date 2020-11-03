from flask import Flask, request, render_template
import pandas as pd
import datetime
import os
from fmiopendata.wfs import download_stored_query
from sklearn import linear_model

app = Flask(__name__, template_folder="templates")
df = pd.read_csv(os.path.join(os.path.dirname(__file__),'data/weather.csv'))
row = df.loc[(df["m"]==10) & (df["d"]==30) & (df["time"]==22) & (df["year"]==2019)]
current_temperature = row["temperature"].iloc[0]

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

data = obs.data[time_of_day][weather_station]
rain = data["Precipitation amount"]["value"]
current_temperature = data["Air temperature"]["value"]
gustSpeed = data["Gust speed"]["value"]
windSpeed = data["Wind speed"]["value"]
windDirection = data["Wind direction"]["value"]
humidity = data["Relative humidity"]["value"]
dew_temperature = data["Dew-point temperature"]["value"]
rain_intensity = data["Precipitation intensity"]["value"]
snow = data["Snow depth"]["value"]
pressure = data["Pressure (msl)"]["value"]
visibility = data["Horizontal visibility"]["value"]
clouds = data["Cloud amount"]["value"]

current_weather = {'rain':[rain, data["Precipitation amount"]["units"]], 'temperature':[current_temperature, data["Air temperature"]["units"]],
                   'gust_speed':[gustSpeed, data["Gust speed"]["units"]], 'wind_speed':[windSpeed, data["Wind speed"]["units"]],
                   'weather_station':[weather_station], 'wind_direction':[windDirection, data["Wind direction"]["units"]], 'humidity':[humidity,data["Relative humidity"]["units"]],
                   'dew_temperature': [dew_temperature, data["Dew-point temperature"]["units"]], 'rain_intensity': [rain_intensity,data["Precipitation intensity"]["units"]],
                   'snow': [snow, data["Snow depth"]["units"]], 'pressure': [pressure, data["Pressure (msl)"]["units"]],
                   'visibility': [visibility, data["Horizontal visibility"]["units"]], 'clouds': [clouds, data["Cloud amount"]["units"]]}

years = {2017, 2018, 2019}
months = {1,2,3,4,5,6,7,8,9,10,11,12}
days = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31}

reg = linear_model.LinearRegression()
reg.fit(df[["m","time","clouds","pressure","humidity","rain","snow","dew_temperature",
            "visibility","wind_direction","gust_speed","wind_speed"]], df.temperature)

def predict(row):
    columns = ["m","time","clouds","pressure","humidity","rain","snow","dew_temperature",
               "visibility","wind_direction","gust_speed","wind_speed"]
    return reg.predict([[row[c].iloc[0] for c in columns]])

def get_temperature_prediction(year, month, day):
    row = df.loc[(df["m"]==month) & (df["d"]==day) & (df["time"]==13) & (df["year"]==year)]
    return round(predict(row)[0],1)


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
    date = "{}.{}.{}".format(end_time[8:10], end_time[5:7], end_time[0:4])
    return render_template("forecast.html", weather=current_weather, date=date, temperature=current_temperature, years=years, months=months, days=days)

@app.route("/forecast", methods=['POST'])
def forecast():
    inputs = [int(x) for x in request.form.values()]
    year = inputs[0]
    month = inputs[1]
    day = inputs[2]
    date = "{}.{}.{}".format(day, month, year)
    row = df.loc[(df["m"]==month) & (df["d"]==day) & (df["time"]==13) & (df["year"]==year)]
    temperature = row["temperature"].iloc[0]
    prediction = get_temperature_prediction(year, month, day)
    return render_template("forecast.html", date=date, temperature=temperature, prediction=prediction, years=years, months=months, days=days)

app.run(host='0.0.0.0', port=5000, debug=True)
