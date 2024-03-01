from ..repositories.repository import AbstractRepository
from src2.core.schemas import TaskCreate


class TaskService:
	def __init__(self, task_repo: AbstractRepository):
		self.task_repo: AbstractRepository = task_repo()
		
	
	async def add_task(self, task: TaskCreate):
		task_dict = task.model_dump()
		task = await self.task_repo.add_one(task_dict)
		return task
		
	
	