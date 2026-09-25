"""
add workflow checkpoints

Revision ID: add_checkpoints_001
Revises: a9e1f4c2d8b7
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_checkpoints_001"

down_revision: Union[
    str,
    Sequence[str],
    None
] = "a9e1f4c2d8b7"

branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建 checkpoints 表。"""

    op.create_table(
        "checkpoints",

        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),

        sa.Column(
            "run_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "checkpoint_version",
            sa.Integer(),
            nullable=False,
            default=1,
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "current_node",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "state_data",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "outputs",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "errors",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            default=0,
        ),

        sa.Column(
            "pause_reason",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "human_approved",
            sa.Boolean(),
            nullable=False,
            default=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["run_id"],
            ["analysis_runs.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )

    op.create_index(
        "ix_checkpoints_run_id",
        "checkpoints",
        ["run_id"],
    )


def downgrade() -> None:
    """删除 checkpoints 表。"""

    op.drop_index(
        "ix_checkpoints_run_id",
        table_name="checkpoints",
    )

    op.drop_table(
        "checkpoints"
    )