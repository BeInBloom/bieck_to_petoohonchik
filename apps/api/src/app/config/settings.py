from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "litestar-bb-api"
    app_env: str = "dev"
    debug: bool = True
    data_dir: Path = Path("db")
    sqlite_filename: str = "app.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
    )

    @computed_field
    @property
    def sqlite_path(self) -> Path:
        return self.data_dir / self.sqlite_filename

    @computed_field
    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.sqlite_path}"
