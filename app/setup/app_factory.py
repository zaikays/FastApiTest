from collections.abc import Iterable
from contextlib import asynccontextmanager

from dishka import Provider, AsyncContainer, make_async_container
from fastapi import FastAPI, APIRouter
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.presentation.exceptions.handlers import setup_handlers
from app.setup.config.settings import AppSettings


def create_fast_app() -> FastAPI:
    return FastAPI(
        title="RoadNetwork",
        description="A basic MVP to work with GEOJson",
        version="0.0.1",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )


def configure_app(app: FastAPI, root_router: APIRouter) -> None:
    app.include_router(root_router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )
    setup_handlers(app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_async_ioc_container(
    providers: Iterable[Provider],
    settings: AppSettings,
) -> AsyncContainer:
    return make_async_container(
        *providers,
        context={AppSettings: settings},
    )
