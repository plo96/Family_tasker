from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Task(Base):
    __tablename__ = "tasks"

    # id: Mapped[UUID] = mapped_column(Uuid,
    #                                  primary_key=True,
    #                                  init=False,
    #                                  server_default=text("CREATE EXTENSION IF NOT EXISTS 'uuid-ossp'; uuid_generate_v4();"))
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    created_by: Mapped[str]
    created_at: Mapped[datetime]
    finished_by: Mapped[str | None]
    finished_at: Mapped[datetime | None]

