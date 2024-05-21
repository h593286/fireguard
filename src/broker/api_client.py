from datetime import datetime, UTC, timedelta
import os
import requests

class ApiClient:

    def __init__(self) -> None:
        self.AUTH_URL = os.getenv("KEYCLOAK_SERVER_URL")
        self.REALM = os.getenv("KEYCLOAK_REALM_NAME")
        
        self.CLIENT_ID = os.getenv("CLIENT_ID")

        self.USER_ID = os.getenv("USER_ID")
        self.USER_PASSWORD = os.getenv("USER_PASSWORD")
        
        self.API_URL = os.getenv("FIREGUARD_API_URL")

        self.access_token = "none"
        self.token_expiry = datetime.now(UTC) - timedelta(1)
        
    def get_token(self) -> None:
        if self.token_expiry < datetime.now(UTC):
            response = requests.post(f"{self.AUTH_URL}/realms/{self.REALM}/protocol/openid-connect/token", data={
                'grant_type': 'password',
                'client_id': self.CLIENT_ID,
                'username': self.USER_ID,
                'password': self.USER_PASSWORD
            })
            json = response.json()

            self.token_expiry = datetime.now(UTC) + timedelta(seconds=int(json['expires_in'])-5)
            self.access_token = f'Bearer {json["access_token"]}'
        

    def get_data_for_city(self, name: str):
        format_str = '%Y-%m-%dT%H:%M:%SZ'
        ts_from =(datetime.now(UTC)- timedelta(hours=1)).strftime(format_str)
        ts_to = (datetime.now(UTC) + timedelta(hours=1)).strftime(format_str)

        self.get_token()

        response = requests.get(f"{self.API_URL}/fire_risk/city/{name}?ts_from={ts_from}&ts_to={ts_to}", headers={
            'Authorization': self.access_token
        })

        if response.status_code // 100 != 2:
            raise BaseException("not ok status")

        json = response.json()

        return json['firerisks']