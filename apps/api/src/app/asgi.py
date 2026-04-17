from typing import Tuple

from advanced_alchemy.extensions.litestar import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin,
)
from litestar import Litestar
from litestar.di import Provide
from litestar.logging import LoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.types import ControllerRouterHandler, Middleware

from app.config import Settings
from app.http.controllers import (
    AdsController,
    AuthController,
    CategoriesController,
    HealthController,
)
from app.http.providers import (
    get_ad_dependencies,
    get_auth_dependencies,
    get_category_dependencies,
)


def get_logging_config() -> Tuple[LoggingConfig, Middleware]:
    log_config = LoggingConfig(
        root={"level": "DEBUG", "handlers": ["queue_listener"]},
        formatters={"standard": {"format": "%(asctime)s %(levelname)s %(name)s %(message)s"}},
        # Отключит реальные 500-ки, но litestar нет разделения на норм ошибки и "жопа отвалилась"
        log_exceptions="never",
    )

    req_logging = LoggingMiddlewareConfig(
        logger_name="app.http",
        exclude=["/health"],
        request_log_fields=("method", "path"),
        response_log_fields=("status_code"),
    )

    return log_config, req_logging.middleware


def get_dependencies() -> dict[str, Provide]:
    return {
        **get_category_dependencies(),
        **get_ad_dependencies(),
        **get_auth_dependencies(),
    }


def get_handlers() -> list[ControllerRouterHandler]:
    return [HealthController, CategoriesController, AdsController, AuthController]


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

    (log_conf, log_middleware) = get_logging_config()

    app = Litestar(
        logging_config=log_conf,
        route_handlers=get_handlers(),
        plugins=[alchemy],
        dependencies=get_dependencies(),
        middleware=[log_middleware],
    )

    return app


app = create_app()
