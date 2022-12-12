import telebot
from typing import Any
from telebot import types

TOKEN = '5933669640:AAH3fo7iaDZSvdlwA8ydagX0_HefIrEZBmE'  # name_bot: my_project_hotelsbot

bot = telebot.TeleBot('5933669640:AAH3fo7iaDZSvdlwA8ydagX0_HefIrEZBmE')


@bot.message_handler(content_types=['text'])
def welcome(message: Any):
    """Приветствует пользователя."""
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Добро пожаловать! Я помогу сделать лучший выбор среди всех отелей Мира!')
        buttons(message)
    else:
        bot.send_message(message.chat.id, 'Добро пожаловать! Я помогу сделать лучший выбор среди всех отелей Мира!')
        buttons(message)


@bot.message_handler(commands=['help', 'start'])
def buttons(message:Any):
    """Выводит клавиатуру с кнопками 'Помощь' и 'Старт'"""

    keyboard = types.InlineKeyboardMarkup()
    item_1 = types.InlineKeyboardButton('Помощь', callback_data='help')
    item_2 = types.InlineKeyboardButton('Старт', callback_data='start')
    keyboard.add(item_1, item_2, row_width=3)
    welcome_message = 'Тебе нужна помощь, или хочешь сразу преступить к поиску?'
    bot.send_message(message.chat.id, text=welcome_message, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def send_welcome(call):
    """Обрабатывает обратный запрос при нажатии кнопок на клавиатуре"""

    if call.data == 'help':
        bot.send_message(call.message.chat.id, 'Тут скоро будет помощь по командам бота')
    elif call.data == 'start':
        bot.send_message(call.message.chat.id, 'Тут скоро появятся команды')


bot.polling(interval=0)
