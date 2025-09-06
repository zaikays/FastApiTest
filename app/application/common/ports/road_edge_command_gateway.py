from abc import abstractmethod
from typing import Protocol

from app.adapters.models.edge_model import RoadEdgeModel


class RoadEdgeCommandGatewayAsync(Protocol):
    @abstractmethod
    async def add(self, road_edge: RoadEdgeModel) -> None: ...


class RoadEdgeCommandGateway(Protocol):
    @abstractmethod
    def add(self, road_edge: RoadEdgeModel) -> None: ...
