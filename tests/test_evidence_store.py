"""
Evidence Store 单元测试。
"""

import pytest

from app.core.exceptions import ValidationError
from app.evidence.store import EvidenceStore


class FakeSession:

    def add(self, obj):
        pass

    async def flush(self):
        pass


@pytest.mark.asyncio
async def test_invalid_evidence_status():

    store = EvidenceStore(
        FakeSession()
    )

    with pytest.raises(
        ValidationError
    ):

        store.validate_status(
            "INVALID"
        )


@pytest.mark.asyncio
async def test_evidence_status_normalization():

    store = EvidenceStore(
        FakeSession()
    )

    assert (
        store.validate_status(
            "verified"
        )
        == "VERIFIED"
    )