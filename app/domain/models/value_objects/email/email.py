from dataclasses import dataclass

from app.domain.models.value_objects.base import ValueObject
from app.domain.models.value_objects.email.validation import validate_email


@dataclass(frozen=True, repr=False)
class Email(ValueObject):

    value: str

    def __post_init__(self) -> None:
        super().__post_init__()

        validate_email(self.value)
