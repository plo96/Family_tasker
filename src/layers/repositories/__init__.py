"""
    Модуль с реализацией конкретных репозиториев для различных сущностей
"""
__all__ = (
    "TaskRepository",
    "UserRepository",
)

from .tasks import TaskRepository
from .users import UserRepository
