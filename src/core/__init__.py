"""
    Ядро сревиса содержит:
    ОРМ-модели для описания взаимодействия с БД,
    Pydantic-схемы для передачи и валидации данных в различных слоях приложения,
    Зависимости для инъекций
"""

__all__ = (
    "models",
    "schemas",
    "dependencies",
)

from . import models
from . import schemas
from . import dependencies
