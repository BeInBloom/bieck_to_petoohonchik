from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar import Litestar
from litestar.di import Provide

from app.config import Settings
from app.http.controllers import AdsController, CategoriesController, HealthController
from app.http.providers import (
    provide_ad_repository,
    provide_ad_service,
    provide_category_repository,
    provide_category_service,
)


def get_dependencies() -> dict[str, Provide]:
    return {
        "category_repository": Provide(provide_category_repository),
        "category_service": Provide(provide_category_service),
        "ad_repository": Provide(provide_ad_repository),
        "ad_service": Provide(provide_ad_service),
    }


def create_app() -> Litestar:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)

    session_config = AsyncSessionConfig(expire_on_commit=False)
    alchemy_config = SQLAlchemyAsyncConfig(
        connection_string=settings.database_url,
        session_config=session_config,
        before_send_handler="autocommit",
        create_all=False,
    )

    alchemy = SQLAlchemyPlugin(config=alchemy_config)

    app = Litestar(
        route_handlers=[HealthController, CategoriesController, AdsController],
        plugins=[alchemy],
        dependencies=get_dependencies(),
    )

    return app


app = create_app()
