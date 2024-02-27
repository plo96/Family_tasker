from pydantic import BaseModel, Field
from src.project.config import settings


class TaskAdd(BaseModel):
    name: str = Field(max_length=settings.MAX_TASK_NAME_LENGTH)
    description: str = Field(max_length=settings.MAX_TASK_DESCRIPTION_LENGTH)
    price: int = Field(ge=settings.MIN_TASK_PRICE, le=settings.MAX_TASK_PRICE)


class Task(TaskAdd):
    id: int
