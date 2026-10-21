"""Context Manager。

负责把「同一仓库的跨 run 历史分析记忆」
组装成可拼进 LLM prompt 的受控文本块。

历史来自项目记忆存储；run 内数据由各 Skill 从 Workflow state 读取。
"""

from app.core.logging import (
    get_logger,
)

logger = get_logger(__name__)


def _render_history_entry(
    memory: dict,
) -> str:
    """
    把一条历史 run 压成单行摘要。

    刻意只保留「问题 / 状态 / 任务类型与状态」，
    不带任务 output 原文 —— 原文既可能几十 KB，
    又最容易让模型把上一轮的结论误当成本轮的事实。
    """

    line = (
        f"- ({memory.get('created_at') or '时间未知'}) "
        f"问题：{memory.get('question') or '（未记录）'}"
        f" ｜ 状态：{memory.get('status') or '未知'}"
    )

    tasks = memory.get("tasks") or []

    if tasks:

        summary = ", ".join(
            f"{task.get('task_type') or '?'}:"
            f"{task.get('status') or '?'}"
            for task in tasks[:6]
        )

        line += f" ｜ 任务：{summary}"

    return line


class ContextManager:
    """
    组装跨 run 历史记忆的紧凑文本块。
    """

    # 注入 LLM 提示用的历史记忆上限。
    #
    # 必须小而稳：3 条历史 run、1500 字符封顶。
    HISTORY_MAX_RUNS = 3

    HISTORY_MAX_CHARS = 1500

    def __init__(
        self,
        memory_manager,
    ) -> None:

        self.memory_manager = (
            memory_manager
        )

    async def build_history(
        self,
        *,
        run_id: str,
        repository_id: int,
        query: str | None = None,
        limit: int | None = None,
        max_chars: int | None = None,
    ) -> str:
        """
        组装「同一仓库历史分析」的紧凑文本块。

        这是 ContextManager 唯一不可替代的输出：
        本次 run 的数据各 Skill 已从 state 里拿到，
        只有跨 run 的历史是它们拿不到的。
        """

        memories = (
            await self.memory_manager
            .get_project_memory(
                repository_id,
                run_id=run_id,
                query=query,
                limit=(
                    limit
                    or self.HISTORY_MAX_RUNS
                ),
            )
        )

        if not memories:
            return ""

        lines = [
            "<history>",
            (
                "同一仓库此前的分析记录摘要（跨 run 历史）。"
                "可信度低于 <facts>，仅作线索。"
            ),
        ]

        for memory in memories:

            lines.append(
                _render_history_entry(memory)
            )

        lines.append("</history>")

        text = "\n".join(lines)

        char_limit = (
            max_chars
            or self.HISTORY_MAX_CHARS
        )

        if len(text) <= char_limit:
            return text

        return (
            text[:char_limit].rstrip()
            + "\n…[history truncated]"
        )

    @staticmethod
    def _truncate(
        value: str,
        limit: int,
    ) -> str:
        """按字符上限截断单段文本。"""

        if len(value) <= limit:
            return value

        return (
            value[:limit].rstrip()
            + "…[truncated]"
        )
