from src2.services.tasks import TaskService
from ..repositories.tasks import TaskRepository

def get_task_service():
	return TaskService(TaskRepository)
