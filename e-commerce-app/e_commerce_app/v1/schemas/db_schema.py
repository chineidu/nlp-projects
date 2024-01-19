"""It uses Pydantic v2."""

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, constr

Status = Literal["pending", "processing", "shipped", "delivered"]


class BaseSchema(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)


class CustomersSchema(BaseSchema):
    name: str
    email: EmailStr
    password: constr(min_length=8, max_length=24)  # type: ignore
    billing_address: Optional[str] = None
    shipping_address: str
    phone_number: Optional[str] = None


class OrdersSchema(BaseSchema):
    customer_id: int
    order_date: date
    total_price: float
    status: Status


class ProductsSchema(BaseSchema):
    name: str
    description: str
    tags: Optional[str] = None
    price: float
