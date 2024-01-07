from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, constr

Status = Literal["pending", "processing", "shipped", "delivered"]


class Products(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float

    class Config:
        from_attributes = True


class Customers(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    password: constr(min_length=8, max_length=24)  # type: ignore
    billing_address: Optional[str] = None
    shipping_address: str
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True


class CustomersInput(BaseModel):
    """Pydantic V2"""

    input: list[Customers]

    model_config = {
        "json_schema_extra": {
            "example": {
                "input": [
                    {
                        "name": "Neidu",
                        "email": "email@example.com",
                        "password": "kjeth648353",
                        "billing_address": "string",
                        "shipping_address": "Mushin, Lagos.",
                        "phone_number": "4546-242-4351",
                    }
                ]
            }
        }
    }


class CustomersOutput(BaseModel):
    name: str
    email: EmailStr
    billing_address: Optional[str] = None
    shipping_address: str
    phone_number: Optional[str] = None


class Orders(BaseModel):
    id: Optional[int] = None
    customer_id: Optional[int] = None
    order_date: datetime
    total_price: float
    status: Status

    class Config:
        from_attributes = True
