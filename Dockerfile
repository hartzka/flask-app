FROM python:3.10.0a2-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& pip install -r requirements.txt

COPY /app .

CMD ["python3", "app.py"]


