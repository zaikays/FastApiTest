from abc import abstractmethod
from typing import Protocol

from app.adapters.models.road_network_version_model import RoadNetworkVersionModel


class RoadNetworkVersionCommandGatewayAsync(Protocol):
    @abstractmethod
    async def add_async(
        self, road_network_version: RoadNetworkVersionModel
    ) -> None: ...

    @abstractmethod
    async def read_by_id_async(
        self,
        road_network_version_id: int,
        for_update: bool = False,
    ) -> RoadNetworkVersionModel | None: ...


class RoadNetworkVersionCommandGateway(Protocol):
    @abstractmethod
    def read_by_id(
        self,
        road_network_version_id: int,
        for_update: bool = False,
    ) -> RoadNetworkVersionModel | None: ...
