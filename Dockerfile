FROM python:3.6-alpine


WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& pip download scipy==1.3 \
&& pip install -r requirements.txt

COPY /app .

CMD ["python3", "app.py"]


