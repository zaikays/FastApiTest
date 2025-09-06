from dishka import Provider, Scope, from_context, provide
from pydantic import PostgresDsn

from app.adapters.auth.jwt_processor import JwtSecret, JwtAlgorithm
from app.adapters.auth.utils.auth_token_timer import (
    AuthAccessTokenTtlMin,
    AuthRefreshTokenTtlMin,
)
from app.adapters.services.bcrypt_hasher import PasswordPepper
from app.adapters.services.celery_service import CeleryBrokerUrl, CeleryResultBackend
from app.adapters.services.redis_client import RedisEndpointUrl, RedisPort
from app.adapters.services.s3_store_client import (
    S3EndpointUrl,
    S3AccessKey,
    S3SecretKey,
    S3BucketName,
)
from app.setup.config.settings import AppSettings


class SettingsProvider(Provider):
    scope = Scope.APP

    settings = from_context(provides=AppSettings)

    @provide
    def provide_postgres_dsn(self, settings: AppSettings) -> PostgresDsn:
        return PostgresDsn(settings.postgres.dsn)

    @provide
    def provide_password_pepper(self, settings: AppSettings) -> PasswordPepper:
        return PasswordPepper(settings.security.password_pepper)

    @provide
    def provide_jwt_secret(self, settings: AppSettings) -> JwtSecret:
        return JwtSecret(settings.security.jwt_secret)

    @provide
    def provide_jwt_algorithm(self, settings: AppSettings) -> JwtAlgorithm:
        return settings.security.jwt_algorithm

    @provide
    def provide_access_token_ttl_min(
        self, settings: AppSettings
    ) -> AuthAccessTokenTtlMin:
        return AuthAccessTokenTtlMin(settings.security.jwt_access_token_ttl_min)

    @provide
    def provide_refresh_token_ttl_min(
        self, settings: AppSettings
    ) -> AuthRefreshTokenTtlMin:
        return AuthRefreshTokenTtlMin(settings.security.jwt_refresh_token_ttl_min)

    @provide
    def provide_s3_endpoint_url(self, settings: AppSettings) -> S3EndpointUrl:
        return S3EndpointUrl(settings.security.s3_endpoint_url)

    @provide
    def provide_s3_access_key(self, settings: AppSettings) -> S3AccessKey:
        return S3AccessKey(settings.security.s3_access_key)

    @provide
    def provide_s3_secret_key(self, settings: AppSettings) -> S3SecretKey:
        return S3SecretKey(settings.security.s3_secret_key)

    @provide
    def provide_s3_bucket_name(self, settings: AppSettings) -> S3BucketName:
        return S3BucketName(settings.security.s3_bucket_name)

    @provide
    def provide_redis_host(self, settings: AppSettings) -> RedisEndpointUrl:
        return RedisEndpointUrl(settings.security.redis_host)

    @provide
    def provide_redis_port(self, settings: AppSettings) -> RedisPort:
        return RedisPort(settings.security.redis_port)

    @provide
    def provide_celery_broker_url(self, settings: AppSettings) -> CeleryBrokerUrl:
        return CeleryBrokerUrl(settings.security.celery_broker_url)

    @provide
    def provide_celery_result_backend(
        self, settings: AppSettings
    ) -> CeleryResultBackend:
        return CeleryResultBackend(settings.security.celery_result_backend)
