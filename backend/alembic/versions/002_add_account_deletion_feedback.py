"""Create account_deletion_feedback table."""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'account_deletion_feedback_002'
down_revision = 'avatar_url_001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account_deletion_feedback',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('reason', sa.String(100), nullable=False),
        sa.Column('additional_feedback', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('account_deletion_feedback')
