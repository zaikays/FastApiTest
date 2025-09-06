from dishka import provide, Provider, Scope, provide_all
from fastapi.security import HTTPAuthorizationCredentials

from app.adapters.auth.jwt_processor import (
    JwtAccessTokenProcessor,
    JwtAlgorithm,
    JwtSecret,
)
from app.adapters.auth.utils.auth_token_timer import (
    UtcAuthTokenTimer,
    AuthAccessTokenTtlMin,
    AuthRefreshTokenTtlMin,
)
from app.adapters.services.bcrypt_hasher import BcryptHasher
from app.adapters.services.celery_service import (
    CeleryService,
    CeleryBrokerUrl,
    CeleryResultBackend,
)
from app.adapters.services.current_user_service import CurrentUserService
from app.adapters.services.file_service import FileService
from app.adapters.services.redis_client import RedisClient, RedisEndpointUrl, RedisPort
from app.adapters.services.s3_store_client import (
    S3EndpointUrl,
    S3AccessKey,
    S3BucketName,
    S3Client,
    S3SecretKey,
)
from app.application.handlers.login_handler import LoginHandler
from app.application.handlers.network_edges_handler import NetworkEdgesHandler
from app.application.handlers.network_upload_handler import NetworkUploadHandler
from app.application.handlers.network_update_handler import NetworkUpdateHandler
from app.application.handlers.sign_up_handler import SignUpHandler
from app.application.services.user_service import UserService
from app.domain.services.password_hasher import PasswordHasher
from app.presentation.controllers.fastapi_openapi_markers import bearer_scheme
from fastapi import Request


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.REQUEST)
    def get_token_processor(
        self, secret: JwtSecret, algorithm: JwtAlgorithm
    ) -> JwtAccessTokenProcessor:
        return JwtAccessTokenProcessor(secret, algorithm)

    @provide(scope=Scope.REQUEST)
    def get_s3_client(
        self,
        endpoint_url: S3EndpointUrl,
        access_key: S3AccessKey,
        secret_key: S3SecretKey,
        bucket_name: S3BucketName,
    ) -> S3Client:
        return S3Client(endpoint_url, access_key, secret_key, bucket_name)

    @provide(scope=Scope.REQUEST)
    def get_redis_client(
        self, endpoint_url: RedisEndpointUrl, port: RedisPort
    ) -> RedisClient:
        return RedisClient(endpoint_url, port)

    @provide(scope=Scope.REQUEST)
    def get_celery_client(
        self,
        celery_broker_url: CeleryBrokerUrl,
        celery_result_backend: CeleryResultBackend,
    ) -> CeleryService:
        return CeleryService(celery_broker_url, celery_result_backend)

    @provide(scope=Scope.REQUEST)
    def token_timer(
        self,
        auth_access_token_ttl_min: AuthAccessTokenTtlMin,
        auth_refresh_token_ttl_min: AuthRefreshTokenTtlMin,
    ) -> UtcAuthTokenTimer:
        return UtcAuthTokenTimer(auth_access_token_ttl_min, auth_refresh_token_ttl_min)

    @provide(scope=Scope.REQUEST)
    def request_provider(self) -> Request:
        return Request(scope=self.scope.value)

    @provide(scope=Scope.REQUEST)
    async def get_credentials(self, request: Request) -> HTTPAuthorizationCredentials:
        return await bearer_scheme(request)

    password_hasher = provide(
        source=BcryptHasher,
        provides=PasswordHasher,
    )

    services = provide_all(
        UserService,
        CurrentUserService,
        FileService,
    )

    handlers = provide_all(
        SignUpHandler,
        LoginHandler,
        NetworkUploadHandler,
        NetworkUpdateHandler,
        NetworkEdgesHandler,
    )
