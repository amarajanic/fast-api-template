from typing import Any, List
from pydantic import BaseModel

class WeatherDisplay(BaseModel):
    lat: int
    long: int
    timezone: str
    temp_per_hour: Any