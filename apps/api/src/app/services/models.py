from dataclasses import dataclass

from app.domain import Ad, User


@dataclass(slots=True)
class AdsPage:
    items: list[Ad]
    total: int
    limit: int
    offset: int


@dataclass(slots=True)
class AuthResult:
    user: User
    session_token: str
