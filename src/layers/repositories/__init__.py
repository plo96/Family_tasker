"""
    Модуль с реализацией конкретных репозиториев для различных сущностей
"""

__all__ = (
    "IRepository",
    "TaskRepository",
    "UserRepository",
)

from .tasks_repository import TaskRepository
from .users_repository import UserRepository
from .i_repository import IRepository
