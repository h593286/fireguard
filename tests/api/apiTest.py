from unittest import TestCase, main
from unittest.mock import MagicMock, Mock
from src.api.requesthandler.api_logic import FireLogic
from src.api.requesthandler.buildFireguardAPI import load_cities
from src.service.frcapi import FireRiskModelAPI

class MyTestCase(TestCase):
    def setUp(self):
        cities = load_cities()
        self.firelogic = FireLogic(name="Fireguard", cities=cities, modelApi=MagicMock(spec=FireRiskModelAPI))

    def test_read_city(self):
        json_city = self.firelogic.read_city("Oslo")
        if json_city is not None:
            self.assertEqual(json_city["city"], "Oslo")
        else:
            self.fail("read_city('Oslo') returned None, expected city string")

    def test_read_city_non_existing(self):
        json_city = self.firelogic.read_city("Doesn't exist")
        if json_city is None:
            self.assertIsNone(json_city)
        else:
            self.fail("read_city('Doesn't exist') returned a city string, expected None")


'''    def test_read_city_by_coordinates(self):
        self.assertEqual(True, False)

    def test_get_firerisk_by_city(self):
        self.assertEqual(True, False)

    def test_get_firerisk_by_coordinates(self):
        self.assertEqual(True, False)
    
    def test_get_firerisk_by_coordinates_now(self):
        self.assertEqual(True, False)'''
    


if __name__ == '__main__':
    main()
