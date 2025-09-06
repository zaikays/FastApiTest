from fastapi import APIRouter, Security

from app.presentation.controllers.fastapi_openapi_markers import bearer_scheme
from app.presentation.controllers.road_network.retrieve import retrieve_network_router
from app.presentation.controllers.road_network.update import update_network_router
from app.presentation.controllers.road_network.upload import create_network_router

network_router = APIRouter(
    prefix="/networks", tags=["Networks"], dependencies=[Security(bearer_scheme)]
)
network_sub_routers: tuple[APIRouter, ...] = (
    create_network_router,
    update_network_router,
    retrieve_network_router,
)

for router in network_sub_routers:
    network_router.include_router(router)
