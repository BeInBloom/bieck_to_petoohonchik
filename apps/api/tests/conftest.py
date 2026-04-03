import asyncio
from collections.abc import Generator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.asgi import create_app
from app.config import Settings


@pytest.fixture()
def test_settings(monkeypatch, tmp_path) -> Settings:
    monkeypatch.setenv("APP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APP_SQLITE_FILENAME", "test.db")
    return Settings()


@pytest.fixture()
def db_session_factory(
    test_settings: Settings,
) -> Generator[async_sessionmaker[AsyncSession], None, None]:
    alembic_ini_path = Path(__file__).resolve().parents[1] / "alembic.ini"
    alembic_config = Config(str(alembic_ini_path))

    command.upgrade(alembic_config, "head")

    engine = create_async_engine(test_settings.database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    try:
        yield session_factory
    finally:
        asyncio.run(engine.dispose())
        command.downgrade(alembic_config, "base")


@pytest.fixture()
def client(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> Generator[TestClient, None, None]:
    with TestClient(app=create_app()) as test_client:
        yield test_client
