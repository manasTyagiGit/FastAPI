"""create_likes_table

Revision ID: 945565c59801
Revises: 
Create Date: 2026-02-09 20:34:19.644303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '945565c59801'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table ('likes', sa.Column('user_id', sa.Integer(), nullable=False, primary_key=True),
                              sa.Column('post_id', sa.Integer(), nullable=False, primary_key=True))
    pass


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('likes')
    pass
