from collections.abc import Iterable

from dishka import Provider

from app.setup.ioc.application import ApplicationProvider
from app.setup.ioc.database import DatabaseProviderAsync
from app.setup.ioc.settings import SettingsProvider


def get_providers() -> Iterable[Provider]:
    return (
        ApplicationProvider(),
        DatabaseProviderAsync(),
        SettingsProvider(),
    )
