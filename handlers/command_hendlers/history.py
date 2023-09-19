import history_data
from loader import bot
from models.user import User


@bot.message_handler(commands=['history'])
def user_history(message):
    """
    Возвращает в чат с пользователем список последних найденных отелей в количестве не более 10 штук.
    """

    user = User.get_user(message.from_user.id)
    notes = history_data.print_history(user.user_id)

    for i_note in notes:
        bot.send_message(
            message.from_user.id,
            f'Дата {i_note[1]}\n'
            f'Отправили команду /{i_note[0]}\n'
            f'Дата поиска отеля: {user.date_enter_command}\n'
            f'Отель {i_note[2]}'
        )
