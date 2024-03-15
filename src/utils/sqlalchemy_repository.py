from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy import insert, select, delete

from .base_repository import BaseRepository


class SQLAlchemyRepository(BaseRepository):
    """SQLAlchemy-класс для работы с рапозиторием для конкретной модели ORM"""
    model = None

    def __init__(self, session: AsyncSession | async_scoped_session):
        self.session = session

    async def add_one(self, data: dict) -> model:
        new_one = self.model(**data)
        self.session.add(new_one)
        await self.session.flush()
        await self.session.refresh(new_one)
        return new_one

    async def get_all(self) -> list[model]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_by_params(self, **kwargs) -> list[model]:
        stmt = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def delete_by_params(self, **kwargs) -> list[model]:
        
        stmt = delete(self.model).filter_by(**kwargs)
        await self.session.execute(stmt)

        query = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(query)
        res = res.scalars().all()
        
        return list(res)
