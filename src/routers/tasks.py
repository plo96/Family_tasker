"""
    Роутер для взаимодействия с Task
"""
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import TaskDTO, TaskCreate, TaskUpdate, TaskUpdatePartial
from src.core.dependencies import get_actual_uow
from src.services import TaskService
from src.utils import UnitOfWorkBase


router = APIRouter(prefix="/tasks",
                   tags=["Tasks",])


@router.get("/", response_model=list[TaskDTO])
async def get_tasks(uow: UnitOfWorkBase = Depends(get_actual_uow)) -> list[TaskDTO]:
    """Эндпоинт для запроса списка всех задач"""
    return await TaskService.get_tasks(uow=uow)


@router.get("/{task_id}", response_model=TaskDTO)
async def get_task_by_id(task_id: int,
                         uow: UnitOfWorkBase = Depends(get_actual_uow)) -> TaskDTO:
    """Эндпоинт для запроса одной задачи по id"""
    try:
        return await TaskService.get_task_by_id(task_id, uow=uow)
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.post("/", response_model=TaskDTO)
async def add_task(new_task: TaskCreate,
                   uow: UnitOfWorkBase = Depends(get_actual_uow)) -> TaskDTO:
    """Эндпоинт для добавления одной задачи"""
    return await TaskService.add_task(new_task, uow=uow)


@router.delete("/{task_id}")
async def delete_task_by_id(task_id: int,
                            uow: UnitOfWorkBase = Depends(get_actual_uow)) -> JSONResponse:
    """Эндпоинт для удаления одной задачи по id"""
    try:
        await TaskService.delete_task_by_id(task_id, uow=uow)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'detail': f'Task with id={task_id} is successfully deleted'})
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.put("/{task_id}", response_model=TaskDTO)
async def put_task_by_id(task_id: int, task: TaskUpdate,
                         uow: UnitOfWorkBase = Depends(get_actual_uow)) -> TaskDTO:
    """Эндпоинт для полного изменения одной задачи по id"""
    try:
        return await TaskService.update_task_by_id(task_id, task, uow=uow)
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.patch("/{task_id}", response_model=TaskDTO)
async def patch_task_by_id(task_id: int, task: TaskUpdatePartial,
                           uow: UnitOfWorkBase = Depends(get_actual_uow)) -> TaskDTO:
    """Эндпоинт для частичного изменения одной задачи по id"""
    try:
        return await TaskService.update_task_by_id(task_id, task, uow=uow)
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")
