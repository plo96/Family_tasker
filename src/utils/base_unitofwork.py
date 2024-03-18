"""
    Интерфейс для работы с UnitOfWork
"""
from abc import ABC, abstractmethod

from src.repositories.tasks import TaskRepository


class UnitOfWorkBase(ABC):
    """Базовый абстрактный класс для создания интерфейса UoW"""
    tasks: TaskRepository

    @abstractmethod
    def __init__(self, **kwargs):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        """Сохранение изменений в БД"""
        ...

    @abstractmethod
    async def rollback(self):
        """Откат изменений в БД"""
        ...
