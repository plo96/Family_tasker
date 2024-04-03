"""
    Настройки для приложения
"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

HOME_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """Класс, содержащий основные настройки для приложения"""
    model_config = SettingsConfigDict(env_file=f"{HOME_DIR}/.env")
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    TEST_DB_NAME: str

    SQLITE_NAME: str
    TEST_SQLITE_NAME: str

    ECHO: bool
    TEST_ECHO: bool

    @property
    def DATABASE_URL_asyncpg(self):
        """URL для подключения к БД (asyncpg)"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_async_sqlite(self):
        """URL для подключения к БД (aiosqlite)"""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/{self.SQLITE_NAME}"


    @property
    def DATABASE_URL_sqlite(self):
        """URL для подключения к БД (sqlite3)"""
        return f"sqlite:///{HOME_DIR}/src/database/{self.SQLITE_NAME}"

    @property
    def TEST_DATABASE_URL_async_sqlite(self):
        """URL для подключения к тестовой БД (aiosqlite)"""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/{self.TEST_SQLITE_NAME}"

    @property
    def HOME_DIR(self):
        """Корневая директория проекта"""
        return str(HOME_DIR)


settings = Settings()           # type: ignore
