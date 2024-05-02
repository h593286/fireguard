from src.broker.publisher import Publisher


publisher = Publisher()
publisher.connect()

# List of cities and corresponding TTF (time to fire) values you want to publish
data_to_publish = [("Stavanger", "Should not see this"),
                   ("Bergen", "success"),
                   ("Oslo", "Should not see this")]

# Publish each item in the list
for city, ttf in data_to_publish:
    publisher.publish(city, ttf)

print('ferdig')

