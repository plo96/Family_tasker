from random import randint

import pytest
from faker import Faker
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import async_scoped_session

from src.core.schemas import TaskCreate, TaskUpdate, MAX_TASK_NAME_LENGTH, MAX_TASK_DESCRIPTION_LENGTH, MIN_TASK_PRICE, \
    MAX_TASK_PRICE
from src.core.models import Task

from tests.conftest import get_actual_session_factory, NUM_TESTS

fake = Faker()


def get_new_task_dict(name: str = None,
                      description: str = None,
                      price: int = None) -> dict:
    if not name: name = fake.text(MAX_TASK_NAME_LENGTH)
    if not description: description = fake.text(MAX_TASK_DESCRIPTION_LENGTH)
    if not price: price = randint(MIN_TASK_PRICE, MAX_TASK_PRICE)
    return dict(name=name, description=description, price=price)


@pytest.fixture(scope='session')
def task_url() -> str:
    return '/tasks/'


@pytest.fixture
def one_new_task(request) -> TaskCreate:
    return TaskCreate(**get_new_task_dict())


@pytest.fixture(params=[_ for _ in range(NUM_TESTS)])
def new_task(request) -> TaskCreate:
    return TaskCreate(**get_new_task_dict())


@pytest.fixture(params=[i for i in range(NUM_TESTS)])
def new_task_bad_price_min(request) -> dict:
    return get_new_task_dict(price=MIN_TASK_PRICE - 1 - request.param)


@pytest.fixture(params=[i for i in range(NUM_TESTS)])
def new_task_bad_price_max(request) -> dict:
    return get_new_task_dict(price=MAX_TASK_PRICE + 1 + request.param)


@pytest.fixture(params=[_ for _ in range(NUM_TESTS)])
def new_task_bad_name() -> dict:
    return get_new_task_dict(name=f'{fake.text(MAX_TASK_NAME_LENGTH * 4)}')


@pytest.fixture(params=[_ for _ in range(NUM_TESTS)])
def new_task_bad_description() -> dict:
    return get_new_task_dict(description=f'{fake.text(MAX_TASK_DESCRIPTION_LENGTH * 2)}')


@pytest.fixture
async def some_data_added(clear_database: None) -> None:
    new_tasks = [get_new_task_dict() for _ in range(NUM_TESTS)]
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        for new_task in new_tasks:
            stmt = insert(Task).values(**new_task)
            await session.execute(stmt)
        await session.commit()
    if isinstance(session_factory, async_scoped_session):
        await session_factory.remove()


@pytest.fixture
async def all_tasks_ids() -> list:
    session_factory = get_actual_session_factory()
    async with session_factory() as session:
        stmt = select(Task)
        result = await session.execute(stmt)
        all_entities = result.scalars().all()
        all_ids = [entity.id for entity in all_entities]
    if isinstance(session_factory, async_scoped_session):
        await session_factory.remove()
    return all_ids
