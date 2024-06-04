"""
    Сервис для осуществления бизнес-логики работы с сущностью пользователей.
"""
from uuid import UUID

from src.auth.security import pwd_context, create_jwt_token
from src.layers.utils.proxy_access_repositories import IProxyAccessRepositories
from src.layers.utils.background_tasker import IBackgroundTasker
from src.project.exceptions import ObjectNotFoundError, PasswordIsNotCorrect, UserNotAllowedError, UserNotExistError
from src.core.schemas import UserCreate, UserDTO, UserUpdatePartial, UserCheck


class UserService:
	
	@staticmethod
	async def get_token(
			proxy_access_repositories: IProxyAccessRepositories,
			user_check: UserCheck,
	) -> str:
		"""
		Проверка данных пользователя и выдача токена в случае прохождения аутентификации.
		:param proxy_access_repositories: Единая точка доступа к репозиториям, передается через DI.
    	:param user_check: Экземпляр UserCheck, содержащий имя и пароль пользователя.
		:return: Токен для авторизации данного пользователя.
		"""
		async with proxy_access_repositories as repositories:
			res = await repositories.users.get_by_params(name=user_check.name)
			if not res:
				raise UserNotExistError
			res = res[0]
		user = UserDTO.model_validate(res)
		
		if user.is_deleted or not user.is_verified:
			raise UserNotAllowedError
		
		is_password_correct = pwd_context.verify(user_check.password, user.hashed_password)
		if not is_password_correct:
			raise PasswordIsNotCorrect
		
		token = create_jwt_token({"id": user.id.__str__()})
		return token
	
	@staticmethod
	async def get_users(
			proxy_access_repositories: IProxyAccessRepositories,
	) -> list[UserDTO]:
		"""Запрос всех пользователей из БД и сопутствующие действия."""
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
		"""Запрос одного пользователя по id из БД и сопутствующие действия."""
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
		"""Добавление пользователя в БД, хеширование пароля, отправка задачи по отправке сообщения верификации."""
		new_user.password = pwd_context.hash(new_user.password)
		user_dict = new_user.model_dump()
		user_dict["hashed_password"] = user_dict.pop("password")
		
		async with proxy_access_repositories as repositories:
			res = await repositories.users.add_one(data=user_dict)
			new_user = UserDTO.model_validate(res)
			await repositories.commit()
		
		# send_verify_message()
		
		return new_user
	
	@staticmethod
	async def delete_user_by_id(
			user_id: UUID,
			proxy_access_repositories: IProxyAccessRepositories
	) -> None:
		"""Установление для пользователя статуса "удалён" по id из БД и сопутствующие действия."""
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
			user_changing: UserUpdatePartial,
			proxy_access_repositories: IProxyAccessRepositories
	) -> UserDTO:
		"""Частичное или полное изменение одного пользователя по id из БД и сопутствующие действия."""
		async with proxy_access_repositories as repositories:
			res = await repositories.users.get_by_params(id=user_id)
			if not res:
				raise ObjectNotFoundError(object_type='user', parameter='id')
			entity = res[0]
			user_dict = user_changing.model_dump(exclude_unset=True, exclude_none=True)
			res = await repositories.users.update_one_entity(entity=entity, data=user_dict)
			user = UserDTO.model_validate(res)
			await repositories.commit()
		return user


# user_service = UserService(
# 	proxy_access_repositories:,
# )
