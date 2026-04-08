from typing import Annotated

from litestar import Controller, get
from litestar.exceptions import NotFoundException
from litestar.params import Dependency

from app.http.schemas import CategoryRead
from app.services.category_service import CategoryServiceContract


class CategoriesController(Controller):
    path = "/categories"

    @get()
    async def list_categories(
        self,
        category_service: Annotated[CategoryServiceContract, Dependency(skip_validation=True)],
    ) -> list[CategoryRead]:
        categories = await category_service.list_categories()
        return CategoryRead.validate_list(categories)

    @get("/{slug:str}")
    async def get_category(
        self,
        slug: str,
        category_service: Annotated[CategoryServiceContract, Dependency(skip_validation=True)],
    ) -> CategoryRead:
        category = await category_service.get_category(slug)

        if category is None:
            raise NotFoundException("category not found")

        return CategoryRead.validate_value(category)
