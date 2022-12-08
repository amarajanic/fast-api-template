from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from weather.fetch import fetch_weather
from weather.schemas import WeatherDisplay



async def get_weather(lat:float, long:float):
    response = await fetch_weather(lat, long)

    time = response["hourly"]["time"]
    temp = response["hourly"]["temperature_2m"]

    time_and_temp = {}

    for index, ti in enumerate(time):
            time_and_temp[ti] = temp[index]
            if index == 24:
                break

    data = WeatherDisplay(
        lat= response["latitude"],
        long=response["longitude"],
        timezone= response["timezone"],
        temp_per_hour= time_and_temp
    )
    return data

