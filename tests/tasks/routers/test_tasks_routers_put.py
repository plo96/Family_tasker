from random import choice
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select

from src.core.models import Task
from src.core.schemas import TaskCreate
from tests.conftest import get_fake_session_factory


@pytest.mark.usefixtures("some_data_added")
async def test_put_task_by_id(
    task_url: str, async_client: AsyncClient, all_tasks_ids: list, new_task: TaskCreate
):
    task_id = choice(all_tasks_ids)
    result = await async_client.put(
        url=task_url + f"{task_id}", json=new_task.model_dump()
    )
    assert result.status_code == status.HTTP_200_OK
    assert all(i in result.json().items() for i in new_task.model_dump().items())
    # Проверка изменений в БД
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        changed_entity: Task = result.scalars().one()
    assert all(
        i in changed_entity.__dict__.items() for i in new_task.model_dump().items()
    )


@pytest.mark.usefixtures("clear_database")
async def test_put_task_by_bad_id(
    task_url: str, async_client: AsyncClient, one_new_task: TaskCreate
):
    result = await async_client.put(
        url=task_url + str(uuid4()), json=one_new_task.model_dump()
    )
    assert result.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("some_data_added")
async def test_put_task_by_id_bad_name(
    task_url: str,
    async_client: AsyncClient,
    all_tasks_ids: list,
    new_task_bad_name: dict,
):
    task_id = choice(all_tasks_ids)
    # Изначальное значение сущности в БД
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    result = await async_client.put(url=task_url + f"{task_id}", json=new_task_bad_name)
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Проверка изменений в БД
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        end_entity: Task = result.scalars().one()
    begin_items_list = list(begin_entity.__dict__.items())
    end_items_list = list(end_entity.__dict__.items())
    assert begin_items_list[1:] == end_items_list[1:]


@pytest.mark.usefixtures("some_data_added")
async def test_put_task_by_id_bad_description(
    task_url: str,
    async_client: AsyncClient,
    all_tasks_ids: list,
    new_task_bad_description: dict,
):
    task_id = choice(all_tasks_ids)
    # Изначальное значение сущности в БД
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    result = await async_client.put(
        url=task_url + f"{task_id}", json=new_task_bad_description
    )
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Проверка изменений в БД
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        end_entity: Task = result.scalars().one()
    begin_items_list = list(begin_entity.__dict__.items())
    end_items_list = list(end_entity.__dict__.items())
    assert begin_items_list[1:] == end_items_list[1:]


@pytest.mark.usefixtures("some_data_added")
async def test_put_task_by_id_bad_price_min(
    task_url: str,
    async_client: AsyncClient,
    all_tasks_ids: list,
    new_task_bad_price_min: dict,
):
    task_id = choice(all_tasks_ids)
    # Изначальное значение сущности в БД
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    result = await async_client.put(
        url=task_url + f"{task_id}", json=new_task_bad_price_min
    )
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Проверка изменений в БД
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        end_entity: Task = result.scalars().one()
    begin_items_list = list(begin_entity.__dict__.items())
    end_items_list = list(end_entity.__dict__.items())
    assert begin_items_list[1:] == end_items_list[1:]


@pytest.mark.usefixtures("some_data_added")
async def test_put_task_by_id_bad_price_max(
    task_url: str,
    async_client: AsyncClient,
    all_tasks_ids: list,
    new_task_bad_price_max: dict,
):
    task_id = choice(all_tasks_ids)
    # Изначальное значение сущности в БД
    session_factory = get_fake_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    result = await async_client.put(
        url=task_url + f"{task_id}", json=new_task_bad_price_max
    )
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Проверка изменений в БД
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        end_entity: Task = result.scalars().one()
    begin_items_list = list(begin_entity.__dict__.items())
    end_items_list = list(end_entity.__dict__.items())
    assert begin_items_list[1:] == end_items_list[1:]
