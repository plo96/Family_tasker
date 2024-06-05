"""
    Настройки для приложения
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

HOME_DIR = Path(__file__).parent.parent.parent.absolute()


class Settings(BaseSettings):
    """Класс, содержащий основные настройки для приложения"""
    model_config = SettingsConfigDict(env_file=f"{HOME_DIR}/.env")
    
    _SQLITE_NAME: str
    _TEST_SQLITE_NAME: str
    
    _REDIS_HOST: str
    _REDIS_PORT: int
    _REDIS_PWD: str
    
    ECHO: bool
    TEST_ECHO: bool
    
    SECRET_KEY: str
    ALGORITHM: str
    EXPIRATION_TIME: int
    
    EMAIL_SMTP_HOST: str
    EMAIL_SMTP_PORT: int
    EMAIL_SMTP_USER: str
    EMAIL_SMTP_PWD: str
    
    @property
    def REDIS_URL(self):
        """URL для подключения к redis"""
        return f"redis://{self._REDIS_PWD}@{self._REDIS_HOST}:{self._REDIS_PORT}/0"

    # @property
    # def DATABASE_URL_asyncpg(self):
    #     """URL для подключения к БД (asyncpg)"""
    #     return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_async_sqlite(self):
        """URL для подключения к БД (aiosqlite)"""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/{self._SQLITE_NAME}"


    @property
    def DATABASE_URL_sqlite(self):
        """URL для подключения к БД (sqlite3)"""
        return f"sqlite:///{HOME_DIR}/src/database/{self._SQLITE_NAME}"

    @property
    def TEST_DATABASE_URL_async_sqlite(self):
        """URL для подключения к тестовой БД (aiosqlite)"""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/{self._TEST_SQLITE_NAME}"

    @property
    def HOME_DIR(self):
        """Корневая директория проекта"""
        return str(HOME_DIR)


settings = Settings()           # type: ignore
