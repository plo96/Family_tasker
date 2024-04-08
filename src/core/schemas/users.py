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
    """Базовая pydantic-модель для пользователей"""
    name: str = Field(max_length=MAX_USER_NAME_LENGTH, min_length=MIN_USER_NAME_LENGTH)


class UserCreate(UserBase):
    """pydantic-модель для создания пользователя"""
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)
    email: str
    role: str


class UserUpdatePartial(UserBase):
    """pydantic-модель для частичного изменения пользователя"""
    name: str = Field(max_length=MAX_USER_NAME_LENGTH, min_length=MIN_USER_NAME_LENGTH, default=None)
    password: str = Field(min_length=MIN_PASSWORD_LENGTH, default=None)
    email: str = Field(default=None)
    role: str = Field(default=None)
    
    
class UserCheck(UserBase):
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)


class UserDTO(UserBase):
    """ДТО-класс для преобразования ответа алхимии к pydantic и дальнейшей работы с ней"""
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
 