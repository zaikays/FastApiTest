from inspect import getdoc

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile
from starlette import status

from app.application.handlers.network_upload_handler import NetworkUploadHandler
from app.presentation.dtos.network import RoadNetworkResponse

create_network_router = APIRouter()


@create_network_router.post(
    "/upload",
    description=getdoc(NetworkUploadHandler),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_network(
    file: UploadFile,
    handler: FromDishka[NetworkUploadHandler],
) -> RoadNetworkResponse:
    return await handler.execute(file)
