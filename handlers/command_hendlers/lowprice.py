import time

from loader import bot
from models.user import User
from telebot.types import Message
from utils.api_requests_data import get_city_location


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message) -> None:
    """
    Сохраняет команду пользователя. Запрашивает город для поиска отелей.
    Перебрасывает в функцию 'get_city_location'
    """

    user = User.get_user(message.from_user.id)  # получение оъекта - пользователь
    user.user_command = 'lowprice'
    now_time = time.strftime('%d.%m.20%y %X', time.gmtime(time.time()))  # Получение текущей даты и времени
    user.date_enter_command = now_time  # cохраняем время ввода команды
    bot.send_message(message.from_user.id, 'Отправьте боту название города для поиска отелей.')
    bot.register_next_step_handler(message, get_city_location)
