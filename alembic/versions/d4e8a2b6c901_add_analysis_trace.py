"""Add ordered analysis trace streams and events."""

import sqlalchemy as sa

from alembic import op

revision = "add_analysis_trace_001"
down_revision = "add_run_error_message_001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "analysis_trace_streams",
        sa.Column("run_id", sa.String(36), primary_key=True),
        sa.Column("last_sequence", sa.BigInteger(), nullable=False),
        sa.Column("execution", sa.JSON(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "analysis_trace_events",
        sa.Column("event_id", sa.String(36), primary_key=True),
        sa.Column("run_id", sa.String(36), nullable=False),
        sa.Column("sequence", sa.BigInteger(), nullable=False),
        sa.Column("execution_id", sa.String(36), nullable=False),
        sa.Column("span_id", sa.String(36)),
        sa.Column("parent_span_id", sa.String(36)),
        sa.Column("event_type", sa.String(40), nullable=False),
        sa.Column("category", sa.String(20), nullable=False),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("message", sa.String(500), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("level", sa.String(12), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), nullable=False),
        sa.Column("duration_ms", sa.Integer()),
        sa.Column("attributes", sa.JSON(), nullable=False),
        sa.UniqueConstraint("run_id", "sequence", name="uq_trace_run_sequence"),
    )
    op.create_index("ix_trace_run_execution_span", "analysis_trace_events", ["run_id", "execution_id", "span_id"])
    op.create_index("ix_analysis_trace_events_run_id", "analysis_trace_events", ["run_id"])


def downgrade():
    op.drop_table("analysis_trace_events")
    op.drop_table("analysis_trace_streams")
