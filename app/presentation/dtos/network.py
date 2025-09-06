from dataclasses import dataclass
from typing import TypedDict, List

from fastapi import UploadFile


@dataclass(frozen=True, slots=True, kw_only=True)
class NetworkFileRequest:
    file: UploadFile


class RoadNetworkResponse(TypedDict):
    road_network_id: int


class RoadEdgeResponse(TypedDict):
    type: str
    geometry: dict
    properties: dict


class RoadEdgesResponse(TypedDict):
    features: List[RoadEdgeResponse]
