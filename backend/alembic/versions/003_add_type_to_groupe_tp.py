"""Add type column to groupe_tp table to support multiple session types.

This migration adds support for CM, TD, TP, EXAM, SEMINAR session types.
The type field defaults to 'TP' for backward compatibility.

Phase 4 of Backend Improvements: Session Type Generalization
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'groupe_tp_type_001'
down_revision = '141083d88fd4_updated_database'
branch_labels = None
depends_on = None


def upgrade():
    """Add type column to groupe_tp table with default value 'TP'."""
    op.add_column(
        'groupe_tp',
        sa.Column(
            'type',
            sa.String(50),
            nullable=False,
            server_default='TP',
            comment='Session type: CM (lecture), TD (tutorial), TP (practical), EXAM (exam), SEMINAR (seminar)'
        )
    )
    
    # Add check constraint to ensure valid type values
    # Note: MySQL/MariaDB support CHECK constraints in version 8.0.16+
    # For older versions, validation is handled in the ORM/API layer
    op.execute(
        "ALTER TABLE groupe_tp ADD CONSTRAINT check_groupe_tp_type CHECK (type IN ('CM', 'TD', 'TP', 'EXAM', 'SEMINAR'))"
    )


def downgrade():
    """Remove type column from groupe_tp table."""
    op.execute("ALTER TABLE groupe_tp DROP CONSTRAINT check_groupe_tp_type")
    op.drop_column('groupe_tp', 'type')
