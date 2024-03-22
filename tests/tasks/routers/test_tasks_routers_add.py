from httpx import AsyncClient
from fastapi import status

from src.core.schemas import TaskCreate


async def test_add_task(task_url: str, async_client: AsyncClient, new_task: TaskCreate):
	result = await async_client.post(task_url, json=new_task.model_dump())
	assert result.status_code == status.HTTP_200_OK
	assert all(i in result.json().items() for i in new_task.model_dump().items())


async def test_add_task_bad_name(task_url: str, async_client: AsyncClient, new_task_bad_name: TaskCreate):
	result = await async_client.post(task_url, json=new_task_bad_name)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_add_task_bad_description(task_url: str, async_client: AsyncClient, new_task_bad_description: TaskCreate):
	result = await async_client.post(task_url, json=new_task_bad_description)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_add_task_bad_price_min(task_url: str, async_client: AsyncClient, new_task_bad_price_min: TaskCreate):
	result = await async_client.post(task_url, json=new_task_bad_price_min)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_add_task_bad_price_max(task_url: str, async_client: AsyncClient, new_task_bad_price_max: TaskCreate):
	result = await async_client.post(task_url, json=new_task_bad_price_max)
	assert result.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
	