from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.constants.db_const import DB_QUERY_FAILED
from app.adapters.exceptions.gateway import DataMapperError
from app.adapters.models.road_network_model import RoadNetworkModel
from app.application.common.ports.road_network_command_gateway import (
    RoadNetworkCommandGatewayAsync,
    RoadNetworkCommandGateway,
)


class SqlaRoadNetworkDataMapperAsync(RoadNetworkCommandGatewayAsync):

    def __init__(
        self,
        session: AsyncSession,
    ):
        self._session = session

    async def read_by_id(self, road_network_id: int) -> RoadNetworkModel | None:
        stmt = select(RoadNetworkModel).where(RoadNetworkModel.id == road_network_id)
        result = await self._session.execute(stmt)
        road_network_db_model = result.scalar_one_or_none()
        if road_network_db_model:
            return road_network_db_model
        return None

    async def add(self, road_network: RoadNetworkModel) -> None:
        try:
            self._session.add(road_network)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error


class SqlaRoadNetworkDataMapper(RoadNetworkCommandGateway):

    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def read_by_id(self, road_network_id: int) -> RoadNetworkModel | None:
        stmt = select(RoadNetworkModel).where(RoadNetworkModel.id == road_network_id)
        result = self._session.execute(stmt)
        road_network_db_model = result.scalar_one_or_none()
        if road_network_db_model:
            return road_network_db_model
        return None

    def add(self, road_network: RoadNetworkModel) -> None:
        try:
            self._session.add(road_network)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error
