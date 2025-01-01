"""
    Роутер для взаимодействия с сущностью пользователей (для пользователей).
"""

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from src.project.exceptions import endpoint_exceptions_processing
from src.core.schemas import UserCreate, UserDTO
from src.layers.services import users_service

router = APIRouter(
    tags=["Users AllUsers"],
)


@router.post("/token")
@endpoint_exceptions_processing
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> JSONResponse:
    """
    Эндпоинт для получения токена по имени и паролю.
    :param user_check: Экземпляр OAuth2PasswordRequestForm, содержащий имя и пароль пользователя.
    :return: Ответ JSON со статусом 200 и токеном в теле ответа в случае успешного прохождения аутентификации.
             UserNotExistError в случае отсутствия пользователя с таким именем.
             UserNotAllowedError в случае если пользователь с таким именем удалён или не верифицирован.
             PasswordIsNotCorrect в случае если пароль пользователя неверен.
    """
    token = await users_service.get_token(
        user_check=form_data,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"access_token": token, "token_type": "bearer"},
    )


@router.post("/add", response_model=UserDTO)
@endpoint_exceptions_processing
async def add_user(
    new_user: UserCreate,
) -> UserDTO:
    """
    Эндпоинт для регистрации одного пользователя.
    :param new_user: Данные для создания нового пользователя в виде экземпляра UserCreate.
    :return: Экземпляр UserDTO, соответствующий новой созданному пользователю.
    """
    return await users_service.add_user(
        new_user=new_user,
    )
