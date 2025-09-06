from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.constants.db_const import DB_QUERY_FAILED
from app.adapters.exceptions.gateway import DataMapperError
from app.adapters.models.edge_model import RoadEdgeModel
from app.application.common.ports.road_edge_command_gateway import (
    RoadEdgeCommandGatewayAsync,
    RoadEdgeCommandGateway,
)


class SqlaRoadEdgeDataMapperAsync(RoadEdgeCommandGatewayAsync):

    def __init__(
        self,
        session_async: AsyncSession,
    ):
        self._session_async = session_async

    async def read_by_id(self, road_edge_id: int) -> RoadEdgeModel | None:
        stmt = select(RoadEdgeModel).where(RoadEdgeModel.id == road_edge_id)
        result = await self._session_async.execute(stmt)
        road_edge_db_model = result.scalar_one_or_none()
        if road_edge_db_model:
            return road_edge_db_model
        return None

    async def add(self, road_edge: RoadEdgeModel) -> None:
        try:
            self._session_async.add(road_edge)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error


class SqlaRoadEdgeDataMapper(RoadEdgeCommandGateway):

    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def read_by_id(self, road_edge_id: int) -> RoadEdgeModel | None:
        stmt = select(RoadEdgeModel).where(RoadEdgeModel.id == road_edge_id)
        result = self._session.execute(stmt)
        road_edge_db_model = result.scalar_one_or_none()
        if road_edge_db_model:
            return road_edge_db_model
        return None

    def add(self, road_edge: RoadEdgeModel) -> None:
        try:
            self._session.add(road_edge)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error
