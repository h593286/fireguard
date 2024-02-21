import unittest
from src.data.apihandler.frostClient import FrostClient

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.handler = FrostClient()
    def test_Station(self):
        nearest = self.handler.nearestStation(10, 59)
        target = 'SN30242'
        self.assertEqual(target, nearest)

    def test_Observation(self):
        r = self.handler.sendObservationRequest(10,59)
        self.assertEqual(r.status_code,200)



if __name__ == '__main__':
    unittest.main()
