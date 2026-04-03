from typing import Iterable

from pydantic import BaseModel, ConfigDict, TypeAdapter


class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    parent_id: int | None

    @classmethod
    def validate_list(cls, value: Iterable[object]) -> list["CategoryRead"]:
        return TypeAdapter(list["CategoryRead"]).validate_python(value, from_attributes=True)

    @classmethod
    def validate_value(cls, value: object) -> "CategoryRead":
        return cls.model_validate(value, from_attributes=True)
