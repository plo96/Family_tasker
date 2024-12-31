"""
    Роутеры для сущности задач.
"""

__all__ = ("router",)

from fastapi import APIRouter

from .admin_tasks_router import router as admin_tasks_router
from .tasks_router import router as tasks_router

router = APIRouter(
    prefix="/tasks",
    tags=[
        "Tasks",
    ],
)

router.include_router(admin_tasks_router)
router.include_router(tasks_router)
