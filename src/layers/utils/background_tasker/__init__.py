"""
	Выполнение некоторых задач в фоне.
"""

__all__ = (
    "IBackgroundTasker",
    "BackgroundTasker",
)
from .i_background_tasker import IBackgroundTasker
from .background_tasker import BackgroundTasker
