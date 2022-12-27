import telebot
from telebot import types
import low_price
import best_deal
import content_request
from check_data import is_date_valid, check_count_hotels, check_price_range
from typing import Any, Dict, Optional, List


TOKEN = '5933669640:AAH3fo7iaDZSvdlwA8ydagX0_HefIrEZBmE'  # name_bot: my_project_hotelsbot
bot = telebot.TeleBot('5933669640:AAH3fo7iaDZSvdlwA8ydagX0_HefIrEZBmE')


class User:
    """
    Класс Пользователь.
        Pars: user_id - уникальный идентификатор пользователя Telegram.
        Attrs:  all_users: Dict[int: Any]: - словарь хранящий пользователей.
                self.city: : Optional[str] - город, запрашиваемый пользователем.
                self.city_id: Optional[bool | str] - код ID города.
                self.hotels_count: Optional[bool | int] - количество отелей, запрашиваемое пользователем.
                self.user_command: Optional[str] - команда, введеная пользователем.
                self.check_in: Optional[bool | List[str, str, str]] - дата въезда в отель.
                self.check_out: Optional[bool | List[str, str, str]] - дата выезда из отеля.
                self.price_range: Optional[bool | List[int, int]] - диапозон цен на указанный пользователем период
                self.get_photo (bool) - флаг получения фото. True - получаем фото, False - не получаем.
    """
    all_users: Dict[int, Any] = dict()

    def __init__(self, user_id: int) -> None:
        self.city: Optional[str] = None
        self.city_id: Optional[bool | str] = None
        self.hotels_count: Optional[bool | int] = None
        self.user_command: Optional[str] = None
        self.check_in: Optional[bool | List[str, str, str]] = None
        self.check_out: Optional[bool | List[str, str, str]] = None
        self.get_photo: bool = False
        # self.blook_chose_date = False
        # self.need_to_get_ranges_flag = False
        self.price_range: Optional[bool | List[int, int]] = None

        User.add_user(user_id, self)

    @staticmethod
    def get_user(user_id: int) -> Any:
        """
        :param user_id: уникальный идентификатор пользователя Telegram.
        :return: Объект пользователь
        Метод возвращает объект (пользователь).
        Если в словаре нет значения (объект пользователь) по заданному user_id,
        то возвращается новый объект (пользователь).
        """

        if User.all_users.get(user_id) is None:
            new_user = User(user_id)
            return new_user
        return User.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id: int, user: Optional[Any]) -> None:
        """
        :param user_id: уникальный идентификатор пользователя Telegram.
        :param user: объект пользователь

        Метод добавляет в словарь нового пользователя.
        """
        cls.all_users[user_id] = user

    @staticmethod
    def del_user(user_id: int) -> None:
        """
        :param user_id: уникальный идентификатор пользователя Telegram.
        Метод удаляет user_id из словаря, если нет закрепленного объекта за ним.
        """
        if User.all_users.get(user_id) is not None:
            del User.all_users[user_id]


@bot.message_handler(commands=['start'])
def welcome(message: Any) -> None:
    """
    Функция приветствия пользователя.
    Приветствует. Выдает пользователю кнопку 'Help' для помощи по командам бота.
    """
    if message.from_user.id not in User.all_users:
        User(message.from_user.id)
    bot.send_message(message.chat.id, 'Добро пожаловать!')
    keyboard = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton('Help', callback_data='help_me')
    keyboard.add(item_1, row_width=1)
    welcome_message = 'Нажми "Help" , чтобы узнать возможности бота.'
    bot.send_message(message.chat.id, text=welcome_message, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_text(message: Any) -> None:
    """
    Функция отправляет в чат ответ на команду '/help'
    """

    bot.send_message(message.chat.id,
                     '/lowprice - Узнать топ самых дешёвых отелей в городе.')
    bot.send_message(message.chat.id,
                     '/bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра.')
    bot.send_message(message.chat.id,
                     '/history - Узнать историю поиска отелей.')
    bot.send_message(message.chat.id,
                     '/help - помощь по командам бота.')


@bot.callback_query_handler(func=lambda call: True)
def catches_answer(call: Any) -> None:
    """
    Обрабатывает обратные запросы пользователя, которые получается как ответ на вопросы с клавиатуры.
    """
    user = User.get_user(call.message.chat.id)  # Получение оъекта - пользователь.
    if call.data == 'help_me':  # Выводт текста помощи при нажатии на кнопку 'Help'.
        bot.send_message(call.message.chat.id,
                         '/lowprice - Узнать топ самых дешёвых отелей в городе.')
        bot.send_message(call.message.chat.id,
                         '/bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра.')
        bot.send_message(call.message.chat.id,
                         '/history - Узнать историю поиска отелей.')
        bot.send_message(call.message.chat.id,
                         '/help - помощь по командам бота.')
    # Изменяет значение в объекте 'user' аттрибута 'user.get_photo'.
    if call.data == 'yes':
        user.get_photo = True
        call.data = 'no'
    # Если команда от пользователя '/lowprice' выводит список отелей по заданным данным от дешевого к дорогому.
    if call.data == 'no':
        hotels: Optional[list] = None
        hotels_address: Optional[list] = None
        if user.user_command == 'lowprice':  # Передаем все полученные данные в функцию для получения списка отелей.
            find_data = low_price.hotels_filter(
                user.city_id,
                user.check_in,
                user.check_out,
                user.hotels_count
            )
            hotels = find_data[0]  # Список отелей.
            hotels_address = low_price.get_address(find_data[1])  # Cписок адресов отелей.
        if user.user_command == 'bestdeal':  # Передаем все полученные данные в функцию для получения списка отелей.
            find_data = best_deal.hotels_filter(
                user.city_id,
                user.check_in,
                user.check_out,
                user.hotels_count,
                user.price_range
            )
            hotels = find_data[0]
            hotels_address = best_deal.get_address(find_data[1])
        for i_num, i_hotel in enumerate(hotels):  # Вывод пользователю информации об отеле.
            bot.send_message(call.message.chat.id, f'********************************************')
            bot.send_message(call.message.chat.id, f'Отель: {i_hotel["name"]}.')
            bot.send_message(call.message.chat.id, f'Адрес отеля: {hotels_address[i_num]}.')
            bot.send_message(call.message.chat.id,
                             f'Расстояние до центра в км: '
                             f'{i_hotel["destinationInfo"]["distanceFromDestination"]["value"]}.')
            bot.send_message(call.message.chat.id,
                             f'Цена за указанный период: '
                             f'{i_hotel["price"]["displayMessages"][1]["lineItems"][0]["value"].replace("total", "$")}.')
            bot.send_message(call.message.chat.id,
                             f'Ссылка на сайт отеля: https://www.hotels.com/h{i_hotel["id"]}.Hotel-Information)')
            if user.get_photo:  # Вывод пользователю фотографий по отелю.
                photos: List[str] = content_request.get_hotel_photo(i_hotel['id'])  # Список ссылок на фотографии.
                for i_photo in photos:
                    bot.send_photo(call.message.chat.id, i_photo)


@bot.message_handler(commands=['lowprice'])
def lowprice(message: Any) -> None:
    """
    Сохраняет команду пользователя. Запрашивает город для поиска отелей.
    Перебрасывает в функцию 'get_city_location'
    """
    user = User.get_user(message.from_user.id)  # получение оъекта - пользователь
    user.user_command = 'lowprice'
    bot.send_message(message.from_user.id, 'Отправьте боту название города для поиска отелей.')
    bot.register_next_step_handler(message, get_city_location)


@bot.message_handler(commands=['bestdeal'])
def bestdeal(message):
    """
    Сохраняет команду пользователя. Запрашивает город для поиска отелей.
    Перебрасывает в функцию 'get_city_location'
    """
    user = User.get_user(message.from_user.id)  # получение оъекта - пользователь
    user.user_command = 'bestdeal'
    bot.send_message(message.from_user.id, 'Отправьте боту название города для поиска отелей.')
    bot.register_next_step_handler(message, get_city_location)

# @bot.message_handler(commands=['history'])
# def history(message):
#     pass


def get_city_location(message: Any) -> None:
    """
     По заданному городу использует строковый метод 'capitalize'.
     Проверяет существует ли ID города. Сохраняет город в объект 'user' в аттрибут 'self.city',
     cохраняет ID города в аттр 'self.city_id'.
     Если существует ID города, запрашивает дату въезда.
     Нет - выводит сообщение об ошибке, запрашивает повторно название города
     и возвращает в начало функции до корректного введения города.
    """
    user = User.get_user(message.from_user.id)  # Получение оъекта - пользователь.
    user.city = message.text.capitalize()
    user.city_id = content_request.find_location(user.city)
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
    user = User.get_user(message.from_user.id)  # Получение оъекта - пользователь.
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
    user = User.get_user(message.from_user.id)  # Получение оъекта - пользователь.
    user.check_out = is_date_valid(message.text)
    if user.check_out:
        if user.user_command == 'lowprice':
            bot.send_message(message.chat.id, 'Какое количество отелей показать? (не более 25)')
            bot.register_next_step_handler(message, get_count_hotels)
        if user.user_command == 'bestdeal':
            bot.send_message(message.chat.id,
                             'Введите диапозон цен за ночь в отеле, в формате: 10$-50$.')
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
    user = User.get_user(message.from_user.id)  # Получение оъекта - пользователь.
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
    user = User.get_user(message.from_user.id)  # Получение оъекта - пользователь.
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


bot.polling(interval=0)
