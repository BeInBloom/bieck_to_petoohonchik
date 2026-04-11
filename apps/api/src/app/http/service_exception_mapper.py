from collections.abc import Callable
from typing import Never, TypeAlias

from litestar.exceptions import ClientException, HTTPException, NotAuthorizedException
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.services.exceptions import (
    CategoryNotFoundError,
    InactiveUserError,
    InvalidCredentialsError,
    ServiceError,
    UserAlreadyExistsError,
)

HttpExceptionFactory: TypeAlias = Callable[[ServiceError], HTTPException]


class ServiceExceptionMapper:
    def __init__(
        self,
        mapping: dict[type[ServiceError], HttpExceptionFactory] | None = None,
    ) -> None:
        self._mapping = mapping or {
            UserAlreadyExistsError: self._map_user_already_exists,
            InvalidCredentialsError: self._map_invalid_credentials,
            InactiveUserError: self._map_inactive_user,
            CategoryNotFoundError: self._map_category_not_found,
        }

    def raise_http_exception(self, error: ServiceError) -> Never:
        for error_type, factory in self._mapping.items():
            if isinstance(error, error_type):
                raise factory(error) from error

        raise error

    def _map_user_already_exists(self, _: ServiceError) -> HTTPException:
        return ClientException("user already exists", status_code=HTTP_409_CONFLICT)

    def _map_invalid_credentials(self, _: ServiceError) -> HTTPException:
        return NotAuthorizedException("invalid credentials")

    def _map_inactive_user(self, _: ServiceError) -> HTTPException:
        return NotAuthorizedException("user is inactive")

    def _map_category_not_found(self, _: ServiceError) -> HTTPException:
        return ClientException("category not found", status_code=HTTP_404_NOT_FOUND)


service_exception_mapper = ServiceExceptionMapper()
