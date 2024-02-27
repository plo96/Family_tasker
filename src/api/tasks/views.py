from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_helper import db_helper
from schemas import Task

from . import crud

router = APIRouter(prefix="/tasks")

@router.get("/")
async def get_tasks(session: AsyncSession = Depends(db_helper.get_session)) -> list[Task]:
    return await crud.get_tasks
