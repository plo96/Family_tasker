"""
    Модуль с реализацией конкретных репозиториев для различных сущностей
"""
__all__ = (
    "IRepository",
    "TaskRepository",
    "UserRepository",
)

from .tasks import TaskRepository
from .users import UserRepository
from .i_repository import IRepository
