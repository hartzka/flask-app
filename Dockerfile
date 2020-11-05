FROM ubuntu:17.04

WORKDIR /app

COPY requirements.txt .

RUN set -xe \
&& apt-get update && apt-get install -y \
    python3.6 \
    python3-pip \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
&& python3 -m pip install --upgrade pip \
&& python3 -m pip install -r requirements.txt \
&& python3 -m pip install scikit-learn

COPY /app .

CMD ["python3", "app.py"]


