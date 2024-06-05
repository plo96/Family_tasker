"""
    Содержит все основные зависимости, используемые в приложении.
"""
from typing import Callable

from uuid import UUID
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.core.schemas import UserDTO
from src.auth.security import oauth2_scheme, verify_jwt_token
from src.database import db_helper
from src.layers.utils.proxy_access_repositories import ProxyAccessRepositories, IProxyAccessRepositories
from src.layers.utils.background_tasker import IBackgroundTasker, BackgroundTasker
from src.project import settings
from src.project.exceptions import AccessPermissionError, TokenError


def get_actual_session_factory() -> async_sessionmaker:
    return db_helper.get_session_factory()


def get_proxy_access_repositories(
        session_factory: async_sessionmaker = Depends(get_actual_session_factory),
) -> IProxyAccessRepositories:
    """
    Возвращает актуальный экземпляр ProxyAccessRepositories для единого доступа ко всем репозиториям сущностей.
    :param session_factory: Фабрика сессий для доступа к БД.
    :return: Экземпляр ProxyAccessRepositories, реализующий интерфейс IProxyAccessRepositories.
    """
    return ProxyAccessRepositories(session_factory=session_factory)


def get_background_tasker() -> IBackgroundTasker:
    """Возвращает актуальный экземпляр BackgroundTasker для осуществления задач в фоне."""
    return BackgroundTasker(email_stmp_user=settings.EMAIL_SMTP_USER)


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> UserDTO:
    """
    Получение текущего пользователя по токену, содержащемуся в request.headers.get("Authorization").
    :param token: JWT-токен, получается из заголовков в DI.
    :param proxy_access_repositories: Единая точка доступа ко всем репозиториям, получается в DI.
    :return: Экземпляр UserDTO, соответствующий текущему пользователю.
    """
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise TokenError(detail="Invalid token.")

    decoded_data["id"] = UUID(decoded_data["id"])
    async with proxy_access_repositories as repositories:
        result = await repositories.users.get_by_params(id=decoded_data["id"])
        if not result:
            raise TokenError(detail="User is not exist.")
        result = result[0]
        user = UserDTO.model_validate(result)
    
    if user.is_deleted:
        raise TokenError(detail="User is not allowed (is deleted).")

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
        :return: Экземпляр UserDTO, соответствующий текущему пользователю, в случае наличия у него требуемой роли.
                 HTTPException с кодом 406 в случае отсутствия у пользователя требуемой роли.
        """
        if role not in current_user.role:
            raise AccessPermissionError

        return current_user
    
    return role_validator
