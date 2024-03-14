from fastapi import APIRouter, Depends

from src.core.schemas import TaskDTO, TaskCreate
from src.services import TaskService


router = APIRouter(prefix="/tasks")


@router.post("/")
async def add_task(new_task: TaskCreate) -> TaskDTO:
    return await TaskService.add_task(new_task)


@router.get("/")
async def get_tasks() -> list[TaskDTO]:
    return await TaskService.get_tasks()

#
# @router.get("/{task_id}")
# async def get_task_from_id(task_id: int = ) -> TaskDTO:
#     return await crud.get_task_from_id

