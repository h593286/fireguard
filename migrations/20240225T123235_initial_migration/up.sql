CREATE TABLE Stations(
    id: INTEGER PRIMARY KEY
    stationId: VARCHAR(20) NOT NULL,
    placement: POINT NOT NULL
);

CREATE TABLE Observations(
    id: INTEGER PRIMARY KEY,
    observedOn: Timestamp NOT NULL,
    stationId: INTEGER FOREIGN KEY REFERENCES Stations(id),
    temperature: Decimal(5,5) NOT NULL,
    relative_humidity: Decimal(5, 5) NOT NULL,
    wind_speed: Decimal(5, 5) NOT NULL,
);

CREATE INDEX Observation_timestamp_station_idx ON Observations(stationId, observedOn);
