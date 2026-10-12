"""
Evidence Store 单元测试。
"""

import pytest

from app.core.exceptions import ValidationError
from app.infrastructure.enrichment.evidence.store import EvidenceStore


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


@pytest.mark.asyncio
async def test_create_evidence_rejects_empty_content():
    """
    空内容不是证据。

    这条用例原先挂在 EvidenceService 上，
    而 EvidenceService 已在第 5 阶段删除
    （它对 store 只是透传 + 补 uuid），
    校验本身一直在这里，因此测试跟着搬过来。
    """

    store = EvidenceStore(
        FakeSession()
    )

    with pytest.raises(
        ValidationError
    ):

        await store.create_evidence(
            evidence_id="e-1",
            repository_id=1,
            source_type="source",
            content="   ",
        )
