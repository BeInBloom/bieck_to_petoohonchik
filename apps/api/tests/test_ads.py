import asyncio
from datetime import datetime, timezone

from litestar.testing import TestClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import Ad, Category, User


def _seed_user(*, email: str = "user@example.com") -> User:
    return User(
        email=email,
        display_name="User",
        password_hash="hashed-password",
    )


def _register_user(
    client: TestClient,
    *,
    email: str = "user@example.com",
    display_name: str = "User",
    password: str = "secret-password",
) -> None:
    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "display_name": display_name,
            "password": password,
        },
    )

    assert response.status_code == 201


def _seed_category(
    db_session_factory: async_sessionmaker[AsyncSession],
    *,
    name: str = "Dogs",
    slug: str = "dogs",
) -> None:
    async def run_test() -> None:
        async with db_session_factory() as session:
            session.add(Category(name=name, slug=slug))
            await session.commit()

    asyncio.run(run_test())


def _count_ads(db_session_factory: async_sessionmaker[AsyncSession]) -> int:
    async def run_test() -> int:
        async with db_session_factory() as session:
            result = await session.execute(select(func.count()).select_from(Ad))
            return result.scalar_one()

    return asyncio.run(run_test())


def test_get_ad_returns_ad(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_ad() -> None:
        async with db_session_factory() as session:
            user = _seed_user()
            category = Category(name="Dogs", slug="dogs")
            session.add_all([user, category])
            await session.flush()

            session.add(
                Ad(
                    title="Puppy",
                    description="Healthy puppy",
                    price_minor=150_000,
                    category_id=category.id,
                    owner_id=user.id,
                )
            )
            await session.commit()

    asyncio.run(seed_ad())

    response = client.get("/ads/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Puppy"
    assert response.json()["description"] == "Healthy puppy"
    assert response.json()["price_minor"] == 150_000
    assert response.json()["category_id"] == 1
    assert response.json()["published_at"] is None
    assert response.json()["deleted_at"] is None
    assert response.json()["created_at"] is not None
    assert response.json()["updated_at"] is not None


def test_get_ad_returns_404_when_ad_not_found(client: TestClient) -> None:
    response = client.get("/ads/999")

    assert response.status_code == 404


def test_get_ad_returns_404_when_ad_is_soft_deleted(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_deleted_ad() -> None:
        async with db_session_factory() as session:
            user = _seed_user()
            category = Category(name="Dogs", slug="dogs")
            session.add_all([user, category])
            await session.flush()

            session.add(
                Ad(
                    title="Hidden puppy",
                    description="Should not be visible",
                    price_minor=90_000,
                    category_id=category.id,
                    deleted_at=datetime.now(timezone.utc),
                    owner_id=user.id,
                )
            )
            await session.commit()

    asyncio.run(seed_deleted_ad())

    response = client.get("/ads/1")

    assert response.status_code == 404


def test_list_ads_returns_paginated_items(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_ads() -> None:
        async with db_session_factory() as session:
            user = _seed_user()
            category = Category(name="Dogs", slug="dogs")
            session.add_all([user, category])
            await session.flush()

            session.add_all(
                [
                    Ad(
                        title="First ad",
                        description="First description",
                        price_minor=100_000,
                        category_id=category.id,
                        owner_id=user.id,
                    ),
                    Ad(
                        title="Second ad",
                        description="Second description",
                        price_minor=200_000,
                        category_id=category.id,
                        owner_id=user.id,
                    ),
                    Ad(
                        title="Deleted ad",
                        description="Should not be listed",
                        price_minor=300_000,
                        category_id=category.id,
                        deleted_at=datetime.now(timezone.utc),
                        owner_id=user.id,
                    ),
                ]
            )
            await session.commit()

    asyncio.run(seed_ads())

    response = client.get("/ads?limit=1&offset=0")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert response.json()["limit"] == 1
    assert response.json()["offset"] == 0
    assert [item["title"] for item in response.json()["items"]] == ["Second ad"]


def test_list_ads_respects_offset(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_ads() -> None:
        async with db_session_factory() as session:
            user = _seed_user()
            category = Category(name="Dogs", slug="dogs")
            session.add_all([user, category])
            await session.flush()

            session.add_all(
                [
                    Ad(
                        title="First ad",
                        description="First description",
                        price_minor=100_000,
                        category_id=category.id,
                        owner_id=user.id,
                    ),
                    Ad(
                        title="Second ad",
                        description="Second description",
                        price_minor=200_000,
                        category_id=category.id,
                        owner_id=user.id,
                    ),
                ]
            )
            await session.commit()

    asyncio.run(seed_ads())

    response = client.get("/ads?limit=1&offset=1")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert response.json()["limit"] == 1
    assert response.json()["offset"] == 1
    assert [item["title"] for item in response.json()["items"]] == ["First ad"]


def test_post_ad_creates_ad(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    _seed_category(db_session_factory)
    _register_user(client)

    response = client.post(
        "/ads",
        json={
            "title": "Puppy",
            "description": "Healthy puppy",
            "price_minor": 150_000,
            "category_id": 1,
        },
    )

    assert response.status_code == 201
    assert response.json() == {"status": "ok", "id": 1}

    get_response = client.get("/ads/1")

    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Puppy"
    assert get_response.json()["description"] == "Healthy puppy"
    assert get_response.json()["price_minor"] == 150_000
    assert get_response.json()["category_id"] == 1


def test_post_ad_persists_authenticated_user_as_owner(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    _seed_category(db_session_factory)
    _register_user(client, email="owner@example.com", display_name="Owner")

    response = client.post(
        "/ads",
        json={
            "title": "Puppy",
            "description": "Healthy puppy",
            "price_minor": 150_000,
            "category_id": 1,
        },
    )

    assert response.status_code == 201

    async def load_ad_and_owner() -> tuple[Ad | None, User | None]:
        async with db_session_factory() as session:
            created_ad = await session.get(Ad, response.json()["id"])
            owner = await session.scalar(select(User).where(User.email == "owner@example.com"))
            return created_ad, owner

    created_ad, owner = asyncio.run(load_ad_and_owner())

    assert created_ad is not None
    assert owner is not None
    assert created_ad.owner_id == owner.id


def test_post_ad_returns_401_when_user_is_not_authenticated(client: TestClient) -> None:
    response = client.post(
        "/ads",
        json={
            "title": "Puppy",
            "description": "Healthy puppy",
            "price_minor": 150_000,
            "category_id": 1,
        },
    )

    assert response.status_code == 401


def test_post_ad_returns_404_when_category_not_found(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    _register_user(client)

    response = client.post(
        "/ads",
        json={
            "title": "Puppy",
            "description": "Healthy puppy",
            "price_minor": 150_000,
            "category_id": 999,
        },
    )

    assert response.status_code == 404
    assert _count_ads(db_session_factory) == 0
