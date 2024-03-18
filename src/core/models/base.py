"""
    Инициализация базового класса для последующего наследования от него всех ОРМ-моделей
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
