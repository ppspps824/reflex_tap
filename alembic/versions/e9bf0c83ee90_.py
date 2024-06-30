"""empty message

Revision ID: e9bf0c83ee90
Revises: 58ea2f164f59
Create Date: 2024-06-30 15:39:19.297540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'e9bf0c83ee90'
down_revision: Union[str, None] = '58ea2f164f59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('character')
    op.drop_table('member')
    op.drop_table('chat_logs')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_logs',
    sa.Column('chat_id', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('role', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('message', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('sent_time', sa.NUMERIC(), autoincrement=False, nullable=True)
    )
    op.create_table('member',
    sa.Column('chat_id', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('time', sa.NUMERIC(), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('role', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('key', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('key', name='member_pkey'),
    sa.UniqueConstraint('key', name='member_key_key')
    )
    op.create_table('character',
    sa.Column('chat_id', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('persona', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('key', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('key', name='character_pkey'),
    sa.UniqueConstraint('key', name='character_key_key')
    )
    # ### end Alembic commands ###
