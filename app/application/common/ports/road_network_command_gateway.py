from abc import abstractmethod
from typing import Protocol

from app.adapters.models.road_network_model import RoadNetworkModel


class RoadNetworkCommandGatewayAsync(Protocol):

    @abstractmethod
    async def read_by_id(self, road_network_id: int) -> RoadNetworkModel | None: ...

    @abstractmethod
    async def add(self, road_network: RoadNetworkModel) -> None: ...


class RoadNetworkCommandGateway(Protocol):

    @abstractmethod
    def read_by_id(self, road_network_id: int) -> RoadNetworkModel | None: ...

    @abstractmethod
    def add(self, road_network: RoadNetworkModel) -> None: ...
