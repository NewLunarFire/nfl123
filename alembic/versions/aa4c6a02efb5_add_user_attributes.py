"""Add user attributes

Revision ID: aa4c6a02efb5
Revises: 90490aacb3f9
Create Date: 2022-08-09 21:11:08.003485

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "aa4c6a02efb5"
down_revision = "90490aacb3f9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users", sa.Column("is_admin", sa.Boolean, nullable=False, default=False)
    )
    op.add_column("users", sa.Column("lang", sa.String, nullable=False, default="en"))
    pass


def downgrade():
    op.drop_column("users", "is_admin")
    op.drop_column("users", "lang")
    pass
