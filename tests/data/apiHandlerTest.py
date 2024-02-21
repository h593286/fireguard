import unittest
from src.data.apihandler.apihandler import APIHandler

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.apiHandler = APIHandler()
    def test_Observation(self):
        observation = self.apiHandler.getObservation(10,59)
        self.assertEqual(observation.status_code,200)

    def test_Forcast(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
