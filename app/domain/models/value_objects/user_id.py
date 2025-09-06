from dataclasses import dataclass

from app.domain.models.value_objects.base import ValueObject


@dataclass(frozen=True, repr=False)
class UserId(ValueObject):
    value: int | None = None
