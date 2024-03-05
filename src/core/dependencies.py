
from src.utils import UnitOfWorkSQLAlchemy as UoW



def get_actual_uow(**kwargs):
	uow = UoW(**kwargs)
	return uow

