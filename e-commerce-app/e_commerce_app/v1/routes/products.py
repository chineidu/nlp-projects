from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from e_commerce_app.database import get_db
from e_commerce_app.utils import crud
from e_commerce_app.v1.schemas import model_schema

product_router = APIRouter()


@product_router.post(path="/products/")
def create_product(
    data: model_schema.CustomersInput, db: Session = Depends(get_db)
) -> model_schema.CustomersOutput:
    _data = data.data[0]
    db_user = crud.get_customer_by_email(db=db, email=_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db=db, data=_data)


@product_router.get(path="/product/{id}")
def read_user(id: int, db: Session = Depends(get_db)) -> model_schema.CustomersOutput:
    db_user = crud.get_customer(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@product_router.get(path="/products/")
def read_users(db: Session = Depends(get_db)) -> list[model_schema.CustomersOutput]:
    db_user = crud.get_customers(db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user