from typing import Any

from pydantic import BaseModel

from app.setup.config.database import PostgresSettings, SqlaEngineSettings
from app.setup.config.loader import ValidEnvs, get_current_env, load_full_config
from app.setup.config.security import SecuritySettings


class AppSettings(BaseModel):
    postgres: PostgresSettings
    sqla: SqlaEngineSettings
    security: SecuritySettings


def get_key_specified_envs(key_prefix: str, raw_config: dict) -> dict[str, Any]:
    return {k: v for k, v in raw_config.items() if k.startswith(key_prefix)}


def load_settings(env: ValidEnvs | None = None) -> AppSettings:
    if env is None:
        env = get_current_env()
    raw_config = load_full_config(env=env)
    raw_config = {
        "postgres": get_key_specified_envs("POSTGRES_", raw_config),
        "sqla": get_key_specified_envs("SQLA_", raw_config),
        "security": get_key_specified_envs("SECURITY_", raw_config),
    }
    return AppSettings.model_validate(raw_config)
