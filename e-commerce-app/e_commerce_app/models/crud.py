from typing import Any, Optional

import models
import schemas
from rich.console import Console
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from typeguard import typechecked

console = Console()


@typechecked
def _exclude_sensitive_data(
    output: dict[str, Any], unwanted: list[str] = ["password"]
) -> dict[str, Any]:
    """This is used to exclude unnecessary fileds."""
    result: dict[str, Any] = {key: val for key, val in output.items() if key not in unwanted}
    return result


@typechecked
def get_customer(db: Session, id: int) -> Any:
    """Return the customer information."""
    stmt = select(models.Customers).filter_by(id=id)
    try:
        result = db.execute(stmt).scalar_one()
        return result
    except Exception:
        return None


@typechecked
def get_customer_by_email(db: Session, email: str) -> Optional[Any]:
    """Return the the customer information."""
    stmt: Any = select(models.Customers).filter_by(email=email)
    try:
        result: Any = db.execute(stmt).scalar_one()
        return result
    except Exception:
        return None


@typechecked
def get_customers(db: Session, skip: int = 0, limit: int = 100) -> Optional[Any]:
    """Return all the customer information."""
    stmt: Any = select(models.Customers).offset(skip).limit(limit)
    try:
        result: Any = db.execute(stmt).scalars().all()
        return result
    except Exception:
        return None


@typechecked
def create_customer(db: Session, data: schemas.Customers) -> Optional[Any]:
    """This is used to add a new customer to the database.

    Note: I used Pydantic v2.

    """
    stmt: Any = insert(models.Customers).values(**data.model_dump())
    try:
        db.execute(stmt)
        db_user: dict[str, Any] = _exclude_sensitive_data(output=stmt.compile().params)
        db.commit()
        return db_user

    except Exception:
        db.rollback()
        return None
