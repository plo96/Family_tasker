"""
	Реализация для класса, исполняющего фоновые задачи.
"""

from email.message import EmailMessage

from . import IBackgroundTasker
from .i_background_tasker import IBackgroundTasker
from .tasks import send_message
from src.core.schemas import UserDTO


class BackgroundTasker(IBackgroundTasker):

    def send_verify_email_message(
        self,
        user: UserDTO,
    ) -> None:
        """
        Добавление в очередь задачи по отправке верифицирующего email сообщения.
        :param user: Экземпляр класса UserDTO пользователя, которому отправляется сообщение.
        """
        verify_email_text = self.get_verify_email_content(user=user)
        verify_email_subject = "Подтверждение регистрации в приложении Family Tasker."
        send_message.delay(
            msg_subject=verify_email_subject,
            msg_text=verify_email_text,
            send_to=user.email,
        )

    @staticmethod
    def get_verify_email_content(
        user: UserDTO,
    ) -> str:
        """Возвращает текст индивидуального email сообщения для верификации пользователя."""
        return f"""
				Привет, {user.username}!
				Вы пытались зарегистрироваться в приложении Family Tasker, используя данный адрес электронной почты.
				Для подтверждения регистрации пройдите по ссылке:
				
				Если вы не пытались зарегистрироваться в данном приложении, проигнорируйте это сообщение.
				"""


def get_background_tasker() -> IBackgroundTasker:
    """Возвращает актуальный экземпляр BackgroundTasker для осуществления задач в фоне."""
    return BackgroundTasker()
