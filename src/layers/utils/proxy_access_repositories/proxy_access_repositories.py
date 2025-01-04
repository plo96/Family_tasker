"""
    Конкретная реализация класса для работы со всеми репозиториями в рамках одной сессии
    через асинхронный контекстный менеджер.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session

from src.database.db_helper import get_actual_session_factory
from src.layers.repositories import TaskRepository, UserRepository
from src.layers.utils.proxy_access_repositories import IProxyAccessRepositories
from src.layers.utils.proxy_access_repositories.i_proxy_access_repositories import (
    IProxyAccessRepositories,
)


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
        return self

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


def get_proxy_access_repositories(
    session_factory: async_sessionmaker = get_actual_session_factory(),
) -> IProxyAccessRepositories:
    """
    Возвращает актуальный экземпляр ProxyAccessRepositories для единого доступа ко всем репозиториям сущностей.
    :param session_factory: Фабрика сессий для доступа к БД.
    :return: Экземпляр ProxyAccessRepositories, реализующий интерфейс IProxyAccessRepositories.
    """
    return ProxyAccessRepositories(session_factory=session_factory)
