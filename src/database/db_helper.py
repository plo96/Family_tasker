"""
    Вспомогательный класс DatabaseHelper для установления соединения с базой данных
    и выдачи сессии (на основе SQLAlchemy)
"""
from sqlalchemy.ext.asyncio import async_scoped_session, create_async_engine, async_sessionmaker
from asyncio import current_task

from src.project.config import settings


class DatabaseHelper:
	def __init__(self, url: str, echo: str):
		self._engine = create_async_engine(
			url=url,
			echo=echo,
			# pool_size=5,
			# max_overflow=10
		)
		
		self._session_factory = async_sessionmaker(
			bind=self._engine,
			autoflush=False,
			autocommit=False,
			expire_on_commit=False,
		)
		
		self._scoped_session_factory = async_scoped_session(
			session_factory=self._session_factory,
			scopefunc=current_task,
		)
	
	def get_session_factory(self) -> async_sessionmaker:
		return self._session_factory
	
	def get_scoped_session_factory(self) -> async_scoped_session:
		return self._scoped_session_factory


db_helper = DatabaseHelper(url=settings.DATABASE_URL_async_sqlite,
						   echo=settings.ECHO)  # type: ignore
