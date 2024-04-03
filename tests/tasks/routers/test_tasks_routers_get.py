from random import choice
from uuid import uuid4

import pytest
from httpx import AsyncClient
from fastapi import status

from src.core.schemas import TaskDTO


@pytest.mark.usefixtures("some_data_added")
async def test_get_all_tasks(task_url: str, async_client: AsyncClient, all_tasks_ids: list):
	result = await async_client.get(url=task_url)
	assert result.status_code == status.HTTP_200_OK
	assert len(result.json()) == len(all_tasks_ids)
	for task in result.json():
		assert TaskDTO.model_validate(task)


@pytest.mark.usefixtures("some_data_added")
async def \
		test_get_task_by_id(task_url: str, async_client: AsyncClient, all_tasks_ids: list):
	for _ in range(len(all_tasks_ids)):
		task_id = choice(all_tasks_ids)
		result = await async_client.get(url=task_url + f'{task_id}')
		assert result.status_code == status.HTTP_200_OK
		assert TaskDTO.model_validate(result.json()).id == task_id


@pytest.mark.usefixtures("clear_database")
async def test_get_empty_tasks_list(task_url: str, async_client: AsyncClient):
	result = await async_client.get(url=task_url)
	assert result.status_code == status.HTTP_200_OK
	assert result.json() == []


@pytest.mark.usefixtures("clear_database")
async def test_get_task_by_bad_id(task_url: str, async_client: AsyncClient):
	result = await async_client.get(url=task_url + str(uuid4()))
	assert result.status_code == status.HTTP_404_NOT_FOUND
