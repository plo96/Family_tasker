from src.utils import UnitOfWorkBase
from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import TaskCreate, TaskDTO
from src.core.dependencies import get_actual_uow


class TaskService:
	uow: UnitOfWorkBase
	
	@staticmethod
	async def add_task(task: TaskCreate,
					   uow: UnitOfWorkBase = get_actual_uow(is_tasks=True)) -> TaskDTO:
		async with uow:
			task_dict = task.model_dump()
			res = await uow.tasks.add_one(task_dict)
			task = TaskDTO.model_validate(res)
			await uow.commit()
		
		return task
	
	@staticmethod
	async def get_tasks(uow: UnitOfWorkBase = get_actual_uow(is_tasks=True)) -> list[TaskDTO]:
		async with uow:
			res = await uow.tasks.get_all()
			all_tasks = [TaskDTO.model_validate(task) for task in res]
		
		return all_tasks
	
	@staticmethod
	async def get_task_by_id(task_id: int,
							 uow: UnitOfWorkBase = get_actual_uow(is_tasks=True)) -> TaskDTO:
		async with uow:
			res = await uow.tasks.get_by_params(id=task_id)
			if not res:
				raise ObjectNotFoundError
			res = res[0]
			task = TaskDTO.model_validate(res)
		
		return task
	
	@staticmethod
	async def delete_task_by_id(task_id: int,
								uow: UnitOfWorkBase = get_actual_uow(is_tasks=True)) -> bool:
		async with uow:
			res = await uow.tasks.delete_by_params(id=task_id)
			if not res:
				await uow.commit()
				return True
			return False
