from datetime import datetime
from typing import Iterable

from pydantic import BaseModel, ConfigDict, Field


class AdRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    price_minor: int
    category_id: int
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None
    deleted_at: datetime | None

    @classmethod
    def validate_value(cls, value: object) -> "AdRead":
        return cls.model_validate(value, from_attributes=True)

    @classmethod
    def validate_list(cls, values: Iterable[object]) -> list["AdRead"]:
        return [cls.validate_value(value) for value in values]


class AdsPageRead(BaseModel):
    items: list[AdRead]
    total: int
    limit: int
    offset: int


class AdCreate(BaseModel):
    title: str = Field(min_length=1, max_length=256)
    description: str = Field(min_length=1)
    price_minor: int = Field(ge=0)
    category_id: int = Field(gt=0)


class AdCreated(BaseModel):
    status: str = "ok"
    id: int
