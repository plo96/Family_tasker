"""
    Роутер для взаимодействия с Task
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import TaskDTO, TaskCreate, TaskUpdate, TaskUpdatePartial
from src.services import TaskService


router = APIRouter(prefix="/tasks",
                   tags=["Tasks",])


@router.get("/", response_model=list[TaskDTO])
async def get_tasks():
    return await TaskService.get_tasks()


@router.get("/{task_id}", response_model=TaskDTO)
async def get_task_from_id(task_id: int):
    try:
        return await TaskService.get_task_by_id(task_id)
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.post("/", response_model=TaskDTO)
async def add_task(new_task: TaskCreate):
    return await TaskService.add_task(new_task)


@router.delete("/{task_id}")
async def delete_task_from_id(task_id: int) -> JSONResponse:
    try:
        await TaskService.delete_task_by_id(task_id)
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
async def put_task_from_id(task_id: int, task: TaskUpdate):
    try:
        return await TaskService.update_task_by_id(task_id, task)
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


@router.patch("/{task_id}", response_model=TaskDTO)
async def patch_task_from_id(task_id: int, task: TaskUpdatePartial):
    try:
        return await TaskService.update_task_by_id(task_id, task)
    except ObjectNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Object with this id is not found in database")
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")


