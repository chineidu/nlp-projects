"""Pydantic v2."""

from typing import Any, Optional, Union

from passlib.context import CryptContext
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from typeguard import typechecked

from e_commerce_app import models
from e_commerce_app.v1.schemas import db_schema

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@typechecked
def get_password_hash(password: str) -> str:
    """This returns the hashed password."""
    return pwd_context.hash(password)


@typechecked
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """This returns True if the passwords match otherwise it returns False."""
    return pwd_context.verify(plain_password, hashed_password)


@typechecked
def authenticate_user(username: str, password: str, db: Session) -> Union[Any, bool]:
    """This returns the user if it's correctly authenticated otherwise False."""
    user: Optional[dict[str, Any]] = get_customer_by_username(db=db, username=username)

    if not user:
        return False

    is_valid: bool = verify_password(plain_password=password, hashed_password=user.hashed_password)  # type: ignore

    if not is_valid:
        return False

    return user


@typechecked
def get_customer(db: Optional[Session], id: int) -> Optional[dict[str, Any]]:
    """Return the customer information."""
    stmt = select(models.Customers).filter_by(id=id)
    try:
        result = db.execute(stmt).scalar_one()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def get_customer_by_email(db: Optional[Session], email: str) -> Optional[dict[str, Any]]:
    """Return the the customer information."""
    stmt: Any = select(models.Customers).filter_by(email=email)  # type: ignore
    try:
        result: Any = db.execute(stmt).scalar_one()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def get_customer_by_username(db, username: str) -> Optional[dict[str, Any]]:
    """Return the the customer information."""
    stmt: Any = select(models.Customers).filter_by(username=username)

    try:
        result: Any = db.execute(stmt).scalar_one()
        return result
    except Exception:
        return None


@typechecked
def get_customers(
    db: Optional[Session], skip: int = 0, limit: int = 100
) -> Optional[list[dict[str, Any]]]:
    """Return all the customer information."""
    stmt: Any = select(models.Customers).offset(skip).limit(limit)  # type: ignore
    try:
        result: list[Any] = db.execute(stmt).scalars().all()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def create_customer(
    db: Optional[Session], data: db_schema.CustomersSchemaInDB
) -> Optional[dict[str, Any]]:
    """This is used to add a new customer to the database."""
    input_data: dict[str, Any] = data.model_dump()
    # Add hashed_password
    input_data["hashed_password"] = get_password_hash(password=input_data.get("hashed_password"))  # type: ignore
    stmt: Any = insert(models.Customers).values(**input_data)  # type: ignore

    try:
        _ = db.execute(stmt)  # type: ignore
        db.commit()  # type: ignore
        return input_data

    except Exception:
        db.rollback()  # type: ignore
        return None


@typechecked
def get_products_by_name(db: Optional[Session], name: str) -> Optional[dict[str, Any]]:
    """Return the customer information."""
    stmt = select(models.Products).filter_by(name=name)
    try:
        result = db.execute(stmt).scalar_one()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def get_products_by_id(db: Optional[Session], id: Optional[int]) -> Optional[dict[str, Any]]:
    """Return the product information."""
    stmt = select(models.Products).filter_by(id=id)
    try:
        result = db.execute(stmt).scalar_one()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def get_products(
    db: Optional[Session], skip: int = 0, limit: int = 100
) -> Optional[list[dict[str, Any]]]:
    """Return all the product information."""
    stmt: Any = select(models.Products).offset(skip).limit(limit)
    try:
        result: Any = db.execute(stmt).scalars().all()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def create_product(
    db: Optional[Session], data: db_schema.ProductsSchema
) -> Optional[dict[str, Any]]:
    """This is used to add a new product to the database."""
    input_data: dict[str, Any] = data.model_dump()
    stmt: Any = insert(models.Products).values(**input_data)
    try:
        db.execute(stmt)  # type: ignore
        db.commit()  # type: ignore
        return input_data

    except Exception:
        db.rollback()  # type: ignore
        return None


@typechecked
def get_orders(
    db: Optional[Session], skip: int = 0, limit: int = 100
) -> Optional[list[dict[str, Any]]]:
    """Return all the orders information."""
    stmt: Any = select(models.Orders).offset(skip).limit(limit)
    try:
        result: Any = db.execute(stmt).scalars().all()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def get_orders_by_id_n_status(
    db: Optional[Session],
    customer_id: Optional[int],
    status: Optional[db_schema.Status],
) -> Optional[list[dict[str, Any]]]:
    """Return the order information."""
    stmt = select(models.Orders).filter_by(customer_id=customer_id, status=status)
    try:
        result = db.execute(stmt).scalars().all()  # type: ignore
        return result
    except Exception:
        return None


@typechecked
def create_order(db: Optional[Session], data: db_schema.OrdersSchema) -> Optional[dict[str, Any]]:
    """This is used to add a new order to the database."""
    input_data: dict[str, Any] = data.model_dump()
    stmt: Any = insert(models.Orders).values(**input_data)
    try:
        db.execute(stmt)  # type: ignore
        db.commit()  # type: ignore
        return input_data

    except Exception:
        db.rollback()  # type: ignore
        return None
