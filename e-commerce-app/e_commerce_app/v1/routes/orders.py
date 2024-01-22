"""This module contains the order endpoints of the API.

Author: Chinedu Ezeofor
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typeguard import typechecked

from e_commerce_app.models import get_db
from e_commerce_app.utils import crud
from e_commerce_app.v1.auth.jwt_auth import get_current_user
from e_commerce_app.v1.schemas import input_schema, output_schema
from e_commerce_app.v1.schemas.db_schema import Status

orders_router = APIRouter(tags=["orders"])

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[output_schema.OrdersOutputSchema, Depends(get_current_user)]


@typechecked
@orders_router.post(path="/orders/")
def create_order(
    data: input_schema.OrdersInputSchema,
    db: db_dependency,
    current_user: current_user_dependency,
) -> output_schema.OrdersOutputSchema:
    """This is used to create a new order."""
    _data = data.data[0]
    result: output_schema.OrdersOutputSchema = crud.create_order(db=db, data=_data)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"customer_id={_data.customer_id} is not present in table!",
        )

    return result


@typechecked
@orders_router.get(path="/order/{customer_id}")
def get_order(
    customer_id: int,
    order_status: Status,
    db: db_dependency,
    current_user: current_user_dependency,
) -> list[output_schema.OrdersOutputSchema]:
    """This is used to retrieve an available order.

    Usage: GET /order/customer_id?status=pending
    """
    result: output_schema.OrdersOutputSchema = crud.get_orders_by_id_n_status(
        db=db, customer_id=customer_id, status=order_status
    )
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return result


@typechecked
@orders_router.get(path="/orders/")
def get_orders(
    db: db_dependency,
    current_user: current_user_dependency,
) -> list[output_schema.OrdersOutputSchema]:
    """This is used to retrieve all available orders."""
    result: output_schema.OrdersOutputSchema = crud.get_orders(db=db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    return result
