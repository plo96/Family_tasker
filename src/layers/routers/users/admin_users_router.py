"""
    Роутер для взаимодействия с сущностью пользователей (для админов).
"""

from uuid import UUID

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.core.dependencies import get_current_user_having_role
from src.project.exceptions import endpoint_exceptions_processing
from src.core.schemas import UserDTO, UserUpdatePartial, UserCreate
from src.layers.services import users_service

router = APIRouter(
    tags=["Users Admin"],
)


@router.post("/add_adm/", response_model=UserDTO)
@endpoint_exceptions_processing
async def add_admin_user(
    new_user: UserCreate,
) -> UserDTO:
    """
    Эндпоинт для добавления одного пользователя-админа.
    :param new_user: Данные для создания нового пользователя в виде экземпляра UserCreate.
    :return: Экземпляр UserDTO, соответствующий новой созданному пользователю.
    """
    return await users_service.add_admin_user(
        new_user=new_user,
    )


@router.get("/", response_model=list[UserDTO])
@endpoint_exceptions_processing
async def get_users(
    current_user: UserDTO = Depends(get_current_user_having_role("admin")),
) -> list[UserDTO]:
    """Эндпоинт для запроса списка всех пользователей."""
    return await users_service.get_users()


@router.get("/{user_id}", response_model=UserDTO)
@endpoint_exceptions_processing
async def get_user_by_id(
    user_id: UUID,
    current_user: UserDTO = Depends(get_current_user_having_role("admin")),
) -> UserDTO:
    """
    Эндпоинт для запроса одного пользователя по id.
    :param user_id: id запрашиваемого пользователя.
    :return: Экзмепляр UserDTO если пользователь с таким id найден.
             ObjectNotFoundError в случае если пользователь не найден.
    """
    return await users_service.get_user_by_id(
        user_id=user_id,
    )


@router.delete("/{user_id}")
@endpoint_exceptions_processing
async def delete_user_by_id(
    user_id: UUID,
    current_user: UserDTO = Depends(get_current_user_having_role("admin")),
) -> JSONResponse:
    """
    Эндпоинт для удаления одного пользователя по id.
    :param user_id: id пользователя, которого нужно удалить.
    :return: Ответ JSON со статусом 200 в случае успешного удаления.
             ObjectNotFoundError в случае отсутствия пользователя с таким id в БД.
    """
    await users_service.delete_user_by_id(
        user_id=user_id,
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": f"User with id={user_id} is successfully deleted"},
    )


@router.patch("/{user_id}", response_model=UserDTO)
@endpoint_exceptions_processing
async def patch_user_by_id(
    user_id: UUID,
    user_changing: UserUpdatePartial,
    current_user: UserDTO = Depends(get_current_user_having_role("admin")),
) -> UserDTO:
    """
    Эндпоинт для частичного изменения данных одного пользователя по id.
    :param user_id: id пользователя, данные которого нужно изменить.
    :param user_changing: Экземпляр UserUpdatePartial с данными для частичного изменения пользователя.
    :return: Экземпляр UserDTO, соответствующий изменённому пользователю.
             ObjectNotFoundError в случае отсутствия пользователя с таким id в БД.
    """
    return await users_service.update_user_by_id(
        user_id=user_id,
        user_changing=user_changing,
    )
