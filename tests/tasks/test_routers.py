from datetime import datetime
from random import randint
from time import sleep
import pytest
from httpx import AsyncClient
from faker import Faker
from fastapi import status

from src.core.schemas import (TaskCreate, MAX_TASK_NAME_LENGTH,
							  MAX_TASK_DESCRIPTION_LENGTH, MIN_TASK_PRICE, MAX_TASK_PRICE)

fake = Faker()

TASKS_URL='/tasks/'

@pytest.fixture(scope='session', params=[i for i in range(MIN_TASK_PRICE, MAX_TASK_PRICE + 1)])
def new_task(request) -> TaskCreate:
	return TaskCreate(name=f'{fake.text(MAX_TASK_NAME_LENGTH)}',
					  description=f'{fake.text(MAX_TASK_DESCRIPTION_LENGTH)}',
					  price=request.param
					  )


@pytest.fixture(scope='session', params=[i for i in range(MIN_TASK_PRICE, MAX_TASK_PRICE + 1)])
def new_task_2(request) -> TaskCreate:
	return TaskCreate(name=f'{fake.text(MAX_TASK_NAME_LENGTH)}',
					  description=f'{fake.text(MAX_TASK_DESCRIPTION_LENGTH)}',
					  price=request.param
					  )


@pytest.fixture(scope='session', params=[i for i in range(1, 10)])
def new_task_bad_price_min(request) -> dict:
	return dict(name=f'{fake.text(MAX_TASK_NAME_LENGTH)}',
				description=f'{fake.text(MAX_TASK_DESCRIPTION_LENGTH)}',
				price=MIN_TASK_PRICE - request.param,
				)


@pytest.fixture(scope='session', params=[i for i in range(1, 10)])
def new_task_bad_price_max(request) -> dict:
	return dict(name=f'{fake.text(MAX_TASK_NAME_LENGTH)}',
				description=f'{fake.text(MAX_TASK_DESCRIPTION_LENGTH)}',
				price=MAX_TASK_PRICE + request.param,
				)


@pytest.fixture(params=[i for i in range(1, 10)])
def new_task_bad_name() -> dict:
	return dict(name=f'{fake.text(MAX_TASK_NAME_LENGTH * 3)}',
				description=f'{fake.text(MAX_TASK_DESCRIPTION_LENGTH)}',
				price=randint(MIN_TASK_PRICE, MAX_TASK_PRICE),
				)


@pytest.fixture(params=[i for i in range(1, 10)])
def new_task_bad_description() -> dict:
	return dict(name=f'{fake.text(MAX_TASK_NAME_LENGTH)}',
				description=f'{fake.text(MAX_TASK_DESCRIPTION_LENGTH * 2)}',
				price=randint(MIN_TASK_PRICE, MAX_TASK_PRICE),
				)


async def test_add_task(async_client: AsyncClient, new_task: TaskCreate):
	result = await async_client.post(TASKS_URL, json=new_task.model_dump())
	assert result.status_code == status.HTTP_200_OK
	assert all(i in result.json().items() for i in new_task.model_dump().items())


async def test_add_task_bad_name(async_client: AsyncClient, new_task_bad_name: TaskCreate):
	result = await async_client.post(TASKS_URL, json=new_task_bad_name)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_add_task_bad_description(async_client: AsyncClient, new_task_bad_description: TaskCreate):
	result = await async_client.post(TASKS_URL, json=new_task_bad_description)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_add_task_bad_price_min(async_client: AsyncClient, new_task_bad_price_min: TaskCreate):
	result = await async_client.post(TASKS_URL, json=new_task_bad_price_min)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_add_task_bad_price_max(async_client: AsyncClient, new_task_bad_price_max: TaskCreate):
	result = await async_client.post(TASKS_URL, json=new_task_bad_price_max)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

