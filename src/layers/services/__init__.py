"""
    Модуль с реализацией конкретных сервисов для различных сущностей
"""
__all__ = (
    "tasks_service",
    "users_service",
)

from .users_service import UsersService
from .tasks_service import TaskService
from src.core.dependencies import get_proxy_access_repositories, get_background_tasker

users_service = UsersService(
	proxy_access_repositories=get_proxy_access_repositories(),
	background_tasker=get_background_tasker(),
)

tasks_service = TaskService(
    proxy_access_repositories=get_proxy_access_repositories(),
)
