"""
    Реализация конкретного UnitOfWork на базе SQLAlchemy
"""
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session

from src.repositories import TaskRepository
from .base_unitofwork import UnitOfWorkBase


class UnitOfWorkSQLAlchemy(UnitOfWorkBase):
    """Реализация UoW на базе SQLAlchemy"""
	
    def __init__(self, session_factory: async_sessionmaker | async_scoped_session):
        self._session_factory = session_factory
	
    async def __aenter__(self):
        self._session = self._session_factory()
        self.tasks = TaskRepository(self._session)
	
    async def __aexit__(self, *args):
        await self.rollback()
        if isinstance(self._session_factory, async_sessionmaker):
            await self._session.close()
        if isinstance(self._session_factory, async_scoped_session):
            await self._session_factory.remove()
	
    async def commit(self):
        await self._session.commit()
	
    async def rollback(self):
        await self._session.rollback()
