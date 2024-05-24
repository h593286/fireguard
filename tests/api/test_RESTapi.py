
from unittest import TestCase, main
from unittest.mock import MagicMock
import datetime

# Fireguard API
from src.api.requesthandler.api_logic import FireLogic
from src.data.dataTypes import FireRisk
from src.service.frcapi import FireRiskModelAPI, FireRiskPrediction,Location


# REST API
from src.api.requesthandler.api_server import app
from fastapi.testclient import TestClient

client = TestClient(app)

class MyTestCase(TestCase):
    def setUp(self):
        self.expected_result = {
            "city": "Oslo", 
            "lat": "59.9133", 
            "lng": "10.7389", 
            "country": "Norway", 
            "iso2": "NO", 
            "admin_name": "Oslo", 
            "capital": "primary", 
            "population": "1064235", 
            "population_proper": "709037"
        }
        
        cities = [{"city": self.expected_result['city'], "lat": self.expected_result['lat'], "lng": self.expected_result['lng']}]
        self.firelogic = FireLogic(name="Fireguard", cities=cities, modelApi=MagicMock(spec=FireRiskModelAPI))

    def test_read_city(self):
        json_city = self.firelogic.read_city(self.expected_result["city"])
        if json_city is not None:
            self.assertEqual(json_city["city"], self.expected_result["city"])
            self.assertIsInstance(json_city, dict)
        else:
            self.fail(f"read_city('{self.expected_result['city']}') returned None, expected city string")

    def test_read_city_non_existing(self):
        json_city = self.firelogic.read_city("Doesn't exist")
        if json_city is None:
            self.assertIsNone(json_city)
        else:
            self.fail("read_city('Doesn't exist') returned a city string, expected None")


    def test_read_city_by_coordinates(self):
        json_city = self.firelogic.read_city_by_coordinates(float(self.expected_result["lat"]), float(self.expected_result["lng"]))
        if json_city is not None:
            self.assertEqual(json_city["city"], self.expected_result['city'])
            self.assertIsInstance(json_city, dict)
        else:
            self.fail(f"read_city_by_coordinates({float(self.expected_result['lat'])}, {float(self.expected_result['lng'])}) returned None, expected city string")

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
            expected_prediction = FireRiskPrediction(location=Location(
                latitude=float(self.expected_result['lat']), longitude=float(self.expected_result['lng'])),
                  firerisks=[FireRisk(timestamp=datetime.datetime.now(), 
                    ttf=1.5)])
            self.firelogic.modelApi.compute = MagicMock(return_value=expected_prediction)

            # Act
            result = self.firelogic.get_firerisk_by_city(self.expected_result['city'])

            # Assert
            self.firelogic.modelApi.compute.assert_called_once_with(
                Location(
                    latitude=float(self.expected_result['lat']),
                    longitude=float(self.expected_result['lng']))
                    )
            self.assertEqual(result, expected_prediction)

    def test_get_firerisk_by_coordinates(self):
        # Arrange
        expected_prediction = FireRiskPrediction(
            location=Location(
                latitude=float(self.expected_result['lat']),
                longitude=float(self.expected_result['lng'])
                ), 
            firerisks=[
                FireRisk(timestamp=datetime.datetime.now(), 
                ttf=1.5)
                ]
            )
        self.firelogic.modelApi.compute = MagicMock(return_value=expected_prediction)

        # Act
        result = self.firelogic.get_firerisk_by_coordinates(float(self.expected_result['lat']), float(self.expected_result['lng']))

        # Assert
        self.firelogic.modelApi.compute.assert_called_once_with(
            Location(
                latitude=float(self.expected_result['lat']), 
                longitude=float(self.expected_result['lng'])
                )
            )
        self.assertEqual(result, expected_prediction)


    if __name__ == '__main__':
        main()
