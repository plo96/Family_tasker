"""
    Роутер для взаимодействия с Task
"""
from uuid import UUID
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.project.exceptions import exceptions_processing
from src.core.schemas import TaskDTO, TaskCreate, TaskUpdate, TaskUpdatePartial
from src.core.dependencies import get_proxy_access_repositories
from src.layers.services import TaskService
from src.layers.utils import IProxyAccessRepositories


router = APIRouter(prefix="/tasks",
                   tags=["Tasks",])


@router.get("/", response_model=list[TaskDTO])
@exceptions_processing
async def get_tasks(
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> list[TaskDTO]:
    """Эндпоинт для запроса списка всех задач"""
    return await TaskService.get_tasks(proxy_access_repositories=proxy_access_repositories)


@router.get("/{task_id}", response_model=TaskDTO)
@exceptions_processing
async def get_task_by_id(
        task_id: UUID,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> TaskDTO:
    """Эндпоинт для запроса одной задачи по id"""
    return await TaskService.get_task_by_id(task_id, proxy_access_repositories=proxy_access_repositories)


@router.post("/", response_model=TaskDTO)
@exceptions_processing
async def add_task(
        new_task: TaskCreate,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> TaskDTO:
    """Эндпоинт для добавления одной задачи"""
    return await TaskService.add_task(new_task, proxy_access_repositories=proxy_access_repositories)


@router.delete("/{task_id}")
@exceptions_processing
async def delete_task_by_id(
        task_id: UUID,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> JSONResponse:
    """Эндпоинт для удаления одной задачи по id"""
    await TaskService.delete_task_by_id(task_id, proxy_access_repositories=proxy_access_repositories)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'detail': f'Task with id={task_id} is successfully deleted'})


@router.put("/{task_id}", response_model=TaskDTO)
@exceptions_processing
async def put_task_by_id(
        task_id: UUID,
        task: TaskUpdate,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> TaskDTO:
    """Эндпоинт для полного изменения одной задачи по id"""
    return await TaskService.update_task_by_id(task_id, task, proxy_access_repositories=proxy_access_repositories)


@router.patch("/{task_id}", response_model=TaskDTO)
@exceptions_processing
async def patch_task_by_id(
        task_id: UUID,
        task: TaskUpdatePartial,
        proxy_access_repositories: IProxyAccessRepositories = Depends(get_proxy_access_repositories),
) -> TaskDTO:
    """Эндпоинт для частичного изменения одной задачи по id"""
    return await TaskService.update_task_by_id(task_id, task, proxy_access_repositories=proxy_access_repositories)
