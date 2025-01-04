"""
    Вспомогательный класс DatabaseHelper для установления соединения с базой данных
    и выдачи сессии (на основе SQLAlchemy)
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.project.config import settings


class DatabaseHelper:
    """Класс, обеспечивающий подключение к базе данных с определёнными настройками"""

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

    def get_session_factory(self) -> async_sessionmaker:
        """Возвращает фабрику сессий для подключения к БД"""
        return self._session_factory


db_helper = DatabaseHelper(
    url=settings.DATABASE_URL_ASYNC_SQLITE, echo=settings.ECHO
)  # type: ignore


def get_actual_session_factory() -> async_sessionmaker:
    return db_helper.get_session_factory()
