# Fireguard
 An ADA504 group-project

*By Fredrik Fluge, Daniel K.Gunleiksrud, Magnus Noreide and Eilert Skram*


# Architecture
The project is a monorepo (barley) micro-service. Each component is split into its respective folder and the broker aspect of the architecture is separated out. 

![ADA524 - Page 1(1)](https://github.com/h593286/fireguard/assets/69848516/ac06372c-1e74-461d-be83-9b4cfc8fa97a)

## GitHub Structure

**src/**
api (API layer):
- logic: Contains functions with the logic thats being executed when the endpoints are called
- server: Endpoint hosting
- build: Init and builds the API

broker:
- publisher: The TTF publisher, publishes TTF to the HiveMQ. Runs through the list of cities and publishes their respective TTF at a set time-interval (i.e once a day)-
- runner: Runs the publisher, maintains uptime
- api client: Enables communication with the api for the broker 

client:
- clientprototype: The webclient prototype, now no longer functional for Get req to the api (Does not have auth), but acts as a subscriber. Displays the subscribed city.

data (data layer):
- apihandler: The apihandler and the respective api clients for external api-servies, i.e MET and FROST.  
- databasehandler: the databasehandlers for storage and collection of existing data
- dataextractor: Component for extracting data from weather servies into correct format.

service (Service layer):
- TTFmodel: Model for calculating TTF
- datacollector: The component responsible for collecting data
- frcapi: Business logic

# Instructions 

To replicate the project and to run it on your own device, please follow the instructions below.
### Pre-req:
- HiveMQ: https://console.hivemq.cloud/ (Create subscriber and publisher)
- Poetry
- Docker
- MongoDB

## 1. Clone GitHub project
Clone the GitHub project.

If you are unsure on how to do this, follow this [link](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).


## 2. Add the .env files to the project
add a `.env` file in the root folder of the repository and add the following values
```cs
FROST_CLIENT_ID=<your client id>
FROST_CLIENT_SECRET=<your client secret>

MONGO_DB_CONNECTION_STRING=mongodb://username:password@fireguard-database:27017/admin?retryWrites=true&loadBalanced=false&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1

BROKER_URL = the broker url
BROKER_PORT= the broker port
PUBLISHER_USERNAME = your publisher's username
PUBLISHER_PASSWORD = your publisher's password
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
curl http://localhost:8080/fire_risk/city/Bergen?ts_from=2024-04-30T21:59:59Z&ts_to=2024-05-09T18:59:59Z -H "Authorization: Bearer "$token
```


