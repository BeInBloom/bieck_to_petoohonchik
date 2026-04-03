from pathlib import Path

from alembic import command
from alembic.config import Config
from litestar.testing import TestClient

from app.asgi import create_app
from app.config import Settings


def test_alembic_upgrade_bootstraps_clean_database(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("APP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APP_SQLITE_FILENAME", "test.db")

    settings = Settings()
    assert not settings.sqlite_path.exists()

    alembic_ini_path = Path(__file__).resolve().parents[1] / "alembic.ini"
    alembic_config = Config(str(alembic_ini_path))

    command.upgrade(alembic_config, "head")

    assert settings.sqlite_path.exists()

    try:
        with TestClient(app=create_app()) as client:
            health_response = client.get("/health/db")
            ads_response = client.get("/ads")

        assert health_response.status_code == 200
        assert health_response.json() == {"status": "ok", "db": "ok"}
        assert ads_response.status_code == 200
        assert ads_response.json() == {
            "items": [],
            "total": 0,
            "limit": 20,
            "offset": 0,
        }
    finally:
        command.downgrade(alembic_config, "base")
