from fastapi import APIRouter, Depends

from ..core.schemas import TaskDTO, TaskCreate

from ..services import TaskService

router = APIRouter(prefix="/tasks")


@router.post("/")
async def add_task(new_task: TaskCreate,
                   task_service: TaskService = Depends(get_task_service())) -> list[TaskDTO]:
    return await task_service.add_task(new_task)

# @router.get("/")
# async def get_tasks() -> list[TaskDTO]:
#     return await crud.get_tasks
#
# @router.get("/{task_id}")
# async def get_task_from_id(task_id: int = ) -> TaskDTO:
#     return await crud.get_task_from_id

