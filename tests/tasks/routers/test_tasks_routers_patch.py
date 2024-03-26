from random import choice, randint
import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select

from src.core.models import Task
from src.core.schemas import TaskCreate
from tests.conftest import get_actual_session_factory


def get_partial_dict(some_dict: dict) -> tuple[dict, list]:
    num_of_unused_keys = randint(0, len(some_dict))
    list_of_unused_keys = []
    for _ in range(num_of_unused_keys):
        unused_key = choice(list(some_dict.keys()))
        list_of_unused_keys.append(unused_key)
        some_dict.pop(unused_key)
    return some_dict, list_of_unused_keys


@pytest.mark.usefixtures("some_data_added")
async def test_patch_task_by_id(task_url: str, async_client: AsyncClient,
                                all_tasks_ids: list, new_task: TaskCreate):
    task_id = choice(all_tasks_ids)

    new_task_dict = new_task.model_dump()
    new_task_dict, list_of_unused_keys = get_partial_dict(new_task_dict)

    # Изначальное значение сущности в БД
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    # Запрос на изменение
    result = await async_client.patch(url=task_url + f'{task_id}', json=new_task_dict)
    assert result.status_code == status.HTTP_200_OK
    assert all(i in result.json().items() for i in new_task_dict.items())

    # Проверка изменений в БД
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        end_entity: Task = result.scalars().one()
    assert all(i in end_entity.__dict__.items() for i in new_task_dict.items())
    for unused_key in list_of_unused_keys:
        assert getattr(end_entity, unused_key) == getattr(begin_entity, unused_key)


@pytest.mark.usefixtures("clear_database")
async def test_patch_task_by_bad_id(task_url: str, async_client: AsyncClient,
                                    one_new_task: TaskCreate):
    new_task_dict = one_new_task.model_dump()
    new_task_dict, list_of_unused_keys = get_partial_dict(new_task_dict)
    result = await async_client.patch(url=task_url + '1', json=new_task_dict)
    assert result.status_code == status.HTTP_404_NOT_FOUND
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=1)
        result = await session.execute(stmt)
        entity: Task | None = result.scalars().one_or_none()
    assert entity is None


@pytest.mark.usefixtures("some_data_added")
async def test_patch_task_by_id_bad_name(task_url: str, async_client: AsyncClient,
                                         all_tasks_ids: list, new_task_bad_name: dict):
    task_id = choice(all_tasks_ids)

    bad_name = new_task_bad_name['name']
    new_task_dict = new_task_bad_name
    new_task_dict, list_of_unused_keys = get_partial_dict(new_task_dict)
    if "name" in list_of_unused_keys:
        list_of_unused_keys.remove('name')
        new_task_dict['name'] = bad_name

    # Изначальное значение сущности в БД
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    # Запрос на изменение
    result = await async_client.patch(url=task_url + f'{task_id}', json=new_task_dict)
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
async def test_patch_task_by_id_bad_name(task_url: str, async_client: AsyncClient,
                                         all_tasks_ids: list, new_task_bad_description: dict):
    task_id = choice(all_tasks_ids)

    bad_description = new_task_bad_description['description']
    new_task_dict = new_task_bad_description
    new_task_dict, list_of_unused_keys = get_partial_dict(new_task_dict)
    if "description" in list_of_unused_keys:
        list_of_unused_keys.remove('description')
        new_task_dict['description'] = bad_description

    # Изначальное значение сущности в БД
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    # Запрос на изменение
    result = await async_client.patch(url=task_url + f'{task_id}', json=new_task_dict)
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
async def test_patch_task_by_id_bad_price_min(task_url: str, async_client: AsyncClient,
                                              all_tasks_ids: list, new_task_bad_price_min: dict):
    task_id = choice(all_tasks_ids)

    bad_description = new_task_bad_price_min['price']
    new_task_dict = new_task_bad_price_min
    new_task_dict, list_of_unused_keys = get_partial_dict(new_task_dict)
    if "price" in list_of_unused_keys:
        list_of_unused_keys.remove('price')
        new_task_dict['price'] = bad_description

    # Изначальное значение сущности в БД
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    # Запрос на изменение
    result = await async_client.patch(url=task_url + f'{task_id}', json=new_task_dict)
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
async def test_patch_task_by_id_bad_price_max(task_url: str, async_client: AsyncClient,
                                              all_tasks_ids: list, new_task_bad_price_max: dict):
    task_id = choice(all_tasks_ids)

    bad_description = new_task_bad_price_max['price']
    new_task_dict = new_task_bad_price_max
    new_task_dict, list_of_unused_keys = get_partial_dict(new_task_dict)
    if "price" in list_of_unused_keys:
        list_of_unused_keys.remove('price')
        new_task_dict['price'] = bad_description

    # Изначальное значение сущности в БД
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        begin_entity: Task = result.scalars().one()

    # Запрос на изменение
    result = await async_client.patch(url=task_url + f'{task_id}', json=new_task_dict)
    assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Проверка изменений в БД
    async with session_factory() as session:
        stmt = select(Task).filter_by(id=task_id)
        result = await session.execute(stmt)
        end_entity: Task = result.scalars().one()
    begin_items_list = list(begin_entity.__dict__.items())
    end_items_list = list(end_entity.__dict__.items())
    assert begin_items_list[1:] == end_items_list[1:]
