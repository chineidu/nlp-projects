"""create orders table

Revision ID: d77c6e912d62
Revises: a68a3bf93401
Create Date: 2024-01-20 19:35:07.900794

"""
from datetime import datetime
from typing import Sequence, Union

from sqlalchemy import FLOAT, INTEGER, VARCHAR, Column, DateTime, ForeignKey

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "d77c6e912d62"
down_revision: Union[str, None] = "a68a3bf93401"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name: str = "orders"


def upgrade() -> None:
    """This is used to create a table."""
    op.create_table(
        table_name,
        Column("id", INTEGER, primary_key=True),
        Column("customer_id", INTEGER, ForeignKey("customers.id"), nullable=False),
        Column("order_date", DateTime, default=datetime.utcnow),
        Column("total_price", FLOAT, nullable=False),
        Column("status", VARCHAR(20), nullable=False),
    )


def downgrade() -> None:
    """This is used to drop a table."""
    op.drop_table(table_name)
