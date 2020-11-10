from flask import Flask, request, render_template
import pandas as pd
import datetime
import os
from fmiopendata.wfs import download_stored_query
from sklearn import linear_model, metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__, template_folder="templates")

global weather_station
global weather_data
global current_weather
global current_date

weather_station = "Vantaa Helsinki-Vantaan lentoasema"

def update_current_weather():
    global weather_station
    global weather_data
    global current_weather
    global current_date

    start_time = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    end_time = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    start_time = start_time.isoformat(timespec="seconds") + "Z"
    end_time = end_time.isoformat(timespec="seconds") + "Z"
    obs = download_stored_query("fmi::observations::weather::multipointcoverage",
                                args=["bbox=20,59,32,71", "timeseries=True",
                                    "starttime=" + start_time,
                                    "endtime=" + end_time])
        
    data = obs.data[weather_station]
    rain = data["r_1h"]["values"][-1]
    current_temperature = data["t2m"]["values"][-1]
    gustSpeed = data["wg_10min"]["values"][-1]
    windSpeed = data["ws_10min"]["values"][-1]
    windDirection = data["wd_10min"]["values"][-1]
    humidity = data["rh"]["values"][-1]
    dew_temperature = data["td"]["values"][-1]
    rain_intensity = data["ri_10min"]["values"][-1]
    snow = data["snow_aws"]["values"][-1]
    pressure = data["p_sea"]["values"][-1]
    visibility = data["vis"]["values"][-1]
    clouds = data["n_man"]["values"][-1]
    latest_observation = data["times"][-1]
    latest_observation = latest_observation.isoformat(timespec="seconds") + "Z"

    current_date = {"day": latest_observation[8:10], "month": latest_observation[5:7], "year": latest_observation[0:4], "time": latest_observation[11:13], "min": latest_observation[14:16]}
    current_weather = {"d": [str(int(current_date["month"])*100+int(current_date["day"]))], "time": [current_date["time"]], "min": [current_date["min"]],
                    "rain":[rain, data["r_1h"]["unit"]], "temperature":[current_temperature, data["t2m"]["unit"]],
                    "gust_speed":[gustSpeed, data["wg_10min"]["unit"]], "wind_speed":[windSpeed, data["ws_10min"]["unit"]],
                    "weather_station": [weather_station], "wind_direction":[windDirection, data["wd_10min"]["unit"]], "humidity":[humidity,data["rh"]["unit"]],
                    "dew_temperature": [dew_temperature, data["td"]["unit"]], "rain_intensity": [rain_intensity,data["ri_10min"]["unit"]],
                    "snow": [snow, data["snow_aws"]["unit"]], "pressure": [pressure, data["p_sea"]["unit"]],
                    "visibility": [visibility, data["vis"]["unit"]], "clouds": [clouds, data["n_man"]["unit"]]}


update_current_weather()

years = [2016, 2017, 2018, 2019]
months = [1,2,3,4,5,6,7,8,9,10,11,12]
days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
areas = {"Helsinki-Vantaa lentoasema": "vantaa", "Helsinki Kumpula": "kumpula", "Oulu lentoasema": "oulu", "Utsjoki Kevo": "kevo"}

def set_weather_data(area):
    global weather_station
    global weather_data
    global current_weather
    path = "data/weather_{}.csv".format(area)
    if (area ==  "kumpula"):
        weather_station = "Helsinki Kumpula"
    elif (area ==  "oulu"):
        weather_station = "Oulu lentoasema"
    elif (area ==  "kevo"):
        weather_station = "Utsjoki Kevo"
    else:
        weather_station = "Vantaa Helsinki-Vantaan lentoasema"
        path = "data/weather_vantaa.csv"
    update_current_weather()
    weather_data = pd.read_csv(os.path.join(os.path.dirname(__file__), path))

set_weather_data('vantaa')

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
    row = weather_data.loc[((weather_data["year"]==year) & (weather_data["time"]==13) & (weather_data["d"]==d))]
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
    return render_template("weather_data.html")

@app.route("/current")
def current():
    return render_template("predict.html", weather=current_weather, date=current_date, checks={}, temperature=current_weather["temperature"], years=years, months=months, days=days, areas=areas)

@app.route("/predict", methods=['POST'])
def predict():
    year = int(request.form.get("year"))
    month = int(request.form.get("month"))
    day = int(request.form.get("day"))
    area = request.form.get("area")
    model = request.form.get("model")
    d = month*100+day
    columns = ["d", "time"]
    set_weather_data(area)
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
    if not row.empty:
        actual_temperature = row["temperature"].iloc[0]/10
        prediction = get_temperature_prediction(year, month, day, columns, model)
    else:
        actual_temperature = ''
        prediction = ''
    return render_template("predict.html", date=date, dateformat=dateformat, model=model, checks=columns, temperature=actual_temperature,
                            prediction=prediction, years=years, months=months, days=days, area=area, areas=areas)

@app.route("/forecast", methods=['POST', 'GET'])
def forecast():
    model = request.form.get("model")
    area = request.form.get("area")
    set_weather_data(area)
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
    return render_template("forecast.html", weather=current_weather, date=current_date, dateformat=dateformat, temperature=current_weather["temperature"],
                            model=model, checks=columns, prediction=prediction, years=years, months=months, days=days, area=area, areas=areas)

app.run(host='0.0.0.0', port=5000, debug=True)
