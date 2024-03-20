import pytest
from httpx import AsyncClient

from src.core.schemas import TaskCreate

async def test_add_task(async_client: AsyncClient):
	new_task = TaskCreate(name='new_task_1', description='new_test_task_1', price=5)
	result = async_client.post('/tasks/', json=new_task.model_dump())
	print(result)


