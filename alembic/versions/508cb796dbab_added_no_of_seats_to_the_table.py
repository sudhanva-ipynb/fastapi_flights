"""added no_of_seats to the table

Revision ID: 508cb796dbab
Revises: 8002d8c7a488
Create Date: 2023-02-16 15:59:52.930320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '508cb796dbab'
down_revision = '8002d8c7a488'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('flights',sa.Column('no_of_seats',sa.Integer(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('flights','no_of_seats')
    pass
