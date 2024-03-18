"""
    Инициализация репозитория для ОРМ-модели Task
"""
from src.utils.sqlalchemy_repository import SQLAlchemyRepository
from src.core.models.tasks import Task


class TaskRepository(SQLAlchemyRepository):
    model = Task
