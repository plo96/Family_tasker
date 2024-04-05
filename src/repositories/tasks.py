"""
    Инициализация репозитория для ОРМ-модели Task
"""
from src.utils import SQLAlchemyRepository
from src.core.models import Task


class TaskRepository(SQLAlchemyRepository):
    """Реализация репозитория для модели задач (Task)"""
    model = Task
