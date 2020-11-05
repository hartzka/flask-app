FROM ubuntu:16.04

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
&& pip install --upgrade pip \
&& pip install -r requirements.txt \
&& pip install scikit-learn

COPY /app .

CMD ["python3", "app.py"]


