FROM python:3.8-slim-buster

WORKDIR /app

# gcc is needed to install all needed python packages
# Caused errors in the past
RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir paho-mqtt adafruit-circuitpython-dht RPi.GPIO

COPY temperature_sensor.py ./

CMD [ "python", "temperature_sensor.py" ]
