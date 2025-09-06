from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.adapters.constants.db_const import DB_QUERY_FAILED
from app.adapters.exceptions.gateway import DataMapperError
from app.application.common.ports.user_command_gateway import UserCommandGatewayAsync
from app.adapters.models.user_model import UserModel
from app.domain.models.value_objects.email.email import Email


class SqlaUserDataMapperAsync(UserCommandGatewayAsync):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def read_by_id(self, user_id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        user_db_model = result.scalar_one_or_none()
        if user_db_model:
            return user_db_model
        return None

    async def add(self, user: UserModel) -> None:
        try:
            self._session.add(user)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def read_by_email(self, email: Email, for_update=False) -> UserModel | None:
        select_stmt = select(UserModel).where(UserModel.email == email.value)

        if for_update:
            select_stmt = select_stmt.with_for_update()

        try:
            user: UserModel | None = (
                await self._session.execute(select_stmt)
            ).scalar_one_or_none()
            return user
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error
