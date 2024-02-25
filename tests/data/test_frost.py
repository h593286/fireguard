import unittest
from src.data.apihandler.frostClient import FrostClient
import src.data.dataTypes as dt

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.handler = FrostClient()

    def test_Station(self):
        location = dt.Location(longitude=10, latitude=59)
        nearest = self.handler.nearestStation(location)
        target = 'SN30242'
        self.assertEqual(target, nearest)

    def test_Observation(self):
        location = dt.Location(longitude=10, latitude=59)
        r = self.handler.sendObservationRequest(location)
        self.assertEqual(r.status_code,200)

if __name__ == '__main__':
    unittest.main()
