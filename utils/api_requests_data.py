from typing import Any
from telebot import types
from content_requests import content_requests
from loader import bot
from models.user import User
from utils.user_input_validator import is_date_valid, check_price_range, check_count_hotels


def get_city_location(message: Any) -> None:
    """
    Проверяет существует ли ID города. Сохраняет город в объект 'user' в аттрибут 'self.city',
    cохраняет ID города в аттр 'self.city_id'.
    Если существует ID города, запрашивает дату въезда.
    Если нет - выводит сообщение об ошибке, запрашивает повторно название города
    и возвращает в начало функции до корректного введения города.
    """

    user = User.get_user(message.from_user.id)
    user.city = message.text
    user.city_id = content_requests.find_location(user.city)
    user.get_photo = False

    if user.city_id:
        bot.send_message(message.chat.id, 'Напишите дату заезда в формате: дд.мм.гггг')
        bot.register_next_step_handler(message, get_check_in)
    elif not user.city_id:
        bot.send_message(message.chat.id, 'Указанный Вами город не найден.')
        bot.send_message(message.chat.id, 'Попробуйте еще раз.')
        bot.register_next_step_handler(message, get_city_location)


def get_check_in(message: Any) -> None:
    """
    Проверяет корректность полученной от пользователя даты въезда в отель.
    Если корректный формат, сохраняет дату в аттр 'self.check_in', запрашивает дату выезда
    и перекидывает в функцию 'get_check_out'. Если не корректный формат даты , выводит сообщение об ошибке,
    возвращает в начало функции.
    """

    user = User.get_user(message.from_user.id)
    user.check_in = is_date_valid(message.text)

    if user.check_in:
        bot.send_message(message.chat.id, 'Напишите дату выезда в формате: дд.мм.гггг')
        bot.register_next_step_handler(message, get_check_out)
    elif not user.check_in:
        bot.send_message(message.chat.id, 'Указан некорректный формат даты.')
        bot.send_message(message.chat.id, 'Попробуйте еще раз. Пример: 23.05.2023 (дд.мм.гггг)')
        bot.register_next_step_handler(message, get_check_in)


def get_check_out(message: Any) -> None:
    """
    Проверяет корректность ввода даты выезда из отеля. Если корректный формат, сохраняет даты в аттр 'self.check_out',
    в зависимости от введенной команды продолжает исполнение программы в функцию 'get_count_hotels' или
    'get_price_range'. Если не корректный формат даты , выводит сообщение об ошибке,
    возвращает в начало функции.
    """

    user = User.get_user(message.from_user.id)
    user.check_out = is_date_valid(message.text)
    if user.check_out:
        if user.user_command == 'lowprice':
            bot.send_message(message.chat.id, 'Какое количество отелей показать? (не более 25)')
            bot.register_next_step_handler(message, get_count_hotels)
        if user.user_command == 'bestdeal':
            bot.send_message(message.chat.id,
                             'Введите диапозон цен (в долларах) за ночь в отеле, в формате: 10-50.')
            bot.register_next_step_handler(message, get_price_range)

    elif not user.check_out:
        bot.send_message(message.chat.id, 'Указан некорректный формат даты.')
        bot.send_message(message.chat.id, 'Попробуйте еще раз. Пример: 23.05.2023 (дд.мм.гггг)')
        bot.register_next_step_handler(message, get_check_out)


def get_price_range(message: Any) -> None:
    """
    Проверяет корректность ввода диапозона цен. Если корректный формат, сохраняет диапозон цен в аттр 'self.price_range'
    и переводит выполнение программы в функцию 'get_distance_range'. Если не корректный формат диапозона цен ,
    выводит сообщение об ошибке, возвращает в начало функции.
    """

    user = User.get_user(message.from_user.id)
    user.price_range = check_price_range(message.text)

    if user.price_range:
        bot.send_message(message.chat.id, 'Какое количество отелей показать? (не более 25)')
        bot.register_next_step_handler(message, get_count_hotels)
    if not user.price_range:
        bot.send_message(message.chat.id, 'Введен не корректный диапозон цен')
        bot.send_message(message.chat.id, 'Попробуйте еще раз. Пример: 10$-50$')
        bot.register_next_step_handler(message, get_price_range)


def get_count_hotels(message: Any) -> None:
    """
    Проверяет корректность ввода количества отелей. Если формат верный, выводит пользователю вопрос о получении
    фотографий отеля с кнопка 'Да' и 'Нет'. Если формат количества отелей не верный, выводит сообщение об ошибке
    и возвращает в начало функции.
    """

    user = User.get_user(message.from_user.id)
    user.hotels_count = check_count_hotels(message.text)

    if user.hotels_count:
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
        button_2 = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(button_1, button_2, row_width=2)
        bot.send_message(message.chat.id, 'Показать фотографии отеля?', reply_markup=keyboard)
    elif not user.hotels_count:
        bot.send_message(message.chat.id, 'Количество отелей не указано в нужном диапозоне.')
        bot.send_message(message.chat.id, 'Попробуйте еще раз: напишите цифру от 1 до 25.')
        bot.register_next_step_handler(message, get_count_hotels)
