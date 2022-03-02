"""add last few columns to posts table

Revision ID: 346214444963
Revises: c3a81c8c8134
Create Date: 2022-03-02 00:30:35.108209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '346214444963'
down_revision = 'c3a81c8c8134'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
