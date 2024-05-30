"""
    Сервис для осуществления бизнес-логики работы с User
"""
from uuid import UUID

from src.auth.security import pwd_context, create_jwt_token
from src.layers.utils import IProxyAccessRepositories
from src.project.exceptions import ObjectNotFoundError, PasswordIsNotCorrect
from src.core.schemas import UserCreate, UserDTO, UserUpdatePartial, UserCheck


class UserService:
	
	@staticmethod
	async def get_token(
			proxy_access_repositories: IProxyAccessRepositories,
			user_check: UserCheck
	) -> str:
		"""Проверка пользователя и выдача токена"""
		async with proxy_access_repositories as repositories:
			res = await repositories.users.get_by_params(name=user_check.name)
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
			proxy_access_repositories: IProxyAccessRepositories
	) -> list[UserDTO]:
		"""Запрос всех пользователей из БД и сопутствующие действия"""
		async with proxy_access_repositories as repositories:
			res = await repositories.users.get_all()
			all_users = [
				UserDTO.model_validate(user)
				for user in res
			]
			all_active_users = list(filter(lambda user: getattr(user, 'is_deleted'), all_users))
		return all_active_users
	
	@staticmethod
	async def get_user_by_id(
			user_id: UUID,
			proxy_access_repositories: IProxyAccessRepositories
	) -> UserDTO:
		"""Запрос одного пользователя по id из БД и сопутствующие действия"""
		async with proxy_access_repositories as repositories:
			res = await repositories.users.get_by_params(id=user_id, is_deleted=False)
			if not res:
				raise ObjectNotFoundError
			res = res[0]
			user = UserDTO.model_validate(res)
		return user
	
	@staticmethod
	async def add_user(
			new_user: UserCreate,
			proxy_access_repositories: IProxyAccessRepositories
	) -> UserDTO:
		"""Добавление пользователя в БД и сопутствующие действия"""
		new_user.password = pwd_context.hash(new_user.password)
		user_dict = new_user.model_dump()
		user_dict["hashed_password"] = user_dict.pop("password")
		async with proxy_access_repositories as repositories:
			res = await repositories.users.add_one(data=user_dict)
			new_user = UserDTO.model_validate(res)
			await repositories.commit()
		return new_user
	
	@staticmethod
	async def delete_user_by_id(
			user_id: UUID,
			proxy_access_repositories: IProxyAccessRepositories
	) -> None:
		"""Установление для пользователя статуса "удалён" по id из БД и сопутствующие действия"""
		async with proxy_access_repositories as repositories:
			res = await repositories.users.get_by_params(id=user_id)
			if not res:
				raise ObjectNotFoundError(object_type='user', parameter='id')
			entity = res[0]
			await repositories.users.update_one_entity(entity=entity, data={'is_deleted': True})
			await repositories.commit()
	
	@staticmethod
	async def update_user_by_id(
			user_id: UUID,
			updated_user: UserUpdatePartial,
			proxy_access_repositories: IProxyAccessRepositories
	) -> UserDTO:
		"""Частичное или полное изменение одного пользователя по id из БД и сопутствующие действия"""
		async with proxy_access_repositories as repositories:
			res = await repositories.users.get_by_params(id=user_id)
			if not res:
				raise ObjectNotFoundError(object_type='user', parameter='id')
			entity = res[0]
			user_dict = updated_user.model_dump(exclude_unset=True, exclude_none=True)
			res = await repositories.users.update_one_entity(entity=entity, data=user_dict)
			user = UserDTO.model_validate(res)
			await repositories.commit()
		return user
