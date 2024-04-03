"""
    Содержит все основные зависимости, используемые в приложении
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from src.database import db_helper
from src.utils import UnitOfWorkSQLAlchemy, UnitOfWorkBase


def get_actual_session_factory() -> async_sessionmaker:
    return db_helper.get_session_factory()


def get_actual_uow(session_factory: async_sessionmaker = Depends(get_actual_session_factory)) -> UnitOfWorkBase:
    """Возвращает актуальный экземпляр UnitOfWork с передачей ему метода получения сессий с БД"""
    return UnitOfWorkSQLAlchemy(session_factory=session_factory)


