"""
    Содержит все основные зависимости, используемые в приложении
"""
from typing import Callable

from uuid import UUID
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.schemas import UserDTO
from src.auth.security import oauth2_scheme, verify_jwt_token
from src.database import db_helper
from src.layers.utils import ProxyAccessRepositories, IProxyAccessRepositories


def get_actual_session_factory() -> async_sessionmaker:
    return db_helper.get_session_factory()


def get_proxy_access_repositories(
        session_factory: async_sessionmaker = Depends(get_actual_session_factory),
) -> IProxyAccessRepositories:
    """Возвращает актуальный экземпляр ProxyAccessRepositories с передачей ему метода получения сессий с БД."""
    return ProxyAccessRepositories(session_factory=session_factory)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> UserDTO:
    """
    Получение текущего пользователя по токену, содержащемуся в request.headers.get("Authorization").
    :param token: JWT-токен, получается из заголовков в DI.
    :param proxy_access_repositories: Единая точка доступа ко всем репозиториям, получается в DI.
    :return:
    """
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    decoded_data["id"] = UUID(decoded_data["id"])
    async with proxy_access_repositories as repositories:
        result = await repositories.users.get_by_params(id=decoded_data["id"])
        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
        result = result[0]
        user = UserDTO.model_validate(result)
    
    if user.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not allowed")

    return user


def get_current_user_having_role(role: str) -> Callable[[UserDTO], UserDTO]:
    """
    Замыкание над функцией авторизации пользователя role_validator с передачей ей роли пользователя для проверки.
    :param role: Требуемая роль в наличии у пользователя для авторизации.
    :return: Функция role_validator с определённой ролью для поверки.
    """
    def role_validator(current_user: UserDTO = Depends(get_current_user)) -> UserDTO:
        """
        Авторизация текущего пользователя.
        :param current_user: ДТО для текущего пользователя, получение из DI.
        :return: ДТО пользователя в случае наличия у пользователя требуемой роли.
                 HTTPException с кодом 406 в случае отсутствия у пользователя требуемой роли.
        """
        if role not in current_user.role:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="insufficient permissions")
        return current_user
    
    return role_validator
