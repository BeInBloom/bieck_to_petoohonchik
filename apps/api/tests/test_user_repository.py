import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import User, UserRole
from app.repositories.user_repository import UserRepository


def test_create_user_persists_user(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            repository = UserRepository(session)

            created = await repository.create_user(
                email="user@example.com",
                display_name="User",
                password_hash="hashed-password",
            )
            await session.commit()

            assert created.id is not None
            assert created.role == UserRole.USER

        async with db_session_factory() as session:
            persisted = await session.get(User, created.id)

            assert persisted is not None
            assert persisted.email == "user@example.com"
            assert persisted.display_name == "User"
            assert persisted.password_hash == "hashed-password"
            assert persisted.role == UserRole.USER

    asyncio.run(run_test())


def test_get_user_by_id_returns_user(
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
            await session.commit()

        async with db_session_factory() as session:
            repository = UserRepository(session)

            found = await repository.get_user_by_id(user.id)

            assert found is not None
            assert found.id == user.id
            assert found.email == "user@example.com"

    asyncio.run(run_test())


def test_get_user_by_email_returns_user(
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
            await session.commit()

        async with db_session_factory() as session:
            repository = UserRepository(session)

            found = await repository.get_user_by_email("user@example.com")

            assert found is not None
            assert found.id == user.id
            assert found.email == "user@example.com"

    asyncio.run(run_test())


def test_get_user_by_email_returns_none_when_missing(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            repository = UserRepository(session)

            found = await repository.get_user_by_email("missing@example.com")

            assert found is None

    asyncio.run(run_test())
