from dataclasses import dataclass

from app.domain import Ad


@dataclass(slots=True)
class AdsPage:
    items: list[Ad]
    total: int
    limit: int
    offset: int
