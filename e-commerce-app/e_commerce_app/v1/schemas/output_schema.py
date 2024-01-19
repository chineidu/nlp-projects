"""It uses Pydantic v2."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from e_commerce_app.v1.schemas.db_schema import Status


class CustomersOutputSchema(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    billing_address: Optional[str] = None
    shipping_address: str
    phone_number: Optional[str] = None


class OrdersOutputSchema(BaseModel):
    id: Optional[int] = None
    customer_id: int
    order_date: datetime
    total_price: float
    status: Status


class ProductsOutputSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    tags: Optional[str] = None
    price: float
