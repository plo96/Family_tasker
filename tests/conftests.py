"""
    Настройки для прогона тестов
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

HOME_DIR = Path(__file__).parent.parent


class TestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{HOME_DIR}/tests/.env")
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    TEST_SQLITE_NAME: str

    TEST_ECHO: bool

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_async_sqlite(self):
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/{self.SQLITE_NAME}"

    @property
    def DATABASE_URL_sqlite(self):
        return f"sqlite:///{HOME_DIR}/src/database/{self.SQLITE_NAME}"

    @property
    def HOME_DIR(self):
        return str(HOME_DIR)


test_settings = TestSettings()           # type: ignore


