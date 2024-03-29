"""Introduce weeks table

Revision ID: 7cce80338914
Revises: ba5af60b7de3
Create Date: 2022-08-14 19:54:03.581550

"""
import enum

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "7cce80338914"
down_revision = "ba5af60b7de3"
branch_labels = None
depends_on = None


class WeekType(enum.Enum):
    preseason = 1
    season = 2
    playoffs = 3


def upgrade():
    op.create_table(
        "weeks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("display_name", sa.String, nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("type", sa.Enum(WeekType), nullable=False),
        sa.Column("start_time", sa.DateTime, nullable=False),
    )

    pass


def downgrade():
    op.drop_table("weeks")
    pass
