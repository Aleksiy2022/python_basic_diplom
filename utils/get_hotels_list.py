from typing import Optional
from telebot import types
import history_data
from content_requests import content_requests
from loader import bot


def get_hotels_list(call, user):
    hotels: Optional[list] = None
    hotels_address: Optional[list] = None
    if user.user_command == 'lowprice':  # Передаем все полученные данные в функцию для получения списка отелей.
        find_data = content_requests.hotels_filter(
            user.city_id,
            user.check_in,
            user.check_out,
            user.hotels_count
        )
        hotels = find_data[0]  # Список отелей.
        hotels_address = content_requests.get_address(find_data[1])  # Cписок адресов отелей.
        # Сохранение информации в БД о команде, даты и времени введения команды, и запрошенных отелях.
        for hotel in hotels:
            history_data.data_recording(
                user.user_id, user.user_command, user.date_enter_command, hotel["name"]
            )
    if user.user_command == 'bestdeal':  # Передаем все полученные данные в функцию для получения списка отелей.
        find_data = content_requests.hotels_filter(
            user.city_id,
            user.check_in,
            user.check_out,
            user.hotels_count,
            user.price_range
        )
        hotels = find_data[0]
        hotels_address = content_requests.get_address(find_data[1])
        # Сохранение информации в БД о команде, даты и времени введения команды, и запрошенных отелях.
        for hotel in hotels:
            history_data.data_recording(
                user.user_id, user.user_command, user.date_enter_command, hotel["name"]
            )
    for i_num, i_hotel in enumerate(hotels):  # Вывод пользователю информации об отеле.
        if user.get_photo:  # Вывод пользователю фотографий по отелю.
            photos: list[str] = content_requests.get_hotel_photo(i_hotel['id'])  # Список ссылок на фотографии.
            media = []
            for number, i_photos in enumerate(photos):
                if number == 4:
                    media.append(types.InputMediaPhoto(
                        i_photos,
                        caption=
                        f'Отель: {i_hotel["name"]}.\n'
                        f'Адрес отеля: {hotels_address[i_num]}.\n'
                        f'Расстояние до центра в км: ' +
                        f'{i_hotel["destinationInfo"]["distanceFromDestination"]["value"]}\n'
                        f'Цена за указанный период: ' +
                        f'{i_hotel["price"]["displayMessages"][1]["lineItems"][0]["value"].replace("total", "$")}.\n'
                        f'Ссылка на сайт отеля: https://www.hotels.com/h{i_hotel["id"]}.Hotel-Information)'))
                else:
                    media.append(types.InputMediaPhoto(i_photos))
            bot.send_media_group(call.message.chat.id, media)
        elif not user.get_photo:
            bot.send_message(
                call.message.chat.id,
                f'Отель: {i_hotel["name"]}.\n'
                f'Адрес отеля: {hotels_address[i_num]}.\n'
                f'Расстояние до центра в км: ' +
                f'{i_hotel["destinationInfo"]["distanceFromDestination"]["value"]}\n'
                f'Цена за указанный период: ' +
                f'{i_hotel["price"]["displayMessages"][1]["lineItems"][0]["value"].replace("total", "$")}.\n'
                f'Ссылка на сайт отеля: https://www.hotels.com/h{i_hotel["id"]}.Hotel-Information)'
            )
