import paho.mqtt.client as mqtt


brokerURL = 'c406645d204a4c93919e442f4c8bcc09.s1.eu.hivemq.cloud'
port = 8883

client = mqtt.Client()
client.tls_set()  # Set up TLS
client.connect("brokerURL", port, 60)

# Publish a message
client.publish("test/topic", "Hello from Python over WebSockets!")

# Disconnect from the broker
client.disconnect()

