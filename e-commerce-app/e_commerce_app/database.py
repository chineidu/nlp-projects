from typing import Any, Literal

import click
from psycopg2 import connect
from psycopg2.errors import DuplicateDatabase, InvalidCatalogName
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

COMMANDS = Literal["create_db", "drop_db"]
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


@typechecked
def drop_db() -> None:
    """This is used to drop a database."""
    conn = connect(**db_params)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    query: str = f"DROP DATABASE {DB_NAME};"
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        logger.warning(f"{DB_NAME!r} dropped successfully!")

    except InvalidCatalogName as err:
        logger.error(err)

    finally:
        conn.close()


# ======== CLI ========
@typechecked
def get_ctx(ctx: Any) -> COMMANDS:
    """Return the required click context.

    Params:
    -------
        ctx: (Any)

    Returns:
    --------
        command: (COMMANDS)
    """
    command: COMMANDS = ctx.obj.get("command")
    return command


@click.group()
@click.option(
    "-c",
    "--command",
    help=(
        f"The Data Definition Language(DDL) command. "
        f"It's either {COMMANDS.__args__[0]!r} or {COMMANDS.__args__[1]!r}."  # type: ignore
    ),
)
@click.pass_context
@typechecked
def cli(ctx: Any, command: COMMANDS) -> None:
    """Click command object."""
    ctx.ensure_object(dict)
    ctx.obj["command"] = command


# ===== Subcommands =====
@cli.command()
@click.pass_context
@typechecked
def database_manager(ctx: Any) -> None:
    """This is used to `create` or `drop` the database."""
    command = get_ctx(ctx=ctx)

    if command == "create_db":
        click.secho("\n\n>>[INFO]: Creating the database <<")
        _ = create_db()
    elif command == "drop_db":
        click.secho("\n\n>> [WARNING]: Dropping the database <<", color="red")
        _ = drop_db()
    click.secho(message="\n\n ========== Done ========== ", bg="blue", fg="blue")


if __name__ == "__main__":
    cli(obj={})
