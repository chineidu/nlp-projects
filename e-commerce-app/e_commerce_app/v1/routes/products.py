from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from e_commerce_app.models import get_db
from e_commerce_app.utils import crud
from e_commerce_app.v1.schemas import input_schema, output_schema

product_router = APIRouter()


@product_router.post(path="/products/", tags=["products"])
def create_product(
    data: input_schema.ProductsInputSchema, db: Session = Depends(get_db)
) -> output_schema.ProductsOutputSchema:
    """This is used to create a new user."""
    _data = data.data[0]
    product = crud.get_products_by_id(db=db, id=_data.id)

    if product:
        raise HTTPException(status_code=400, detail=f"Product with id={_data.id} already exists")
    return crud.create_product(db=db, data=_data)


@product_router.get(path="/product/{name}", tags=["products"])
def get_product(name: str, db: Session = Depends(get_db)) -> output_schema.ProductsOutputSchema:
    """This is used to retrieve an available product."""
    name = name.strip().lower()
    product = crud.get_products_by_name(db=db, name=name)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@product_router.get(path="/products/", tags=["products"])
def get_products(
    db: Session = Depends(get_db),
) -> list[output_schema.ProductsOutputSchema]:
    """This is used to retrieve all available products."""
    db_product = crud.get_products(db=db)
    if db_product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return db_product
