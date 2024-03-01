from sqlalchemy.ext.asyncio import AsyncSession

from schemas import TaskDTO

async def get_tasks(session: AsyncSession) -> list[TaskDTO]:
    pass


async def get_task_from_id(task_id: int, session: AsyncSession) -> TaskDTO:
    pass