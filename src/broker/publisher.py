import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
import time

load_dotenv()

class Publisher:
    def __init__(self):
        self.brokerURL = os.getenv('BROKER_URL')
        self.port = int(os.getenv('BROKER_PORT'))
        self.client = mqtt.Client()
        self.client.username_pw_set(os.getenv('PUBLISHER_USERNAME'), os.getenv('PUBLISHER_PASSWORD'))
        self.client.tls_set()  # Set up TLS

    # Connect to the MQTT broker
    def connect(self):
        self.client.connect(self.brokerURL, self.port, 60)

    # Disconnect from the MQTT broker
    def disconnect(self):
        self.client.disconnect()

    # Publish a message
    def publish(self, city, TTF):
        self.connect()  # Connect to broker
        self.client.publish("city/"+city, TTF)  # Publish message
        time.sleep(1)  # Wait for 1 second (adjust as needed)
        self.disconnect()  # Disconnect from broker
