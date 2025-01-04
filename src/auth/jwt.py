import logging
from datetime import datetime, timezone
import jwt

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.project import settings

logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def create_jwt_token(data_dict: dict) -> str:
    """
    Создание jwt-токена по входному словарю.
    :param data_dict: Параметры для шифрования.
    :return: JWT-токен в виде строки.
    """
    expiration = datetime.now(tz=timezone.utc).timestamp() + settings.EXPIRATION_TIME
    data_dict.update({"exp": expiration})
    token = jwt.encode(data_dict, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def verify_jwt_token(token: str) -> dict | None:
    """
    Декодирование токена.
    :param token: JWT-токен в виде строки.
    :return: Словарь с декодированными данными.
                     jwt.PyJWTError в случае ошибки валидации токена.
    """
    try:
        decoded_data = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_data
    except jwt.PyJWTError:
        return None
