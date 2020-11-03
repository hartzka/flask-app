import os
import glob
import pandas as pd
import numpy as np

path =r'./weatherdata'

def weather_data(fn, area):
    filenames = glob.glob(path + fn)
    dfs = []
    for filename in filenames:
        dfs.append(pd.read_csv(filename))

    data = pd.concat(dfs, ignore_index=True)
    data['area'] = area
    return data

data_vantaa = weather_data("/vantaa/*.csv", 1)

weather_data = pd.concat([data_vantaa])

del weather_data['Time zone']
print(weather_data['Precipitation intensity (mm/h)'])
weather_data = weather_data.rename(columns = {"Cloud amount (1/8)":"clouds","Pressure (msl) (hPa)":"pressure",
                                              "Relative humidity (%)":"humidity", "Precipitation intensity (mm/h)":"rain",
                                              "Snow depth (cm)":"snow", "Air temperature (degC)":"temperature",
                                              "Dew-point temperature (degC)":"dew_temperature","Horizontal visibility (m)":"visibility",
                                              "Wind direction (deg)":"wind_direction","Gust speed (m/s)":"gust_speed",
                                              "Wind speed (m/s)":"wind_speed","Year":"year","Time":"time"}, inplace = False)

weather_data["time"] = weather_data["time"].astype(str).str.replace(":00","").astype(int)
weather_data = weather_data.fillna(0)

data_folder = "./app/data"
destination=os.path.join(data_folder, "weather.csv")
weather_data.to_csv(destination, index = False)
