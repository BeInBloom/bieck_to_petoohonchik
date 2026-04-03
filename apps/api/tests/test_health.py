from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.asgi import create_app


def test_healthcheck_returns_ok() -> None:
    with TestClient(app=create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_db_healthcheck_returns_ok(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("APP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APP_SQLITE_FILENAME", "test.db")

    with TestClient(app=create_app()) as client:
        response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "ok"}


def test_db_healthcheck_returns_unexpected_when_query_result_is_not_one(
    monkeypatch, tmp_path
) -> None:
    class FakeResult:
        @staticmethod
        def scalar_one() -> int:
            return 0

    async def fake_execute(self, statement):
        return FakeResult()

    monkeypatch.setenv("APP_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("APP_SQLITE_FILENAME", "test.db")
    monkeypatch.setattr(AsyncSession, "execute", fake_execute)

    with TestClient(app=create_app()) as client:
        response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "db": "unexpected"}
