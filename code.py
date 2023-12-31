import os
import requests

from dotenv import load_dotenv

load_dotenv()


def get_temperature(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    appid = os.getenv('APIKEY')
    response = requests.get(url, params={
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'appid': appid
    })
    return response.json()


def get_address_using_location(lat, lon):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "c17d02e5-a388-44b5-bc78-b3415fda0509",
        "geocode": f"{lon},{lat}",
        "lang": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data_p = response.json()
    city = data_p['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']['formatted']
    return city
