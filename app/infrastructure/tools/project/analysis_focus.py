"""
本次分析的重点维度。

为什么需要它
============

在此之前，用户提出的问题（question）
只影响结论层的措辞，完全不影响采集与报告：

    PlannerAgent 的任务表是写死的 5 个 agent
    ArchitectureAnalysisSkill 的配额是写死的
    ReportGenerationSkill 的章节是写死的

于是「分析这个项目的 agent」和
「分析它的 workflow」得到的报告一模一样 ——
每个模块都是同样的深度，看不出重点。

真实反馈：
    「我让分析的是 agent，为什么报告里还是什么都有」

本模块把「用户关心什么」变成一份显式的焦点，
供采集层（分配文件配额）与报告层（展开 / 压缩）共同使用。

焦点怎么来
==========

    llm       由 PlannerAgent 调 LLM 从 question 解析（首选）
    keywords  关键词回退（LLM 不可用时）
    none      没有识别出重点 —— 此时报告保持全量等深，
              与旧行为一致，不做任何裁剪

「识别不出重点」与「重点是空」是两回事：
前者保持现状，后者是用户明确说「只看 agent」。
"""

import re


class AnalysisFocus:
    """本次分析的重点维度。"""

    # 与 CodeStructureExtractor.DIMENSIONS、
    # 报告 04-09 章一一对应。
    DIMENSIONS = (
        "agents",
        "workflow",
        "skills",
        "tools",
        "rag",
        "memory",
    )

    # 维度名 -> 展示名。
    TITLES = {
        "agents": "Agent 架构",
        "workflow": "Workflow",
        "skills": "Skill",
        "tools": "Tool",
        "rag": "RAG",
        "memory": "Memory",
    }

    # 关键词回退表。
    #
    # 只在 LLM 不可用时使用，
    # 因此宁可保守：宁可不识别出重点
    # （保持全量报告），
    # 也不要误判成「只看某一个维度」
    # （那会让用户拿不到其它章节）。
    KEYWORDS = {
        "agents": (
            "agent",
            "智能体",
            "代理",
            "多智能体",
            "multi-agent",
            "multi agent",
            "supervisor",
            "planner",
            "reAct",
            "react",
            "角色",
        ),
        "workflow": (
            "workflow",
            "工作流",
            "编排",
            "流程",
            "graph",
            "状态机",
            "langgraph",
            "节点",
            "路由",
        ),
        "skills": (
            "skill",
            "技能",
            "能力",
            "capability",
        ),
        "tools": (
            "tool",
            "工具",
            "函数调用",
            "function call",
            "mcp",
        ),
        "rag": (
            "rag",
            "检索",
            "向量",
            "知识库",
            "embedding",
            "召回",
            "retrieval",
        ),
        "memory": (
            "memory",
            "记忆",
            "上下文",
            "会话",
            "checkpoint",
            "持久化",
        ),
    }

    # 一次最多认几个重点维度。
    #
    # 认太多等于没有重点：
    # 用户问「agent 和 workflow」是合理的，
    # 一次点名五个就不是在提重点了。
    MAX_DIMENSIONS = 3

    def __init__(
        self,
        dimensions=None,
        notes=None,
        source="none",
    ):
        self.dimensions = self._normalize(
            dimensions
        )

        self.notes = (
            notes.strip()
            if isinstance(notes, str)
            else ""
        )

        self.source = source

    # ------------------------------------------------------------------
    # 构造
    # ------------------------------------------------------------------

    @classmethod
    def none(cls) -> "AnalysisFocus":
        """没有识别出重点 —— 报告保持全量等深。"""

        return cls()

    @classmethod
    def _normalize(
        cls,
        dimensions,
    ) -> list:
        """去重、只保留已知维度、限长，保持顺序。"""

        if not isinstance(
            dimensions,
            (list, tuple),
        ):
            return []

        result = []

        for item in dimensions:

            name = str(item).strip().lower()

            if name not in cls.DIMENSIONS:
                continue

            if name in result:
                continue

            result.append(name)

            if len(result) >= cls.MAX_DIMENSIONS:
                break

        return result

    @classmethod
    def from_question(
        cls,
        question,
    ) -> "AnalysisFocus":
        """
        关键词回退：从问题文本里认重点维度。

        只在 LLM 规划不可用时使用。
        一条都没命中时返回 none()，
        而不是「猜一个」。
        """

        if not isinstance(question, str):
            return cls.none()

        lowered = question.lower()

        hits = []

        for name in cls.DIMENSIONS:

            if cls._matches(lowered, name):

                hits.append(name)

        if not hits:
            return cls.none()

        return cls(
            dimensions=hits,
            notes="",
            source="keywords",
        )

    @classmethod
    def _matches(
        cls,
        lowered: str,
        dimension: str,
    ) -> bool:
        """判断文本是否命中该维度的关键词。"""

        for keyword in cls.KEYWORDS[dimension]:

            # 中文关键词直接子串匹配；
            # 英文关键词要词边界，
            # 否则 "agent" 会命中 "reagent"。
            if re.search(r"[一-鿿]", keyword):

                if keyword in lowered:
                    return True

                continue

            if re.search(
                r"(?:^|[^a-z0-9])"
                + re.escape(keyword)
                + r"(?:$|[^a-z0-9])",
                lowered,
            ):
                return True

        return False

    @classmethod
    def from_plan(
        cls,
        research_plan,
    ) -> "AnalysisFocus":
        """
        从 research_plan 里读回焦点。

        采集层与报告层都用这个入口，
        避免两处各自解析导致行为不一致。
        """

        if not isinstance(research_plan, dict):
            return cls.none()

        raw = research_plan.get("focus")

        if not isinstance(raw, dict):

            # 兼容旧 run：research_plan 里没有 focus。
            # 退回用 question 做关键词匹配，
            # 这样历史数据的报告也能有点侧重。
            return cls.from_question(
                research_plan.get("question")
            )

        source = raw.get("source") or "none"

        if source == "none":
            return cls.none()

        return cls(
            dimensions=raw.get("dimensions"),
            notes=raw.get("notes"),
            source=source,
        )

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------

    @property
    def is_focused(self) -> bool:
        """是否识别出了明确重点。"""

        return bool(self.dimensions)

    def is_primary(self, dimension) -> bool:
        """该维度是否是本次重点。"""

        return dimension in self.dimensions

    def rank(self, dimension) -> int:
        """
        维度在重点里的排序。

        越靠前越重要；不在重点里返回一个很大的值。
        """

        try:

            return self.dimensions.index(
                dimension
            )

        except ValueError:

            return len(self.DIMENSIONS)

    def titles(self) -> list:
        """重点维度的展示名，用于写进报告开头。"""

        return [
            self.TITLES.get(name, name)
            for name in self.dimensions
        ]

    def to_dict(self) -> dict:
        """落进 research_plan 的形态。"""

        return {
            "dimensions": list(self.dimensions),
            "notes": self.notes,
            "source": self.source,
        }

    def __repr__(self) -> str:

        return (
            f"AnalysisFocus({self.dimensions!r}, "
            f"source={self.source!r})"
        )
