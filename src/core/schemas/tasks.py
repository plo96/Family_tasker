"""
    Создание различных вариаций класса Task на базе Pydantic для последующей валидации данных
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

MAX_TASK_NAME_LENGTH: int = 64
MAX_TASK_DESCRIPTION_LENGTH: int = 1024
MIN_TASK_PRICE: int = 0
MAX_TASK_PRICE: int = 10


class TaskBase(BaseModel):
    """Базовая pydantic-схема для задач."""
    pass


class TaskCreate(TaskBase):
    """Схема для создания задачи."""
    name: str = Field(max_length=MAX_TASK_NAME_LENGTH)
    description: str = Field(max_length=MAX_TASK_DESCRIPTION_LENGTH)
    price: int = Field(ge=MIN_TASK_PRICE, le=MAX_TASK_PRICE)


class TaskUpdate(TaskCreate):
    """Схема для полного изменения задачи."""
    pass


class TaskUpdatePartial(TaskBase):
    """Схема для частичного изменения задачи."""
    name: str = Field(max_length=MAX_TASK_NAME_LENGTH, default=None)
    description: str = Field(max_length=MAX_TASK_DESCRIPTION_LENGTH, default=None)
    price: int = Field(ge=MIN_TASK_PRICE, le=MAX_TASK_PRICE, default=None)


class TaskDTO(TaskBase):
    """ДТО-класс для сущности задачи."""
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str = Field(max_length=MAX_TASK_NAME_LENGTH)
    description: str = Field(max_length=MAX_TASK_DESCRIPTION_LENGTH)
    price: int = Field(ge=MIN_TASK_PRICE, le=MAX_TASK_PRICE)
    created_by: Optional[str]           # TODO: Автоматизировать получение автора задачи и убарть Optional
    created_at: Optional[datetime]      # TODO: Автоматизировать получение времени создания задачи и убарть Optional
    updated_at: Optional[datetime]
    finished_by: Optional[str]
    finished_at: Optional[datetime]
