"""
    Сервис для осуществления бизнес-логики работы с User
"""
from uuid import UUID

from src.utils import UnitOfWorkBase
from src.project.exceptions import ObjectNotFoundError
from src.core.schemas import UserCreate, UserDTO, UserUpdate, UserUpdatePartial


class UserService:
	uow: UnitOfWorkBase
	
	@staticmethod
	async def get_users(uow: UnitOfWorkBase) -> list[UserDTO]:
		"""Запрос всех пользователей из БД и сопутствующие действия"""
		async with uow:
			res = await uow.users.get_all()
			all_users = [
				UserDTO.model_validate(user)
				for user in res
			]
			all_active_users = list(filter(lambda user: getattr(user, 'is_deleted'), all_users))
		return all_active_users
	
	@staticmethod
	async def get_user_by_id(user_id: UUID,
							 uow: UnitOfWorkBase) -> UserDTO:
		"""Запрос одного пользователя по id из БД и сопутствующие действия"""
		async with uow:
			res = await uow.users.get_by_params(id=user_id, is_deleted=False)
			if not res:
				raise ObjectNotFoundError
			res = res[0]
			user = UserDTO.model_validate(res)
		return user
	
	@staticmethod
	async def add_user(user: UserCreate,
					   uow: UnitOfWorkBase) -> UserDTO:
		"""Добавление пользователя в БД и сопутствующие действия"""
		async with uow:
			user_dict = user.model_dump()
			res = await uow.users.add_one(data=user_dict)
			user = UserDTO.model_validate(res)
			await uow.commit()
		return user
	
	@staticmethod
	async def delete_user_by_id(user_id: UUID,
								uow: UnitOfWorkBase) -> None:
		"""Установление для пользователя статуса "удалён" по id из БД и сопутствующие действия"""
		async with uow:
			res = await uow.tasks.get_by_params(id=user_id)
			if not res:
				raise ObjectNotFoundError
			entity = res[0]
			await uow.users.update_one(entity=entity, data={'is_deleted': True})
			await uow.commit()
#
# @staticmethod
# async def update_task_by_id(task_id: UUID,
# 							updated_task: TaskUpdate | TaskUpdatePartial,
# 							uow: UnitOfWorkBase) -> TaskDTO:
# 	"""Частичное или полное изменение одной задачи по id из БД и сопутствующие действия"""
# 	async with uow:
# 		res = await uow.tasks.get_by_params(id=task_id)
# 		if not res:
# 			raise ObjectNotFoundError
# 		entity = res[0]
# 		task_dict = updated_task.model_dump(exclude_unset=True, exclude_none=True)
# 		res = await uow.tasks.update_one(entity=entity, data=task_dict)
# 		task = TaskDTO.model_validate(res)
# 		await uow.commit()
#
# 	return task
