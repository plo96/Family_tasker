"""
    Модуль с реализацией конкретных роутеров для различных сущностей
"""
__all__ = (
    "router",
)

from fastapi import APIRouter

from .tasks_router import router as task_router
from .users import router as user_router

router = APIRouter()

router.include_router(task_router)
router.include_router(user_router)
