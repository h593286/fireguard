import paho.mqtt.client as mqtt


brokerURL = 'c406645d204a4c93919e442f4c8bcc09.s1.eu.hivemq.cloud'
port = 8883

client = mqtt.Client()
client.tls_set()  # Set up TLS

##publish
def connect():
    client.connect("brokerURL", port, 60)
def disconnect():
    client.disconnect()

def publish(city, TTF):
    client.publish("test/topic", city + ", TTF: " + TTF)
