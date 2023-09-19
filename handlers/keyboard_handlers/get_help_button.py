from config_data.config import DEFAULT_COMMANDS
from loader import bot
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: call.data == 'help_me')
def handler_help_button_clik(call: CallbackQuery):
    """
    При нажатии на кнопку HELP возвращает в чат информацию по командам бота.
    """

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(call.message.chat.id, "\n".join(text))
