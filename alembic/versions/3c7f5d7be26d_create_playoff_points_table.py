"""Create playoff points table

Revision ID: 3c7f5d7be26d
Revises: 7cce80338914
Create Date: 2023-01-02 17:07:51.354528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3c7f5d7be26d"
down_revision = "7cce80338914"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "playoff_points",
        sa.Column("match_id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("points", sa.Integer, nullable=False),
    )

    pass


def downgrade():
    op.drop_table("playoff_points")
    pass
