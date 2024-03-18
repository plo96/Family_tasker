"""
    Содержит все основные зависимости, используемые в приложении
"""
from src.utils.sqlalchemy_unitofwork import UnitOfWorkSQLAlchemy as UoW


def get_actual_uow(**kwargs):
    uow = UoW(**kwargs)
    return uow
