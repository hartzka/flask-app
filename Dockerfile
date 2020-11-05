FROM ubuntu:16.04

WORKDIR /app

COPY requirements.txt .

RUN set -xe \
&& apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
&& python3 -m pip3 install --upgrade pip \
&& pip3 install -r requirements.txt \
&& pip3 install scikit-learn

COPY /app .

CMD ["python3", "app.py"]


