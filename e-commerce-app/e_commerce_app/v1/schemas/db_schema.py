"""It uses Pydantic v2."""

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, constr

Status = Literal["pending", "processing", "shipped", "delivered"]

# class BaseSchema(BaseModel):
# model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)


class CustomersSchema(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)

    id: Optional[int] = None
    name: str
    email: EmailStr
    password: constr(min_length=8, max_length=24)  # type: ignore
    billing_address: Optional[str] = None
    shipping_address: str
    phone_number: Optional[str] = None


class OrdersSchema(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)

    id: Optional[int] = None
    customer_id: int
    order_date: datetime
    total_price: float
    status: Status


class ProductsSchema(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)

    id: Optional[int] = None
    name: str
    description: str
    tags: Optional[str] = None
    price: float
