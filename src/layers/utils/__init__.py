"""
    Интерфейсы и реализации репозитория и UoW
"""
__all__ = (
	"IProxyAccessRepositories",
	"ProxyAccessRepositories",
)

from .i_proxy_access_repositories import IProxyAccessRepositories
from .proxy_access_repositories import ProxyAccessRepositories
