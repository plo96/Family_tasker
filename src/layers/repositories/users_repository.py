"""
    Инициализация репозитория для ОРМ-модели User
"""

from src.layers.repositories.base_repository import BaseRepository
from src.core.models import User


class UserRepository(BaseRepository):
    """Реализация репозитория для модели пользователей (User)"""

    model = User
