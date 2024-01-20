"""create products table

Revision ID: a68a3bf93401
Revises: 11b231b3c831
Create Date: 2024-01-20 19:28:02.596172

"""
from typing import Sequence, Union

from sqlalchemy import FLOAT, INTEGER, VARCHAR, Column

from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = "a68a3bf93401"
down_revision: Union[str, None] = "11b231b3c831"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name: str = "products"


def upgrade() -> None:
    """This is used to create a table."""
    op.create_table(
        table_name,
        Column("id", INTEGER, primary_key=True),
        Column("name", VARCHAR(255), nullable=False),
        Column("description", VARCHAR(255), nullable=False),
        Column("tags", VARCHAR(255), nullable=False),
        Column("price", FLOAT, nullable=False),
    )


def downgrade() -> None:
    """This is used to drop a table."""
    op.drop_table(table_name)
