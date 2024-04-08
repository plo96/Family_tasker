"""
   Кастомные exceptions для данного приложения
"""


class ObjectNotFoundError(Exception):
    """Не удалось найти объект с указанными параметрами в базе"""
    ...

class PasswordIsNotCorrect(Exception):
    """Пароль пользователя не совпадает с данными в базе"""
    ...
