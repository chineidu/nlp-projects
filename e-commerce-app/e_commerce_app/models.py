from datetime import datetime
from typing import Any, Literal

from rich.console import Console
from sqlalchemy import (
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)
from typeguard import typechecked

console = Console()

# Sqlite dialect
path: str = "sqlite:///./e-commerce.db"
engine = create_engine(path, echo=False, connect_args={"check_same_thread": False})
session_local = Session(engine)


Status = Literal["pending", "processing", "shipped", "delivered"]


@typechecked
def format_date(date_string: str, date_format: str = "%d-%m-%Y") -> datetime:
    """Convert the string to a datetime object."""
    formatted_date = datetime.strptime(date_string, date_format)

    return formatted_date


class Base(DeclarativeBase):
    pass


class Products(Base):
    __tablename__: str = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"({self.__class__.__name__}(id={self.id!r}, name={self.name!r}, "
            f"description={self.description!r}, price={self.price:,})"
        )


class Customers(Base):
    __tablename__: str = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    billing_address: Mapped[str] = mapped_column(nullable=True)
    shipping_address: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)

    order: Mapped["Orders"] = relationship(back_populates="customers")

    def __repr__(self) -> str:
        return (
            f"({self.__class__.__name__}(id={self.id!r}, name={self.name!r}, email={self.email!r}, "
            f"password={self.password!r}, shipping_address={self.shipping_address!r})"
        )


class Orders(Base):
    __tablename__: str = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    order_date: Mapped[Any] = mapped_column(DateTime, default=datetime.utcnow)
    total_price: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False)

    customers: Mapped["Customers"] = relationship(back_populates="order")

    def __repr__(self) -> str:
        return (
            f"({self.__class__.__name__}(id={self.id!r}, customer_id={self.customer_id!r}, "
            f"order_date={self.order_date!r}, total_price={self.total_price!r}, "
            f"status={self.status!r})"
        )