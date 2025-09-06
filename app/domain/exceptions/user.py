from typing import Any

from app.domain.exceptions.base import DomainError


class EmailAlreadyExistsError(DomainError):
    def __init__(self, email: Any):
        message = f"User with email {email!r} already exists."
        super().__init__(message)
