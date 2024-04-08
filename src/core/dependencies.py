"""
    Содержит все основные зависимости, используемые в приложении
"""
from typing import Callable

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.schemas import UserDTO
from src.auth.security import oauth2_scheme, verify_jwt_token
from src.database import db_helper
from src.layers.utils import UnitOfWorkSQLAlchemy, UnitOfWorkBase


def get_actual_session_factory() -> async_sessionmaker:
    return db_helper.get_session_factory()


def get_actual_uow(session_factory: async_sessionmaker = Depends(get_actual_session_factory)) -> UnitOfWorkBase:
    """Возвращает актуальный экземпляр UnitOfWork с передачей ему метода получения сессий с БД"""
    return UnitOfWorkSQLAlchemy(session_factory=session_factory)


async def get_current_user(token: str = Depends(oauth2_scheme),
                           uow: UnitOfWorkBase = Depends(get_actual_uow)) -> UserDTO:
    """Получение текущего пользователя по токену, содержащемуся в request.headers.get("Authorization")"""
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    
    async with uow:
        result = await uow.users.get_by_params(id=decoded_data["id"])
        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
        user = result[0]

    if user.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not allowed")

    return user


def get_current_user_with_role(role: str) -> Callable[[UserDTO], UserDTO]:
    """Возвращение сущности текущего пользователя в случае наличия у него требуемой роли"""
    def role_validator(current_user: UserDTO = Depends(get_current_user)) -> UserDTO:
        if role not in current_user.roles:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="insufficient permissions")
        return current_user
    
    return role_validator
    