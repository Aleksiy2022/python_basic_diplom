import json
import requests


def hotels_filter(region_id: str, first_day: str, last_day: str, count_hotels: int) -> list:
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
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {}
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


def get_address(propertyid_list):
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
