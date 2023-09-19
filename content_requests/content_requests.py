import json
import requests
from typing import Optional, Any
import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")


def find_location(my_city: str) -> Optional[Any]:
    """
    :param my_city: str - город, указанный пользователем
    :return: Если gaia_id указанного города не найден возвращает 'None'.
             Если найден возвращает gaia_id (str) - id указанного города.
    """

    gaia_id = ''

    try:
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": my_city, "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_data = json.loads(response.text)

        if len(json_data['sr']) == 0:
            raise TypeError

        for i_element in json_data['sr']:
            if i_element['type'] == 'CITY':
                if i_element['regionNames']['lastSearchName'] == my_city:
                    gaia_id = i_element.get('gaiaId')

        return gaia_id
    except (TypeError, ValueError):
        return None


def get_hotel_photo(hotel_id: str) -> list:
    """
    :param hotel_id: (str) - код отеля;
    :return: Возвращает список url для получения фотографий с сайта.
    """

    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": str(hotel_id)
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    result = json.loads(response.text)
    photos = []

    for i_photo in range(5):
        photo = result['data']['propertyInfo']['propertyGallery']['images'][i_photo]['image']['url']
        photos.append(photo)

    return photos

def hotels_filter(region_id: str, first_day: str, last_day: str, count_hotels: int, price_range: list=None) -> list:

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    filters = {}

    if price_range:
        filters = {
            "max": price_range[1],
            "min": price_range[0]
        }

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": region_id},
        "checkInDate": {
            "day": int(first_day[0]),
            "month": int(first_day[1]),
            "year": int(first_day[2])
        },
        "checkOutDate": {
            "day": int(last_day[0]),
            "month": int(last_day[1]),
            "year": int(last_day[2])
        },
        "rooms": [
            {
                "adults": 1
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": count_hotels,
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": filters
    }

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    result = json.loads(response.text)
    hotels = result['data']['propertySearch']['properties']
    propertyid_list = [i_hotel['id'] for i_hotel in hotels]

    return [hotels, propertyid_list]


def get_address(propertyid_list: list) -> list:
    """
    Отправляет запрос к API для получения списка адресов отелей.
    :param propertyid_list: список id отелей
    :return: возвращает список адресов Отелей
    """

    property_addresses = []

    for i_id in propertyid_list:
        url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "propertyId": str(i_id)
        }

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        result = json.loads(response.text)
        hotel_address = result['data']['propertyInfo']['summary']['location']['address']['addressLine']
        property_addresses.append(hotel_address)

    return property_addresses

