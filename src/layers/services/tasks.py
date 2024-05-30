"""
    Сервис для осуществления бизнес-логики работы с Task
"""
from uuid import UUID

from src.layers.utils import IProxyAccessRepositories
from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import TaskCreate, TaskDTO, TaskUpdate, TaskUpdatePartial


class TaskService:
    proxy_access_repositories: IProxyAccessRepositories
    
    @staticmethod
    async def get_tasks(
            proxy_access_repositories: IProxyAccessRepositories,
    ) -> list[TaskDTO]:
        """Запрос всех задач из БД и сопутствующие действия"""
        async with proxy_access_repositories:
            res = await proxy_access_repositories.tasks.get_all()
            all_tasks = [TaskDTO.model_validate(task) for task in res]

        return all_tasks
    
    @staticmethod
    async def get_task_by_id(
            task_id: UUID,
            proxy_access_repositories: IProxyAccessRepositories,
    ) -> TaskDTO:
        """Запрос одной задачи по id из БД и сопутствующие действия"""
        async with proxy_access_repositories:
            res = await proxy_access_repositories.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type='task', parameter='id')
            res = res[0]
            task = TaskDTO.model_validate(res)

        return task
    
    @staticmethod
    async def add_task(
            task: TaskCreate,
            proxy_access_repositories: IProxyAccessRepositories,
    ) -> TaskDTO:
        """Добавление задачи в БД и сопутствующие действия"""
        async with proxy_access_repositories:
            task_dict = task.model_dump()
            res = await proxy_access_repositories.tasks.add_one(data=task_dict)
            task = TaskDTO.model_validate(res)
            await proxy_access_repositories.commit()

        return task

    @staticmethod
    async def delete_task_by_id(
            task_id: UUID,
            proxy_access_repositories: IProxyAccessRepositories,
    ) -> None:
        """Удаление одной задачи по id из БД и сопутствующие действия"""
        async with proxy_access_repositories:
            res = await proxy_access_repositories.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type='task', parameter='id')
            entity = res[0]
            await proxy_access_repositories.tasks.delete_one_entity(entity=entity)
            await proxy_access_repositories.commit()

    @staticmethod
    async def update_task_by_id(
            task_id: UUID,
            updated_task: TaskUpdate | TaskUpdatePartial,
            proxy_access_repositories: IProxyAccessRepositories,
    ) -> TaskDTO:
        """Частичное или полное изменение одной задачи по id из БД и сопутствующие действия"""
        async with proxy_access_repositories:
            res = await proxy_access_repositories.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type='task', parameter='id')
            entity = res[0]
            task_dict = updated_task.model_dump(exclude_unset=True, exclude_none=True)
            res = await proxy_access_repositories.tasks.update_one_entity(entity=entity, data=task_dict)
            task = TaskDTO.model_validate(res)
            await proxy_access_repositories.commit()

        return task
