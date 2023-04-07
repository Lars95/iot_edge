import time
import random
import logging
import board
import adafruit_dht
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Define here if the dht22 sensor or a random number should be used
use_dht22 = False

# Define MQTT broker parameters
broker_address = "mqtt-broker"  # Replace with your MQTT broker address
broker_port = 8250

# Create MQTT client instance and connect to MQTT broker
client = mqtt.Client()
client.connect(broker_address, broker_port)

if use_dht22:
    # Initial the dht device, with data pin connected to:
    # Here the data pin is connected to GPIO2
    dhtDevice = adafruit_dht.DHT22(board.D2, use_pulseio=False)

while True:
    if use_dht22:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

        except RuntimeError as error:
            logging.error(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            logging.error("DHT exit")
            raise error
    else:
        temperature = random.uniform(0,50)
        humidity = random.uniform(0,50)
    
    # Construct MQTT message
    message = f"dht22 temperature={temperature}"
    # Publish MQTT message
    client.publish("sensors/rpi", message)
    message = f"dht22 humidity={humidity}"
    # Publish MQTT message
    client.publish("sensors/rpi", message)
    logging.info(f"Published msg: {message} (Use dht: {str(use_dht22)})")
    # Wait for 10 seconds
    time.sleep(10)
