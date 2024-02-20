import unittest
from src.data.apihandler.frostHandler import FrostHandler

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.handler = FrostHandler()
    def test_Station(self):
        nearest = self.handler.nearestStation(10, 59)
        target = 'SN30242'
        self.assertEqual(target, nearest)

    def test_Observation(self):
        source = 'SN30242'
        r = self.handler.sendObservationRequest(source)
        self.assertEqual(r.status_code,200)



if __name__ == '__main__':
    unittest.main()
