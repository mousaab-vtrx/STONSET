"""Add avatar_url column to user table."""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'avatar_url_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Add avatar_url column to user table."""
    op.add_column('user', sa.Column('avatar_url', sa.String(500), nullable=True))


def downgrade():
    """Remove avatar_url column from user table."""
    op.drop_column('user', 'avatar_url')
