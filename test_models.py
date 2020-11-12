import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn import linear_model

reg = linear_model.LinearRegression()
columns = ["d","time","clouds","pressure","humidity","rain","snow","dew_temperature",
               "visibility","wind_direction","gust_speed","wind_speed"]

col_names = ["year","d","time","clouds","pressure","humidity","rain","snow","temperature",
"dew_temperature","visibility","wind_direction","gust_speed","wind_speed","area"]

weather_data1 = pd.read_csv("app/data/weather_vantaa.csv", header=1, names=col_names)
weather_data2 = pd.read_csv("app/data/weather_kumpula.csv", header=1, names=col_names)
weather_data3 = pd.read_csv("app/data/weather_oulu.csv", header=1, names=col_names)
weather_data4 = pd.read_csv("app/data/weather_kevo.csv", header=1, names=col_names)

feature_cols=[1,2,3,4,5,6,7,9,10,11,12,13]

def predict(d, weather_data):
    row = weather_data[(weather_data["d"]==d) & (weather_data["year"]==2019) & (weather_data["time"]==13)]
    reg.fit(weather_data[columns], weather_data.temperature)
    print("day: ", d)
    print("linear model prediction", round(reg.predict([[row[c].iloc[0] for c in columns]])[0]/10, 1))

    X = weather_data.iloc[:,feature_cols]
    y = weather_data.temperature
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, train_size=0.75, random_state=50)
    classifier = DecisionTreeClassifier().fit(X_train,y_train)
    y_pred = classifier.predict(X_test)
    print("Decision trees rediction:", round(classifier.predict([[row[c].iloc[0] for c in columns]])[0]/10, 1))

    print("actual temperature: ", round(row["temperature"].iloc[0]/10, 1))
    print()


for wd in [weather_data1, weather_data2, weather_data3, weather_data4]:
    for i in range(1, 13):
        predict(i*100+1, wd)
        predict(i*100+15, wd)
