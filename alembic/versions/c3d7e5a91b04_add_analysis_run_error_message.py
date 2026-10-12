"""
add analysis_runs.error_message

Revision ID: add_run_error_message_001
Revises: add_checkpoints_001
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_run_error_message_001"

down_revision: Union[
    str,
    Sequence[str],
    None
] = "add_checkpoints_001"

branch_labels = None
depends_on = None


def upgrade() -> None:
    """给 analysis_runs 增加 error_message 列。"""

    op.add_column(
        "analysis_runs",
        sa.Column(
            "error_message",
            sa.Text(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """移除 error_message 列。"""

    op.drop_column(
        "analysis_runs",
        "error_message",
    )
