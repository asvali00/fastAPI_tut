"""add content to posts table

Revision ID: 567be5896c5a
Revises: e8538de8e988
Create Date: 2022-03-01 23:47:51.669956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '567be5896c5a'
down_revision = 'e8538de8e988'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", 'content')
    pass
