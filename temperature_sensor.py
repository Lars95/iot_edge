import paho.mqtt.client as mqtt
import time
import board
import adafruit_dht

# Define MQTT broker parameters
broker_address = "mqtt-broker"  # Replace with your MQTT broker address
broker_port = 8250

# Create MQTT client instance and connect to MQTT broker
client = mqtt.Client()
client.connect(broker_address, broker_port)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D2, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    
    # Construct MQTT message
    message = f"dht22 temperature={temperature}"
    # Publish MQTT message
    client.publish("sensors/rpi", message)
    message = f"dht22 humidity={humidity}"
    # Publish MQTT message
    client.publish("sensors/rpi", message)
    # Wait for 10 seconds
    time.sleep(10)
