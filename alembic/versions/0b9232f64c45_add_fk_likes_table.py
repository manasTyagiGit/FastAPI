"""Add_FK_Likes_Table

Revision ID: 0b9232f64c45
Revises: 945565c59801
Create Date: 2026-02-09 20:53:39.007414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b9232f64c45'
down_revision: Union[str, Sequence[str], None] = '945565c59801'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_foreign_key('posts_likes_fk', source_table='likes', referent_table='posts', local_cols=['post_id'], remote_cols=['id'], ondelete="CASCADE")

    op.create_foreign_key('posts_users_fk', source_table='likes', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint ('posts_likes_fk', 'likes')
    op.drop_constraint ('posts_users_fk', 'likes')
    pass
