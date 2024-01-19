"""Pydantic v2."""

from typing import Any, Optional

from rich.console import Console
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from typeguard import typechecked

from e_commerce_app import models
from e_commerce_app.v1.schemas import db_schema

console = Console()


@typechecked
def _exclude_sensitive_data(
    output: dict[str, Any], unwanted: list[str] = ["password"]
) -> dict[str, Any]:
    """This is used to exclude unnecessary fileds."""
    result: dict[str, Any] = {key: val for key, val in output.items() if key not in unwanted}
    return result


@typechecked
def get_customer(db: Session, id: int) -> Optional[Any]:
    """Return the customer information."""
    stmt = select(models.Customers).filter_by(id=id)
    try:
        result = db.execute(stmt).scalar_one()
        return result
    except Exception:
        return None


@typechecked
def get_customer_by_email(db: Session, email: str) -> Any:
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
        result: list[Any] = db.execute(stmt).scalars().all()
        return result
    except Exception:
        return None


@typechecked
def create_customer(db: Session, data: db_schema.CustomersSchema) -> Optional[dict[str, Any]]:
    """This is used to add a new customer to the database."""
    input_data: dict[str, Any] = data.model_dump()
    stmt: Any = insert(models.Customers).values(**input_data)
    try:
        _ = db.execute(stmt)
        user: dict[str, Any] = _exclude_sensitive_data(output=input_data)
        db.commit()
        return user

    except Exception as err:
        db.rollback()
        return None


@typechecked
def get_products_by_name(db: Session, name: str) -> Optional[dict[str, Any]]:
    """Return the customer information."""
    stmt = select(models.Products).filter_by(name=name)
    try:
        result = db.execute(stmt).scalar_one()
        return result
    except Exception:
        return None


@typechecked
def get_products_by_id(db: Session, id: Optional[int]) -> Optional[dict[str, Any]]:
    """Return the product information."""
    stmt = select(models.Products).filter_by(id=id)
    try:
        result = db.execute(stmt).scalar_one()
        return result
    except Exception:
        return None


@typechecked
def get_products(db: Session, skip: int = 0, limit: int = 100) -> Optional[dict[str, Any]]:
    """Return all the product information."""
    stmt: Any = select(models.Products).offset(skip).limit(limit)
    try:
        result: Any = db.execute(stmt).scalars().all()
        return result
    except Exception:
        return None


@typechecked
def create_product(db: Session, data: db_schema.ProductsSchema) -> Optional[dict[str, Any]]:
    """This is used to add a new product to the database."""
    input_data: dict[str, Any] = data.model_dump()
    stmt: Any = insert(models.Products).values(**input_data)
    try:
        db.execute(stmt)
        db.commit()
        return input_data

    except Exception:
        db.rollback()
        return None


@typechecked
def get_orders(db: Session, skip: int = 0, limit: int = 100) -> Optional[Any]:
    """Return all the orders information."""
    stmt: Any = select(models.Orders).offset(skip).limit(limit)
    try:
        result: Any = db.execute(stmt).scalars().all()
        return result
    except Exception:
        return None


@typechecked
def get_orders_by_id(db: Session, id: Optional[int]) -> Optional[dict[str, Any]]:
    """Return the order information."""
    stmt = select(models.Products).filter_by(id=id)
    try:
        result = db.execute(stmt).scalar_one()
        return result
    except Exception:
        return None


@typechecked
def create_order(db: Session, data: db_schema.ProductsSchema) -> Optional[Any]:
    """This is used to add a new order to the database."""
    input_data: dict[str, Any] = data.model_dump()
    stmt: Any = insert(models.Orders).values(**input_data)
    try:
        db.execute(stmt)
        db.commit()
        return input_data

    except Exception:
        db.rollback()
        return None
