"""
    Роутер для взаимодействия с User
"""
from uuid import UUID

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.project.exceptions import exceptions_processing
from src.core.schemas import UserCreate, UserDTO, UserCheck
from src.core.dependencies import get_proxy_access_repositories, get_current_user_having_role, get_current_user
from src.layers.services import UserService
from src.layers.utils import IProxyAccessRepositories

router = APIRouter(prefix="/users",
                   tags=["Users", ])


@router.post("/token")
@exceptions_processing
async def token(
        user_check: UserCheck,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> JSONResponse:
    """Эндпоинт для получения токена по имени и паролю"""
    token = await UserService.get_token(
        proxy_access_repositories=proxy_access_repositories,
        user_check=user_check,
    )
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"access_token": token, "token_type": "bearer"})


@router.get("/", response_model=list[UserDTO])
@exceptions_processing
async def get_users(
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories)
) -> list[UserDTO]:
    """Эндпоинт для запроса списка всех пользователей"""
    return await UserService.get_users(
        proxy_access_repositories=proxy_access_repositories,
    )


@router.get("/me", response_model=UserDTO)
@exceptions_processing
async def get_me(
        current_user: UserDTO = Depends(get_current_user),
) -> UserDTO:
    """Эндпоинт для возвращения данных актуального пользователя"""
    return current_user


@router.get("/{user_id}", response_model=UserDTO)
@exceptions_processing
async def get_user_by_id(
        user_id: UUID,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories)
) -> UserDTO:
    """Эндпоинт для запроса одной задачи по id"""
    return await UserService.get_user_by_id(
        proxy_access_repositories=proxy_access_repositories,
        user_id=user_id,
    )


@router.post("/", response_model=UserDTO)
@exceptions_processing
async def add_user(
        new_user: UserCreate,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories)
) -> UserDTO:
    """Эндпоинт для добавления одного пользователя."""
    return await UserService.add_user(
        proxy_access_repositories=proxy_access_repositories,
        new_user=new_user,
    )


@router.delete("/{user_id}")
@exceptions_processing
async def delete_user_by_id(
        user_id: UUID,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> JSONResponse:
    """Эндпоинт для удаления одного пользователя по id"""
    await UserService.delete_user_by_id(
        proxy_access_repositories=proxy_access_repositories,
        user_id=user_id,
    )
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'detail': f'Task with id={user_id} is successfully deleted'})


# @router.put("/{task_id}", response_model=TaskDTO)
# async def put_task_by_id(task_id: int, task: TaskUpdate,
#                          uow: UnitOfWorkBase = Depends(get_actual_uow)) -> TaskDTO:
#     """Эндпоинт для полного изменения одной задачи по id"""
#     try:
#         return await TaskService.update_task_by_id(task_id, task, uow=uow)
#     except ObjectNotFoundError as _ex:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{_ex.object_type} with this {_ex.parameter} is not found in database")
#     except Exception as _ex:
#         print(_ex)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Unknown internal server error")
#
#
# @router.patch("/{task_id}", response_model=TaskDTO)
# async def patch_task_by_id(task_id: int, task: TaskUpdatePartial,
#                            uow: UnitOfWorkBase = Depends(get_actual_uow)) -> TaskDTO:
#     """Эндпоинт для частичного изменения одной задачи по id"""
#     try:
#         return await TaskService.update_task_by_id(task_id, task, uow=uow)
#     except ObjectNotFoundError as _ex:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"{_ex.object_type} with this {_ex.parameter} is not found in database")
#     except Exception as _ex:
#         print(_ex)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Unknown internal server error")
