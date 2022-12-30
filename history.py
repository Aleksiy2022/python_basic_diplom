import sqlite3 as sq


def data_recording(user_id: int, command: str, date: str, name_hotel: str) -> None:
    """
    Функция сохраняет в базу данных информацию по переданным параметрам.
    :param user_id: int - уникальный идентификатор пользователя Telegram;
    :param command: str - команда, введеная пользователем;
    :param date: str - дата , когда пользователь отправил боту команду;
    :param name_hotel: str - наименование отеля;
    :return: None.
    """
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        cur.execute(
            f'INSERT INTO users (user_id, user_command, date_enter_command, hotel)'
            f'VALUES ("{user_id}", "{command}", "{date}", "{name_hotel}")'
        )


def print_history(user_id: int) -> list:
    """
    :param user_id: int - уникальный идентификатор пользователя Telegram;
    :return: Список кортежей с информацией из БД.
    """
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        history = cur.execute(
            f'SELECT user_command, date_enter_command, hotel FROM users WHERE user_id == "{user_id}"'
        )

        return history.fetchall()
