import os
from typing import Final

from pydantic import BaseModel, Field, PostgresDsn, field_validator

PORT_MIN: Final[int] = 1
PORT_MAX: Final[int] = 65535


class PostgresSettings(BaseModel):
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    db: str = Field(alias="POSTGRES_DB")
    host: str = Field(
        alias="POSTGRES_HOST", default=os.getenv("POSTGRES_HOST", "localhost")
    )
    port: int = Field(alias="POSTGRES_PORT")
    driver: str = Field(alias="POSTGRES_DRIVER", default="asyncpg")

    @field_validator("host", mode="before")
    @classmethod
    def override_host_from_env(cls, v: str) -> str:
        postgres_host_env = os.environ.get("POSTGRES_HOST")
        if postgres_host_env:
            return postgres_host_env
        return v

    @field_validator("port")
    @classmethod
    def validate_port_range(cls, v: int) -> int:
        if not PORT_MIN <= v <= PORT_MAX:
            raise ValueError(f"Port must be between {PORT_MIN} and {PORT_MAX}")
        return v

    @property
    def dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{self.driver}",
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db,
            ),
        )


class SqlaEngineSettings(BaseModel):
    echo: bool = Field(alias="ECHO", default=False)
    echo_pool: bool = Field(alias="ECHO_POOL", default=False)
    pool_size: int = Field(alias="POOL_SIZE", default=50)
    max_overflow: int = Field(alias="MAX_OVERFLOW", default=10)
