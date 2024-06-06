"""
    Роутер для взаимодействия с сущностю задач (для админа).
"""
from uuid import UUID
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from src.project.exceptions import endpoint_exceptions_processing
from src.core.schemas import TaskDTO, UserDTO
from src.core.dependencies import get_current_user_having_role
from src.layers.services import tasks_service


router = APIRouter(tags=["Tasks", "Admin"])


@router.get("/", response_model=list[TaskDTO])
@endpoint_exceptions_processing
async def get_tasks(
		current_user: UserDTO = Depends(get_current_user_having_role('admin')),
) -> list[TaskDTO]:
    """Эндпоинт для запроса списка всех задач в БД."""
    return await tasks_service.get_tasks()


@router.delete("/{task_id}")
@endpoint_exceptions_processing
async def delete_task_by_id(
		task_id: UUID,
		current_user: UserDTO = Depends(get_current_user_having_role('admin')),
) -> JSONResponse:
    """
    Эндпоинт для удаления одной задачи по id.
    :param task_id: id задачи, которую нужно удалить.
    :return: Ответ JSON со статусом 200 в случае успешного удаления.
             ObjectNotFoundError в случае отсутствия задачи с таким id в БД.
    """
    await tasks_service.delete_task_by_id(task_id=task_id)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'detail': f'Task with id={task_id} is successfully deleted'})
