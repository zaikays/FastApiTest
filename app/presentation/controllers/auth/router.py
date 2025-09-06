from fastapi import APIRouter

from app.presentation.controllers.auth.login import login_router
from app.presentation.controllers.auth.sign_up import sign_up_router

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)
account_sub_routers: tuple[APIRouter, ...] = (
    sign_up_router,
    login_router,
)

for router in account_sub_routers:
    auth_router.include_router(router)
