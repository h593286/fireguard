# fireguard
 ADA504 project

## Clone GitHub project
Frist clone the GitHub project.
If unsure how to do this, follow this [link](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

## Add Frost client-key and secret in GitHub
This is done by doing the following
- Enter the cloned repository
- Click *Settings*
- Click *Secrets and Variables*
- Click *Actions*
- In *Actions*, press *New Repository Secret*
- Put name as *FROST_CLIENT_ID* and value as your Frost Client-Id
- Press *Add Secret*
- Repeat process, but now for *FROST_CLIENT_SECRET*

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
 (username= admin, password= admin)

[http://localhost:8090](http://127.0.0.1:8090)

for auth token, use postman or:

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
