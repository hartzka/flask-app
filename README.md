Weather analyzer and predictor that uses open data from [ilmatieteenlaitos](https://www.ilmatieteenlaitos.fi/havaintojen-lataus)

[![CircleCI](https://circleci.com/gh/hartzka/flask-app.svg?style=shield)](https://app.circleci.com/pipelines/github/hartzka/flask-app)

The project is running at heroku: https://flaskapp12121.herokuapp.com/

How to run locally:
run `python app/app.py` to start the application.
The application should be running at `localhost:5000`

run `python test_linear.py` or `python test_decision_trees.py` to
test the models and to get predictions.

run `python script.py` to generate weather data files in csv format that the application uses. The weather data source folder is `/weatherdata` and the script generates merged csv files for each weather station in `/app/data`. It also generates `weather_data.html` page in `/app/templates`.
