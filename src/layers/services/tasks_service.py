"""
    Сервис для осуществления бизнес-логики работы с сущностью задач.
"""

from uuid import UUID

from src.layers.utils.proxy_access_repositories import IProxyAccessRepositories
from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import TaskCreate, TaskDTO, TaskUpdate, TaskUpdatePartial


class TaskService:
    proxy_access_repositories: IProxyAccessRepositories

    def __init__(
        self,
        proxy_access_repositories: IProxyAccessRepositories,
    ):
        self.proxy_access_repositories = proxy_access_repositories

    async def get_tasks(
        self,
    ) -> list[TaskDTO]:
        """Запрос всех задач из БД."""
        async with self.proxy_access_repositories as repositories:
            res = await repositories.tasks.get_all()
            all_tasks = [TaskDTO.model_validate(task) for task in res]

        return all_tasks

    async def get_task_by_id(
        self,
        task_id: UUID,
    ) -> TaskDTO:
        """Запрос одной задачи по id из БД."""
        async with self.proxy_access_repositories as repositories:
            res = await repositories.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type="task", parameter="id")
            res = res[0]
            task = TaskDTO.model_validate(res)

        return task

    async def add_task(
        self,
        new_task: TaskCreate,
    ) -> TaskDTO:
        """Добавление задачи в БД и сопутствующие действия."""
        async with self.proxy_access_repositories as repositories:
            task_dict = new_task.model_dump()
            res = await repositories.tasks.add_one(data=task_dict)
            task = TaskDTO.model_validate(res)
            await repositories.commit()

        return task

    async def delete_task_by_id(
        self,
        task_id: UUID,
    ) -> None:
        """Удаление одной задачи по id из БД и сопутствующие действия."""
        async with self.proxy_access_repositories as repositories:
            res = await repositories.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type="task", parameter="id")
            entity = res[0]
            await repositories.tasks.delete_one_entity(entity=entity)
            await repositories.commit()

    async def update_task_by_id(
        self,
        task_id: UUID,
        task_changing: TaskUpdate | TaskUpdatePartial,
    ) -> TaskDTO:
        """Частичное или полное изменение одной задачи по id из БД и сопутствующие действия."""
        async with self.proxy_access_repositories as repositories:
            res = await repositories.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type="task", parameter="id")
            entity = res[0]
            task_dict = task_changing.model_dump(exclude_unset=True, exclude_none=True)
            res = await repositories.tasks.update_one_entity(
                entity=entity, data=task_dict
            )
            task = TaskDTO.model_validate(res)
            await repositories.commit()

        return task
