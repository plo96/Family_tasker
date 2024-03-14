from fastapi import Depends

from ..utils import UnitOfWorkBase

from ..core.schemas import TaskCreate, TaskDTO
from ..core.dependencies import get_actual_uow


class TaskService:
    uow: UnitOfWorkBase

    @staticmethod
    async def add_task(task: TaskCreate,
                       uow: UnitOfWorkBase = get_actual_uow(is_tasks=True)) -> TaskDTO:
        async with uow:
            task_dict = task.model_dump()
            res = await uow.tasks.add_one(task_dict)
            task = TaskDTO.model_validate(res, from_attributes=True)
            await uow.commit()

        return task

    @staticmethod
    async def get_tasks(uow: UnitOfWorkBase = get_actual_uow(is_tasks=True)) -> list[TaskDTO]:
        async with uow:
            res = await uow.tasks.get_all()
            all_tasks = [TaskDTO.model_validate(task, from_attributes=True) for task in res]

        return all_tasks


