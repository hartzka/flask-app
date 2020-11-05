FROM ubuntu:16.04

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    python3-pip \
    gfortran \
    libopenblas-dev \
    liblapack-dev

RUN python3-pip install --upgrade python3-pip \
&& python3-pip install -r requirements.txt \
&& python3-pip install scikit-learn

COPY /app .

CMD ["python3", "app.py"]


