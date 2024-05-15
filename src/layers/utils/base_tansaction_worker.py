"""
    Интерфейс для единого метода работы с транзакциями.
"""
from abc import ABC, abstractmethod

from src.layers.repositories import TaskRepository, UserRepository


class TransactionWorkerBase(ABC):
    """Базовый абстрактный класс для создания интерфейса TransactionWorkerBase"""
    tasks: TaskRepository
    users: UserRepository

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