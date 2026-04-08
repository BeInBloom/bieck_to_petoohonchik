import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import User
from app.repositories.session_repository import SessionRepository
from app.security.session_token_hasher import SessionTokenHasher
from app.services.session_service import SessionService


def test_create_for_user_creates_hashed_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            user = User(
                email="user@example.com",
                display_name="User",
                password_hash="hashed-password",
            )
            session.add(user)
            await session.flush()

            repository = SessionRepository(session)
            hasher = SessionTokenHasher()
            service = SessionService(repository, hasher)

            raw_token = await service.create_for_user(user.id)
            await session.commit()

            persisted = await repository.get_session_by_token_hash(hasher.hash(raw_token))

            assert persisted is not None
            assert persisted.user_id == user.id
            assert persisted.token_hash != raw_token

    asyncio.run(run_test())


def test_get_active_session_returns_session_for_valid_token(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            user = User(
                email="user@example.com",
                display_name="User",
                password_hash="hashed-password",
            )
            session.add(user)
            await session.flush()

            repository = SessionRepository(session)
            service = SessionService(repository)

            raw_token = await service.create_for_user(user.id)
            await session.commit()

        async with db_session_factory() as session:
            repository = SessionRepository(session)
            service = SessionService(repository)

            found = await service.get_active_session(raw_token)

            assert found is not None
            assert found.user_id == user.id

    asyncio.run(run_test())


def test_get_active_session_returns_none_for_expired_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            user = User(
                email="user@example.com",
                display_name="User",
                password_hash="hashed-password",
            )
            session.add(user)
            await session.flush()

            repository = SessionRepository(session)
            hasher = SessionTokenHasher()
            service = SessionService(repository, hasher)
            raw_token = "raw-token"

            await repository.create_session(
                user_id=user.id,
                token_hash=hasher.hash(raw_token),
                expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
            )
            await session.commit()

        async with db_session_factory() as session:
            repository = SessionRepository(session)
            service = SessionService(repository)

            found = await service.get_active_session(raw_token)

            assert found is None

    asyncio.run(run_test())


def test_get_active_session_returns_none_for_revoked_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            user = User(
                email="user@example.com",
                display_name="User",
                password_hash="hashed-password",
            )
            session.add(user)
            await session.flush()

            repository = SessionRepository(session)
            hasher = SessionTokenHasher()
            service = SessionService(repository, hasher)
            raw_token = "raw-token"
            created = await repository.create_session(
                user_id=user.id,
                token_hash=hasher.hash(raw_token),
                expires_at=datetime.now(timezone.utc) + timedelta(days=1),
            )
            await repository.revoke_session(
                created.id,
                datetime.now(timezone.utc),
            )
            await session.commit()

        async with db_session_factory() as session:
            repository = SessionRepository(session)
            service = SessionService(repository)

            found = await service.get_active_session(raw_token)

            assert found is None

    asyncio.run(run_test())


def test_revoke_by_token_marks_session_as_revoked(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            user = User(
                email="user@example.com",
                display_name="User",
                password_hash="hashed-password",
            )
            session.add(user)
            await session.flush()

            repository = SessionRepository(session)
            service = SessionService(repository)

            raw_token = await service.create_for_user(user.id)
            await session.commit()

        async with db_session_factory() as session:
            repository = SessionRepository(session)
            hasher = SessionTokenHasher()
            service = SessionService(repository, hasher)

            await service.revoke_by_token(raw_token)
            await session.commit()

            revoked = await repository.get_session_by_token_hash(hasher.hash(raw_token))

            assert revoked is not None
            assert revoked.revoked_at is not None

    asyncio.run(run_test())
