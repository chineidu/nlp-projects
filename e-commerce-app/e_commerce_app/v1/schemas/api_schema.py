from pydantic import BaseModel


class APIConfigSchema(BaseModel):
    """API Configurations."""

    API_VERSION_STR: str
    API_FLOAT_VERSION: str
    PROJECT_NAME: str


class DBConfig(BaseModel):
    DB_PATH: str


class ConfigVars(BaseModel):
    """Main configuration object."""

    api_config_schema: APIConfigSchema
    db_config: DBConfig
