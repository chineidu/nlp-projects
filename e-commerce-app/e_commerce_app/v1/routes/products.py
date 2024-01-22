from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typeguard import typechecked

from e_commerce_app.models import get_db
from e_commerce_app.utils import crud
from e_commerce_app.v1.auth.jwt_auth import get_current_user
from e_commerce_app.v1.schemas import input_schema, output_schema

products_router = APIRouter(tags=["products"])

db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[output_schema.ProductsOutputSchema, Depends(get_current_user)]


@typechecked
@products_router.post(path="/products/")
def create_product(
    data: input_schema.ProductsInputSchema,
    db: db_dependency,
    current_user: current_user_dependency,
) -> output_schema.ProductsOutputSchema:
    """This is used to create a new product."""
    _data = data.data[0]
    result: output_schema.ProductsOutputSchema = crud.create_product(db=db, data=_data)
    return result


@typechecked
@products_router.get(path="/product/{name}")
def get_product(
    name: str,
    db: db_dependency,
    current_user: current_user_dependency,
) -> output_schema.ProductsOutputSchema:
    """This is used to retrieve an available product."""
    name = name.strip().lower()
    result: output_schema.ProductsOutputSchema = crud.get_products_by_name(db=db, name=name)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return result


@typechecked
@products_router.get(path="/products/")
def get_products(
    db: db_dependency,
    current_user: current_user_dependency,
) -> list[output_schema.ProductsOutputSchema]:
    """This is used to retrieve all available products."""
    result: output_schema.ProductsOutputSchema = crud.get_products(db=db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return result
