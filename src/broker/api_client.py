from datetime import datetime, UTC, timedelta
import os
import requests

# {
#   "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI3YXNTelpGVktIVmNnTkZEUHNyWHJJN2dIdm4wdGQ2dWRKVUp2clplMzh3In0.eyJleHAiOjE3MTQ2NzUzODIsImlhdCI6MTcxNDY3NTA4MiwianRpIjoiNWZmN2FhMDEtZGU4NS00NmE3LWJmNWItZTNhMjQ0NjQzYTQ1IiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDkwL3JlYWxtcy9maXJlZ3VhcmQiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiYzMzNTk5MzMtN2QwNi00YWRiLWI5Y2EtMzVjYjdmN2FmYmE2IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZmlyZWd1YXJkX2NsaWVudCIsInNlc3Npb25fc3RhdGUiOiI2ZDQ3Zjk2MC1mZTlhLTQ2YWUtOWRkZC1kMjg3OTg0MmQ5Y2EiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLWZpcmVndWFyZCIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJBRE1JTiIsIlVTRVIiXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJzaWQiOiI2ZDQ3Zjk2MC1mZTlhLTQ2YWUtOWRkZC1kMjg3OTg0MmQ5Y2EiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsInByZWZlcnJlZF91c2VybmFtZSI6ImFkbWluIn0.MrUsxKX6iYV7GZhiZq0JtsnX3EimSAw34QXMVnOFxGlBTRUs7Urebe0V0tACzWdBo6GYKyWH0GVPirxKLAwWp5U1094rPHP7CAQUydO68MaOrD2cnnkFEGsrEYzVtoxdZ8Itm-uAzKaBFl2NerVoisrFcgaxfN5VO0850BW0LZteb6-cWyNWO6SL9OUC8weQzQE5hLXccwxd1VgPPJcIQDs0tlS9IhzR8TfEhR2aGRjG5RbO7KE1yIBG785Uv7zyJK85NrjYEginPE-928XgOOLpLVjC6jBEJ8G-g9XFt8NryqssiuxGEgCeyzcfa3HM7r6Uf7WgeN28hAIjwANT6Q",
#   "expires_in": 300,
#   "refresh_expires_in": 1800,
#   "refresh_token": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI4MTU5Y2Q4ZS1jYTJhLTRmM2ItOGQ3OS1lYWViZmI5NWVlZDMifQ.eyJleHAiOjE3MTQ2NzY4ODIsImlhdCI6MTcxNDY3NTA4MiwianRpIjoiNTc4YTBkNGUtMDk1NS00ZTI0LWE3MDYtOTlmNTNkMzFlMTBlIiwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDkwL3JlYWxtcy9maXJlZ3VhcmQiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjgwOTAvcmVhbG1zL2ZpcmVndWFyZCIsInN1YiI6ImMzMzU5OTMzLTdkMDYtNGFkYi1iOWNhLTM1Y2I3ZjdhZmJhNiIsInR5cCI6IlJlZnJlc2giLCJhenAiOiJmaXJlZ3VhcmRfY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6IjZkNDdmOTYwLWZlOWEtNDZhZS05ZGRkLWQyODc5ODQyZDljYSIsInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6IjZkNDdmOTYwLWZlOWEtNDZhZS05ZGRkLWQyODc5ODQyZDljYSJ9.Dai5MqCoynvgXcZvCZwOaTcJgM1WJJFVM-H3ZyrBoOHplaHyoFETbdblBwUTZJlUz28Wrtx6hqVBhKPXmuJdBQ",
#   "token_type": "Bearer",
#   "not-before-policy": 0,
#   "session_state": "6d47f960-fe9a-46ae-9ddd-d2879842d9ca",
#   "scope": "profile email"
# }


class ApiClient:

    def __init__(self) -> None:
        #self.AUTH_URL = os.getenv("AUTH_URL")
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.USER_PASSWORD = os.getenv("USER_PASSWORD")
        self.USER_ID = os.getenv("USER_ID")
        self.access_token = "none"
        self.token_expiry = datetime.now(UTC) - timedelta(1)
        
    def get_token(self) -> None:
        if self.token_expiry < datetime.now(UTC):
            response = requests.post("http://keycloak:8080/realms/fireguard/protocol/openid-connect/token", data={
                'grant_type': 'password',
                'client_id': self.CLIENT_ID,
                'username': self.USER_ID,
                'password': self.USER_PASSWORD
            })
            json = response.json()

            self.token_expiry = datetime.now(UTC) + timedelta(seconds=int(json['expires_in'])-5)
            self.access_token = f'Bearer {json["access_token"]}'
        

    def get_data_for_city(self, name: str):
        ts_from =(datetime.now(UTC)- timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        ts_to = (datetime.now(UTC) + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%SZ')

    

        self.get_token()
        
        response = requests.get(f"http://web-api:80/fire_risk/city/{name}?ts_from={ts_from}&ts_to={ts_to}", headers={
            'Authorization': self.access_token
        })

        if response.status_code // 100 != 2:
            raise BaseException("not ok status")

        json = response.json()

        return json['firerisks']
        
        

        