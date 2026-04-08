import asyncio
from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import Session, User
from app.repositories.session_repository import SessionRepository


def test_create_session_persists_session(
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
            created = await repository.create_session(
                user_id=user.id,
                token_hash="token-hash-1",
                expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            )
            await session.commit()

            assert created.id is not None

        async with db_session_factory() as session:
            persisted = await session.get(Session, created.id)

            assert persisted is not None
            assert persisted.user_id == user.id
            assert persisted.token_hash == "token-hash-1"

    asyncio.run(run_test())


def test_get_session_by_token_hash_returns_session(
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

            seeded = Session(
                user_id=user.id,
                token_hash="token-hash-1",
                expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            )
            session.add(seeded)
            await session.commit()

        async with db_session_factory() as session:
            repository = SessionRepository(session)
            found = await repository.get_session_by_token_hash("token-hash-1")

            assert found is not None
            assert found.user_id == user.id
            assert found.token_hash == "token-hash-1"

    asyncio.run(run_test())


def test_delete_session_removes_only_target_session(
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

            first = Session(
                user_id=user.id,
                token_hash="token-hash-1",
                expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            )
            second = Session(
                user_id=user.id,
                token_hash="token-hash-2",
                expires_at=datetime.now(timezone.utc) + timedelta(days=7),
            )
            session.add_all([first, second])
            await session.flush()

            repository = SessionRepository(session)
            await repository.delete_session(first.id)
            await session.commit()

        async with db_session_factory() as session:
            remaining_ids = await session.scalars(select(Session.id).order_by(Session.id))

            assert list(remaining_ids) == [second.id]

    asyncio.run(run_test())


def test_delete_user_sessions_removes_all_user_sessions(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            first_user = User(
                email="first@example.com",
                display_name="First",
                password_hash="hashed-password",
            )
            second_user = User(
                email="second@example.com",
                display_name="Second",
                password_hash="hashed-password",
            )
            session.add_all([first_user, second_user])
            await session.flush()

            session.add_all(
                [
                    Session(
                        user_id=first_user.id,
                        token_hash="token-hash-1",
                        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
                    ),
                    Session(
                        user_id=first_user.id,
                        token_hash="token-hash-2",
                        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
                    ),
                    Session(
                        user_id=second_user.id,
                        token_hash="token-hash-3",
                        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
                    ),
                ]
            )
            await session.flush()

            repository = SessionRepository(session)
            await repository.delete_user_sessions(first_user.id)
            await session.commit()

        async with db_session_factory() as session:
            remaining_hashes = await session.scalars(
                select(Session.token_hash).order_by(Session.token_hash)
            )

            assert list(remaining_hashes) == ["token-hash-3"]

    asyncio.run(run_test())
