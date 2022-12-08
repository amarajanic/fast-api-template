from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from weather.schemas import WeatherDisplay
from weather.services import get_weather


router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("", response_model=WeatherDisplay)
async def get_current_weather(lat:float, long:float):
    response = await get_weather(lat, long)
    return response
