"""Hotels-title-unique

Revision ID: 123aa4155c57
Revises: 611459d61ce8
Create Date: 2024-10-20 20:04:21.778879

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "123aa4155c57"
down_revision: Union[str, None] = "611459d61ce8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "hotels", ["title"])


def downgrade() -> None:
    op.drop_constraint(None, "hotels", type_="unique")

