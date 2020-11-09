import os
import glob
import pandas as pd
import numpy as np

def get_weather_data(area, number):
    path = "./weatherdata/{}/{}".format(area, area)
    years = ["16", "17", "18", "19"]
    dfs = []
    for year in years:
        dfs.append(pd.read_csv(path + year + ".csv"))

    data = pd.concat(dfs, ignore_index=True)
    data['area'] = number
    return data

def generate_area(area, number):
    data = get_weather_data(area, number)

    weather_data = pd.concat([data])

    del weather_data['Time zone']
    weather_data = weather_data.rename(columns = {"Cloud amount (1/8)":"clouds","Pressure (msl) (hPa)":"pressure",
                                                "Relative humidity (%)":"humidity", "Precipitation intensity (mm/h)":"rain",
                                                "Snow depth (cm)":"snow", "Air temperature (degC)":"temperature",
                                                "Dew-point temperature (degC)":"dew_temperature","Horizontal visibility (m)":"visibility",
                                                "Wind direction (deg)":"wind_direction","Gust speed (m/s)":"gust_speed",
                                                "Wind speed (m/s)":"wind_speed","Year":"year","Time":"time"}, inplace = False)

    weather_data["time"] = weather_data["time"].astype(str).str.replace(":00","").astype(int)
    weather_data = weather_data.fillna(0)
    weather_data["temperature"] = weather_data["temperature"]*10
    weather_data["temperature"] = weather_data["temperature"].astype(int)
    weather_data["d"] = weather_data["m"]*100 + weather_data["d"]
    del weather_data["m"]
    weather_data["temperature"] = weather_data["temperature"].shift(-24)
    weather_data = weather_data[:-24]

    data_folder = "./app/data"
    destination=os.path.join(data_folder, "weather_{}.csv".format(area))
    weather_data.to_csv(destination, index = False)
    return weather_data

data_vantaa = generate_area("vantaa", 1)
html = data_vantaa.to_html()
text_file = open("./app/templates/weather_data.html", "w")
text_file.write(html)
text_file.close()

generate_area("kumpula", 2)
generate_area("oulu", 3)
generate_area("kevo", 4)
