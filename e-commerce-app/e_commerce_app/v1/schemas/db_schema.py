"""This module contains the database schema of the API.
It uses Pydantic v2.

Author: Chinedu Ezeofor
"""

from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

Status = Literal["pending", "processing", "shipped", "delivered"]


class BaseSchema(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)


class CustomersSchema(BaseModel):
    # Use BaseModel!
    name: str
    username: str
    email: EmailStr
    billing_address: Optional[str] = None
    shipping_address: str
    phone_number: Optional[str] = None


class CustomersSchemaInDB(CustomersSchema):
    # hashed_password
    hashed_password: str


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
