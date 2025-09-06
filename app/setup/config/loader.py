import logging
import os
from collections.abc import Mapping
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final

from dotenv import dotenv_values

ConfigDict = dict[str, Any]

log = logging.getLogger(__name__)

ENV_VAR_NAME: Final[str] = "APP_ENV"


class ValidEnvs(StrEnum):
    LOCAL = "local"
    PROD = "prod"


def validate_env(env: str | None) -> ValidEnvs:
    if env is None:
        raise ValueError(f"{ENV_VAR_NAME} is not set.")
    try:
        return ValidEnvs(env)
    except ValueError as e:
        valid_values = ", ".join(f"'{e}'" for e in ValidEnvs)
        raise ValueError(
            f"Invalid {ENV_VAR_NAME}: '{env}'. Must be one of: {valid_values}.",
        ) from e


def get_current_env() -> ValidEnvs:
    return validate_env(os.getenv(ENV_VAR_NAME))


BASE_DIR_PATH = Path(__file__).resolve().parents[3]
CONFIG_PATH: Final[Path] = BASE_DIR_PATH / "config"

ENV_TO_DIR_PATHS: Final[Mapping[ValidEnvs, Path]] = MappingProxyType(
    {
        ValidEnvs.LOCAL: CONFIG_PATH / ValidEnvs.LOCAL,
        ValidEnvs.PROD: CONFIG_PATH / ValidEnvs.PROD,
    }
)


def load_full_config(
    env: ValidEnvs,
    dir_paths: Mapping[ValidEnvs, Path] = ENV_TO_DIR_PATHS,
) -> ConfigDict:
    dir_path = dir_paths.get(env)
    if dir_path is None:
        raise FileNotFoundError(f"No directory path configured for environment: {env}")
    file_path = dir_path / ".env"
    if not file_path.is_file():
        raise FileNotFoundError(
            f"The file does not exist at the specified path: {file_path}",
        )
    values = dotenv_values(file_path)
    return ConfigDict(values)
