from fastapi import Depends

from ..utils import UnitOfWorkBase

from ..core.schemas import TaskCreate, TaskDTO
from ..core.dependencies import get_actual_uow


class TaskService:
	uow: UnitOfWorkBase
	
	async def add_task(self,
					   task: TaskCreate,
					   uow: UnitOfWorkBase = get_actual_uow(is_tasks=True)) -> TaskDTO:
		async with uow:
			task_dict = task.model_dump()
			res = await uow.tasks.add_one(task_dict)
			# task = TaskDTO.model_validate(res, from_attributes=True)
			print(res)
			task = TaskDTO.model_validate(res, from_attributes=True)
			print(task)
			await uow.commit()
		
		return res
