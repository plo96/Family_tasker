"""
    Реализация конкретного UnitOfWork на базе SQLAlchemy
"""
from src.repositories.tasks import TaskRepository
from src.database.db_helper import db_helper

from .base_unitofwork import UnitOfWorkBase


class UnitOfWorkSQLAlchemy(UnitOfWorkBase):
    """Реализация UoW на базе SQLAlchemy"""
    def __init__(self, is_tasks: bool = False):
        # self._session_factory = db_helper.get_scoped_session_factory
        self._session = db_helper.get_scoped_session_factory()
        self.is_tasks = is_tasks

    async def __aenter__(self):
        if self.is_tasks:
            self.tasks = TaskRepository(self._session)

    async def __aexit__(self, *args):
        await self.rollback()
        # await self._session.close()
        await self._session.remove()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
