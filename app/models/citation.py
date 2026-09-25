"""
Citation 数据模型。

表示：

Claim
  ↓
Evidence
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Citation(Base):
    """
    Claim 与 Evidence 的关联关系。
    """

    __tablename__ = "citations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    claim_id: Mapped[str] = mapped_column(
        ForeignKey("claims.id"),
        nullable=False,
        index=True,
    )

    evidence_id: Mapped[str] = mapped_column(
        ForeignKey("evidences.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "claim_id",
            "evidence_id",
            name="uq_citations_claim_evidence",
        ),
    )