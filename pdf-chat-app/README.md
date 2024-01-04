# Tutorials

## Table of Content

- [Tutorials](#tutorials)
  - [Table of Content](#table-of-content)
  - [SQLAlchemy](#sqlalchemy)
    - [Setting Up MetaData With Table Objects](#setting-up-metadata-with-table-objects)
    - [Declarative Approach](#declarative-approach)

## SQLAlchemy

- [Engine (docs)](https://docs.sqlalchemy.org/en/20/tutorial/engine.html)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import text


console= Console()

# Sqlite dialect
path: str = "sqlite+pysqlite:///:memory:"
engine = create_engine(path, echo=True)

# Connetion object
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    console.print(result.all())
    conn.commit()

# Session object
with Session(engine) as session:
    result = session.execute(text("select 'hello Neidu'"))
    console.print(result.all())
    session.commit()
```

### Setting Up MetaData With Table Objects

```python
from sqlalchemy import MetaData, Table, Column, Integer, String


metadata_obj = MetaData()

# name, metadata
user_table: Table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(300))
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(1_000), nullable=False),
)

metadata_obj.create_all(engine)
```

### Declarative Approach

```python
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from rich.console import Console


console = Console()

# Sqlite dialect
path: str = "sqlite+pysqlite:///:memory:"
engine = create_engine(path, echo=True)
session = Session(engine)


### Declarative Approach
class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[list["Address"]] = relationship("Address", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"(User(id={self.id!r}, name={self.name!r}, "
            f"fullname={self.fullname!r}, addresses={self.addresses!r})"
        )


class Address(Base):
    __tablename__: str = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


sandy: User = User(name="neidu", fullname="Chinedu Emmanuel")
console.print(sandy)


```
