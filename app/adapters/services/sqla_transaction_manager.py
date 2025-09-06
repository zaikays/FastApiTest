import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.adapters.constants.db_const import DB_QUERY_FAILED, DB_COMMIT_FAILED
from app.adapters.exceptions.gateway import DataMapperError
from app.application.common.ports.transaction_manager import (
    TransactionManagerAsync,
    TransactionManager,
)

log = logging.getLogger(__name__)


class SqlaTransactionManagerAsync(TransactionManagerAsync):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()

        except SQLAlchemyError as error:
            raise DataMapperError(f"{DB_QUERY_FAILED} {DB_COMMIT_FAILED}") from error

    async def rollback(self) -> None:
        await self._session.rollback()


class SqlaTransactionManager(TransactionManager):
    def __init__(self, session: Session):
        self._session = session

    def commit(self) -> None:
        try:
            self._session.commit()

        except SQLAlchemyError as error:
            raise DataMapperError(f"{DB_QUERY_FAILED} {DB_COMMIT_FAILED}") from error

    def rollback(self) -> None:
        self._session.rollback()
