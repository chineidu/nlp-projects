from pathlib import Path
from typing import Any, Optional, Union

import yaml  # type: ignore[import]
from typeguard import typechecked

# Custom Imports
import e_commerce_app
from e_commerce_app.logger_config import logger
from e_commerce_app.v1.schemas.api_schema import APIConfigSchema, ConfigVars, PathConfig

SRC_ROOT: Path = Path(e_commerce_app.__file__).absolute().parent  # src/
ROOT: Path = SRC_ROOT.parent  # proj/src
CONFIG_FILEPATH: Path = SRC_ROOT / "config/config.yaml"


@typechecked
def load_yaml_file(*, filename: Optional[Path] = None) -> Union[dict[str, Any], None]:
    """This loads the YAML file as a dict."""
    if filename is None:
        filename = CONFIG_FILEPATH

    try:
        with open(filename, "r") as file:
            config_dict = yaml.safe_load(stream=file)
            logger.info("Config file successfully loaded!")
            return config_dict

    except FileNotFoundError as err:
        logger.error(f"No config file found! {err}")
        return None


@typechecked
def validate_config_file(*, filename: Optional[Path] = None) -> ConfigVars:
    """This loads the config as a Pydantic object."""
    config_dict = load_yaml_file(filename=filename)

    # Validate config
    config_file = ConfigVars(
        api_config_schema=APIConfigSchema(**config_dict),  # type: ignore
        path_config=PathConfig(**config_dict),  # type: ignore
    )
    return config_file


config: ConfigVars = validate_config_file(filename=None)
DB_PATH: Path = ROOT / config.path_config.DB_PATH
ENV_PATH: Path = ROOT / config.path_config.ENV_FILE_PATH
