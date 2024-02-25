import unittest
from src.data.apihandler.apihandler import APIHandler
import datetime

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.apiHandler = APIHandler()
        self.today = datetime.date.today()
        self.timeSeries = [datetime.date(2024, 2, 12), datetime.date(2024,2,13)]

    def test_Observation(self):

        default_observation = self.apiHandler.getObservation(10,59)
        self.assertEqual(default_observation.status_code,200)

        singleDateobservation = self.apiHandler.getObservation(10, 59, self.today)
        self.assertEqual(singleDateobservation.status_code, 200)

        timeseriesobservation = self.apiHandler.getObservation(10,59,self.timeSeries)
        self.assertEqual(timeseriesobservation.status_code, 200)






    def test_Forcast(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
