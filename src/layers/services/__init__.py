"""
    Модуль с реализацией конкретных сервисов для различных сущностей
"""
__all__ = (
    "TaskService",
    "UserService",
)

from .tasks import TaskService
from .users import UserService
