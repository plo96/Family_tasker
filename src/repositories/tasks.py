from ..utils.sqlalchemy_repository import SQLAlchemyRepository
from ..core.models.tasks import Task


class TaskRepository(SQLAlchemyRepository):
	model = Task
	