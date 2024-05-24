from re import S
import unittest
from datetime import datetime
from mongomock import MongoClient

from src.data.dataTypes import Location, Observations
from src.data.databasehandler.mongodb import MongoDbHandler


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.nonexisting_location = Location(latitude=20, longitude=20)
        self.existing_location = Location(latitude=30, longitude=30)
        
        self.date = datetime(2024, 5, 24, 5, minute=30, second=35)
        
        mockClient = MongoClient()
        observations = mockClient.db.get_collection("Observations")

        observations.insert_one({       
            'timestamp': '2024|05|24|5',
            'temperature': 25,
            'humidity': 5.0,
            'wind_speed': 5.0
        })
        
        
        self.databaseHandler = MongoDbHandler(mongo_client=MongoClient())
        
    def test_getObservation_withNonExistingEntry_returnsNone(self):
        observation = self.databaseHandler.getObservation(location=self.nonexisting_location, time=self.date)
        self.assertIsNone(observation, "Should not return observation for nonexisting entry")
        
    def test_getObservation_withStoredEntry_returnsObservation(self):
        observation: Observations = self.databaseHandler.getObservation(location=self.existing_location, time=self.date) # type: ignore
        
        self.assertIsNotNone(observation, "Should return observation")
        self.assertEqual(len(observation.data), 1, "Should only have one entry")
        self.assertEqual(observation.data[0].timestamp, datetime(year=2024, month=5, day=24, hour=5, minute=0, second=0), "Should have datetime from key")
        self.assertEqual(observation.data[0].temperature, 25, "Should be 25 degrees")
        self.assertEqual(observation.data[0].humidity, 5, "Should be 5 humidity")
        self.assertEqual(observation.data[0].wind_speed, 5, "Should be 5 wind_speed")
        


if __name__ == '__main__':
    unittest.main()
