"""
EvidenceService 测试。
"""

import pytest

from app.core.exceptions import ValidationError
from app.services.evidence_service import (
    EvidenceService,
)


class FakeSession:

    async def commit(self):
        pass


@pytest.mark.asyncio
async def test_create_evidence_rejects_empty_content():

    service = EvidenceService(
        FakeSession()
    )

    with pytest.raises(
        ValidationError
    ):

        await service.create_evidence(
            repository_id=1,
            source_type="source",
            content="   ",
        )