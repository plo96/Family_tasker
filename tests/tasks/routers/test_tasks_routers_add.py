from httpx import AsyncClient
from fastapi import status
from sqlalchemy import select

from src.core.models import Task
from src.core.schemas import TaskCreate
from tests.conftest import get_fake_session_factory


async def test_add_task(task_url: str, async_client: AsyncClient, new_task: TaskCreate):
    result = await async_client.post(task_url, json=new_task.model_dump())
    assert result.status_code == status.HTTP_200_OK
    assert all(i in result.json().items() for i in new_task.model_dump().items())
    # Проверка изменений в БД
    task_id = result.json()['id']
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        added_entity: Task = result.scalars().one()
    assert all(i in added_entity.__dict__.items() for i in new_task.model_dump().items())


async def test_add_task_bad_name(task_url: str, async_client: AsyncClient, new_task_bad_name: dict):
    result = await async_client.post(task_url, json=new_task_bad_name)
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # Проверка изменений в БД
    task_name = new_task_bad_name["name"]
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(name=task_name)
        result = await session.execute(stmt)
        added_entity: Task | None = result.scalars().one_or_none()
    assert added_entity is None


async def test_add_task_bad_description(task_url: str, async_client: AsyncClient, new_task_bad_description: dict):
    result = await async_client.post(task_url, json=new_task_bad_description)
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # Проверка изменений в БД
    task_name = new_task_bad_description["name"]
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(name=task_name)
        result = await session.execute(stmt)
        added_entity: Task | None = result.scalars().one_or_none()
    assert added_entity is None


async def test_add_task_bad_price_min(task_url: str, async_client: AsyncClient, new_task_bad_price_min: dict):
    result = await async_client.post(task_url, json=new_task_bad_price_min)
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # Проверка изменений в БД
    task_name = new_task_bad_price_min["name"]
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(name=task_name)
        result = await session.execute(stmt)
        added_entity: Task | None = result.scalars().one_or_none()
    assert added_entity is None


async def test_add_task_bad_price_max(task_url: str, async_client: AsyncClient, new_task_bad_price_max: dict):
    result = await async_client.post(task_url, json=new_task_bad_price_max)
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    # Проверка изменений в БД
    task_name = new_task_bad_price_max["name"]
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(name=task_name)
        result = await session.execute(stmt)
        added_entity: Task | None = result.scalars().one_or_none()
    assert added_entity is None
