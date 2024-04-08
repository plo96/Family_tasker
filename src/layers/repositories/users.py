"""
    Инициализация репозитория для ОРМ-модели User
"""
from src.layers.utils import SQLAlchemyRepository
from src.core.models import User


class UserRepository(SQLAlchemyRepository):
    """Реализация репозитория для модели пользователей (User)"""
    model = User
