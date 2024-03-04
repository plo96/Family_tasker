# from typing import Annotated
#
# from ..repositories.tasks import TaskRepository
from ..services.tasks import TaskService
from ..utils import UnitOfWorkSQLAlchemy as UoW


def get_task_service():
	task_service = TaskService()
	return task_service


def get_actual_uow(**kwargs):
	uow = UoW(**kwargs)
	return uow

