from collections.abc import Mapping
from types import MappingProxyType
from typing import Final

import pydantic
from starlette import status

from app.adapters.exceptions.auth import AuthenticationError
from app.application.common.exceptions.authorization import AuthorizationError
from app.application.common.exceptions.base import ApplicationError

from app.domain.exceptions.base import DomainError, DomainFieldError
from app.domain.exceptions.user import (
    EmailAlreadyExistsError,
)


MSG_INTERNAL_SERVER_ERROR: Final[str] = "Internal server error."
MSG_SERVICE_UNAVAILABLE: Final[str] = (
    "Service temporarily unavailable. Please try again later."
)

ERROR_STATUS_MAPPING: Final[Mapping[type[Exception], int]] = MappingProxyType(
    {
        # 400
        DomainFieldError: status.HTTP_400_BAD_REQUEST,
        # 401
        AuthenticationError: status.HTTP_401_UNAUTHORIZED,
        # 403
        AuthorizationError: status.HTTP_403_FORBIDDEN,
        # 409
        EmailAlreadyExistsError: status.HTTP_409_CONFLICT,
        # 422
        pydantic.ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
        # 500
        ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        DomainError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
)
