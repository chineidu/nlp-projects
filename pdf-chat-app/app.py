from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import crud, models, schemas
from models.models import session_local

# Create tables
models.Base.metadata.create_all(models.engine)

app = FastAPI(title="E-Commerce Website", version="0.1.0")


def get_db() -> Session:
    """L\This is used to load the database instance."""
    db = session_local
    try:
        yield db
    finally:
        db.close()


@app.post(path="/customers/", response_model=schemas.CustomersOutput)
def create_customer(
    data: schemas.CustomersInput, db: Session = Depends(get_db)
) -> schemas.Customers:
    _data = data.input[0]
    db_user = crud.get_customer_by_email(db=db, email=_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_customer(db=db, data=_data)


@app.get(path="/customer/{id}", response_model=schemas.CustomersOutput)
def read_user(id: int, db: Session = Depends(get_db)) -> schemas.CustomersOutput:
    db_user = crud.get_customer(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get(path="/customers/", response_model=list[schemas.CustomersOutput])
def read_users(db: Session = Depends(get_db)) -> list[schemas.CustomersOutput]:
    db_user = crud.get_customers(db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
