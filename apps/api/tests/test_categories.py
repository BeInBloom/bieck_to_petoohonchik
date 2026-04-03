import asyncio

from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain import Category


def test_list_categories_returns_empty_list(client: TestClient) -> None:
    response = client.get("/categories")

    assert response.status_code == 200
    assert response.json() == []


def test_list_categories_returns_categories(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_categories() -> None:
        async with db_session_factory() as session:
            session.add_all(
                [
                    Category(name="Dogs", slug="dogs"),
                    Category(name="Cats", slug="cats"),
                ]
            )
            await session.commit()

    asyncio.run(seed_categories())

    response = client.get("/categories")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 2, "name": "Cats", "slug": "cats", "parent_id": None},
        {"id": 1, "name": "Dogs", "slug": "dogs", "parent_id": None},
    ]


def test_get_category_returns_category(
    client: TestClient,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    async def seed_category() -> None:
        async with db_session_factory() as session:
            session.add(Category(name="Dogs", slug="dogs"))
            await session.commit()

    asyncio.run(seed_category())

    response = client.get("/categories/dogs")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Dogs",
        "slug": "dogs",
        "parent_id": None,
    }


def test_get_category_returns_404_when_category_not_found(client: TestClient) -> None:
    response = client.get("/categories/missing")

    assert response.status_code == 404
