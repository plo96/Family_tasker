from sqlalchemy.ext.asyncio import AsyncSession

from schemas import Task

async def get_tasks(session: AsyncSession) -> list[Task]:
    pass