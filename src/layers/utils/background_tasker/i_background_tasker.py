"""
	Интерфейс для класса, исполняющего фоновые задачи.
"""

from abc import ABC, abstractmethod

from src.core.schemas import UserDTO


class IBackgroundTasker(ABC):

    @abstractmethod
    def send_verify_email_message(
        self,
        user: UserDTO,
    ) -> None:
        """Добавление задачи по отправке верифицирующего email сообщения."""
        ...
