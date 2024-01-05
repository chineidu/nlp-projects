from typing import Optional
from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column, relationship


from rich.console import Console


console = Console()

# Sqlite dialect
path: str = "sqlite:///./test.db"
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
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship("User", back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


# neidu: User = User(name="neidu", fullname="Chinedu Emmanuel")
# sandy: User = User(name="sandy", fullname="Sandy Kenbrigs")
# console.print(neidu)

# Create tables
Base.metadata.create_all(engine)
