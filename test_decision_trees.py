import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
col_names = ["year","d","time","clouds","pressure","humidity","rain","snow","temperature",
"dew_temperature","visibility","wind_direction","gust_speed","wind_speed","area"]
weather_data = pd.read_csv("app/data/weather_vantaa.csv", header=1, names=col_names)
feature_cols=[1,2,3,4,5,6,7,9,10,11,12,13]
X = weather_data.iloc[:,feature_cols]
y = weather_data.temperature

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, train_size=0.75, random_state=50)
classifier = DecisionTreeClassifier()
classifier = classifier.fit(X_train,y_train)
y_pred = classifier.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Prediction:", classifier.predict([[707,13,5.0,1000.0,77.0,0.0,-1.0,12.1,50000.0,11.0,5.7,4.2]]))