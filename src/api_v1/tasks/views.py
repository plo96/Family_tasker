from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.db_helper import db_helper
from schemas import TaskDTO

from . import crud

router = APIRouter(prefix="/tasks")

@router.get("/")
async def get_tasks(session: AsyncSession = Depends(db_helper.get_session)) -> list[TaskDTO]:
    return await crud.get_tasks

@router.get("/{task_id}")
async def get_task_from_id(task_id: int,
                           session: AsyncSession = Depends(db_helper.get_session)) -> TaskDTO:
    return await crud.get_task_from_id

