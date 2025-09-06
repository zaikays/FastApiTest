import asyncio
from dishka import make_async_container

from app.setup.ioc.provider_registry import get_providers
from app.setup.config.settings import load_settings, AppSettings
from app.adapters.services.celery_service import CeleryService

settings = load_settings()
container = make_async_container(
    *get_providers(),
    context={AppSettings: settings},
)


async def get_app_app_settings():
    return await container.get(AppSettings)


app_settings = asyncio.run(get_app_app_settings())

celery_service = CeleryService(
    app_settings.security.celery_broker_url, app_settings.security.celery_result_backend
)

app = celery_service.app
