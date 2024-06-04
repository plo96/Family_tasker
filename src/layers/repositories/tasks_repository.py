"""
    Инициализация репозитория для ОРМ-модели Task
"""
from src.layers.repositories.base_repository import BaseRepository
from src.core.models import Task


class TaskRepository(BaseRepository):
    """Реализация репозитория для модели задач (Task)"""
    model = Task
