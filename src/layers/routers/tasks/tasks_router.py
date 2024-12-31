"""
    Роутер для взаимодействия с сущностю задач (для пользователей).
"""

from uuid import UUID
from fastapi import APIRouter, Depends

from src.core.dependencies import get_current_user_having_role
from src.project.exceptions import endpoint_exceptions_processing
from src.core.schemas import TaskDTO, TaskCreate, TaskUpdate, TaskUpdatePartial
from src.layers.services import tasks_service


router = APIRouter(
    tags=["Tasks AllUsers"],
    # dependencies=[Depends(get_current_user_having_role('user')), ],
)


@router.get("/{task_id}", response_model=TaskDTO)
@endpoint_exceptions_processing
async def get_task_by_id(
    task_id: UUID,
) -> TaskDTO:
    """
    Эндпоинт для запроса одной задачи по id.
    :param task_id: id запрашиваемой задачи.
    :return: Экзмепляр TaskDTO если задача с таким id найдена.
             ObjectNotFoundError в случае если задача не найдена.
    """
    return await tasks_service.get_task_by_id(task_id=task_id)


@router.post("/", response_model=TaskDTO)
@endpoint_exceptions_processing
async def add_task(
    new_task: TaskCreate,
) -> TaskDTO:
    """
    Эндпоинт для добавления одной задачи."
    :param new_task: Данные для создания новой задачи в виде экземпляра TaskCreate.
    :return: Экземпляр TaskDTO, соответствующий новой созданной задаче.
    """ ""
    return await tasks_service.add_task(new_task=new_task)


@router.put("/{task_id}", response_model=TaskDTO)
@endpoint_exceptions_processing
async def put_task_by_id(
    task_id: UUID,
    task_changing: TaskUpdate,
) -> TaskDTO:
    """
    Эндпоинт для полного изменения одной задачи по id.
    :param task_id: id изменяемой задачи.
    :param task: Экземпляр TaskUpdate с данными для изменения задачи.
    :return: Экземпляр TaskDTO, соответствующий изменённой задаче.
             ObjectNotFoundError в случае отсутствия задачи с таким id в БД.
    """
    return await tasks_service.update_task_by_id(
        task_id=task_id,
        task_changing=task_changing,
    )


@router.patch("/{task_id}", response_model=TaskDTO)
@endpoint_exceptions_processing
async def patch_task_by_id(
    task_id: UUID,
    task_changing: TaskUpdatePartial,
) -> TaskDTO:
    """
    Эндпоинт для частичного изменения одной задачи по id.
    :param task_id: id частично изменяемой задачи.
    :param task: Экземпляр TaskUpdatePartial с данными для частичного изменения задачи.
    :return: Экземпляр TaskDTO, соответствующий изменённой задаче.
             ObjectNotFoundError в случае отсутствия задачи с таким id в БД.
    """
    return await tasks_service.update_task_by_id(
        task_id=task_id,
        task_changing=task_changing,
    )
