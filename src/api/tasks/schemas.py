from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .config import *


class TaskCreate(BaseModel):
    name: str = Field(max_length=MAX_TASK_NAME_LENGTH)
    description: str = Field(max_length=MAX_TASK_DESCRIPTION_LENGTH)
    price: int = Field(ge=MIN_TASK_PRICE, le=MAX_TASK_PRICE)


class TaskDTO(TaskCreate):
    id: int
    created_by: str
    created_at: datetime
    finished_by: Optional[str]
    finished_at: Optional[datetime]


class TaskUpdate(TaskCreate):
    pass


class TaskUpdatePartial(TaskCreate):
    name: str(max_length=MAX_TASK_NAME_LENGTH)
