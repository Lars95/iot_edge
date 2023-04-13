FROM python:3.8-slim-buster

WORKDIR /app

RUN pip install --no-cache-dir pandas scikit-learn paho-mqtt

# Copy the Python script and the trained model
COPY score_dht22_anomalies.py .
COPY isolation_forest_model.pkl .

# Run the Python script to continuously score anomalies and publish the results via MQTT
CMD ["python", "score_dht22_anomalies.py"]
