import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os

load_dotenv()

class Publisher:
    def __init__(self):
        self.brokerURL = 'c406645d204a4c93919e442f4c8bcc09.s1.eu.hivemq.cloud'
        self.port = 8883
        self.client = mqtt.Client()
        self.client.username_pw_set(os.getenv('PUBLISHER_USERNAME'),os.getenv('PUBLISHER_PASSWORD'))
        self.client.tls_set()  # Set up TLS

    ##publish
    def connect(self):
        self.client.connect(self.brokerURL, self.port, 60)
    def disconnect(self):
        self.client.disconnect()

    def publish(self,city, TTF):
        self.client.publish("test/topic", city + ", TTF: " + TTF)

        #Correct when implementation tested works
        #self.client.publish("city/"+city, TTF)

