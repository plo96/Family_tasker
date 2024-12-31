"""
	Реализация для класса, исполняющего фоновые задачи.
"""

from email.message import EmailMessage

from .i_background_tasker import IBackgroundTasker
from .tasks import send_message
from src.core.schemas import UserDTO


class BackgroundTasker(IBackgroundTasker):

    def __init__(
        self,
        email_stmp_user: str,
    ):
        self._email_stmp_user = email_stmp_user

    def send_verify_email_message(
        self,
        user: UserDTO,
    ) -> None:
        """
        Добавление в очередь задачи по отправке верифицирующего email сообщения.
        :param user: Экземпляр класса UserDTO пользователя, которому отправляется сообщение.
        """
        verify_email = self.create_personal_verify_email_message(user=user)
        send_message.delay(email=verify_email)

    def create_personal_verify_email_message(
        self,
        user: UserDTO,
    ) -> EmailMessage:
        """Создание индивидуального email сообщения для верификации пользователя."""
        email = EmailMessage()
        email["Subject"] = "Подтверждение регистрации в приложении Family Tasker."
        email["From"] = self._email_stmp_user
        email["To"] = user.email

        email.set_content(self.get_verify_email_content(user=user))

        return email

    @staticmethod
    def get_verify_email_content(
        user: UserDTO,
    ) -> str:
        """Возвращает текст индивидуального email сообщения для верификации пользователя."""
        return f"""
				Привет, {user.name}!
				Вы пытались зарегистрироваться в приложении Family Tasker, используя данный адрес электронной почты.
				Для подтверждения регистрации пройдите по ссылке:
				
				Если вы не пытались зарегистрироваться в данном приложении, проигнорируйте это сообщение.
				"""
