FROM python:3.9.0b3-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& apt-get install python3-sklearn python3-sklearn-lib python3-sklearn-doc \
&& pip install -r requirements.txt

COPY /app .

CMD ["python3", "app.py"]


