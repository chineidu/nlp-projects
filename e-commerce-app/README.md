# Tutorials

## Table of Content

- [Tutorials](#tutorials)
  - [Table of Content](#table-of-content)
  - [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Setup Environment Variables](#setup-environment-variables)
  - [Manage Database \[Without Docker\]](#manage-database-without-docker)
    - [Database Migrations](#database-migrations)
      - [Autogenerate The Tables (Using Alembic)](#autogenerate-the-tables-using-alembic)
      - [Apply Latest Migrations](#apply-latest-migrations)
    - [Run App](#run-app)
  - [Docker Setup](#docker-setup)
    - [Start The Services](#start-the-services)
    - [Setup PgAdmin](#setup-pgadmin)
    - [Database Migrations \[Docker\]](#database-migrations-docker)
  - [Project Structure](#project-structure)
    - [Directories And Files](#directories-and-files)
    - [Database Schema](#database-schema)
  - [Note](#note)

## Setup

### Install Dependencies

```sh
pip install -U pip && pip install poetry

# Virtual ENVs are created in the project directory.
poetry config virtualenvs.in-project true

# Install requirements
poetry install

# Activate Shell
poetry shell
```

### Setup Environment Variables

```sh
# Create .env file
cp env/example.env env/.env
```

## Manage Database [Without Docker]

```sh
# Drop the database if it exists
make drop_db

# Create a new database
make create_db
```

### Database Migrations

#### Autogenerate The Tables (Using Alembic)

```sh
alembic revision --autogenerate -m "New migration"
```

#### Apply Latest Migrations

```sh
# View the SQL commands
alembic upgrade head --sql

# Apply
alembic upgrade head
```

### Run App

```sh
uvicorn app:app --port 8000 --host "0.0.0.0"

## Check listening ports
# sudo lsof -i -P | grep LISTEN
```

## Docker Setup

### Start The Services

```sh
docker-compose up
```

### Setup PgAdmin

- Creds can be found at `e_commerce_app/env/example.env`

- Go to http://localhost:5050/

- Credentials
  - email: `admin@admin.com`
  - password: `admin`

- Create a `server` and connect to the `database`

### Database Migrations [Docker]

- ssh into the `app` container.

```sh
# Autogenerate The Tables (Using Alembic)
alembic revision --autogenerate -m "New migration"

# Apply
alembic upgrade head
```

## Project Structure

### Directories And Files

```text
├── README.md
├── app.py
├── e_commerce_app
│   ├── __init__.py
│   ├── config
│   │   ├── config.yaml
│   │   ├── core.py
│   │   └── settings.py
│   ├── logger_config.py
│   ├── models.py
│   ├── utils
│   │   ├── __init__.py
│   │   └── crud.py
│   └── v1
│       ├── __init__.py
│       ├── routes
│       │   ├── __init__.py
│       │   ├── customers.py
│       │   ├── health.py
│       │   └── products.py
│       └── schemas
│           ├── __init__.py
│           ├── api_schema.py
│           ├── db_schema.py
│           ├── input_schema.py
│           └── output_schema.py
├── poetry.lock
├── pyproject.toml
└── tests
    └── __init__.py
```

### Database Schema

```text
Customers:
    id: Optional[int] = None
    name: str
    email: EmailStr
    password: constr(min_length=8, max_length=24)  # type: ignore
    billing_address: Optional[str] = None
    shipping_address: str
    phone_number: Optional[str] = None


Orders:
    id: Optional[int] = None
    customer_id: int
    order_date: datetime
    total_price: float
    status: Status


Products:
    id: Optional[int] = None
    name: str
    description: str
    tags: Optional[str] = None
    price: float
```

## Note

- Any syntax works fine.
  - `db_dependency = Annotated[Session, Depends(get_db)]`
    - i.e `db: db_dependency`
  - `db: Session = Depends(get_db)`

```python
from typing import Annotated
from fastapi import Depends


db_dependency = Annotated[Session, Depends(get_db)]


@product_router.post(path="/products/", tags=["products"])
def create_product(db: db_dependency) -> output_schema.ProductsOutputSchema:
    """This is used to create a new user."""
    pass

# OR
@product_router.post(path="/products/", tags=["products"])
def create_product(db: Session = Depends(get_db)) -> output_schema.ProductsOutputSchema:
    """This is used to create a new user."""
    pass
```
