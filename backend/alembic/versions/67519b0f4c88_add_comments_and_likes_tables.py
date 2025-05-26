"""Add comments and likes tables

Revision ID: 67519b0f4c88
Revises: 8a168ae78851
Create Date: 2025-05-26 15:07:20.421824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67519b0f4c88'
down_revision: Union[str, None] = '8a168ae78851'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('author_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('prompt_id', pg.UUID(as_uuid=True), sa.ForeignKey('prompts.id', ondelete='CASCADE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )
    op.create_table(
        'likes',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('prompt_id', pg.UUID(as_uuid=True), sa.ForeignKey('prompts.id', ondelete='CASCADE')),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('comments')
    op.drop_table('likes')