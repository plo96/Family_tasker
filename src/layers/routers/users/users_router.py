"""
    Роутер для взаимодействия с сущностью пользователей.
"""

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.project.exceptions import endpoint_exceptions_processing
from src.core.schemas import UserCreate, UserDTO, UserCheck
from src.core.dependencies import get_proxy_access_repositories
from src.layers.services import UserService
from src.layers.utils import IProxyAccessRepositories

router = APIRouter(
    tags=["Users", "AllUsers"],
)


@router.post("/token")
@endpoint_exceptions_processing
async def token(
        user_check: UserCheck,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> JSONResponse:
    """
    Эндпоинт для получения токена по имени и паролю.
    :param user_check: Экземпляр UserCheck, содержащий имя и пароль пользователя.
    :param proxy_access_repositories: Единая точка доступа к репозиториям, передается через DI.
    :return: Ответ JSON со статусом 200 и токеном в теле ответа в случае успешного прохождения аутентификации.
             UserNotExistError в случае отсутствия пользователя с таким именем.
             UserNotAllowedError в случае если пользователь с таким именем удалён или не верифицирован.
             PasswordIsNotCorrect в случае если пароль пользователя неверен.
    """
    token = await UserService.get_token(
        proxy_access_repositories=proxy_access_repositories,
        user_check=user_check,
    )
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"access_token": token, "token_type": "bearer"})


@router.post("/", response_model=UserDTO)
@endpoint_exceptions_processing
async def add_user(
        new_user: UserCreate,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> UserDTO:
    """
    Эндпоинт для добавления одного пользователя.
    :param new_user: Данные для создания нового пользователя в виде экземпляра UserCreate.
    :param proxy_access_repositories: Единая точка доступа к репозиториям, передается через DI.
    :return: Экземпляр UserDTO, соответствующий новой созданному пользователю.
    """
    return await UserService.add_user(
        proxy_access_repositories=proxy_access_repositories,
        new_user=new_user,
    )
