from typing import Dict, Any, Optional, List


class User:
    """
    Класс Пользователь.
    Pars: user_id: int - уникальный идентификатор пользователя Telegram.
    Attrs:  all_users: Dict[int: Any]: - словарь хранящий пользователей.
            self.city: : Optional[str] - город, запрашиваемый пользователем.
            self.city_id: Optional[bool | str] - код ID города.
            self.hotels_count: Optional[bool | int] - количество отелей, запрашиваемое пользователем.
            self.user_command: Optional[str] - команда, введеная пользователем.
            self.check_in: Optional[bool | List[str, str, str]] - дата въезда в отель.
            self.check_out: Optional[bool | List[str, str, str]] - дата выезда из отеля.
            self.price_range: Optional[bool | List[int, int]] - диапозон цен на указанный пользователем период
            self.get_photo: bool - флаг получения фото. True - получаем фото, False - не получаем.
            self.date_enter_command: Optional[str] - сохраняет время отправки команды пользователем
    """

    all_users: Dict[int, Any] = dict()

    def __init__(self, user_id: int) -> None:
        self.user_id: int = user_id
        self.city: Optional[str] = None
        self.city_id: Optional[bool | str] = None
        self.hotels_count: Optional[bool | int] = None
        self.user_command: Optional[str] = None
        self.check_in: Optional[bool | List[str, str, str]] = None
        self.check_out: Optional[bool | List[str, str, str]] = None
        self.get_photo: bool = False
        self.price_range: Optional[bool | List[int, int]] = None
        self.date_enter_command: Optional[str] = None
        User.add_user(user_id, self)

    @staticmethod
    def get_user(user_id: int) -> Any:
        """
        :param user_id: уникальный идентификатор пользователя Telegram.
        :return: Объект пользователь
        Метод возвращает объект (пользователь).
        Если в словаре нет значения (объект пользователь) по заданному user_id,
        то возвращается новый объект (пользователь).
        """

        if User.all_users.get(user_id) is None:
            new_user = User(user_id)
            return new_user
        return User.all_users.get(user_id)

    @classmethod
    def add_user(cls, user_id: int, user: object) -> None:
        """
        Метод добавляет в словарь нового пользователя.
        :param user_id: уникальный идентификатор пользователя Telegram.
        :param user: объект пользователь
        """

        cls.all_users[user_id] = user

    @staticmethod
    def del_user(user_id: int) -> None:
        """
        :param user_id: уникальный идентификатор пользователя Telegram.
        Метод удаляет user_id из словаря, если нет закрепленного объекта за ним.
        """

        if User.all_users.get(user_id) is not None:
            del User.all_users[user_id]
