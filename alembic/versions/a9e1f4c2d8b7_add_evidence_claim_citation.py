"""
add evidence claim citation

Revision ID: a9e1f4c2d8b7
Revises: 479571222143
"""

from alembic import op
import sqlalchemy as sa


revision = "a9e1f4c2d8b7"

down_revision = "479571222143"

branch_labels = None

depends_on = None


def upgrade() -> None:

    op.create_table(
        "evidences",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "repository_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "source_type",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "source_url",
            sa.String(length=1000),
            nullable=True,
        ),

        sa.Column(
            "file_path",
            sa.String(length=1000),
            nullable=True,
        ),

        sa.Column(
            "line_start",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "line_end",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "verification_status",
            sa.String(length=20),
            nullable=False,
            server_default="UNVERIFIED",
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["repository_id"],
            ["repositories.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_evidences_repository_id",
        "evidences",
        ["repository_id"],
    )

    op.create_table(
        "claims",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "run_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "claim_text",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "verification_status",
            sa.String(length=20),
            nullable=False,
            server_default="UNVERIFIED",
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

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_claims_run_id",
        "claims",
        ["run_id"],
    )

    op.create_table(
        "citations",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "claim_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "evidence_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["claim_id"],
            ["claims.id"],
        ),

        sa.ForeignKeyConstraint(
            ["evidence_id"],
            ["evidences.id"],
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "claim_id",
            "evidence_id",
            name="uq_citations_claim_evidence",
        ),
    )

    op.create_index(
        "ix_citations_claim_id",
        "citations",
        ["claim_id"],
    )

    op.create_index(
        "ix_citations_evidence_id",
        "citations",
        ["evidence_id"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_citations_evidence_id",
        table_name="citations",
    )

    op.drop_index(
        "ix_citations_claim_id",
        table_name="citations",
    )

    op.drop_table("citations")

    op.drop_index(
        "ix_claims_run_id",
        table_name="claims",
    )

    op.drop_table("claims")

    op.drop_index(
        "ix_evidences_repository_id",
        table_name="evidences",
    )

    op.drop_table("evidences")