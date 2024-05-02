import paho.mqtt.client as mqtt

# Create a client instance
client = mqtt.Client(transport='websockets')

localHost = "127.0.0.1"

# Connect to the broker
client.connect(localHost, 8081)  # Use WebSocket port, typically 8080 or 9001

# Publish a message
client.publish("test/topic", "Hello from Python over WebSockets!")

# Disconnect from the broker
client.disconnect()


