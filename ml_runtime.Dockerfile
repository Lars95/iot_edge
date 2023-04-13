FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas paho-mqtt numpy scipy scikit-learn

# Copy the Python script and the trained model
COPY score_dht22_anomalies.py .
COPY isolation_forest_model.pkl .

# Run the Python script to continuously score anomalies and publish the results via MQTT
CMD ["python", "score_dht22_anomalies.py"]
