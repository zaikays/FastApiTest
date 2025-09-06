from dishka import Provider
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.presentation.controllers.root_router import root_router
from app.setup.app_factory import (
    create_fast_app,
    configure_app,
    create_async_ioc_container,
)
from app.setup.config.settings import AppSettings, load_settings
from app.setup.ioc.provider_registry import get_providers


def make_app(
    *di_providers: Provider,
    settings: AppSettings | None = None,
):
    if settings is None:
        settings = load_settings()

    app: FastAPI = create_fast_app()
    configure_app(app=app, root_router=root_router)
    async_ioc_container = create_async_ioc_container(
        providers=(*get_providers(), *di_providers),
        settings=settings,
    )
    setup_dishka(container=async_ioc_container, app=app)
    return app


app = make_app()
