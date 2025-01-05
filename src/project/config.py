"""
    Настройки для приложения
"""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

HOME_DIR = Path(__file__).parent.parent.parent.absolute()


class Settings(BaseSettings):
    """Класс, содержащий основные настройки для приложения"""

    model_config = SettingsConfigDict(
        env_file=f"{HOME_DIR}/.env",
    )

    SQLITE_NAME: str
    TEST_SQLITE_NAME: str

    DB_NAME: str
    DB_USER: str
    DB_PWD: str

    DB_HOST: str
    DB_PORT: int

    ECHO: bool
    TEST_ECHO: bool

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PWD: str

    SECRET_KEY: str
    ALGORITHM: str
    EXPIRATION_TIME: int

    EMAIL_SMTP_HOST: str
    EMAIL_SMTP_PORT: int
    EMAIL_SMTP_USER: str
    EMAIL_SMTP_PWD: str

    # main configs
    MASTER_ADM_NAME: str
    MASTER_ADM_PWD: str
    MASTER_ADM_EMAIL: str

    @property
    def REDIS_URL(self):
        """URL для подключения к redis"""
        return f"redis://:{self.REDIS_PWD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def DATABASE_URL_asyncpg(self):
        """URL для подключения к БД (asyncpg)"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PWD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_ASYNC_SQLITE(self):
        """URL для подключения к БД (aiosqlite)"""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/storage/{self.SQLITE_NAME}"

    @property
    def DATABASE_URL_SQLITE(self):
        """URL для подключения к БД (sqlite3)"""
        return f"sqlite:///{HOME_DIR}/src/database/storage/{self.SQLITE_NAME}"

    @property
    def TEST_DATABASE_URL_ASYNC_SQLITE(self):
        """URL для подключения к тестовой БД (aiosqlite)"""
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/storage/{self.TEST_SQLITE_NAME}"

    @property
    def HOME_DIR(self):
        """Корневая директория проекта"""
        return str(HOME_DIR)


settings = Settings()  # type: ignore
