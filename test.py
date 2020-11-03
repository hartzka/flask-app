import pandas as pd
import numpy as np
from sklearn import linear_model

df = pd.read_csv("app/data/weather.csv")
reg = linear_model.LinearRegression()
reg.fit(df[["m","time","clouds","pressure","humidity","rain","snow","dew_temperature",
            "visibility","wind_direction","gust_speed","wind_speed"]], df.temperature)

print(reg.predict([[2,0,0.0,1049.5,74.0,0.0,31.0,-23.4,50000.0,41.0,5.1,4.0]]))

def predict(row):
    columns = ["m","time","clouds","pressure","humidity","rain","snow","dew_temperature",
               "visibility","wind_direction","gust_speed","wind_speed"]
    return reg.predict([[row[c].iloc[0] for c in columns]])
