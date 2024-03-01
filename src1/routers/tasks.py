from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src2.repository.db_helper import db_helper
from src2.core.schemas.tasks import TaskDTO, TaskCreate

from src.api_v1.tasks import crud

from ..core.dependencies import get_task_service
from ..services.tasks import TaskService

router = APIRouter(prefix="/tasks")


@router.post("/")
async def add_task(task: TaskCreate,
                   task_service: TaskService = Depends(get_task_service),
                   session: AsyncSession = Depends(db_helper.get_session)) -> list[TaskDTO]:
    return await task_service.add_task(task)

@router.get("/")
async def get_tasks(session: AsyncSession = Depends(db_helper.get_session)) -> list[TaskDTO]:
    return await crud.get_tasks

@router.get("/{task_id}")
async def get_task_from_id(task_id: int,
                           session: AsyncSession = Depends(db_helper.get_session)) -> TaskDTO:
    return await crud.get_task_from_id

