"""
Evidence / Claim / Citation 数据契约。
"""

from datetime import datetime

from pydantic import BaseModel, Field


class EvidenceCreateRequest(BaseModel):
    repository_id: int

    source_type: str = Field(
        min_length=1,
        max_length=50,
    )

    source_url: str | None = None

    file_path: str | None = None

    line_start: int | None = Field(
        default=None,
        ge=1,
    )

    line_end: int | None = Field(
        default=None,
        ge=1,
    )

    content: str = Field(
        min_length=1,
    )

    verification_status: str = "UNVERIFIED"


class EvidenceResponse(BaseModel):
    id: str
    repository_id: int
    source_type: str
    source_url: str | None
    file_path: str | None
    line_start: int | None
    line_end: int | None
    content: str
    verification_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ClaimCreateRequest(BaseModel):
    run_id: str

    claim_text: str = Field(
        min_length=1,
    )

    verification_status: str = "UNVERIFIED"


class ClaimResponse(BaseModel):
    id: str
    run_id: str
    claim_text: str
    verification_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class CitationCreateRequest(BaseModel):
    claim_id: str
    evidence_id: str


class CitationResponse(BaseModel):
    id: str
    claim_id: str
    evidence_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }