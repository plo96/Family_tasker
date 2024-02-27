from typing import Optional
from sqlalchemy import String, Uuid, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from uuid import UUID

from src.project.config import settings

class Base(DeclarativeBase):
    pass


class TaskOrm(Base):
    __tablename__ = "tasks"

    # id: Mapped[UUID] = mapped_column(Uuid,
    #                                  primary_key=True,
    #                                  init=False,
    #                                  server_default=text("CREATE EXTENSION IF NOT EXISTS 'uuid-ossp'; uuid_generate_v4();"))
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(settings.MAX_TASK_NAME_LENGTH))
    description: Mapped[Optional[str]] = mapped_column(String(settings.MAX_TASK_DESCRIPTION_LENGTH))
    price: Mapped[int]

