import json
import requests
from typing import Optional, Any


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
            "X-RapidAPI-Key": "1b236d6a0fmsha230fb245ece2fbp12459fjsnd513e7eba581",
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
    photos = []
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": str(hotel_id)
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "1b236d6a0fmsha230fb245ece2fbp12459fjsnd513e7eba581",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    result = json.loads(response.text)
    for i_photo in range(5):
        photo = result['data']['propertyInfo']['propertyGallery']['images'][i_photo]['image']['url']
        photos.append(photo)

    return photos

