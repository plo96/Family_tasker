from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

HOME_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{HOME_DIR}/src/.env")
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SQLITE_NAME: str

    ECHO: str

    MAX_TASK_NAME_LENGTH: int = 64
    MAX_TASK_DESCRIPTION_LENGTH: int = 512
    MIN_TASK_PRICE: int = 0
    MAX_TASK_PRICE: int = 10

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_async_sqlite(self):
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/database/DB/{self.SQLITE_NAME}"

    @property
    def HOME_DIR(self):
        return str(HOME_DIR)


settings = Settings()


