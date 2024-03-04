from typing import Generic, TypeVar, Callable

from .base_unitofwork import UnitOfWorkBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session

from ..repositories.tasks import TaskRepository
from .db_helper import db_helper


# _AS = TypeVar("_AS", bound="AsyncSession")
# Generic[_AS]
class UnitOfWorkSQLAlchemy(UnitOfWorkBase):
    def __init__(self, is_tasks: bool = False):
        self._session_factory = db_helper.scoped_session_factory

        if is_tasks: self.tasks = TaskRepository(self._session)

    async def __aenter__(self):
        self._session = self._session_factory()
        # return self

    async def __aexit__(self, *args):
        await self.rollback()
        # await self._session.remove()
        await self._session_factory.remove()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

