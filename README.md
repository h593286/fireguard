# Fireguard
 An ADA504 group-project

*By Fredrik Fluge, Daniel K.Gunleiksrud, Magnus Noreide and Eilert Skram*



# Instructions 

To replicate the project and to run it on your own device, please follow the instructions below.

## 1. Clone GitHub project
Clone the GitHub project.

If you are unsure on how to do this, follow this [link](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## 2. Add the .env file to the project
the `.env` file should be placed in the folder `src/data/apihandler/`, and contain the following values
```env
FROST_CLIENT_ID=<your client id>
FROST_CLIENT_SECRET=<your client secret>

MONGO_DB_CONNECTION_STRING=mongodb://username:password@fireguard-database:27017/admin?retryWrites=true&loadBalanced=false&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1
```

## 3. Spin up development application
```haskell
docker compose -f docker-compose.yml -f docker-compose.development.yml up
```

API server
[http://127.0.0.1:8080/](http://127.0.0.1:8080)

Authorization server
[http://127.0.0.1:8090](http://127.0.0.1:8090)

## Get bearer token for protected endpoints:
for auth token, use postman or shell:

```shell
export token=$(\
curl -X POST http://localhost:8090/realms/fireguard/protocol/openid-connect/token \
-d 'client_id=fireguard_client' \
-d 'username=admin&password=password&grant_type=password'| jq --raw-output '.access_token' \
)
```

then, use token on one of the protected endpoints (postman or shell):
```shell
curl http://localhost:8080/60.3894/5.3300 -H "Authorization: Bearer "$token
```

