import pandas as pd
from sklearn.ensemble import IsolationForest
import paho.mqtt.client as mqtt
import pickle

# Load the trained model from the pickle file
with open('isolation_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define MQTT broker parameters
broker_address = "mqtt-broker"  # Replace with your MQTT broker address
broker_port = 8250

# Create MQTT client instance and connect to MQTT broker
client = mqtt.Client()
client.connect(broker_address, broker_port)

topic = "sensors/rpi"
ml_topic = "ml_scores/anomalies"

# Load trained model
with open('isolation_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define variables to store latest temperature and humidity
latest_temperature = None
latest_humidity = None

# Define function to score data and publish results to MQTT
def score_and_publish(client, data):
    # Convert data to DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'temperature', 'humidity'])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Set timestamp as index
    df.set_index('timestamp', inplace=True)

    # Score data using isolation forest model
    scores = model.score_samples(df[['temperature', 'humidity']])

    # Publish scores to MQTT
    for score in scores:
        client.publish(ml_topic, str(score))

# Define function to handle MQTT messages
def on_message(client, userdata, message):
    global latest_temperature, latest_humidity
    # Parse message payload
    payload = str(message.payload.decode("utf-8"))
    if 'temperature' in payload:
        # Parse temperature data from payload
        latest_temperature = float(payload.split('temperature=')[1].split()[0])
    elif 'humidity' in payload:
        # Parse humidity data from payload
        latest_humidity = float(payload.split('humidity=')[1])
    if latest_temperature is not None and latest_humidity is not None:
        # Get current timestamp
        timestamp = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create data array
        data = [[timestamp, latest_temperature, latest_humidity]]

        # Score data and publish results to MQTT
        score_and_publish(client, data)

        # Reset variables
        latest_temperature = None
        latest_humidity = None

# Connect to MQTT broker and subscribe to topic
client.on_message = on_message
client.subscribe(topic)

# Start MQTT loop
client.loop_forever()
