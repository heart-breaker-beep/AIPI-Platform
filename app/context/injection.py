"""Context 注入辅助。

把「同一仓库的历史分析记忆」组装成可直接拼进 LLM
user message 的文本块，供真正调用大模型的 Skill 使用。

为什么单独一个模块：

PlanExecutor 跑的是确定性分析 Agent（无 LLM、无 prompt），
在那里构建 Context 没有消费方；真正需要历史记忆的是
report_synthesis / module_deep_dive / learning_path 这几个
拼 prompt 的地方。让它们各自去访问 ContextManager，会把
「怎么取、取哪个字段、失败了怎么办」重复三遍，于是收拢到这里。
"""

from typing import Any

from app.core.logging import (
    get_logger,
)

logger = get_logger(__name__)


def resolve_repository_id(
    context: Any,
    input_data: dict[str, Any] | None,
) -> int | None:
    """
    解析 repository_id。

    多数调用点会把它随 input_data 传下来；
    deep_dive 这类按需入口只传固定字段，
    此时回落到 build_context 写进 config 的那份。
    """

    if input_data:

        value = input_data.get(
            "repository_id"
        )

        if value is not None:
            return value

    config = (
        getattr(
            context,
            "config",
            None,
        )
        or {}
    )

    return config.get("repository_id")


async def build_history_block(
    context: Any,
    *,
    run_id: str | None,
    repository_id: int | None,
    query: str | None = None,
) -> str:
    """
    返回可直接拼进 user message 的 <history> 文本。

    任何缺失或异常都返回空字符串 —— 历史记忆是锦上添花，
    它的失败绝不能让整条分析失败。这与本项目既有的两条约定
    一致：LLMChatTool 永不抛异常（统一返回 available/reason），
    SynthesisNode 兜住综合分析失败并降级为 available=False。
    """

    if context is None:
        return ""

    manager = getattr(
        context,
        "context_manager",
        None,
    )

    # 部分调用路径（如 test_workflow 里手搭的 context）
    # 不带 context_manager，此时静默跳过。
    if manager is None:
        return ""

    if not run_id or repository_id is None:
        return ""

    try:

        text = await manager.build_history(
            run_id=run_id,
            repository_id=repository_id,
            query=query,
        )

    except Exception as error:

        logger.warning(
            "build history block failed | run_id=%s | %s: %s",
            run_id,
            type(error).__name__,
            error,
        )

        return ""

    return text or ""
