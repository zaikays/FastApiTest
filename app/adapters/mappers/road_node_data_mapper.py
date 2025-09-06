import decimal
from typing import List

from geoalchemy2.shape import from_shape
from shapely import Point
from sqlalchemy.orm import Session

from app.adapters.models import RoadNodeModel
from app.application.common.ports.road_node_command_gateway import (
    RoadNodeCommandGatewayAsync,
    RoadNodeCommandGateway,
)

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from app.adapters.constants.db_const import DB_QUERY_FAILED
from app.adapters.exceptions.gateway import DataMapperError


class SqlaRoadNodeDataMapperAsync(RoadNodeCommandGatewayAsync):

    def __init__(
        self,
        session_async: AsyncSession,
    ):
        self._session_async = session_async

    async def read_by_id(self, road_node_id: int) -> RoadNodeModel | None:
        stmt = select(RoadNodeModel).where(RoadNodeModel.id == road_node_id)
        result = await self._session_async.execute(stmt)
        road_node_db_model = result.scalar_one_or_none()
        if road_node_db_model:
            return road_node_db_model
        return None

    async def add(self, road_node: RoadNodeModel) -> None:
        try:
            self._session_async.add(road_node)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    async def add_all(self, road_nodes: List[RoadNodeModel]) -> None:
        try:
            self._session_async.add_all(road_nodes)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error


class SqlaRoadNodeDataMapper(RoadNodeCommandGateway):

    def __init__(
        self,
        session: Session,
    ):
        self._session = session

    def read_by_id(self, road_node_id: int) -> RoadNodeModel | None:
        stmt = select(RoadNodeModel).where(RoadNodeModel.id == road_node_id)
        result = self._session.execute(stmt)
        road_node_db_model = result.scalar_one_or_none()
        if road_node_db_model:
            return road_node_db_model
        return None

    def add(self, road_node: RoadNodeModel) -> None:
        try:
            self._session.add(road_node)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error

    def insert(
        self,
        network_id: int,
        cords: List[decimal] | Point,
        on_conflict_do_nothing=False,
    ) -> RoadNodeModel | None:
        cords = cords if isinstance(cords, Point) else Point(cords[0], cords[1])
        stmt = insert(RoadNodeModel).values(
            network_id=network_id,
            geometry=from_shape(cords, srid=4326),
        )
        if on_conflict_do_nothing:
            stmt = stmt.on_conflict_do_nothing(
                index_elements=["network_id", "geometry"]
            )
        stmt = stmt.returning(RoadNodeModel)
        result = self._session.execute(stmt)
        node = result.scalars().first()
        if not node and on_conflict_do_nothing:
            node = (
                self._session.execute(
                    select(RoadNodeModel).where(
                        RoadNodeModel.network_id == network_id,
                        RoadNodeModel.geometry == from_shape(cords, srid=4326),
                    )
                )
                .scalars()
                .first()
            )
        return node

    def add_all(self, road_nodes: List[RoadNodeModel]) -> None:
        try:
            self._session.add_all(road_nodes)
        except SQLAlchemyError as error:
            raise DataMapperError(DB_QUERY_FAILED) from error
