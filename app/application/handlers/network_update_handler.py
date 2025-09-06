import logging

from fastapi import UploadFile

from app.adapters.models import RoadNetworkVersionModel
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
from app.domain.exceptions.base import DomainFieldError

from app.presentation.dtos.network import RoadNetworkResponse

log = logging.getLogger(__name__)


class NetworkUpdateHandler:
    def __init__(
        self,
        transaction_manager: TransactionManagerAsync,
        current_user_service: CurrentUserService,
        file_service: FileService,
        road_network_command_gateway: RoadNetworkCommandGatewayAsync,
        road_network_version_command_gateway_async: RoadNetworkVersionCommandGatewayAsync,
        celery_service: CeleryService,
        flusher: FlusherAsync,
    ):
        self._current_user_service = current_user_service
        self._file_service = file_service
        self._road_network_command_gateway = road_network_command_gateway
        self._road_network_version_command_gateway_async = (
            road_network_version_command_gateway_async
        )
        self._transaction_manager = transaction_manager
        self._flusher = flusher
        self._celery_service = celery_service

    async def execute(self, network_id: int, file: UploadFile) -> RoadNetworkResponse:
        user = await self._current_user_service.get_current_user()
        self._file_service.validate_file_extension(file.filename, [".geojson", ".json"])
        road_network = await self._road_network_command_gateway.read_by_id(network_id)
        if (
            road_network and road_network.customer_id != user.id
        ) or not road_network is not None:
            raise DomainFieldError(f"Not found network with id {network_id}")
        file_name = await self._file_service.upload_file(file.file, file.filename)
        road_network_version = RoadNetworkVersionModel(
            network_id=road_network.id,
            file_name=file_name,
        )
        await self._road_network_version_command_gateway_async.add_async(
            road_network_version
        )
        await self._flusher.flush()

        await self._transaction_manager.commit()
        self._celery_service.parse_geojson(road_network_version.id)

        return RoadNetworkResponse(road_network_id=road_network.id)
