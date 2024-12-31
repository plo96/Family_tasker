"""
   Кастомные исключения для данного приложения;
   Декоратор для обработки исключений в эндпоинтах.
"""

from functools import wraps

from fastapi import HTTPException, status


def endpoint_exceptions_processing(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ObjectNotFoundError as _ex:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{_ex.object_type} with this {_ex.parameter} is not found in database.",
            )
        except PasswordIsNotCorrect:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST_NOT_FOUND,
                detail="Uncorrected password.",
            )
        except (UserNotExistError, UserNotAllowedError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST_NOT_FOUND,
                detail="Uncorrected user name.",
            )
        except Exception as _ex:
            print(_ex)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unknown internal server error.",
            ) from _ex

    return wrapper


class CustomException(Exception):
    pass


class CustomHTTPException(HTTPException):
    pass


class ObjectNotFoundError(CustomException):
    """Не удалось найти объект с указанными параметрами в базе."""

    def __init__(self, object_type: str = None, parameter: str = None):
        self.object_type = object_type
        self.parameter = parameter


class PasswordIsNotCorrect(CustomException):
    """Пароль пользователя не совпадает с данными в базе."""

    pass


class UserNotExistError(CustomException):
    """Данный пользователь не существует."""

    pass


class UserNotAllowedError(CustomException):
    """Данный пользователь удалён."""

    pass


class AccessPermissionError(CustomHTTPException):
    """У текущего пользователя недостаточно прав для доступа."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Insufficient permissions.",
        )


class TokenError(CustomHTTPException):
    """Токен невозможно декодировать."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )
