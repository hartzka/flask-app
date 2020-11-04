FROM ubuntu:16.04
FROM python:3.9.0b3-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& apt-get install gfortran libopenblas-dev liblapack-dev \
&& pip install scikit-learn

COPY /app .

CMD ["python3", "app.py"]


