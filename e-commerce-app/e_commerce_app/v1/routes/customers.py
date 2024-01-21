from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from e_commerce_app.models import get_db
from e_commerce_app.utils import crud
from e_commerce_app.v1.schemas import input_schema, output_schema

customer_router = APIRouter()


@customer_router.post(path="/customers/", tags=["customers"])
def create_customer(
    data: input_schema.CustomersInputSchema, db: Session = Depends(get_db)
) -> output_schema.CustomersOutputSchema:
    """This is used to create a new user."""
    _data = data.data[0]
    _email: Optional[dict[str, Any]] = crud.get_customer_by_email(db=db, email=_data.email)
    _username: Optional[dict[str, Any]] = crud.get_customer_by_username(
        db=db, username=_data.username
    )

    if _email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    elif _username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    result: output_schema.CustomersOutputSchema = crud.create_customer(db=db, data=_data)
    return result


@customer_router.get(path="/customer/{id}", tags=["customers"])
def get_customer(id: int, db: Session = Depends(get_db)) -> output_schema.CustomersOutputSchema:
    """This is used to retrieve a registered user."""
    result: output_schema.CustomersOutputSchema = crud.get_customer(db=db, id=id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return result


@customer_router.get(path="/customers/", tags=["customers"])
def get_customers(
    db: Session = Depends(get_db),
) -> list[output_schema.CustomersOutputSchema]:
    """This is used to retrieve all registered users."""
    result: output_schema.CustomersOutputSchema = crud.get_customers(db=db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    return result
