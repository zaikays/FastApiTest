import re

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.adapters.constants.db_const import (
    DB_CONSTRAINT_VIOLATION,
    DB_QUERY_FAILED,
    DB_FLUSH_FAILED,
)
from app.adapters.exceptions.gateway import DataMapperError
from app.application.common.ports.flusher import FlusherAsync, Flusher


class SqlaFlusherAsync(FlusherAsync):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _raise_from_name(self, exc_name: str, message: str, error: Exception):
        import app.domain.exceptions.user as excs

        exc_class = getattr(excs, exc_name, None)
        if exc_class is None:
            raise ValueError(f"Unknown exception: {exc_name}")
        raise exc_class(message) from error

    def _user_field_validate(self, field: str, error: IntegrityError):
        if f"users_{field}" in str(error):
            params = error.params
            field_name = "unknown"
            if isinstance(params, dict):
                field_name = params.get(field, "unknown")
            elif isinstance(params, (tuple, list)) and field in error.statement:
                detail = str(error.orig)
                match = re.search(rf"\({field}\)=\((.*?)\)", detail)
                field_name = match.group(1) if match else "unknown"
            self._raise_from_name(
                f"{field.capitalize()}AlreadyExistsError", field_name, error
            )

    async def flush(self) -> None:
        try:
            await self._session.flush()

        except IntegrityError as error:
            self._user_field_validate("email", error)
            self._user_field_validate("email", error)

            raise DataMapperError(DB_CONSTRAINT_VIOLATION) from error

        except SQLAlchemyError as error:
            raise DataMapperError(f"{DB_QUERY_FAILED} {DB_FLUSH_FAILED}") from error


class SqlaFlusher(Flusher):
    def __init__(self, session: Session):
        self._session = session

    def flush(self) -> None:
        try:
            self._session.flush()
        except IntegrityError as error:

            raise DataMapperError(DB_CONSTRAINT_VIOLATION) from error

        except SQLAlchemyError as error:
            raise DataMapperError(f"{DB_QUERY_FAILED} {DB_FLUSH_FAILED}") from error
