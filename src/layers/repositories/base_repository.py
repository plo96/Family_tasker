"""
    Реализация конкретного репозитория на базе SQLAlchemy
"""
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy import select

from src.layers.repositories.i_repository import IRepository
from src.core.models import BaseModel


class BaseRepository(IRepository):
    """SQLAlchemy-класс для работы с репозиторием для конкретной модели ORM"""
    model: type(BaseModel) = None

    def __init__(self, session: AsyncSession | async_scoped_session):
        self.session = session

    async def add_one(self, data: dict) -> model:
        """
        Добавление одного экземпляра текущей модели в БД.
        :param data: Словарь с параметрами модели.
        :return: Созданный экземпляр модели из БД.
        """
        new_one = self.model(**data)
        self.session.add(new_one)
        await self.session.flush()
        await self.session.refresh(new_one)
        return new_one

    async def get_all(self) -> list[model]:
        """
        Получение всех экземпляров текущей модели из БД.
        :return: Список экземпляров модели из БД.
        """
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_by_params(self, **kwargs) -> list[model]:
        """
        Получение списка экземпляров текущей модели из БД, имеющих перечисленные значения указанных полей.
        :param kwargs: Список keyword-аргументов с перечислением требуемых параметров для отбора.
        :return: Список экземпляров модели из БД, удовлетворяющих условию отбора.
        """
        stmt = select(self.model).filter_by(**kwargs)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def delete_one_entity(self, entity: model) -> None:
        """
        Удаление переданного экземпляра модели из БД.
        :param entity: Экземпляр модели для удаления.
        """
        await self.session.delete(entity)
        await self.session.flush()

    async def update_one_entity(self, entity: model, data: dict) -> model:
        """
        Изменение параметров одного экземпляра текущей модели.
        :param entity: Экземпляр модели для изменения.
        :param data: Словарь с параметрами модели, требующими изменения.
        :return: Изменённый экземпляр моедели из БД.
        """
        for name, value in data.items():
            setattr(entity, name, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity
