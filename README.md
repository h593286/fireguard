# fireguard
 ADA504 project


## Spin up development application
```haskell
docker compose -f docker-compose.yml -f docker-compose.development.yml up
```

[http://127.0.0.1:8080/](http://127.0.0.1:8080/index.html)

## Get bearer token for protected endpoints:
for auth token, use postman or:
(need .env in api/authentication: "# keycloak
server_url=http://keycloak:8090/
realm=fireguard
token=")

```shell
export token=$(\
curl -X POST http://localhost:8090/realms/fireguard/protocol/openid-connect/token \
-d 'client_id=fireguard_client' \
-d 'username=admin&password=admin&grant_type=password'| jq --raw-output '.access_token' \
)
```

then, use token on one of the protected endpoints (postman or shell):
```shell
curl http://localhost:8080/60.3894/5.3300 -H "Authorization: Bearer "$token
```