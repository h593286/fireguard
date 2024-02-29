import unittest
from src.data.dataTypes import Location, Observations, Forecast
from src.service.datacollector.dataCollector import DataCollector

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.dataCollector = DataCollector()
        self.location = Location(longitude=10, latitude=59)
    def test_observation(self):
        observation = self.dataCollector.collectObservation(self.location)
        self.assertIsInstance(observation, Observations)

    def test_forecast(self):
        forecast = self.dataCollector.collectForecast(self.location)
        self.assertIsInstance(forecast, Forecast)


if __name__ == '__main__':
    unittest.main()
