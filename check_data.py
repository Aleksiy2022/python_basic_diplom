from typing import Optional, List


def is_date_valid(date_str: str) -> Optional[bool | list]:
    """
    Проверяет формат даты въезда в отель или выезда из отеля введеной пользователем.
    :param date_str: дата въезда или выезда, которые вводит пользователь.
    :return: Возвращает логический тип данных (False) или список строковых значений даты [день, месяц, год]
    """
    try:
        day, month, year = map(int, date_str.split('.'))
        if month in (4, 6, 9, 11):
            last_day = 30
        elif month == 2 and not year % 4 == 0 or \
                month == 2 and year % 4 == 0 and year % 100 == 0 and not year % 400 == 0:
            last_day = 28
        elif month == 2 and year % 400 == 0 or month == 2 and year % 4 == 0:
            last_day = 29
        else:
            last_day = 31
    except ValueError:
        return False
    if 0 < day <= last_day and 1 <= month <= 12 and 0 < year <= 9999:
        return date_str.split('.')


def check_count_hotels(number: str) -> Optional[bool | int]:
    """
    Проверяет формат введенного количества отелей пользователем.
    :param number: количество отелей для вывода пользователю
    :return: Возвращает логический тип данных (False) или количество отелей для вывода пользователю.
    """
    try:
        if int(number) in [i_num for i_num in range(1, 26)]:
            return int(number)
        else:
            return False
    except ValueError:
        return False


def check_price_range(price_range: str) -> Optional[bool | List[int | int]]:
    """
    Проверяет формат введенного пользователем диапозона цен.
    :param price_range: str
    :return: Возвращает булевый тип данных (False) или диапозон в виде списка [int, int]
    """
    try:
        if int(price_range):
            raise TypeError
        price_range = list(map(int, price_range.replace('$', '').split('-')))
        return price_range
    except (ValueError, TypeError):
        return False
