FROM python:3.9.0b3-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& pip install scipy

COPY /app .

CMD ["python3", "app.py"]


