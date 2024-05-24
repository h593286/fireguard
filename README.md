# Fireguard
 An ADA504 group-project

*By Fredrik Fluge, Daniel K.Gunleiksrud, Magnus Noreide and Eilert Skram*


# Architecture
The project is a monorepo  micro-service (bearly). Each component is split into its respective folder and the broker aspect of the architecture is separated out. 

![ADA524 - Page 1(1)](https://github.com/h593286/fireguard/assets/69848516/ac06372c-1e74-461d-be83-9b4cfc8fa97a)

## GitHub Structure

**src/**

api (API layer):
- `authentication`: Contains server logic for handling authentication
    - `auth.py`: contains api guard methods that are used for verifying user tokens
    - `User.py`: contains definition of the `User` object
- `requesthandler`: Contains the api implementation
    - api_logic.py`: Contains functions with the logic thats being executed when the endpoints are called
    - `api_server.py`: Endpoint hosting
    - `buildFireguardApi.py`: Init and builds the API

broker (API layer):
- `publisher.py`: The TTF publisher, publishes TTF to HiveMQ. Runs through the list of cities and publishes their respective TTF at a set time-interval (i.e once a day)
- `runner.py`: Runs the publisher, maintains uptime
- `api_client.py`: Enables communication with the api for the broker 

client (client layer):
- `clientprototype.py`: The webclient prototype, now no longer functional for Get req to the api (Does not have auth), but acts as a subscriber. Displays the subscribed city.

data (data layer):
- `apihandler`: The apihandler and the respective api clients for external api-servies, i.e MET and FROST.
    - `apihandler.py`: common api class for using both MET and FROST APIs
    - `frostClient.py`: api client for using the FROST API
    - `METClient.py`: api client for using the MET API
- `databasehandler`: the databasehandlers for storage and collection of existing data
    - `databaseHandler.py`: contains the abstract class for interfacing with a storage medium. This class is solely used as a interface
    - `mongodb.py`: implementation of the databasehandler interface for storing forecasts and observations on a mongodb server
- `dataextractor`: Component for extracting data from weather servies into correct format.
    - `dataExtractor.py`: implementation of the extractors for getting data out of observations and forecasts returned by MET and FROST
- `datatypes.py`: data transfer objects that are used for returning data through the api, storing data in the database and for computing TTF

helpers (helper methods)
- `annotations.py`: helper annotations for use in the project

service (Service layer):
- `datacollector`: The component responsible for collecting data
    - `dataCollector.py`: implementation of the data collector, utilizes the database handler and api clients for retrieving data
- `TTFmodel`: Model for calculating TTF as provided by the professor
    - `compute.py`: main methods for finding the TTF, based on the temperature, humidity and wind speed
    - `parameters.py`: parameters used by the algorithm for finding TTF
    - `preprocess.py`: methods for preparing the weather data before applying the algorithm
    - `utils.py`: helper methods used by the algorithm
- `frcapi.py`: the applications business logic.

**static**
the static folder contains frontend files for client usage. These files can either be served by running the flask application in src/client or by using the docker compose files. The files are served using the [https://hub.docker.com/r/lipanski/docker-static-website](lipanski/docker-static-website) image

**test**
the test folder contains unittests for the project. The folder structure follows the same pattern as the src folder(to an extent), this helps with locating what tests are associated with a part of the application.


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
add a `.env` file in the root folder of the repository and add the following values, There is an `.env.template` you can copy that contains these env variables.
```cs
FROST_CLIENT_ID            ='your client id'
FROST_CLIENT_SECRET        ='your client secret'
KEYCLOAK_ADMIN             ='admin'
KEYCLOAK_PASSWORD          ='password'
KEYCLOAK_REALM_NAME        = fireguard
MONGO_INITDB_ROOT_USERNAME ='username'
KEYCLOAK_SERVER_URL        = http://localhost:8090
FIREGUARD_API_URL          = http://localhost:8080
MONGO_INITDB_ROOT_PASSWORD ='password'
MONGO_DB_CONNECTION_STRING ='mongodb://username:password@fireguard-database:27017/admin?retryWrites=true&loadBalanced=false&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1'
BROKER_URL                 = 'c406645d204a4c93919e442f4c8bcc09.s1.eu.hivemq.cloud'
BROKER_PORT                = '8883'
PUBLISHER_USERNAME         = 'your hivemq publisher username'
PUBLISHER_PASSWORD         = 'your hivemq publisher password'
CLIENT_ID                  = 'fireguard_client'
USER_ID                    = 'admin'
USER_PASSWORD              = 'password'
```

## 3. Spin up development application
For running the application in development mode, you'll need to include both of the `docker-compose` files in the docker compose call.
`docker-compose.yml` is the main file and spins up everything the application needs to run, while `docker-compose.dev.yml` assigns the src folder as the volume for the broker and api, while also specifying that the application runs in `Development` mode.

```haskell
docker compose -f docker-compose.yml -f docker-compose.development.yml up
```

Local url for the API server
[http://127.0.0.1:8080/](http://127.0.0.1:8080)

Local url for the Authorization server
[http://127.0.0.1:8090](http://127.0.0.1:8090)

Local url for the Frontend
[http://127.0.0.1:3000](http://127.0.0.1:3000)

## Get bearer token for protected endpoints:
for auth token, use postman, web_api.http or shell to make an request against the auth server:

```shell
export token=$(\
curl -X POST http://localhost:8090/realms/fireguard/protocol/openid-connect/token \
-d 'client_id=fireguard_client' \
-d 'username=admin&password=password&grant_type=password'| jq --raw-output '.access_token' \
)
```
This will return an jwt token that can be used for authorizing further requests against the api.

then, use token on one of the protected endpoints (postman or shell):
```shell
curl http://localhost:8080/fire_risk/city/Bergen?ts_from=2024-04-30T21:59:59Z&ts_to=2024-05-09T18:59:59Z -H "Authorization: Bearer "$token
```

# Endpoints
```http
GET cities/{city:string}
```
gets information for the specified city.

Response object
```json
{
    "city": "string", 
    "lat": "string", 
    "lng": "string", 
    "country": "string", 
    "iso2": "string", 
    "admin_name": "string", 
    "capital": "string", 
    "population": "string", 
    "population_proper": "string"
}, 
```

```http
GET cities/{latitude:float}/{longitude:float}
```

Returns the city closest to the provided point

Response object
```json
{
    "city": "string", 
    "lat": "string", 
    "lng": "string", 
    "country": "string", 
    "iso2": "string", 
    "admin_name": "string", 
    "capital": "string", 
    "population": "string", 
    "population_proper": "string"
}, 
```

```http
GET fire_risk/city/{city:string}?ts_from=datetime&ts_to=datetime
```
returns ttf for the specified city and time range.

Response object:
```json
{
  "location": {
    "latitude": "float",
    "longitude": "float"
  },
  "firerisks": [
    {
      "timestamp": "datetime",
      "ttf": "float"
    }
  ]
}
```

```http
GET /fire_risk/{latitude:float}/{longitude:float}?ts_from=datetime&ts_to=datetime
```

Returns ttf for the specified coordinates in the given time range

Response object:
```json
{
  "location": {
    "latitude": "float",
    "longitude": "float"
  },
  "firerisks": [
    {
      "timestamp": "datetime",
      "ttf": "float"
    }
  ]
}
```