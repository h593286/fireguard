import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

class Publisher:
    def __init__(self):
        self.brokerURL = os.getenv('BROKER_URL', '')
        self.port = int(os.getenv('BROKER_PORT', 0))
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
    # Topic = city name, i.e city = bergen
    # TTF = ttf value
    # Usage example: publisher.publish('Bergen', '1234')
    def publish(self, city, TTF):
        self.client.publish(city, TTF)  # Publish message