import asyncio

from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import User
from app.security.password_hasher import PasswordHasher


def _seed_user(
    db_session_factory: async_sessionmaker[AsyncSession],
    *,
    email: str = "user@example.com",
    password: str = "secret-password",
    is_active: bool = True,
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            session.add(
                User(
                    email=email,
                    display_name="User",
                    password_hash=PasswordHasher().hash(password),
                    is_active=is_active,
                )
            )
            await session.commit()

    asyncio.run(run_test())


def test_register_creates_user_and_sets_session_cookie(client: TestClient) -> None:
    response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "display_name": "User",
            "password": "secret-password",
        },
    )

    assert response.status_code == 201
    assert response.json()["user"]["email"] == "user@example.com"
    assert response.json()["user"]["display_name"] == "User"
    assert "session=" in response.headers["set-cookie"]


def test_register_returns_409_when_email_already_exists(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_user() -> None:
        async with db_session_factory() as session:
            session.add(
                User(
                    email="user@example.com",
                    display_name="User",
                    password_hash="hashed-password",
                )
            )
            await session.commit()

    asyncio.run(seed_user())

    response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "display_name": "User",
            "password": "secret-password",
        },
    )

    assert response.status_code == 409


def test_login_returns_user_and_sets_session_cookie(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    _seed_user(db_session_factory)

    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "secret-password",
        },
    )

    assert response.status_code == 200
    assert response.json()["user"]["email"] == "user@example.com"
    assert "session=" in response.headers["set-cookie"]


def test_login_returns_401_for_invalid_credentials(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    _seed_user(db_session_factory)

    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_login_returns_401_for_inactive_user(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    _seed_user(db_session_factory, is_active=False)

    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "secret-password",
        },
    )

    assert response.status_code == 401
    assert "set-cookie" not in response.headers


def test_me_returns_current_user_for_authenticated_client(client: TestClient) -> None:
    register_response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "display_name": "User",
            "password": "secret-password",
        },
    )

    assert register_response.status_code == 201

    response = client.get("/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


def test_me_returns_401_when_not_authenticated(client: TestClient) -> None:
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_returns_401_for_invalid_session_cookie(client: TestClient) -> None:
    client.cookies.set("session", "invalid-session-token")

    response = client.get("/auth/me")

    assert response.status_code == 401


def test_logout_clears_session_cookie_and_me_returns_401(client: TestClient) -> None:
    register_response = client.post(
        "/auth/register",
        json={
            "email": "user@example.com",
            "display_name": "User",
            "password": "secret-password",
        },
    )

    assert register_response.status_code == 201

    logout_response = client.post("/auth/logout")

    assert logout_response.status_code == 204
    assert "session=" in logout_response.headers["set-cookie"]
    assert "Max-Age=0" in logout_response.headers["set-cookie"]

    response = client.get("/auth/me")

    assert response.status_code == 401


def test_logout_is_idempotent_without_session_cookie(client: TestClient) -> None:
    response = client.post("/auth/logout")

    assert response.status_code == 204
    assert "session=" in response.headers["set-cookie"]
    assert "Max-Age=0" in response.headers["set-cookie"]
