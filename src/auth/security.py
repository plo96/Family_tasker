from datetime import datetime, timezone
import jwt

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.project import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRATION_TIME = settings.EXPIRATION_TIME


def create_jwt_token(user_data: dict) -> str:
	"""
	Создание jwt-токена по входному словарю.
	:param user_data: Параметры пользователя для шифрования.
	:return: JWT-токен в виде строки.
	"""
	expiration = datetime.now(tz=timezone.utc).timestamp() + EXPIRATION_TIME
	user_data.update({"exp": expiration})
	token = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
	return token


def verify_jwt_token(token: str) -> dict | None:
	"""
	Декодирование токена.
	:param token: JWT-токен в виде строки.
	:return: Словарь с декодированными данными.
			 jwt.PyJWTError в случае ошибки валидации токена.
	"""
	try:
		decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		return decoded_data
	except jwt.PyJWTError:
		return None
