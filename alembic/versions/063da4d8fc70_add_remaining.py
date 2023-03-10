"""add remaining

Revision ID: 063da4d8fc70
Revises: 508cb796dbab
Create Date: 2023-02-16 16:08:42.828907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '063da4d8fc70'
down_revision = '508cb796dbab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('booking',
    sa.Column('flight_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['flight_id'], ['flights.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('flight_id', 'user_id')
    )
    op.add_column('flights', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('flights', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'flights', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'flights', type_='foreignkey')
    op.drop_column('flights', 'owner_id')
    op.drop_column('flights', 'created_at')
    op.drop_table('booking')
    op.drop_table('users')
    # ### end Alembic commands ###
