"""
    Модель представления сущности пользователя в БД.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from .base_model import BaseModel
from .default_values import get_current_time


class Roles(Enum):
    """Список возможных ролей пользователей."""

    admin = "admin, user"
    user = "user"


class Grade(Enum):
    """Список возможных званий пользователей."""

    Noobie = "Новичок"
    Adept = "Адепт"
    Expert = "Эксперт"
    Veteran = "Ветеран"
    Legend = "Легенда"


class User(BaseModel):
    """ОРМ-модель с декларативным объявлением с помощью SQLAlchemy для пользователей."""

    username: Mapped[str]
    hashed_password: Mapped[str]
    email: Mapped[str]
    role: Mapped[Roles]
    grade: Mapped[Grade] = mapped_column(default="Noobie")
    count: Mapped[int] = mapped_column(default=0)
    registered_at: Mapped[datetime] = mapped_column(default=get_current_time)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=None, onupdate=get_current_time
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
