from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy import insert, select

from .base_repository import BaseRepository


class SQLAlchemyRepository(BaseRepository):
	"""SQLAlchemy-класс для работы с рапозиторием для конкретной модели ORM"""
	model = None

	def __init__(self, session: AsyncSession | async_scoped_session):
		self.session = session
	
	async def add_one(self, data: dict):
		stmt = insert(self.model).values(**data).returning(self.model)
		res = await self.session.execute(stmt)
		return res
		# return res.scalars()
	
	async def get_all(self):
		stmt = select(self.model)
		res = await self.session.execute(stmt)
		return list(res.scalars().all())

		