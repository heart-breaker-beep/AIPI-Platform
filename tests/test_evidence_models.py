"""
Evidence / Claim / Citation 模型测试。
"""

from app.models.claim import Claim
from app.models.citation import Citation
from app.models.evidence import Evidence


def test_evidence_model():

    assert Evidence.__tablename__ == "evidences"

    columns = {
        column.name
        for column in Evidence.__table__.columns
    }

    assert {
        "id",
        "repository_id",
        "source_type",
        "source_url",
        "file_path",
        "line_start",
        "line_end",
        "content",
        "verification_status",
        "created_at",
    }.issubset(columns)


def test_claim_model():

    assert Claim.__tablename__ == "claims"

    columns = {
        column.name
        for column in Claim.__table__.columns
    }

    assert {
        "id",
        "run_id",
        "claim_text",
        "verification_status",
        "created_at",
    }.issubset(columns)


def test_citation_model():

    assert Citation.__tablename__ == "citations"

    columns = {
        column.name
        for column in Citation.__table__.columns
    }

    assert {
        "id",
        "claim_id",
        "evidence_id",
        "created_at",
    }.issubset(columns)