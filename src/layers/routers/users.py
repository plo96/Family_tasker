"""
    Роутер для взаимодействия с User
"""
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.project.exceptions import ObjectNotFoundError, PasswordIsNotCorrect
from src.core.schemas import UserCreate, UserDTO, UserCheck
from src.core.dependencies import get_actual_uow
from src.layers.services import UserService
from src.layers.utils import UnitOfWorkBase

router = APIRouter(prefix="/users",
                   tags=["Users", ])


@router.post("/token", response_model=JSONResponse)
async def token(
        user_check: UserCheck,
        uow: UnitOfWorkBase = Depends(get_actual_uow),
) -> JSONResponse:
    """Эндпоинт для получения токена по имени и паролю"""
    try:
        token = await UserService.get_token(uow=uow, user_check=user_check)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"access_token": token, "token_type": "bearer"})
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with this name is not found in database")
    except PasswordIsNotCorrect:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST_NOT_FOUND,
                            detail="Uncorrected password")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.get("/", response_model=list[UserDTO])
async def get_users(
        uow: UnitOfWorkBase = Depends(get_actual_uow)
) -> list[UserDTO]:
    """Эндпоинт для запроса списка всех пользователей"""
    try:
        return await UserService.get_users(uow=uow)
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.get("/{user_id}", response_model=UserDTO)
async def get_user_by_id(
        user_id: UUID,
        uow: UnitOfWorkBase = Depends(get_actual_uow)
) -> UserDTO:
    """Эндпоинт для запроса одной задачи по id"""
    try:
        return await UserService.get_user_by_id(user_id, uow=uow)
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.post("/", response_model=UserDTO)
async def add_task(
        new_user: UserCreate,
        uow: UnitOfWorkBase = Depends(get_actual_uow)
) -> UserDTO:
    """Эндпоинт для добавления одной задачи"""
    try:
        return await UserService.add_user(new_user, uow=uow)
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.delete("/{user_id}")
async def delete_user_by_id(
        user_id: UUID,
        uow: UnitOfWorkBase = Depends(get_actual_uow)
) -> JSONResponse:
    """Эндпоинт для удаления одной задачи по id"""
    try:
        await UserService.delete_user_by_id(user_id, uow=uow)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'detail': f'Task with id={user_id} is successfully deleted'})
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


# @router.put("/{task_id}", response_model=TaskDTO)
# async def put_task_by_id(task_id: int, task: TaskUpdate,
#                          uow: UnitOfWorkBase = Depends(get_actual_uow)) -> TaskDTO:
#     """Эндпоинт для полного изменения одной задачи по id"""
#     try:
#         return await TaskService.update_task_by_id(task_id, task, uow=uow)
#     except ObjectNotFoundError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Object with this id is not found in database")
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
#     except ObjectNotFoundError:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Object with this id is not found in database")
#     except Exception as _ex:
#         print(_ex)
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail="Unknown internal server error")
