import requests
import json


async def fetch_blogs():
    response = requests.get(f'https://api.publicapis.org/entries')
    data = json.loads(response.text)
    return data
    
