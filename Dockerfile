FROM python:3.9.0b3-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& pip install -U scikit-learn \
&& pip install -r requirements.txt

COPY /app .

CMD ["python3", "app.py"]


