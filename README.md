# fireguard
 ADA504 project


## Spin up development application
```haskell
docker compose -f docker-compose.yml -f docker-compose.development.yml up
```

[http://127.0.0.1:8080/](http://127.0.0.1:8080/index.html)

## Run keycloak server:

from src/api/authentication/keycloak-23.0.7 run:

```haskell
    bin/kc.sh start-dev --http-port 8090
```

(.bat for windows, .sh for mac/linux)

[http://localhost:8090] (username= admin, password= admin)

for auth token, use postman or:

```shell
export token=$(\
curl -X POST http://{IP-address}:8080/realms/SmartOcean/protocol/openid-connect/token \
-d 'client_id=fireguard_client' \
-d 'username=admin&password=admin&grant_type=password'| jq --raw-output '.access_token' \
)
```

then, use token on one of the protected endpoints (postman or shell):
```shell
curl http://localhost:8080/60.3894/5.3300 -H "Authorization: Bearer "$token
```