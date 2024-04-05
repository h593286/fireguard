
from unittest import TestCase, main
from unittest.mock import MagicMock
from urllib.parse import urljoin
import datetime
import os
from dotenv import load_dotenv
import requests
import urllib.parse

# Fireguard API
from src.api.requesthandler.api_logic import FireLogic
from src.api.requesthandler.buildFireguardAPI import load_cities
from src.service.frcapi import FireRiskModelAPI, FireRiskPrediction,Location,FireRisk
import src.api.requesthandler.api_server as api_server


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

    #================================================================================================================
    #Intergration tests
    #================================================================================================================
class myIntegrationTests(TestCase):      

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

    #only want this setup to run once, not once for every test
    @classmethod
    def setUpClass(cls):
        # Set up test client #TODO: make dynamic
        load_dotenv('src/api/authentication/.env')
        credentials = {"client_id": "fireguard_client", "username": "test", "password": "test", "grant_type": "password"}
        credentials_encoded = urllib.parse.urlencode(credentials)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        base_url = os.environ.get('BASE_URL')
        token_endpoint = os.environ.get('TOKEN_ENDPOINT')
        token_endpoint = urljoin(base_url, token_endpoint)

        response = requests.post(token_endpoint, data=credentials_encoded, headers=headers)
        cls.token = response.json().get('access_token')
        # Assert
        assert response.status_code == 200
        assert cls.token is not None


    def test_load_cities(self):
        # Act
        cities = load_cities()
        # Assert
        assert len(cities) > 0
        assert isinstance(cities, list)

    def test_city_public_endpoint(self):
        # Act
        response = client.get(f'/{self.expected_result["city"]}')

        # Assert 
        assert response.status_code == 200
        assert response.json() == self.expected_result

    # Test user authentication
    
    def test_lat_lng_protected_user_endpoint(self):
        # Act
        _headers = {"Authorization": f"Bearer {self.token}"}

        response = requests.get(f"http://127.0.0.1:8080/{self.expected_result['lat']}/{self.expected_result['lng']}", headers=_headers)
        # Assert
        assert response.status_code == 200
        assert response.json() == self.expected_result

   #TODO: fix this test:
    def test_protected_admin_endpoint(self):
        _headers = {"Authorization": f"Bearer {self.token}"}
        #response = client.get('/api/v1/admin', headers=_headers)

        #assert response.status_code == 200
        #assert response.json() == {"Data": "This is a protected resource for ADMIN role."}

    if __name__ == '__main__':
        main()
