import pandas as pd
import numpy as np
from sklearn import linear_model

df = pd.read_csv("app/data/weather.csv")
reg = linear_model.LinearRegression()
columns = ["d","time","clouds","pressure","humidity","rain","snow","dew_temperature",
               "visibility","wind_direction","gust_speed","wind_speed"]
reg.fit(df[columns], df.temperature)

print(reg.predict([[103,8,8.0,1001.9,94.0,0.0,0.0,2.1,15390.0,190.0,9.4,7.0]]))

def predict(row):
    return reg.predict([[row[c].iloc[0] for c in columns]])