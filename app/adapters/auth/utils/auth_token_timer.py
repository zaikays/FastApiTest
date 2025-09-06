from datetime import UTC, datetime, timedelta
from typing import NewType

AuthAccessTokenTtlMin = NewType("AuthAccessTokenTtlMin", timedelta)
AuthRefreshTokenTtlMin = NewType("AuthRefreshTokenTtlMin", timedelta)


class UtcAuthTokenTimer:
    def __init__(
        self,
        auth_access_token_ttl_min: AuthAccessTokenTtlMin,
        auth_refresh_token_ttl_min: AuthRefreshTokenTtlMin,
    ):
        self._auth_access_token_ttl_min = auth_access_token_ttl_min
        self._auth_refresh_token_ttl_min = auth_refresh_token_ttl_min

    @property
    def current_time(self) -> datetime:
        return datetime.now(tz=UTC)

    @property
    def auth_access_token_expiration(self) -> datetime:
        return self.current_time + self._auth_access_token_ttl_min

    @property
    def auth_refresh_token_expiration(self) -> datetime:
        return self.current_time + self._auth_refresh_token_ttl_min
