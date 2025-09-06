from fastapi import APIRouter

from app.presentation.controllers.auth.router import auth_router
from app.presentation.controllers.road_network.router import network_router

api_v1_router = APIRouter(
    prefix="/api/v1",
)

api_v1_sub_routers: tuple[APIRouter, ...] = (auth_router, network_router)


for router in api_v1_sub_routers:
    api_v1_router.include_router(router)
