import time
from loader import bot
from models.user import User
from utils import api_requests_data


@bot.message_handler(commands=['bestdeal'])
def best_deal(message):
    """
    Сохраняет команду пользователя. Запрашивает город для поиска отелей.
    Перебрасывает в функцию 'get_city_location'
    """

    user = User.get_user(message.from_user.id)
    user.user_command = 'bestdeal'
    now_time = time.strftime('%d.%m.20%y %X', time.gmtime(time.time()))
    user.date_enter_command = now_time
    bot.send_message(message.from_user.id, 'Отправьте боту название города для поиска отелей.')
    bot.register_next_step_handler(message, api_requests_data.get_city_location)
