FROM python:3.6.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

CMD ["python", "app.py"]


