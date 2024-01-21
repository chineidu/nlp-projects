"""This module contains the schema for the inputs of the API.
It uses Pydantic v2.

Author: Chinedu Ezeofor
"""

from typing import Any, Literal

from pydantic import BaseModel

from e_commerce_app.v1.schemas import db_schema

Status = Literal["pending", "processing", "shipped", "delivered"]


class CustomersInputSchema(BaseModel):
    """Schema for customer input."""

    data: list[db_schema.CustomersSchemaInDB]

    model_config: dict[str, Any] = {
        "json_schema_extra": {
            "example": {
                "data": [
                    {
                        "name": "Adams Grey",
                        "username": "adam123",
                        "email": "adam123@email.com",
                        "hashed_password": "12345abc",
                        "billing_address": "null",
                        "shipping_address": "Mushin, Lagos.",
                        "phone_number": "4546-242-4351",
                    }
                ]
            }
        }
    }


class OrdersInputSchema(BaseModel):
    """Schema for orders input."""

    data: list[db_schema.OrdersSchema]

    model_config: dict[str, Any] = {
        "json_schema_extra": {
            "example": {
                "data": [
                    {
                        "customer_id": "1",
                        "order_date": "2024-01-01",  # %Y-%m-%d
                        "total_price": 68000.00,
                        "status": "processing",
                    }
                ]
            }
        }
    }


class ProductsInputSchema(BaseModel):
    """Schema for products input."""

    data: list[db_schema.ProductsSchema]

    model_config: dict[str, Any] = {
        "json_schema_extra": {
            "example": {
                "data": [
                    {
                        "name": "Google Chromecast",
                        "description": (
                            "It enables Android TV on your LED TV, smart TV, monitor, etc"
                        ),
                        "tags": "electronics, gadgets, android",
                        "price": 68000.00,
                    }
                ]
            }
        }
    }
