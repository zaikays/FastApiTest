from app.domain.exceptions.base import DomainFieldError
from app.domain.models.value_objects.email.constants import EMAIL_REGEX


def validate_email(email_value: str) -> None:
    if not EMAIL_REGEX.match(email_value):
        raise DomainFieldError("Invalid email address format.")
