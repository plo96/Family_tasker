"""
    Настройки для прогона тестов
"""
from asyncio import current_task
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, async_scoped_session

from src.database import db_helper
from src.project import settings
from src.core.models import Base
from src.main import app

fake_engine = create_async_engine(url=settings.TEST_DATABASE_URL_async_sqlite, poolclass=NullPool)
fake_session_factory = async_sessionmaker(bind=fake_engine, autoflush=False, autocommit=False, expire_on_commit=False)
metadata = Base.metadata
metadata.bind = fake_engine


async def override_get_session() -> async_sessionmaker | async_scoped_session:
    return async_scoped_session(session_factory=fake_session_factory,
                                scopefunc=current_task)
    # return fake_session_factory

app.dependency_overrides[db_helper.get_scoped_session_factory] = override_get_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with fake_engine.begin() as conn:
        conn.run_sync(metadata.create_all)
    
    yield
    
    async with fake_engine.begin() as conn:
        conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session')
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        yield async_client


from src.core.schemas import TaskCreate

# async def test_add_task(async_client: AsyncClient):
# 	new_task = TaskCreate(name='new_task_1', description='new_test_task_1', price=5)
# 	result = async_client.post('/tasks/', json=new_task.model_dump())
# 	print(result)

