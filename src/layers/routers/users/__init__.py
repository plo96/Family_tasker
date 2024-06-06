"""
    Роутеры для сущности пользователей.
"""
__all__ = (
    "router",
)

from fastapi import APIRouter

from .admin_users_router import router as admin_users_router
from .users_router import router as user_router

router = APIRouter(
	prefix="/users",
	tags=["Users", ],
)

router.include_router(admin_users_router)
router.include_router(user_router)