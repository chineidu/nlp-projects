"""create customers table

Revision ID: 11b231b3c831
Revises:
Create Date: 2024-01-20 17:09:19.311672

"""
from typing import Sequence, Union

from sqlalchemy import INTEGER, VARCHAR, Column

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "11b231b3c831"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name: str = "customers"


def upgrade() -> None:
    """This is used to create a table."""
    op.create_table(
        table_name,
        Column("id", INTEGER, primary_key=True),
        Column("name", VARCHAR(255), nullable=False),
        Column("email", VARCHAR(255), nullable=False),
        Column("password", VARCHAR(50), nullable=False),
        Column("billing_address", VARCHAR(255), nullable=True),
        Column("shipping_address", VARCHAR(255), nullable=False),
        Column("phone_number", VARCHAR(255), nullable=True),
    )


def downgrade() -> None:
    """This is used to drop a table."""
    op.drop_table(table_name)
