from loader import bot
from telebot import types
from telebot.types import Message
from models.user import User
from . import help


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """
    Приветствие пользователя. Выдает пользователю кнопку 'Help' для помощи по командам бота.
    """

    if message.from_user.id not in User.all_users:
        User(message.from_user.id)

    bot.send_message(message.chat.id, 'Добро пожаловать!')
    keyboard = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton('Help', callback_data='help_me')
    keyboard.add(item_1, row_width=1)
    welcome_message = 'Нажми "Help" , чтобы узнать возможности бота.'
    bot.send_message(message.chat.id, text=welcome_message, reply_markup=keyboard)
