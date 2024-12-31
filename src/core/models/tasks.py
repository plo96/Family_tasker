"""
    Модель представления сущности задачи в БД.
"""

from typing import Optional
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base_model import BaseModel
from src.core.models.default_values import get_current_time


class Task(BaseModel):
    """ОРМ-класс с декларативным объявлением с помощью SQLAlchemy для задач"""

    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    created_by: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=get_current_time)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=None, onupdate=get_current_time
    )
    finished_by: Mapped[Optional[str]]
    finished_at: Mapped[Optional[datetime]]
