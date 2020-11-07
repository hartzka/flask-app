from flask import Flask, request, render_template
import pandas as pd
import datetime
import os
from fmiopendata.wfs import download_stored_query
from sklearn import linear_model, metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__, template_folder="templates")
weather_data = pd.read_csv(os.path.join(os.path.dirname(__file__),'data/weather.csv'))

end_time = datetime.datetime.utcnow()
start_time = end_time - datetime.timedelta(hours=1)
start_time = start_time.isoformat(timespec="seconds") + "Z"
end_time = end_time.isoformat(timespec="seconds") + "Z"
obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                            args=["bbox=20,59,32,69",
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

current_date = {'day': end_time[8:10], 'month': end_time[5:7], 'year': end_time[0:4], 'time': end_time[11:13]}
current_weather = {'d': [int(current_date['month'])*100+int(current_date['day'])], 'time': [current_date['time']], 'rain':[rain, data["Precipitation amount"]["units"]], 'temperature':[current_temperature, data["Air temperature"]["units"]],
                   'gust_speed':[gustSpeed, data["Gust speed"]["units"]], 'wind_speed':[windSpeed, data["Wind speed"]["units"]],
                   'weather_station':[weather_station], 'wind_direction':[windDirection, data["Wind direction"]["units"]], 'humidity':[humidity,data["Relative humidity"]["units"]],
                   'dew_temperature': [dew_temperature, data["Dew-point temperature"]["units"]], "rain_intensity": [rain_intensity,data["Precipitation intensity"]["units"]],
                   'snow': [snow, data["Snow depth"]["units"]], 'pressure': [pressure, data["Pressure (msl)"]["units"]],
                   'visibility': [visibility, data["Horizontal visibility"]["units"]], 'clouds': [clouds, data["Cloud amount"]["units"]]}

years = {2017, 2018, 2019}
months = {1,2,3,4,5,6,7,8,9,10,11,12}
days = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30}

def predict_linear(row, columns):
    reg = linear_model.LinearRegression()
    reg.fit(weather_data[columns], weather_data.temperature)
    return reg.predict([[row[c].iloc[0] for c in columns]])

def predict_decision_trees(row, columns):
    col_names = {"d":1,"time":2,"clouds":3,"pressure":4,"humidity":5,"rain":6,"snow":7,
    "dew_temperature":9,"visibility":10,"wind_direction":11,"gust_speed":12,"wind_speed":13}
    feature_cols=[col_names[k] for k in col_names if k in columns]
    X = weather_data.iloc[:,feature_cols]
    y = weather_data.temperature
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, train_size=0.75, random_state=50)
    classifier = DecisionTreeClassifier()
    classifier = classifier.fit(X_train,y_train)
    return classifier.predict([[row[c].iloc[0] for c in columns]])

def forecast_linear(row, columns):
    reg = linear_model.LinearRegression()
    reg.fit(weather_data[columns], weather_data.temperature)
    return reg.predict([[row[c] for c in columns]])

def forecast_decision_trees(row, columns):
    col_names = {"d":1,"time":2,"clouds":3,"pressure":4,"humidity":5,"rain":6,"snow":7,
    "dew_temperature":9,"visibility":10,"wind_direction":11,"gust_speed":12,"wind_speed":13}
    feature_cols=[col_names[k] for k in col_names if k in columns]
    X = weather_data.iloc[:,feature_cols]
    y = weather_data.temperature
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, train_size=0.75, random_state=50)
    classifier = DecisionTreeClassifier()
    classifier = classifier.fit(X_train,y_train)
    return classifier.predict([[row[c] for c in columns]])

def get_temperature_prediction(year, month, day, columns, model):
    d = month*100+day
    row = weather_data.loc[(weather_data["d"]==d) & (weather_data["time"]==13 & (weather_data["year"]==year))]
    if (model == "linear"):
        return round(predict_linear(row, columns)[0]/10,1)
    elif (model == "trees"):
        return round(predict_decision_trees(row, columns)[0]/10,1)

def forecast_temperature(row, columns, model):
    if (model == "linear"):
        return round(forecast_linear(row, columns)[0]/10,1)
    elif (model == "trees"):
        return round(forecast_decision_trees(row, columns)[0]/10,1)

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
    dateformat = "{}.{}.{}".format(end_time[8:10], end_time[5:7], end_time[0:4])
    return render_template("predict.html", weather=current_weather, date=current_date, checks={}, dateformat=dateformat, temperature=current_temperature, years=years, months=months, days=days)

@app.route("/predict", methods=['POST'])
def predict():
    year = int(request.form.get("year"))
    month = int(request.form.get("month"))
    day = int(request.form.get("day"))
    model = request.form.get("model")
    d = month*100+day
    columns = ["d", "time"]
    if request.form.get("clouds"):
        columns.append("clouds")
    if request.form.get("pressure"):
        columns.append("pressure")
    if request.form.get("humidity"):
        columns.append("humidity")
    if request.form.get("rain"):
        columns.append("rain")
    if request.form.get("snow"):
        columns.append("snow")
    if request.form.get("dew"):
        columns.append("dew_temperature")
    if request.form.get("visibility"):
        columns.append("visibility")
    if request.form.get("wind_direction"):
        columns.append("wind_direction")
    if request.form.get("gust"):
        columns.append("gust_speed")
    if request.form.get("wind_speed"):
        columns.append("wind_speed")
    date = {'day': day, 'month': month, 'year': year}
    dateformat = "{}.{}.{}".format(day, month, year)
    row = weather_data.loc[(weather_data["d"]==d) & (weather_data["time"]==13) & (weather_data["year"]==year)]
    actual_temperature = row["temperature"].iloc[0]/10
    prediction = get_temperature_prediction(year, month, day, columns, model)
    return render_template("predict.html", date=date, dateformat=dateformat, model=model, checks=columns, temperature=actual_temperature, prediction=prediction, years=years, months=months, days=days)

@app.route("/forecast", methods=['POST', 'GET'])
def forecast():
    model = request.form.get("model")
    columns = ["d", "time"]
    if request.form.get("clouds"):
        columns.append("clouds")
    if request.form.get("pressure"):
        columns.append("pressure")
    if request.form.get("humidity"):
        columns.append("humidity")
    if request.form.get("rain"):
        columns.append("rain")
    if request.form.get("snow"):
        columns.append("snow")
    if request.form.get("dew"):
        columns.append("dew_temperature")
    if request.form.get("visibility"):
        columns.append("visibility")
    if request.form.get("wind_direction"):
        columns.append("wind_direction")
    if request.form.get("gust"):
        columns.append("gust_speed")
    if request.form.get("wind_speed"):
        columns.append("wind_speed")
    dateformat = "{}.{}.{}".format(current_date["day"], current_date["month"], current_date["year"])
    row = {c: int(current_weather[c][0]) for c in columns}
    prediction = forecast_temperature(row, columns, model)
    return render_template("forecast.html", weather=current_weather, date=current_date, dateformat=dateformat, temperature=current_temperature, model=model, checks=columns, prediction=prediction, years=years, months=months, days=days)

app.run(host='0.0.0.0', port=5000, debug=True)
