# Tutorials

## Table of Content

- [Tutorials](#tutorials)
  - [Table of Content](#table-of-content)
  - [Setup](#setup)
    - [Install Dependencies](#install-dependencies)
    - [Run App](#run-app)
  - [Project Structure](#project-structure)
    - [Directories And Files](#directories-and-files)
    - [Database Schema](#database-schema)

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

### Run App

```sh
uvicorn app:app --port 8008 --host "0.0.0.0"
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
