from typing import Annotated

from litestar import Controller, Request, Response, get, post
from litestar.datastructures.cookie import Cookie
from litestar.params import Dependency
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)

from app.domain import User
from app.http.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, UserRead
from app.http.service_exception_mapper import service_exception_mapper
from app.services.auth_service import AuthServiceContract
from app.services.exceptions import ServiceError


class AuthController(Controller):
    SESSION_COOKIE_NAME = "session"
    SESSION_COOKIE_PATH = "/"

    path = "/auth"

    @post("/register", status_code=HTTP_201_CREATED)
    async def register(
        self,
        data: RegisterRequest,
        auth_service: Annotated[AuthServiceContract, Dependency(skip_validation=True)],
    ) -> Response[AuthResponse]:
        try:
            result = await auth_service.register(
                email=str(data.email),
                display_name=data.display_name,
                password=data.password,
            )
        except ServiceError as error:
            service_exception_mapper.raise_http_exception(error)

        return Response(
            AuthResponse(user=UserRead.validate_value(result.user)),
            status_code=HTTP_201_CREATED,
            cookies=[self._build_session_cookie(result.session_token)],
        )

    @post("/login", status_code=HTTP_200_OK)
    async def login(
        self,
        data: LoginRequest,
        auth_service: Annotated[AuthServiceContract, Dependency(skip_validation=True)],
    ) -> Response[AuthResponse]:
        try:
            result = await auth_service.login(
                email=str(data.email),
                password=data.password,
            )
        except ServiceError as error:
            service_exception_mapper.raise_http_exception(error)

        return Response(
            AuthResponse(user=UserRead.validate_value(result.user)),
            status_code=HTTP_200_OK,
            cookies=[self._build_session_cookie(result.session_token)],
        )

    @post("/logout", status_code=HTTP_204_NO_CONTENT)
    async def logout(
        self,
        request: Request,
        auth_service: Annotated[AuthServiceContract, Dependency(skip_validation=True)],
    ) -> Response[None]:
        session_token = request.cookies.get(self.SESSION_COOKIE_NAME)

        if session_token:
            await auth_service.logout(session_token)

        return Response(
            None,
            status_code=HTTP_204_NO_CONTENT,
            cookies=[self._build_logout_cookie()],
        )

    @get("/me", status_code=HTTP_200_OK)
    async def me(
        self,
        required_current_user: Annotated[User, Dependency(skip_validation=True)],
    ) -> UserRead:
        return UserRead.validate_value(required_current_user)

    def _build_session_cookie(self, session_token: str) -> Cookie:
        return Cookie(
            key=self.SESSION_COOKIE_NAME,
            value=session_token,
            httponly=True,
            samesite="lax",
            path=self.SESSION_COOKIE_PATH,
        )

    def _build_logout_cookie(self) -> Cookie:
        return Cookie(
            key=self.SESSION_COOKIE_NAME,
            value="",
            httponly=True,
            samesite="lax",
            path=self.SESSION_COOKIE_PATH,
            max_age=0,
        )
