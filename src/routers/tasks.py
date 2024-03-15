from fastapi import APIRouter, HTTPException, status

from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import TaskDTO, TaskCreate
from src.services import TaskService


router = APIRouter(prefix="/tasks")


@router.post("/")
async def add_task(new_task: TaskCreate) -> TaskDTO:
    return await TaskService.add_task(new_task)


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

@router.delete("/{task_id}", response_model=str)
async def get_task_from_id(task_id: int):
    try:
        return await TaskService.delete_task_by_id(task_id)
    
    except Exception as _ex:
        print(_ex)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unknown internal server error")
