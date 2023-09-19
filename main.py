from loader import bot
from utils.set_bot_commands import set_default_commands
from handlers.command_hendlers import help, start, lowprice, bestdeal, history
from handlers.keyboard_handlers import get_help_button, get_photo_button


if __name__ == "__main__":
    set_default_commands(bot)
    bot.infinity_polling()
