from loader import bot
from telebot.types import CallbackQuery
from utils.get_hotels_list import get_hotels_list
from models.user import User


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def handler_photo_button_clik(call: CallbackQuery):
    """
    Изменяет параметр "get_photo" в модели User на True. Перенаправляет в функцию получения списка отелей.
    """

    user = User.get_user(call.message.chat.id)
    user.get_photo = True
    get_hotels_list(call=call, user=user)


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def handler_photo_button_clik(call: CallbackQuery):
    """
    Оставляет параметр "get_photo" в модели User в статусе False. Перенаправляет в функцию получения списка отелей.
    """

    user = User.get_user(call.message.chat.id)
    get_hotels_list(call=call, user=user)
