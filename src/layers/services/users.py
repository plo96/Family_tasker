"""
    Сервис для осуществления бизнес-логики работы с User
"""
from uuid import UUID

from src.auth.security import pwd_context, create_jwt_token
from src.layers.utils import UnitOfWorkBase
from src.project.exceptions import ObjectNotFoundError, PasswordIsNotCorrect
from src.core.schemas import UserCreate, UserDTO, UserUpdatePartial, UserCheck


class UserService:
	uow: UnitOfWorkBase
	
	@staticmethod
	async def get_token(
			uow: UnitOfWorkBase,
			user_check: UserCheck
	) -> str:
		"""Проверка пользователя и выдача токена"""
		async with uow:
			res = await uow.users.get_by_params(name=user_check.name)
			if not res:
				raise ObjectNotFoundError(object_type='user', parameter='name')
			res = res[0]
			user = UserDTO.model_validate(res)
		
		is_password_correct = pwd_context.verify(user_check.password, user.hashed_password)
		if not is_password_correct:
			raise PasswordIsNotCorrect
		
		token = create_jwt_token({"id": user.id.__str__()})
		return token
	
	@staticmethod
	async def get_users(
			uow: UnitOfWorkBase
	) -> list[UserDTO]:
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
	async def get_user_by_id(
			user_id: UUID,
			uow: UnitOfWorkBase
	) -> UserDTO:
		"""Запрос одного пользователя по id из БД и сопутствующие действия"""
		async with uow:
			res = await uow.users.get_by_params(id=user_id, is_deleted=False)
			if not res:
				raise ObjectNotFoundError
			res = res[0]
			user = UserDTO.model_validate(res)
		return user
	
	@staticmethod
	async def add_user(
			user: UserCreate,
			uow: UnitOfWorkBase
	) -> UserDTO:
		"""Добавление пользователя в БД и сопутствующие действия"""
		async with uow:
			user.password = pwd_context.hash(user.password)
			user_dict = user.model_dump()
			user_dict["hashed_password"] = user_dict.pop("password")
			res = await uow.users.add_one(data=user_dict)
			user = UserDTO.model_validate(res)
			await uow.commit()
		return user
	
	@staticmethod
	async def delete_user_by_id(
			user_id: UUID,
			uow: UnitOfWorkBase
	) -> None:
		"""Установление для пользователя статуса "удалён" по id из БД и сопутствующие действия"""
		async with uow:
			res = await uow.users.get_by_params(id=user_id)
			if not res:
				raise ObjectNotFoundError(object_type='user', parameter='id')
			entity = res[0]
			await uow.users.update_one_entity(entity=entity, data={'is_deleted': True})
			await uow.commit()
	
	@staticmethod
	async def update_user_by_id(
			user_id: UUID,
			updated_user: UserUpdatePartial,
			uow: UnitOfWorkBase
	) -> UserDTO:
		"""Частичное или полное изменение одного пользователя по id из БД и сопутствующие действия"""
		async with uow:
			res = await uow.users.get_by_params(id=user_id)
			if not res:
				raise ObjectNotFoundError(object_type='user', parameter='id')
			entity = res[0]
			user_dict = updated_user.model_dump(exclude_unset=True, exclude_none=True)
			res = await uow.users.update_one_entity(entity=entity, data=user_dict)
			user = UserDTO.model_validate(res)
			await uow.commit()
		return user

