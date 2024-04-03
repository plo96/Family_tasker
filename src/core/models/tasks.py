"""
    ОРМ-модель Task для задач
"""
from typing import Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base, get_current_time, get_uuid


class Task(Base):
    """ОРМ-класс с декларативным объявлением с помощью SQLAlchemy для задач"""
    id: Mapped[UUID] = mapped_column(Uuid,
                                     primary_key=True,
                                     default=get_uuid)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    created_by: Mapped[Optional[str]]
    created_at: Mapped[datetime] = mapped_column(default=get_current_time)
    finished_by: Mapped[Optional[str]]
    finished_at: Mapped[Optional[datetime]]

