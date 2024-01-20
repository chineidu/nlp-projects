from typing import Any

from psycopg2 import connect
from psycopg2.errors import DuplicateDatabase
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typeguard import typechecked

from e_commerce_app.logger_config import logger
from e_commerce_app.utils.credentials import (
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)

# PostgreSQL connection parameters
db_params: dict[str, Any] = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
}


@typechecked
def create_db() -> None:
    """This is used to create a database."""
    conn = connect(**db_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    query: str = f"CREATE DATABASE {DB_NAME};"
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        logger.info(f"{DB_NAME!r} created successfully!")

    except DuplicateDatabase as err:
        logger.error(err)

    finally:
        conn.close()


# Create database
_ = create_db()
