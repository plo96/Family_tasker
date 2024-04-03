from uuid import uuid4
import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select

from src.core.models import Task
from tests.conftest import get_fake_session_factory


@pytest.mark.usefixtures("some_data_added")
async def test_delete_task_by_id(task_url: str, async_client: AsyncClient, all_tasks_ids: list):
    current_task_number = len(all_tasks_ids)
    for task_id in all_tasks_ids:
        print(task_url + f'{str(task_id)}')
        result = await async_client.delete(url=task_url + f'{str(task_id)}')
        assert result.status_code == status.HTTP_200_OK
        current_task_number -= 1
        session_factory = get_fake_session_factory()
        async with session_factory() as session:
            stmt = select(Task)
            result = await session.execute(stmt)
        assert len(result.scalars().all()) == current_task_number
        async with session_factory() as session:
            stmt = select(Task).filter_by(id=task_id)
            result = await session.execute(stmt)
            assert result.scalars().one_or_none() is None


@pytest.mark.usefixtures("clear_database")
async def test_bad_delete_task_by_id(task_url: str, async_client: AsyncClient):
    result = await async_client.delete(url=task_url + str(uuid4()))
    assert result.status_code == status.HTTP_404_NOT_FOUND
