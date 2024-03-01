from abc import ABC, abstractmethod
from fastapi import Depends, insert, select
from sqlalchemy.exc.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .db_helper import db_helper


class AbstractRepository(ABC):
	"""Абстрактный класс для работы с рапозиторием"""
	@abstractmethod
	async def add_one(self, data: dict):
		raise NotImplementedError
	
	@abstractmethod
	async def get_all(self):
		raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
	"""SQLAlchemy-класс для работы с рапозиторием для конкретной модели ORM"""
	model = None
	
	async def add_one(self, data: dict,
					  session: AsyncSession = Depends(db_helper.get_session)) -> model:
		stmt = insert(self.model).values(**data).returning(self.model)
		res = await session.execute(stmt)
		await session.commit()
		return res
		# new_one = self.model(**data)
		# session.add(new_one)
		# await session.commit()
		# await session.refresh(new_one)
		# return new_one
	
	async def get_all(self, session: AsyncSession = Depends(db_helper.get_session)) -> list[model]:
		stmt = select(self.model)
		res = await session.execute(stmt)
		return list(res.scalars().all())

		