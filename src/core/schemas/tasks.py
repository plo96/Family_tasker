from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

MAX_TASK_NAME_LENGTH: int = 64
MAX_TASK_DESCRIPTION_LENGTH: int = 512
MIN_TASK_PRICE: int = 0
MAX_TASK_PRICE: int = 10


class TaskBase(BaseModel):
    pass


class TaskCreate(TaskBase):
    name: str = Field(max_length=MAX_TASK_NAME_LENGTH)
    description: str = Field(max_length=MAX_TASK_DESCRIPTION_LENGTH)
    price: int = Field(ge=MIN_TASK_PRICE, le=MAX_TASK_PRICE)


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(TaskCreate):
    name: str = Field(max_length=MAX_TASK_NAME_LENGTH, default=None)
    description: str = Field(max_length=MAX_TASK_DESCRIPTION_LENGTH, default=None)
    price: int = Field(ge=MIN_TASK_PRICE, le=MAX_TASK_PRICE, default=None)


class TaskDTO(TaskCreate):
    """ДТО-класс для преобразования ответа алхимии к pydantic"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_by: Optional[str]
    created_at: Optional[datetime]
    finished_by: Optional[str]
    finished_at: Optional[datetime]






