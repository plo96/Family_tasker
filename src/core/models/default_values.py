"""
	Ининциализация функций для получения значений по умолчанию в моделях
"""

from datetime import datetime, UTC

from uuid import uuid4, UUID


def get_current_time() -> datetime:
    """Функция для получения значения времени по умолчанию."""
    return datetime.now(UTC)


def get_uuid() -> UUID:
    """Функция для получения значения uuid по умолчанию."""
    return uuid4()
