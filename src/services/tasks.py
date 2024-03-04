from ..utils import UnitOfWorkBase
from ..utils.sqlalchemy_unitofwork import UnitOfWorkSQLAlchemy as UnitOfWork

from ..core.schemas import TaskCreate


class TaskService:
	uow: UnitOfWorkBase
	def __init__(self, uow: UnitOfWorkBase):
		self.uow: UnitOfWorkBase = uow
	
	async def add_task(self, task: TaskCreate):
		# self.uow = UnitOfWork
		task_dict = task.model_dump()
		task = await self.uow.tasks.add_one(task_dict)
		return task
		
	
# task_service = TaskService(UnitOfWork)
