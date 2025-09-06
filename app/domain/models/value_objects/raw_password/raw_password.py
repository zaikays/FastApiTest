from dataclasses import dataclass

from app.domain.models.value_objects.base import ValueObject
from app.domain.models.value_objects.raw_password.validation import (
    validate_password_length,
)


@dataclass(frozen=True, repr=False)
class RawPassword(ValueObject):
    value: str

    def __post_init__(self) -> None:
        super().__post_init__()

        validate_password_length(self.value)
