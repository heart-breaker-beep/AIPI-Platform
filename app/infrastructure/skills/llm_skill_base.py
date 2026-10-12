"""
LLM 类技能的公共骨架。

综合分析 / 学习路线 / 模块深挖三个技能的
「问 LLM 一句话、把回答解析成 JSON」这段流程完全同构：

    取 llm_chat 工具
    → 拼 system + user 两条消息
    → 工具返回 available=False 时降级
    → parse_json_object 解析（含代码块包裹 / 噪声 / 截断的容错）
    → 失败时把原因交回给调用方

差别只在各自的后处理（章节结构、facts、渲染），
因此这里只封装前半段。
"""

from app.infrastructure.skills.base import BaseSkill
from app.infrastructure.skills.json_output import (
    parse_json_object,
)


class LLMSkillBase(BaseSkill):
    """
    LLM 类技能基类。

    子类需要覆盖两个文案常量 ——
    它们会出现在返回给用户的 reason 里，
    不能因为合并而改变措辞（前端与测试都在读）。
    """

    #: 没有注册 llm_chat 工具时的原因
    LLM_TOOL_MISSING_REASON = (
        "Tool not found: llm_chat，无法生成内容。"
    )

    #: LLM 返回内容无法解析成 JSON 时的原因
    LLM_JSON_INVALID_REASON = (
        "LLM 返回的内容不是合法 JSON，无法解析。"
    )

    #: 工具声明可用但没有给出内容时的原因
    LLM_EMPTY_REASON = "LLM 未返回内容。"

    async def _ask_llm(
        self,
        context,
        *,
        system: str,
        prompt: str,
    ) -> tuple[dict | None, str | None]:
        """
        发起一次对话并解析成 JSON。

        Returns:
            (parsed, reason)：
            成功时 (dict, None)，
            失败时 (None, 可直接展示的原因)。

        为什么返回原因而不是只返回 None：
        三个技能都要把失败原因原样放进各自的
        unavailable 返回值里（文案不同、字段不同），
        丢掉原因就只能编一句通用文案。
        """

        tool = context.tools.get(
            "llm_chat"
        )

        if tool is None:

            return (
                None,
                self.LLM_TOOL_MISSING_REASON,
            )

        result = await tool.execute(
            messages=[
                {
                    "role": "system",
                    "content": system,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        if not result.get("available"):

            return (
                None,
                result.get("reason")
                or self.LLM_EMPTY_REASON,
            )

        parsed = parse_json_object(
            result.get("content") or ""
        )

        if parsed is None:

            return (
                None,
                self.LLM_JSON_INVALID_REASON,
            )

        return parsed, None
