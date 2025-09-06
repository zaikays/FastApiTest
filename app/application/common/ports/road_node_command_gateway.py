import decimal
from abc import abstractmethod
from typing import Protocol, List

from asyncpg import Point

from app.adapters.models.node_model import RoadNodeModel


class RoadNodeCommandGatewayAsync(Protocol):
    @abstractmethod
    async def add(self, road_node: RoadNodeModel) -> None: ...

    @abstractmethod
    async def add_all(self, road_nodes: List[RoadNodeModel]) -> None: ...

    @abstractmethod
    async def read_by_id(self, road_node_id: int) -> RoadNodeModel | None: ...


class RoadNodeCommandGateway(Protocol):
    @abstractmethod
    def add(self, road_node: RoadNodeModel) -> None: ...

    @abstractmethod
    def insert(
        self,
        network_id: int,
        cords: List[decimal] | Point,
        on_conflict_do_nothing=False,
    ) -> None | RoadNodeModel: ...

    @abstractmethod
    def add_all(self, road_nodes: List[RoadNodeModel]) -> None: ...

    @abstractmethod
    def read_by_id(self, road_node_id: int) -> RoadNodeModel | None: ...
