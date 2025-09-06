from datetime import timedelta
from typing import Literal, Any
from pydantic import BaseModel, Field, field_validator


class SecuritySettings(BaseModel):
    password_pepper: str = Field(alias="SECURITY_PASSWORD_PEPPER")
    jwt_algorithm: Literal[
        "HS256",
        "HS384",
        "HS512",
        "RS256",
        "RS384",
        "RS512",
    ] = Field(alias="SECURITY_JWT_ALGORITHM")
    jwt_secret: str = Field(alias="SECURITY_JWT_SECRET")
    jwt_access_token_ttl_min: timedelta = Field(
        alias="SECURITY_JWT_ACCESS_TOKEN_TTL_MIN"
    )
    jwt_refresh_token_ttl_min: timedelta = Field(
        alias="SECURITY_JWT_REFRESH_TOKEN_TTL_MIN"
    )
    s3_endpoint_url: str = Field(alias="SECURITY_S3_ENDPOINT_URL")
    s3_access_key: str = Field(alias="SECURITY_S3_ACCESS_KEY")
    s3_secret_key: str = Field(alias="SECURITY_S3_SECRET_KEY")
    s3_bucket_name: str = Field(alias="SECURITY_S3_BUCKET_NAME")
    redis_host: str = Field(alias="SECURITY_REDIS_HOST")
    redis_port: int = Field(alias="SECURITY_REDIS_PORT")
    celery_broker_url: str = Field(alias="SECURITY_CELERY_BROKER_URL")
    celery_result_backend: str = Field(alias="SECURITY_CELERY_RESULT_BACKEND")

    @field_validator("jwt_access_token_ttl_min", mode="before")
    @classmethod
    def convert_access_token_ttl_min(cls, v: Any) -> timedelta:
        if v.isdigit():
            v = float(v)
        if not isinstance(v, (int, float)):
            raise ValueError(
                "SECURITY_JWT_ACCESS_TOKEN_TTL_MIN must be a number (n of minutes, n >= 1)."
            )
        if v < 1:
            raise ValueError(
                "SECURITY_JWT_ACCESS_TOKEN_TTL_MIN must be at least 1 (n of minutes)."
            )
        return timedelta(minutes=v)

    @field_validator("jwt_refresh_token_ttl_min", mode="before")
    @classmethod
    def convert_refresh_token_ttl_min(cls, v: Any) -> timedelta:
        if v.isdigit():
            v = float(v)
        if not isinstance(v, (int, float)):
            raise ValueError(
                "REFRESH_TOKEN_TTL_MIN must be a number (n of minutes, n >= 1)."
            )
        if v < 1:
            raise ValueError("REFRESH_TOKEN_TTL_MIN must be at least 1 (n of minutes).")
        return timedelta(minutes=v)
