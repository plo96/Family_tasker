"""
    Сервис для осуществления бизнес-логики работы с сущностью пользователей.
"""

from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from src.auth.jwt import pwd_context, create_jwt_token
from src.core.models.users import Roles, User
from src.layers.utils.proxy_access_repositories import IProxyAccessRepositories
from src.layers.utils.background_tasker import IBackgroundTasker
from src.project.exceptions import (
    ObjectNotFoundError,
    PasswordIsNotCorrect,
    UserNotAllowedError,
    UserNotExistError,
)
from src.core.schemas import UserCreate, UserDTO, UserUpdatePartial


class UsersService:

    def __init__(
        self,
        proxy_access_repositories: IProxyAccessRepositories,
        background_tasker: IBackgroundTasker,
    ):
        self._proxy_access_repositories = proxy_access_repositories
        self._background_tasker = background_tasker

    async def get_token(
        self,
        user_check: OAuth2PasswordRequestForm,
    ) -> str:
        """
        Проверка данных пользователя и выдача токена в случае прохождения аутентификации.
        :param user_check: Экземпляр OAuth2PasswordRequestForm, содержащий имя и пароль пользователя.
        :return: Токен для авторизации данного пользователя.
        """
        async with self._proxy_access_repositories as repositories:
            res: list[User] = await repositories.users.get_by_params(
                username=user_check.username
            )
            if not res:
                raise UserNotExistError
            user_model = res[0]
            user = UserDTO.model_validate(user_model, from_attributes=True)

        if user.is_deleted or not user.is_verified:
            raise UserNotAllowedError

        is_password_correct = pwd_context.verify(
            user_check.password, user.hashed_password
        )
        if not is_password_correct:
            raise PasswordIsNotCorrect

        token = create_jwt_token({"id": str(user.id)})
        return token

    async def get_users(
        self,
    ) -> list[UserDTO]:
        """Запрос всех пользователей из БД и сопутствующие действия."""
        async with self._proxy_access_repositories as repositories:
            res = await repositories.users.get_all()
            all_users = [UserDTO.model_validate(user) for user in res]
            all_active_users = list(
                filter(lambda user: not getattr(user, "is_deleted"), all_users)
            )
        return all_active_users

    async def get_user_by_id(
        self,
        user_id: UUID,
    ) -> UserDTO:
        """Запрос одного пользователя по id из БД и сопутствующие действия."""
        async with self._proxy_access_repositories as repositories:
            res = await repositories.users.get_by_params(id=user_id, is_deleted=False)
            if not res:
                raise ObjectNotFoundError
            res = res[0]
            user = UserDTO.model_validate(res)
        return user

    async def add_user(
        self,
        new_user: UserCreate,
    ) -> UserDTO:
        """Добавление пользователя в БД, хеширование пароля, отправка задачи по отправке сообщения верификации."""
        new_user.password = pwd_context.hash(new_user.password)
        user_dict = new_user.model_dump()
        user_dict["hashed_password"] = user_dict.pop("password")
        user_dict["role"] = Roles.user

        async with self._proxy_access_repositories as repositories:
            res = await repositories.users.add_one(data=user_dict)
            new_user = UserDTO.model_validate(res)
            await repositories.commit()

        self._background_tasker.send_verify_email_message(user=new_user)

        return new_user

    async def add_admin_user(
        self,
        new_user: UserCreate,
    ) -> UserDTO:
        """Добавление пользователя в БД, хеширование пароля, отправка задачи по отправке сообщения верификации."""
        new_user.password = pwd_context.hash(new_user.password)
        user_dict = new_user.model_dump()
        user_dict["hashed_password"] = user_dict.pop("password")
        user_dict["role"] = Roles.admin
        user_dict["is_verified"] = True

        async with self._proxy_access_repositories as repositories:
            res = await repositories.users.add_one(data=user_dict)
            new_user = UserDTO.model_validate(res)
            await repositories.commit()

        return new_user

    async def delete_user_by_id(
        self,
        user_id: UUID,
    ) -> None:
        """Установление для пользователя статуса "удалён" по id из БД и сопутствующие действия."""
        async with self._proxy_access_repositories as repositories:
            res = await repositories.users.get_by_params(id=user_id)
            if not res:
                raise ObjectNotFoundError(object_type="user", parameter="id")
            entity = res[0]
            await repositories.users.update_one_entity(
                entity=entity, data={"is_deleted": True}
            )
            await repositories.commit()

    async def update_user_by_id(
        self,
        user_id: UUID,
        user_changing: UserUpdatePartial,
    ) -> UserDTO:
        """Частичное или полное изменение одного пользователя по id из БД и сопутствующие действия."""
        async with self._proxy_access_repositories as repositories:
            res = await repositories.users.get_by_params(id=user_id)
            if not res:
                raise ObjectNotFoundError(object_type="user", parameter="id")
            entity = res[0]
            user_dict = user_changing.model_dump(exclude_unset=True, exclude_none=True)
            res = await repositories.users.update_one_entity(
                entity=entity, data=user_dict
            )
            user = UserDTO.model_validate(res)
            await repositories.commit()
        return user
