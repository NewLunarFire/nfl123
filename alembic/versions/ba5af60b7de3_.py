"""Add password for user

Revision ID: ba5af60b7de3
Revises: aa4c6a02efb5
Create Date: 2022-08-14 14:38:15.828744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ba5af60b7de3"
down_revision = "aa4c6a02efb5"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("password", sa.String, nullable=False))
    pass


def downgrade():
    op.drop_column("users", "password")
    pass
