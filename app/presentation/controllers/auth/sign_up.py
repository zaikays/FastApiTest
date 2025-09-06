from inspect import getdoc

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from starlette import status

from app.application.handlers.sign_up_handler import SignUpHandler
from app.presentation.dtos.auth import SignUpRequest, SignUpResponse

sign_up_router = APIRouter()


@sign_up_router.post(
    "/sign-up",
    description=getdoc(SignUpHandler),
    status_code=status.HTTP_201_CREATED,
)
@inject
async def sign_up(
    request_data: SignUpRequest, handler: FromDishka[SignUpHandler]
) -> SignUpResponse:
    return await handler.execute(request_data)
