from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from e_commerce_app.models import get_db
from e_commerce_app.utils import crud
from e_commerce_app.v1.schemas import input_schema, output_schema

products_router = APIRouter(tags=["products"])
db_dependency = Annotated[Session, Depends(get_db)]


@products_router.post(path="/products/")
def create_product(
    data: input_schema.ProductsInputSchema, db: db_dependency
) -> output_schema.ProductsOutputSchema:
    """This is used to create a new product."""
    _data = data.data[0]
    result: output_schema.ProductsOutputSchema = crud.create_product(db=db, data=_data)
    return result


@products_router.get(path="/product/{name}")
def get_product(name: str, db: db_dependency) -> output_schema.ProductsOutputSchema:
    """This is used to retrieve an available product."""
    name = name.strip().lower()
    result: output_schema.ProductsOutputSchema = crud.get_products_by_name(db=db, name=name)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return result


@products_router.get(path="/products/")
def get_products(
    db: db_dependency,
) -> list[output_schema.ProductsOutputSchema]:
    """This is used to retrieve all available products."""
    result: output_schema.ProductsOutputSchema = crud.get_products(db=db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
    return result
