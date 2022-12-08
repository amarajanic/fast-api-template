import requests
import json


async def fetch_weather(lat:float, long:float):
    latitude = str(lat)
    longitude = str(long)
    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m')
    data = json.loads(response.text)
    return data
    
