import json
import requests


def hotels_filter(region_id: str, first_day: str, last_day: str, count_hotels: int, price_range: list) -> list:
    """
    Отправляет запрос с указанными параметрами к API для получения списка отелей.
    :param region_id: ID города
    :param first_day: день заезда в отель
    :param last_day: день выезда из отеля
    :param count_hotels: количество отелей для показа пользователю
    :param price_range: диапазон цен
    :return: возвращает список из списка отелей и списка id отелей
    """
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

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
        "sort": "DISTANCE",
        "filters": {
            "max": price_range[1],
            "min": price_range[0]

        }
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "1b236d6a0fmsha230fb245ece2fbp12459fjsnd513e7eba581",
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
    :param propertyid_list: списjr id отелей
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
            "X-RapidAPI-Key": "1b236d6a0fmsha230fb245ece2fbp12459fjsnd513e7eba581",
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        result = json.loads(response.text)
        hotel_address = result['data']['propertyInfo']['summary']['location']['address']['addressLine']
        property_addresses.append(hotel_address)

    return property_addresses
