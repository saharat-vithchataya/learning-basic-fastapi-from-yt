"""add content column to posts table

Revision ID: 4c5820bd2dea
Revises: a67bc589478a
Create Date: 2024-01-04 17:51:02.808606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4c5820bd2dea"
down_revision: Union[str, None] = "a67bc589478a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
