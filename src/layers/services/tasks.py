"""
    Сервис для осуществления бизнес-логики работы с Task
"""
from uuid import UUID

from src.layers.utils import TransactionWorkerBase
from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import TaskCreate, TaskDTO, TaskUpdate, TaskUpdatePartial


class TaskService:
    transaction_worker: TransactionWorkerBase
    
    @staticmethod
    async def get_tasks(transaction_worker: TransactionWorkerBase) -> list[TaskDTO]:
        """Запрос всех задач из БД и сопутствующие действия"""
        async with transaction_worker:
            res = await transaction_worker.tasks.get_all()
            all_tasks = [TaskDTO.model_validate(task) for task in res]

        return all_tasks
    
    @staticmethod
    async def get_task_by_id(task_id: UUID,
                             transaction_worker: TransactionWorkerBase) -> TaskDTO:
        """Запрос одной задачи по id из БД и сопутствующие действия"""
        async with transaction_worker:
            res = await transaction_worker.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type='task', parameter='id')
            res = res[0]
            task = TaskDTO.model_validate(res)

        return task
    
    @staticmethod
    async def add_task(task: TaskCreate,
                       transaction_worker: TransactionWorkerBase) -> TaskDTO:
        """Добавление задачи в БД и сопутствующие действия"""
        async with transaction_worker:
            task_dict = task.model_dump()
            res = await transaction_worker.tasks.add_one(data=task_dict)
            task = TaskDTO.model_validate(res)
            await transaction_worker.commit()

        return task

    @staticmethod
    async def delete_task_by_id(task_id: UUID,
                                transaction_worker: TransactionWorkerBase) -> None:
        """Удаление одной задачи по id из БД и сопутствующие действия"""
        async with transaction_worker:
            res = await transaction_worker.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type='task', parameter='id')
            entity = res[0]
            await transaction_worker.tasks.delete_one_entity(entity=entity)
            await transaction_worker.commit()

    @staticmethod
    async def update_task_by_id(task_id: UUID,
                                updated_task: TaskUpdate | TaskUpdatePartial,
                                transaction_worker: TransactionWorkerBase) -> TaskDTO:
        """Частичное или полное изменение одной задачи по id из БД и сопутствующие действия"""
        async with transaction_worker:
            res = await transaction_worker.tasks.get_by_params(id=task_id)
            if not res:
                raise ObjectNotFoundError(object_type='task', parameter='id')
            entity = res[0]
            task_dict = updated_task.model_dump(exclude_unset=True, exclude_none=True)
            res = await transaction_worker.tasks.update_one_entity(entity=entity, data=task_dict)
            task = TaskDTO.model_validate(res)
            await transaction_worker.commit()

        return task
