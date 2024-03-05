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

    ECHO: bool

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_async_sqlite(self):
        return f"sqlite+aiosqlite:///{HOME_DIR}/src/DB/{self.SQLITE_NAME}"

    @property
    def DATABASE_URL_sqlite(self):
        return f"sqlite:///{HOME_DIR}/src/DB/{self.SQLITE_NAME}"

    @property
    def HOME_DIR(self):
        return str(HOME_DIR)


settings = Settings()


