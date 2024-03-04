from sqlalchemy.ext.asyncio import async_scoped_session, create_async_engine, async_sessionmaker, AsyncSession
from asyncio import current_task

from src.core.config import settings


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

    def session_factory(self):
        return self._session_factory

    def scoped_session_factory(self):
        return async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=current_task,
        )
    #
    # async def get_session(self) -> AsyncSession:
    #     session = async_scoped_session(
    #         session_factory=self.session_factory,
    #         scopefunc=current_task,
    #     )
    #     yield session
    #     await session.remove()


db_helper = DatabaseHelper(url=settings.DATABASE_URL_async_sqlite,
                           echo=settings.ECHO)

