"""
Context 注入辅助测试。

覆盖三条路径：

1. 正常路径：context 带 context_manager → 返回 <history> 块
2. 降级路径：context 为 None / 无 context_manager / run_id 缺失 /
   repository_id 缺失 / build_history 抛异常 → 一律返回空串且不抛
3. repository_id 解析：优先 input_data，其次 context.config 兜底

为什么降级路径要单独测：历史记忆是锦上添花，它的失败绝不能
让整条分析失败（与 LLMChatTool 永不抛异常、SynthesisNode 兜住
综合分析失败是同一套约定）。测试里的 FakeContext 刻意不带
context_manager —— 这与 tests/test_workflow.py 手搭的 context 一致。

全程不发起任何网络请求。
"""

import pytest

from app.context.injection import (
    build_history_block,
    resolve_repository_id,
)


class FakeContextManager:
    """假的 ContextManager，只实现 build_history。"""

    def __init__(
        self,
        text="<history>\n- 历史\n</history>",
        error=None,
    ):
        self.text = text
        self.error = error
        self.calls = []

    async def build_history(self, **kwargs):
        self.calls.append(kwargs)

        if self.error is not None:
            raise self.error

        return self.text


class FakeContext:

    def __init__(
        self,
        manager=None,
        config=None,
    ):
        self.context_manager = manager
        self.config = config or {}


@pytest.mark.asyncio
async def test_build_history_block_returns_text():
    """正常路径：透传 run_id / repository_id / query。"""

    manager = FakeContextManager()

    text = await build_history_block(
        FakeContext(manager),
        run_id="run-1",
        repository_id=7,
        query="workflow 怎么实现",
    )

    assert text.startswith("<history>")

    assert manager.calls[0]["run_id"] == "run-1"
    assert manager.calls[0]["repository_id"] == 7
    assert manager.calls[0]["query"] == "workflow 怎么实现"


@pytest.mark.asyncio
async def test_build_history_block_degrades_on_missing_inputs():
    """缺 context / 缺 manager / 缺 id 都必须返回空串。"""

    manager = FakeContextManager()

    # context 本身为 None
    assert (
        await build_history_block(
            None,
            run_id="run-1",
            repository_id=7,
        )
        == ""
    )

    # 无 context_manager（手搭的 context 就是这样）
    assert (
        await build_history_block(
            FakeContext(),
            run_id="run-1",
            repository_id=7,
        )
        == ""
    )

    # run_id 缺失
    assert (
        await build_history_block(
            FakeContext(manager),
            run_id=None,
            repository_id=7,
        )
        == ""
    )

    # repository_id 缺失
    assert (
        await build_history_block(
            FakeContext(manager),
            run_id="run-1",
            repository_id=None,
        )
        == ""
    )


@pytest.mark.asyncio
async def test_build_history_block_swallows_build_error():
    """构建阶段抛异常时降级为空串，不冒泡。"""

    manager = FakeContextManager(
        error=RuntimeError("db down"),
    )

    text = await build_history_block(
        FakeContext(manager),
        run_id="run-1",
        repository_id=7,
    )

    assert text == ""


@pytest.mark.asyncio
async def test_build_history_block_passes_through_empty():
    """没有历史记录时返回空串，调用方据此不占位。"""

    manager = FakeContextManager(text="")

    text = await build_history_block(
        FakeContext(manager),
        run_id="run-1",
        repository_id=7,
    )

    assert text == ""


def test_resolve_repository_id_prefers_input_data():
    context = FakeContext(config={"repository_id": 99})

    assert (
        resolve_repository_id(
            context,
            {"repository_id": 5},
        )
        == 5
    )


def test_resolve_repository_id_falls_back_to_config():
    """深挖入口只传固定字段，要靠 config 兜底。"""

    context = FakeContext(config={"repository_id": 99})

    assert (
        resolve_repository_id(
            context,
            {"module": "workflow"},
        )
        == 99
    )

    assert resolve_repository_id(context, None) == 99


def test_resolve_repository_id_returns_none_when_absent():
    assert resolve_repository_id(FakeContext(), {}) is None

    assert resolve_repository_id(None, None) is None
