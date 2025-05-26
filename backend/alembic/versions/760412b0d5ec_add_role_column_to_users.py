"""Add role column to users

Revision ID: 760412b0d5ec
Revises: cc0eba4bee70
Create Date: 2025-05-26 12:21:21.694865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '760412b0d5ec'
down_revision: Union[str, None] = 'cc0eba4bee70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(), nullable=True, server_default='user'))  # 👈 default role


def downgrade() -> None:
    op.drop_column('users', 'role')
