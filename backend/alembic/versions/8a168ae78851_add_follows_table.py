"""Add follows table

Revision ID: 8a168ae78851
Revises: b0aa3adab165
Create Date: 2025-05-26 15:01:15.324963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision: str = '8a168ae78851'
down_revision: Union[str, None] = 'b0aa3adab165'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'follows',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('follower_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete="CASCADE")),
        sa.Column('following_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete="CASCADE")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    op.create_table(
        'comments',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('author_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete="CASCADE")),
        sa.Column('prompt_id', pg.UUID(as_uuid=True), sa.ForeignKey('prompts.id', ondelete="CASCADE")),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )

    op.create_table(
        'likes',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete="CASCADE")),
        sa.Column('prompt_id', pg.UUID(as_uuid=True), sa.ForeignKey('prompts.id', ondelete="CASCADE"))
    )


def downgrade():
    op.drop_table('likes')
    op.drop_table('comments')
    op.drop_table('follows')
