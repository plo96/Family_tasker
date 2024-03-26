"""
    Содержит все основные зависимости, используемые в приложении
"""
from src.database import db_helper
from src.utils.sqlalchemy_unitofwork import UnitOfWorkSQLAlchemy as UoW


def get_actual_uow():
    """Возвращает актуальный экземпляр UnitOfWork с передачей ему метода получения сессий с БД"""
    uow = UoW(session_factory=db_helper.get_session_factory())              # noqa
    # uow = UoW(session_factory=db_helper.get_scoped_session_factory())     # noqa
    return uow
