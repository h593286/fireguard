from pydantic import BaseModel
import datetime

class Location(BaseModel):

    latitude: float
    longitude: float
class WeatherDataPoint(BaseModel):

    temperature: float
    humidity: float
    wind_speed: float
    timestamp: datetime.datetime

    def __str__(self):

        format_str = f'WeatherData[{self.timestamp}] {self.temperature, self.humidity, self.wind_speed}]'

        return format_str


class Observations(BaseModel):

    source: str
    location: Location
    data: list[WeatherDataPoint]

    def __str__(self):
        format_str = f'Observations [Source: {self.source} @ Location: {self.location}]\n'

        # Join all data points using '\n' as a separator
        data_strings = '\n'.join(map(str, self.data))

        return format_str + data_strings + '\n'


class Forecast(BaseModel):

    location: Location
    data: list[WeatherDataPoint]

    def __str__(self):
        format_str = f'Forecast @ Location: {self.location}\n'

        # Join all data points using '\n' as a separator
        data_strings = '\n'.join(map(str, self.data))

        return format_str + data_strings + '\n'

class WeatherData(BaseModel):

    created: datetime.datetime

    observations: Observations
    forecast: Forecast

    def to_json(self):
        return self.model_dump_json()