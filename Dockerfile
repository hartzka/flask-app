FROM ubuntu:16.04

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
&& pip install -r requirements.txt \
&& apt-get install gfortran libopenblas-dev liblapack-dev \
&& pip install scikit-learn

COPY /app .

CMD ["python3", "app.py"]


