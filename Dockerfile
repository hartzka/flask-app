FROM alpine:latest


WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip \
&& pip install -r requirements.txt

COPY /app .

CMD ["python", "app.py"]


