"""
    Конкретная реализация класса для работы со всеми репозиториями в рамках одной сессии
    через асинхронный контекстный менеджер.
"""
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session

from src.layers.repositories import TaskRepository, UserRepository
from .i_proxy_access_repositories import IProxyAccessRepositories


class ProxyAccessRepositories(IProxyAccessRepositories):
    """Реализация класса на базе SQLAlchemy"""

    def __init__(self, session_factory: async_sessionmaker | async_scoped_session):
        """
        :param session_factory: Фабрика сессий для доступа к БД.
        """
        self._session_factory = session_factory

    async def __aenter__(self):
        """
        Вход в асинхронный контекстный менеджер - получение сессии, инициализация репозиториев на основе этой сессии.
        """
        self._session = self._session_factory()
        self.tasks = TaskRepository(self._session)
        self.users = UserRepository(self._session)

    async def __aexit__(self, *args):
        """
        Выход из асинхронного контекстного менеджера - откат несохранённых изменений, закрытие сесии.
        """
        await self.rollback()
        await self._session.close()

    async def commit(self):
        """
        Сохранение текущих изменений в БД.
        """
        await self._session.commit()

    async def rollback(self):
        """
        Откат текущих изменений в БД.
        """
        await self._session.rollback()
