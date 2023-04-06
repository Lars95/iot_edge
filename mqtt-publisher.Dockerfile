FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY temperature_sensor.py ./

CMD [ "python", "temperature_sensor.py" ]
