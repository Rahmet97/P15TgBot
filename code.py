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


def get_address_using_location(lat, lon):
    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "f3d55107-23fa-41bf-88c4-51b44aaf6781",
        "geocode": f"{lon},{lat}",
        "lang": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data_p = response.json()
    city = data_p['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']['formatted']
    return city
