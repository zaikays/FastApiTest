from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.adapters.constants.db_const import DB_QUERY_FAILED
from app.adapters.exceptions.gateway import DataMapperError
from app.adapters.models import RoadNetworkVersionModel
from app.application.common.ports.road_network_version_command_gateway import (
    RoadNetworkVersionCommandGatewayAsync,
    RoadNetworkVersionCommandGateway,
)


class SqlaRoadNetworkVersionDataMapperAsync(RoadNetworkVersionCommandGatewayAsync):

    def __init__(
        self,
        session_async: AsyncSession,
    ):
        self._session_async = session_async

    async def read_by_id_async(
        self, road_network_version_id: int, for_update: bool = False
    ) -> RoadNetworkVersionModel | None:
        select_stmt = select(RoadNetworkVersionModel).where(
            RoadNetworkVersionModel.id == road_network_version_id
        )

        if for_update:
            select_stmt = select_stmt.with_for_update()

        result = await self._session_async.execute(select_stmt)
        road_network_db_model = result.scalar_one_or_none()
        if road_network_db_model:
            return road_network_db_model
        return None

    async def add_async(self, road_network_version: RoadNetworkVersionModel) -> None:
        current_max_version = await self._session_async.scalar(
            select(func.max(RoadNetworkVersionModel.version_number)).where(
                RoadNetworkVersionModel.network_id == road_network_version.network_id
            )
        )
        road_network_version.version_number = (current_max_version or 0) + 1

        try:
            self._session_async.add(road_network_version)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error


class SqlaRoadNetworkVersionDataMapper(RoadNetworkVersionCommandGateway):
    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def read_by_id(
        self, road_network_version_id: int, for_update: bool = False
    ) -> RoadNetworkVersionModel | None:
        select_stmt = select(RoadNetworkVersionModel).where(
            RoadNetworkVersionModel.id == road_network_version_id
        )
        if for_update:
            select_stmt = select_stmt.with_for_update()

        result = self._session.execute(select_stmt)
        road_network_db_model = result.scalar_one_or_none()
        if road_network_db_model:
            return road_network_db_model
        return None
