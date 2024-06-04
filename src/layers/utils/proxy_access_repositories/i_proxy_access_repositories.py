"""
    Интерфейс класса для работы со всеми репозиториями в рамках одной сессии
    через асинхронный контекстный менеджер.
"""
from abc import ABC, abstractmethod

from src.layers.repositories import TaskRepository, UserRepository


class IProxyAccessRepositories(ABC):
    """
    Базовый абстрактный класс для подключения к БД в контекстном менеджере.
    Единая точка доступа ко всем репозиториям различных сущностей.
    """
    users: UserRepository
    tasks: TaskRepository

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass

    @abstractmethod
    async def commit(self):
        """Сохранение изменений в БД"""
        pass

    @abstractmethod
    async def rollback(self):
        """Откат изменений в БД"""
        pass
