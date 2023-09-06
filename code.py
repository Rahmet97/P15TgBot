import os
import requests

from dotenv import load_dotenv

load_dotenv()


def get_temperature(city):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    appid = os.getenv('APIKEY')
    response = requests.get(url, params={
        'q': city,
        'units': 'metric',
        'appid': appid
    })
    return response.json()
