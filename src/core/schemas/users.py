"""
    Создание различных вариаций класса User на базе Pydantic для последующей валидации данных
"""

from datetime import datetime
from typing import Optional

from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

MAX_USER_NAME_LENGTH: int = 32
MIN_USER_NAME_LENGTH: int = 3
MIN_PASSWORD_LENGTH: int = 8


class UserBase(BaseModel):
    """Базовая схема для сущности пользователя."""

    username: str = Field(
        max_length=MAX_USER_NAME_LENGTH, min_length=MIN_USER_NAME_LENGTH
    )


class UserCreate(UserBase):
    """Схема для создания пользователя."""

    password: str = Field(min_length=MIN_PASSWORD_LENGTH)
    email: str


class UserUpdatePartial(UserBase):
    """Схема для частичного изменения пользователя."""

    username: str = Field(
        max_length=MAX_USER_NAME_LENGTH, min_length=MIN_USER_NAME_LENGTH, default=None
    )
    password: str = Field(min_length=MIN_PASSWORD_LENGTH, default=None)
    email: str = Field(default=None)
    role: str = Field(default=None)


class UserDTO(UserBase):
    """ДТО-класс для сущности пользователя."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    hashed_password: str
    email: str
    role: str
    grade: str
    count: int
    registered_at: datetime
    updated_at: Optional[datetime]
    is_deleted: bool
    is_verified: bool
