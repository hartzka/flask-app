FROM alpine:latest


WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    python3-pip
RUN pip install --upgrade pip \
&& pip install -r requirements.txt

COPY /app .

CMD ["python3", "app.py"]


