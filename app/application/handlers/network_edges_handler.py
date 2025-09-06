import logging

from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.adapters.models import RoadNetworkVersionModel
from app.adapters.models.road_network_model import RoadNetworkModel
from app.adapters.services.celery_service import CeleryService
from app.adapters.services.current_user_service import CurrentUserService
from app.adapters.services.file_service import FileService
from app.application.common.ports.flusher import FlusherAsync
from app.application.common.ports.road_network_command_gateway import (
    RoadNetworkCommandGatewayAsync,
)
from app.application.common.ports.road_network_version_command_gateway import (
    RoadNetworkVersionCommandGatewayAsync,
)
from app.application.common.ports.transaction_manager import TransactionManagerAsync
from app.presentation.dtos.network import RoadEdgesResponse

log = logging.getLogger(__name__)


class NetworkEdgesHandler:
    def __init__(
        self,
        road_network_command_gateway: RoadNetworkCommandGatewayAsync,
        road_network_version_command_gateway_async: RoadNetworkVersionCommandGatewayAsync,
        flusher: FlusherAsync,
        transaction_manager: TransactionManagerAsync,
        current_user_service: CurrentUserService,
        file_service: FileService,
        celery_service: CeleryService,
        session_async: AsyncSession,
    ):
        self._session_async = session_async
        self._transaction_manager = transaction_manager
        self._flusher = flusher
        self._road_network_command_gateway = road_network_command_gateway
        self._road_network_version_command_gateway_async = (
            road_network_version_command_gateway_async
        )
        self._current_user_service = current_user_service
        self._file_service = file_service
        self._celery_service = celery_service

    async def execute(
        self, network_id: int, version_number: int | None
    ) -> RoadEdgesResponse:
        current_user = await self._current_user_service.get_current_user()

        stmt = (
            select(RoadNetworkVersionModel)
            .join(RoadNetworkModel)
            .where(
                RoadNetworkModel.customer_id == current_user.id,
                RoadNetworkModel.id == network_id,
            )
            .options(joinedload(RoadNetworkVersionModel.road_edges))
        )
        if version_number is not None:
            stmt = stmt.where(RoadNetworkVersionModel.version_number == version_number)
        else:
            stmt = stmt.order_by(desc(RoadNetworkVersionModel.version_number))
        result = await self._session_async.execute(stmt)
        network_version = result.scalars().first()

        features = []
        if network_version is None:
            return RoadEdgesResponse(features=features)
        for edge in network_version.road_edges:
            geom = to_shape(edge.geometry)
            features.append(
                {
                    "type": "Feature",
                    "geometry": mapping(geom),
                    "properties": edge.properties,
                }
            )
        return RoadEdgesResponse(features=features)
