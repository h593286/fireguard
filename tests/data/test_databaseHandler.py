import unittest
from datetime import UTC, datetime
import mongomock

from src.data.dataTypes import Location, Observations, WeatherDataPoint
from src.data.databasehandler.mongodb import MongoDbHandler


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.nonexisting_location = Location(latitude=20, longitude=20)
        self.existing_location = Location(latitude=30, longitude=30)
        self.location_to_add = Location(latitude=40, longitude=50)
        self.observation_to_add = [
            WeatherDataPoint(
                timestamp=datetime(year=2024, month=8, day=4, hour=3, second=24, minute=4, tzinfo=UTC),
                humidity=4,
                wind_speed=5.3,
                temperature=11.3),
            ]
        
        self.date = datetime(2024, 5, 24, 5, minute=30, second=35)
        

        self.mockClient = mongomock.MongoClient()

        observations = self.mockClient.get_database("observations")
        collection = observations.get_collection(str(self.existing_location))



        collection.insert_one({       
            'timestamp': '2024|05|24|05',
            'temperature': 25,
            'humidity': 5.0,
            'wind_speed': 5.0
        })
        
        self.databaseHandler = MongoDbHandler(mongo_client=self.mockClient)
        
    def test_getObservation_withNonExistingEntry_returnsNone(self):
        observation = self.databaseHandler.getObservation(location=self.nonexisting_location, time=self.date)
        self.assertIsNone(observation, "Should not return observation for nonexisting entry")
        
    def test_getObservation_withStoredEntry_returnsObservation(self):
        observation: Observations = self.databaseHandler.getObservation(location=self.existing_location, time=self.date) # type: ignore
        
        self.assertIsNotNone(observation, "Should return observation")
        self.assertEqual(len(observation.data), 1, "Should only have one entry")
    
        self.assertIsNotNone(observation, "Should return observation")
        self.assertEqual(len(observation.data), 1, "Should only have one entry")
        self.assertEqual(observation.data[0].timestamp, datetime(year=2024, month=5, day=24, hour=5, minute=0, second=0, tzinfo=UTC), "Should have datetime from key")
        self.assertEqual(observation.data[0].temperature, 25, "Should be 25 degrees")
        self.assertEqual(observation.data[0].humidity, 5, "Should be 5 humidity")
        self.assertEqual(observation.data[0].wind_speed, 5, "Should be 5 wind_speed")
    
    def test_addObservation_addsObservation(self):
        self.databaseHandler.storeObservations(self.location_to_add, self.observation_to_add)
        observation: dict = self.mockClient.get_database("observations").get_collection(str(self.location_to_add)).find_one({'timestamp': '2024|08|04|03'}) # type: ignore
        self.assertIsNotNone(observation)
        self.assertEqual(observation['timestamp'], '2024|08|04|03')
        self.assertEqual(observation['temperature'], 11.3)
        self.assertEqual(observation['humidity'], 4)
        self.assertEqual(observation['wind_speed'], 5.3)

    
if __name__ == '__main__':
    unittest.main()
