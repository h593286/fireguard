import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("broker_address", 1883, 60)
client.publish("topic/name", "Hello MQTT")
client.disconnect()
