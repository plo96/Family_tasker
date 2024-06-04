from abc import ABC, abstractmethod


class IBackgroundTasker(ABC):

	@abstractmethod
	def send_verify_message(self) -> None:
		"""Добавление задачи по отправке верифицирующего сообщения."""
		...
