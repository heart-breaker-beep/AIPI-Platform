"""
Planner Agent。

负责：

根据用户需求生成项目分析计划。

关于「计划」
============

任务表仍是固定的 5 个 agent ——
这不是偷懒，而是刻意的：

    这份报告的 01-11 章是文档 15.3 规定的契约，
    每个 agent 对应其中若干章的原始数据。
    少跑一个 agent 就会让对应章节变成
    「真实数据不存在」，
    CriticAgent 也会报字段缺失。

所以 question 驱动的不是「跑不跑」，
而是**重点在哪**：

    focus.dimensions  本次重点关注的维度（有序）

它同时驱动两件事：

    采集层  ArchitectureAnalysisSkill 把更多文件配额
            给到重点维度
    报告层  ReportGenerationSkill 展开重点章节、
            压缩其余章节

焦点怎么定
==========

    1. 先让 LLM 从 question 里解析（理解自然语言意图）
    2. LLM 不可用或返回非法时退回关键词匹配
    3. 都认不出重点时 focus 为空 ——
       此时报告保持全量等深，与旧行为一致

第 3 条很重要：识别不出重点 ≠ 没有重点。
前者保持现状，不让用户因为一句
「分析项目架构」就丢掉别的章节。
"""

from app.agents.base import BaseAgent
from app.project_analysis.analysis_focus import (
    AnalysisFocus,
)
from app.skills.json_output import (
    parse_json_object,
)


class PlannerAgent(
    BaseAgent
):
    """项目分析规划 Agent。"""

    name = "planner_agent"

    description = (
        "Create a research plan for GitHub "
        "project analysis."
    )

    # 固定的分析任务表。
    #
    # 顺序即执行顺序：
    # repository 提供 README，
    # architecture 依赖它抽取项目自述结构，
    # 因此必须排在最前。
    TASKS = (
        "repository_analysis_agent",
        "architecture_analysis_agent",
        "technology_analysis_agent",
        "evidence_analysis_agent",
        "critic_agent",
    )

    # 计划版本。
    #
    # 2 = 增加 focus 字段。
    # 读取方（AnalysisFocus.from_plan）对
    # 没有 focus 的旧计划有回退，
    # 因此历史 run 仍然可读。
    PLAN_VERSION = 2

    async def execute(
        self,
        context,
        input_data,
    ):
        """生成项目分析计划。"""

        question = input_data.get(
            "question"
        )

        tasks = list(self.TASKS)

        focus = await self._resolve_focus(
            context,
            question,
        )

        research_plan = {
            "plan_version": self.PLAN_VERSION,
            "analysis_type": (
                "github_agent_project"
            ),
            "question": question,
            "tasks": tasks,
            "focus": focus.to_dict(),
            "evidence_required": True,
        }

        return {
            "tasks": tasks,
            "research_plan": research_plan,
        }

    # ------------------------------------------------------------------
    # 焦点解析
    # ------------------------------------------------------------------

    async def _resolve_focus(
        self,
        context,
        question,
    ) -> AnalysisFocus:
        """
        解析本次分析的重点维度。

        LLM 优先，关键词兜底，
        都认不出时返回空焦点。
        """

        if not isinstance(
            question,
            str,
        ) or not question.strip():

            return AnalysisFocus.none()

        via_llm = await self._focus_via_llm(
            context,
            question,
        )

        if via_llm is not None:
            return via_llm

        return AnalysisFocus.from_question(
            question
        )

    async def _focus_via_llm(
        self,
        context,
        question: str,
    ):
        """
        让 LLM 判断用户在问哪些模块。

        任何一步失败都返回 None，
        由调用方退回关键词匹配 ——
        规划失败不该让整个分析失败。
        """

        tool = context.tools.get("llm_chat")

        if tool is None:
            return None

        try:

            result = await tool.execute(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            self._system_prompt()
                        ),
                    },
                    {
                        "role": "user",
                        "content": question,
                    },
                ]
            )

        except Exception:

            return None

        if not result.get("available"):
            return None

        parsed = parse_json_object(
            result.get("content") or ""
        )

        if parsed is None:
            return None

        dimensions = AnalysisFocus._normalize(
            parsed.get("dimensions")
        )

        if not dimensions:

            # 模型明确说「没有特定重点」。
            # 这与解析失败不同：
            # 前者是判断结果，不必再走关键词。
            if isinstance(
                parsed.get("dimensions"),
                list,
            ):
                return AnalysisFocus.none()

            return None

        notes = parsed.get("notes")

        return AnalysisFocus(
            dimensions=dimensions,
            notes=(
                notes
                if isinstance(notes, str)
                else ""
            ),
            source="llm",
        )

    @staticmethod
    def _system_prompt() -> str:
        """系统提示词。"""

        return (
            "你在为一个 GitHub 项目分析任务判断重点。\n"
            "\n"
            "可选的模块只有这六个（名字必须原样使用）：\n"
            "\n"
            "    agents    Agent 架构：智能体、角色划分、"
            "多智能体协作、自治边界\n"
            "    workflow  工作流：编排、状态机、图、"
            "节点与路由、执行流程\n"
            "    skills    技能层：可复用的能力封装\n"
            "    tools     工具层：函数调用、外部集成、MCP\n"
            "    rag       检索增强：向量库、检索、召回、"
            "知识库\n"
            "    memory    记忆：会话状态、检查点、持久化\n"
            "\n"
            "规则：\n"
            "\n"
            "1. 只输出用户问题里**明确指向**的模块。\n"
            "   用户只是泛泛地说「分析这个项目」时，\n"
            "   返回空数组，不要猜。\n"
            "2. 最多 3 个，按重要性排序。\n"
            "3. 输出 JSON，不要 markdown 包裹，"
            "不要解释文字：\n"
            "\n"
            '{"dimensions": ["agents"], '
            '"notes": "一句话说明用户关心什么"}\n'
            "\n"
            "没有明确重点时：\n"
            "\n"
            '{"dimensions": [], "notes": ""}\n'
        )
