from inspect import getdoc

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile
from starlette import status

from app.application.handlers.network_update_handler import NetworkUpdateHandler
from app.presentation.dtos.network import RoadNetworkResponse

update_network_router = APIRouter()


@update_network_router.patch(
    "/network_id>/update",
    description=getdoc(NetworkUpdateHandler),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def update_network(
    network_id: int, file: UploadFile, handler: FromDishka[NetworkUpdateHandler]
) -> RoadNetworkResponse:
    return await handler.execute(network_id, file)
