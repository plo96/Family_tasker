"""
    Роутер для взаимодействия с сущностью пользователей (для пользователей).
"""

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.core.dependencies import get_current_user_having_role
from src.project.exceptions import endpoint_exceptions_processing
from src.core.schemas import UserCreate, UserDTO, UserCheck
from src.layers.services import users_service

router = APIRouter(
    tags=["Users", "AllUsers"],
    dependencies=[Depends(get_current_user_having_role('user')), ],
)


@router.post("/token")
@endpoint_exceptions_processing
async def token(
        user_check: UserCheck,
) -> JSONResponse:
    """
    Эндпоинт для получения токена по имени и паролю.
    :param user_check: Экземпляр UserCheck, содержащий имя и пароль пользователя.
    :return: Ответ JSON со статусом 200 и токеном в теле ответа в случае успешного прохождения аутентификации.
             UserNotExistError в случае отсутствия пользователя с таким именем.
             UserNotAllowedError в случае если пользователь с таким именем удалён или не верифицирован.
             PasswordIsNotCorrect в случае если пароль пользователя неверен.
    """
    token = await users_service.get_token(
        user_check=user_check,
    )
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"access_token": token, "token_type": "bearer"})


@router.post("/", response_model=UserDTO)
@endpoint_exceptions_processing
async def add_user(
        new_user: UserCreate,
) -> UserDTO:
    """
    Эндпоинт для добавления одного пользователя.
    :param new_user: Данные для создания нового пользователя в виде экземпляра UserCreate.
    :return: Экземпляр UserDTO, соответствующий новой созданному пользователю.
    """
    return await users_service.add_user(
        new_user=new_user,
    )
