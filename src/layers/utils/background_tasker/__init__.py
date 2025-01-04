"""
	Выполнение некоторых задач в фоне.
"""

__all__ = (
    "IBackgroundTasker",
    "BackgroundTasker",
    "get_background_tasker",
)
from .i_background_tasker import IBackgroundTasker
from .background_tasker import BackgroundTasker, get_background_tasker
