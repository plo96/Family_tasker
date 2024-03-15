from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """Абстрактный класс для работы с рапозиторием"""
    @abstractmethod
    async def add_one(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError
    
    
    @abstractmethod
    async def get_by_params(self, **kwargs):
        raise NotImplementedError

