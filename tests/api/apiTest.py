from unittest import TestCase, main
from unittest.mock import MagicMock
from src.api.requesthandler.api_logic import FireLogic
from src.api.requesthandler.buildFireguardAPI import load_cities
from src.service.frcapi import FireRiskModelAPI, FireRiskPrediction,Location,FireRisk
import datetime


class MyTestCase(TestCase):
    def setUp(self):
        city = "Oslo"
        latitiude = 59.9133
        longitude = 10.7389
        
        cities = [{"city": city, "lat": latitiude, "lng": longitude}]
        self.firelogic = FireLogic(name="Fireguard", cities=cities, modelApi=MagicMock(spec=FireRiskModelAPI))

    def test_read_city(self):
        json_city = self.firelogic.read_city("Oslo")
        if json_city is not None:
            self.assertEqual(json_city["city"], "Oslo")
            self.assertIsInstance(json_city, dict)
        else:
            self.fail("read_city('Oslo') returned None, expected city string")

    def test_read_city_non_existing(self):
        json_city = self.firelogic.read_city("Doesn't exist")
        if json_city is None:
            self.assertIsNone(json_city)
        else:
            self.fail("read_city('Doesn't exist') returned a city string, expected None")


    def test_read_city_by_coordinates(self):
        lat = 59.9133
        lng = 10.7389
        json_city = self.firelogic.read_city_by_coordinates(lat, lng)
        if json_city is not None:
            self.assertEqual(json_city["city"], "Oslo")
            self.assertIsInstance(json_city, dict)
        else:
            self.fail(f"read_city_by_coordinates({lat}, {lng}) returned None, expected city string")

    def test_read_city_by_coordinates_non_existing(self):
        lat = 0
        lng = 0
        json_city = self.firelogic.read_city_by_coordinates(lat, lng)
        if json_city is None:
            self.assertIsNone(json_city)
        else:
            self.fail(f"read_city_by_coordinates({lat}, {lng}) returned a city string, expected None")

    def test_get_firerisk_by_city(self):
            # Arrange
            city = "Oslo"
            latitude = 59.9133
            longitude = 10.7389
            expected_prediction = FireRiskPrediction(location=Location(latitude=latitude, longitude=longitude), firerisks=[FireRisk(timestamp=datetime.datetime.now(), ttf=1.5)])
            self.firelogic.modelApi.compute = MagicMock(return_value=expected_prediction)

            # Act
            result = self.firelogic.get_firerisk_by_city(city)

            # Assert
            self.firelogic.modelApi.compute.assert_called_once_with(Location(latitude=latitude, longitude=longitude))
            self.assertEqual(result, expected_prediction)

    def test_get_firerisk_by_coordinates(self):
        # Arrange
        latitude = 59.9133
        longitude = 10.7389
        expected_prediction = FireRiskPrediction(location=Location(latitude=latitude, longitude=longitude), firerisks=[FireRisk(timestamp=datetime.datetime.now(), ttf=1.5)])
        self.firelogic.modelApi.compute = MagicMock(return_value=expected_prediction)

        # Act
        result = self.firelogic.get_firerisk_by_coordinates(latitude, longitude)

        # Assert
        self.firelogic.modelApi.compute.assert_called_once_with(Location(latitude=latitude, longitude=longitude))
        self.assertEqual(result, expected_prediction)


    #Intergration tests
    def test_get_cities(self):
        cities = load_cities()
        pass


if __name__ == '__main__':
    main()
