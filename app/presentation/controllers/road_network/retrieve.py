from inspect import getdoc

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query
from starlette import status

from app.application.handlers.network_edges_handler import NetworkEdgesHandler
from app.presentation.dtos.network import RoadEdgesResponse

retrieve_network_router = APIRouter()


@retrieve_network_router.get(
    "/<network_id>/edges",
    description=getdoc(NetworkEdgesHandler),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def retrieve_network_edges(
    network_id: int,
    version: int | None = Query(None),
    handler: FromDishka[NetworkEdgesHandler] = None,
) -> RoadEdgesResponse:
    return await handler.execute(network_id, version)
