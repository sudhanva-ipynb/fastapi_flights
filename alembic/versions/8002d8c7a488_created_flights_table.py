"""created flights table

Revision ID: 8002d8c7a488
Revises: 
Create Date: 2023-02-16 15:52:42.335763

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8002d8c7a488'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('flights',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('src',sa.String(),nullable=False),sa.Column('dest',sa.String(),nullable=False))

def downgrade() -> None:
    op.drop_table('flights')
