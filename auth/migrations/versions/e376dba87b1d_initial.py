"""initial

Revision ID: e376dba87b1d
Revises:
Create Date: 2024-01-15 18:25:39.508973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e376dba87b1d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=24), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=True),
    sa.Column('access_level', sa.Enum('base', 'subscriber', 'superuser', name='accesslevel'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_service',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('date_joined', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=False),
    sa.Column('login', sa.String(length=60), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('user_service_id', sa.UUID(), nullable=False),
    sa.Column('profile_picture', sa.Text(), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('phone_number', sa.String(length=24), nullable=True),
    sa.Column('bio', sa.String(length=1000), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_service_id'], ['user_service.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('login_history',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('user_agent', sa.Text(), nullable=False),
    sa.Column('login_date', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('login_history')
    op.drop_table('user')
    op.drop_table('user_service')
    op.drop_table('role')
    # ### end Alembic commands ###