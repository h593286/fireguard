# Fireguard
 An ADA504 group-project

*By Fredrik Fluge, Daniel K.Gunleiksrud, Magnus Noreide and Eilert Skram*



# Instructions 

To replicate the project and to run it on your own device, please follow the instructions below.

## 1. Clone GitHub project
Clone the GitHub project.

If you are unsure on how to do this, follow this [link](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## 2. Add Frost Client-Id and Secret in GitHub
Now you need to add your Frost Client-Id and Frost Client-Secret.

This is done by doing the following steps:
- Enter the cloned repository
- Click *Settings*
- Click *Secrets and Variables*
- Click *Actions*
- In *Actions*, press *New Repository Secret*
- Put **name** as *FROST_CLIENT_ID* and **value** as your personal Frost Client-Id
- Press *Add Secret*
- Repeat process, but now for *FROST_CLIENT_SECRET*

## 3. Spin up development application
```haskell
docker compose -f docker-compose.yml -f docker-compose.development.yml up
```
API
[http://127.0.0.1:8080/](http://127.0.0.1:8080/index.html)

Autentisering
[http://127.0.0.1:8090](http://127.0.0.1:8090)

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
