from typing import Generic, TypeVar, Callable
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from .db_helper import db_helper
from .base_unitofwork import UnitOfWorkBase
from ..repositories.tasks import TaskRepository



# _AS = TypeVar("_AS", bound="AsyncSession")
# Generic[_AS]
class UnitOfWorkSQLAlchemy(UnitOfWorkBase):
    
    def __init__(self, is_tasks: bool = False):
        self._session_factory = db_helper.scoped_session_factory
        self.is_tasks = is_tasks

    async def __aenter__(self):
        self._session = self._session_factory()
        if self.is_tasks: self.tasks = TaskRepository(self._session)

    async def __aexit__(self, *args):
        await self.rollback()
        # await self._session.remove()
        await self._session.remove()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

