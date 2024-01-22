"""This module contains the schema for the outputs of the API.

Author: Chinedu Ezeofor
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict

from e_commerce_app.v1.schemas.db_schema import (
    CustomersSchema,
    OrdersSchema,
    ProductsSchema,
)


class CustomersOutputSchema(CustomersSchema):
    id: Optional[int] = None


class OrdersOutputSchema(OrdersSchema):
    id: Optional[int] = None


class ProductsOutputSchema(ProductsSchema):
    id: Optional[int] = None


class HealthCheckSchema(BaseModel):
    model_config = ConfigDict(str_to_lower=True, str_strip_whitespace=True)

    message: str
    version: str
    status: str
