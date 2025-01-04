from typing import Callable
from uuid import UUID

from fastapi import Depends

from src.auth.jwt import oauth2_scheme, verify_jwt_token
from src.layers.utils.proxy_access_repositories.proxy_access_repositories import (
    get_proxy_access_repositories,
)
from src.core.schemas import UserDTO
from src.layers.utils.proxy_access_repositories import IProxyAccessRepositories
from src.project.exceptions import TokenError, AccessPermissionError


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> UserDTO:
    """
    Получение текущего пользователя по токену, содержащемуся в request.headers.get("Authorization").
    :param token: JWT-токен, получается из заголовков в DI.
    :return: Экземпляр UserDTO, соответствующий текущему пользователю.
    """
    proxy_access_repositories: IProxyAccessRepositories = (
        get_proxy_access_repositories()
    )

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
