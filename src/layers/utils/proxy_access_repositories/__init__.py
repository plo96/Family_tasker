"""
    Интерфейс и реализация класса для реализации единой точки доступа к репозиториям.
"""
__all__ = (
	"IProxyAccessRepositories",
	"ProxyAccessRepositories",
)

from .i_proxy_access_repositories import IProxyAccessRepositories
from .proxy_access_repositories import ProxyAccessRepositories
