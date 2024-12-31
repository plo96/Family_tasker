"""
    Инициализация базового класса для последующего наследования от него всех ОРМ-моделей.
"""

from uuid import UUID

from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped
from sqlalchemy import Uuid

from src.core.models.default_values import get_uuid


class BaseModel(DeclarativeBase):
    """Базовый класс для всех ОРМ-моделей."""

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=get_uuid,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
