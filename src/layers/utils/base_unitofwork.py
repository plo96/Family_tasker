"""
    Интерфейс для работы с UnitOfWork
"""
from abc import ABC, abstractmethod

from src.layers.repositories import TaskRepository, UserRepository


class UnitOfWorkBase(ABC):
    """Базовый абстрактный класс для подключения к БД в контекстном менеджере."""
    tasks: TaskRepository
    users: UserRepository

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
