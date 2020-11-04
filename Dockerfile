FROM python:3.5-alpine


WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& pip download scipy==1.3 \
&& pip install -r requirements.txt

COPY /app .

CMD ["python3", "app.py"]


