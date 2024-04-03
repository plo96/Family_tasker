"""
    Инициализация базового класса для последующего наследования от него всех ОРМ-моделей
"""
from datetime import datetime, UTC
from uuid import uuid4, UUID

from sqlalchemy.orm import DeclarativeBase, declared_attr


def get_current_time() -> datetime:
	return datetime.now(UTC)


def get_uuid() -> UUID:
	return uuid4()


class Base(DeclarativeBase):
	"""Базовый класс для всех ОРМ-моделей для аккумуляции metadata"""
	__abstract__ = True
	
	@declared_attr.directive
	def __tablename__(cls) -> str:
		return f'{cls.__name__.lower()}s'
