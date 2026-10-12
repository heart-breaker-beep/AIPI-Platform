"""数据访问层统一导出。"""

from app.infrastructure.persistence.repositories.analysis_run import (
    AnalysisRunRepository,
)

from app.infrastructure.persistence.repositories.claim import (
    ClaimRepository,
)

from app.infrastructure.persistence.repositories.citation import (
    CitationRepository,
)

from app.infrastructure.persistence.repositories.evidence import (
    EvidenceRepository,
)

from app.infrastructure.persistence.repositories.repository_basic import (
    RepositoryRepository,
)


__all__ = [
    "RepositoryRepository",
    "AnalysisRunRepository",
    "EvidenceRepository",
    "ClaimRepository",
    "CitationRepository",
]
