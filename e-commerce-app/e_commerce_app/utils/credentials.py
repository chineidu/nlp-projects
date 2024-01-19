import os
from typing import Any, Optional

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel
from typeguard import typechecked

_ = load_dotenv(find_dotenv(filename=".env"))


@typechecked
def get_credentials() -> (
    tuple[
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
        Optional[str],
    ]
):
    """This is used to load the credentials."""
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    return (DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT)


class Credentials(BaseModel):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str


(DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT) = get_credentials()
cred_dict: dict[str, Any] = {
    "DB_USER": DB_USER,
    "DB_PASSWORD": DB_PASSWORD,
    "DB_NAME": DB_NAME,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
}
USER_CREDENTIALS = Credentials(**cred_dict)

(DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT) = (
    USER_CREDENTIALS.DB_USER,
    USER_CREDENTIALS.DB_PASSWORD,
    USER_CREDENTIALS.DB_NAME,
    USER_CREDENTIALS.DB_HOST,
    USER_CREDENTIALS.DB_PORT,
)
