import asyncio

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import Session, User
from app.repositories.session_repository import SessionRepository
from app.repositories.user_repository import UserRepository
from app.security.password_hasher import PasswordHasher
from app.services.auth_service import AuthService
from app.services.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from app.services.session_service import SessionService


def _build_auth_service(session: AsyncSession) -> tuple[AuthService, SessionService]:
    user_repo = UserRepository(session)
    session_repo = SessionRepository(session)
    session_service = SessionService(session_repo)
    auth_service = AuthService(user_repo, session_service, PasswordHasher())
    return auth_service, session_service


async def _count_sessions(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(Session))
    return result.scalar_one()


def test_register_creates_user_and_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            auth_service, session_service = _build_auth_service(session)
            password_hasher = PasswordHasher()

            result = await auth_service.register(
                email="user@example.com",
                display_name="User",
                password="secret-password",
            )
            await session.commit()

            assert result.user.id is not None
            assert result.user.email == "user@example.com"
            assert result.user.display_name == "User"
            assert result.session_token
            assert password_hasher.verify(result.user.password_hash, "secret-password") is True

            persisted_session = await session_service.get_active_session(result.session_token)

            assert persisted_session is not None
            assert persisted_session.user_id == result.user.id

    asyncio.run(run_test())


def test_register_raises_when_email_already_exists(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            session.add(
                User(
                    email="user@example.com",
                    display_name="User",
                    password_hash="hashed-password",
                )
            )
            await session.commit()

        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            with pytest.raises(UserAlreadyExistsError):
                await auth_service.register(
                    email="user@example.com",
                    display_name="User",
                    password="secret-password",
                )

    asyncio.run(run_test())


def test_login_returns_user_and_session_for_valid_credentials(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        password_hasher = PasswordHasher()

        async with db_session_factory() as session:
            session.add(
                User(
                    email="user@example.com",
                    display_name="User",
                    password_hash=password_hasher.hash("secret-password"),
                )
            )
            await session.commit()

        async with db_session_factory() as session:
            auth_service, session_service = _build_auth_service(session)

            result = await auth_service.login(
                email="user@example.com",
                password="secret-password",
            )
            await session.commit()

            assert result.user.email == "user@example.com"
            assert result.session_token

            persisted_session = await session_service.get_active_session(result.session_token)

            assert persisted_session is not None
            assert persisted_session.user_id == result.user.id

    asyncio.run(run_test())


def test_login_raises_for_missing_user(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            with pytest.raises(InvalidCredentialsError):
                await auth_service.login(
                    email="missing@example.com",
                    password="secret-password",
                )

            assert await _count_sessions(session) == 0

    asyncio.run(run_test())


def test_login_raises_for_invalid_password(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        password_hasher = PasswordHasher()

        async with db_session_factory() as session:
            session.add(
                User(
                    email="user@example.com",
                    display_name="User",
                    password_hash=password_hasher.hash("secret-password"),
                )
            )
            await session.commit()

        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            with pytest.raises(InvalidCredentialsError):
                await auth_service.login(
                    email="user@example.com",
                    password="wrong-password",
                )

            assert await _count_sessions(session) == 0

    asyncio.run(run_test())


def test_login_raises_for_inactive_user(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        password_hasher = PasswordHasher()

        async with db_session_factory() as session:
            session.add(
                User(
                    email="user@example.com",
                    display_name="User",
                    password_hash=password_hasher.hash("secret-password"),
                    is_active=False,
                )
            )
            await session.commit()

        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            with pytest.raises(InactiveUserError):
                await auth_service.login(
                    email="user@example.com",
                    password="secret-password",
                )

            assert await _count_sessions(session) == 0

    asyncio.run(run_test())


def test_logout_revokes_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            registered = await auth_service.register(
                email="user@example.com",
                display_name="User",
                password="secret-password",
            )
            await session.commit()

        async with db_session_factory() as session:
            auth_service, session_service = _build_auth_service(session)

            await auth_service.logout(registered.session_token)
            await session.commit()

            active_session = await session_service.get_active_session(registered.session_token)

            assert active_session is None

    asyncio.run(run_test())


def test_get_current_user_returns_user_for_active_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            registered = await auth_service.register(
                email="user@example.com",
                display_name="User",
                password="secret-password",
            )
            await session.commit()

        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            current_user = await auth_service.get_current_user(registered.session_token)

            assert current_user is not None
            assert current_user.id == registered.user.id
            assert current_user.email == "user@example.com"

    asyncio.run(run_test())


def test_get_current_user_returns_none_for_invalid_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            auth_service, _ = _build_auth_service(session)

            current_user = await auth_service.get_current_user("invalid-token")

            assert current_user is None

    asyncio.run(run_test())
