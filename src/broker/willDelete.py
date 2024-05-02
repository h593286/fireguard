from src.broker.publisher import Publisher



publisher = Publisher()
publisher.connect()
publisher.publish("city test", "ttf test4")