from inspect import getdoc

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.application.handlers.login_handler import LoginHandler
from app.presentation.dtos.auth import LoginRequest, LoginResponse

login_router = APIRouter()


@login_router.post(
    "/login",
    description=getdoc(LoginHandler),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def login(
    request_data: LoginRequest, handler: FromDishka[LoginHandler]
) -> LoginResponse:
    return await handler.execute(request_data)
