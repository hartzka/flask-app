import os
import glob
import pandas as pd

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

weather_data["Time"] = weather_data["Time"].astype(str).str.replace(":00","").astype(int)
weather_data = weather_data.dropna(axis=0, subset=['Precipitation intensity (mm/h)', 'Air temperature (degC)', 'Gust speed (m/s)', 'Wind speed (m/s)'])

data_folder = "./data"
destination=os.path.join(data_folder, "weather.csv")
weather_data.to_csv(destination, index = False)
