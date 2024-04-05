"""
    Реализация конкретного UnitOfWork на базе SQLAlchemy
"""
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session

from src.repositories import TaskRepository, UserRepository
from .base_unitofwork import UnitOfWorkBase


class UnitOfWorkSQLAlchemy(UnitOfWorkBase):
    """Реализация UoW на базе SQLAlchemy"""

    def __init__(self, session_factory: async_sessionmaker | async_scoped_session):
        self._session_factory = session_factory

    async def __aenter__(self):
        self._session = self._session_factory()
        self.tasks = TaskRepository(self._session)
        self.users = UserRepository(self._session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self._session.close()

    async def commit(self):
        """Сохранение текущих изменений в БД"""
        await self._session.commit()

    async def rollback(self):
        """Откат текущих изменений в БД"""
        await self._session.rollback()
