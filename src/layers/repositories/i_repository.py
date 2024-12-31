"""
    Базовый интерфейс для работы с репозиториями
"""

from abc import ABC, abstractmethod


class IRepository(ABC):

    @abstractmethod
    async def add_one(self, data: dict):
        """Добавление одного объекта в БД через словарь со свойствами."""
        pass

    @abstractmethod
    async def get_all(self):
        """Получение всех объектов данного типа из БД."""
        pass

    @abstractmethod
    async def get_by_params(self, **kwargs):
        """Получение объектов данного типа с указанными параметрами."""
        pass

    @abstractmethod
    async def delete_one_entity(self, entity):
        """Удаление одной сущности, переданной в данный метод."""
        pass

    @abstractmethod
    async def update_one_entity(self, entity, data: dict):
        """Изменение одной сущности, переданной в данный метод.
        Устанавливаются значения параметров в соответствии с переданным словарём."""
        pass
