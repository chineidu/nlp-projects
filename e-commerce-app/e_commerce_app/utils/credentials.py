import os
from typing import Any, Optional

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from typeguard import typechecked

from e_commerce_app.config.core import ENV_PATH

_ = load_dotenv(find_dotenv(filename=ENV_PATH))


@typechecked
def get_credentials() -> (
    tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]
):
    """This is used to load the credentials."""
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    return (DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT)


@typechecked
def get_jwt_credentials() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """This is used to load the jwt credentials."""
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    return (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)


class Credentials(BaseModel):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str


class AuthCredentials(BaseModel):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


(DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT) = get_credentials()
(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES) = get_jwt_credentials()


cred_dict: dict[str, Any] = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
}

jwt_cred_dict: dict[str, Any] = {
    "SECRET_KEY": SECRET_KEY,
    "ALGORITHM": ALGORITHM,
    "ACCESS_TOKEN_EXPIRE_MINUTES": ACCESS_TOKEN_EXPIRE_MINUTES,
}

USER_CREDENTIALS = Credentials(**cred_dict)

(DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT) = (
    USER_CREDENTIALS.DB_USER,
    USER_CREDENTIALS.DB_PASSWORD,
    USER_CREDENTIALS.DB_NAME,
    USER_CREDENTIALS.DB_HOST,
    USER_CREDENTIALS.DB_PORT,
)

JWT_USER_CREDENTIALS = AuthCredentials(**jwt_cred_dict)

(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES) = (
    JWT_USER_CREDENTIALS.SECRET_KEY,
    JWT_USER_CREDENTIALS.ALGORITHM,
    JWT_USER_CREDENTIALS.ACCESS_TOKEN_EXPIRE_MINUTES,
)
