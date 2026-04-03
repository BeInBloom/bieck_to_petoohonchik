from pathlib import Path

from app.config import Settings


def test_settings_build_sqlite_database_url() -> None:
    settings = Settings(data_dir=Path("var"), sqlite_filename="app.db")

    assert settings.sqlite_path == Path("var/app.db")
    assert settings.database_url == "sqlite+aiosqlite:///var/app.db"
