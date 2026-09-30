"""
question 驱动分析计划的测试。

覆盖三层：

1. AnalysisFocus  焦点解析（LLM / 关键词 / 无重点）
2. PlannerAgent   产出 focus，且任务表保持不变
3. 采集与报告     配额重分配、章节展开与压缩

背景（真实反馈）：
    「我让分析的是 agent，为什么报告里还是什么都有」

根因：question 只影响结论措辞，
采集配额与报告章节都是写死的。
"""

import json

from app.agents.planner_agent import PlannerAgent
from app.project_analysis.analysis_focus import (
    AnalysisFocus,
)
from app.skills.architecture_analysis_skill import (
    ArchitectureAnalysisSkill,
)
from app.skills.report_generation_skill import (
    ReportGenerationSkill,
)


class FakeRegistry:

    def get(self, name):
        return None


class FakeLLM:

    def __init__(
        self,
        content,
        available=True,
    ):
        self.content = content
        self.available = available
        self.calls = []

    async def execute(self, messages, **kwargs):

        self.calls.append(messages)

        if not self.available:
            return {
                "available": False,
                "reason": "未配置 LLM_API_KEY",
            }

        return {
            "available": True,
            "content": self.content,
        }


class FakeContext:

    def __init__(self, llm=None):

        self.tools = {}

        if llm is not None:
            self.tools["llm_chat"] = llm


def run_planner(question, llm=None):
    """跑一次真实的 PlannerAgent。"""

    import asyncio

    return asyncio.run(
        PlannerAgent(FakeRegistry()).execute(
            FakeContext(llm),
            {"question": question},
        )
    )


# ----------------------------------------------------------------
# AnalysisFocus
# ----------------------------------------------------------------


def test_keyword_fallback_finds_dimension():

    focus = AnalysisFocus.from_question(
        "分析项目的agent"
    )

    assert focus.dimensions == ["agents"]

    assert focus.source == "keywords"


def test_keyword_fallback_finds_multiple_in_order():

    focus = AnalysisFocus.from_question(
        "重点看 agent 和 memory"
    )

    assert focus.dimensions == ["agents", "memory"]


def test_keyword_fallback_is_conservative():
    """
    认不出重点时返回空焦点，而不是猜一个。

    空焦点意味着报告保持全量等深 ——
    这比误判成「只看某一个维度」
    （用户会丢掉其它章节）安全得多。
    """

    for question in (
        "分析项目架构",
        "这个项目怎么防止重复发票",
        "没有关键词的问题",
    ):

        focus = AnalysisFocus.from_question(
            question
        )

        assert focus.is_focused is False


def test_keyword_uses_word_boundary():
    """reagent 不能命中 agents。"""

    assert (
        AnalysisFocus.from_question(
            "reagent 是什么"
        ).is_focused
        is False
    )


def test_focus_is_capped_at_three():
    """一次点名五个就不是在提重点了。"""

    focus = AnalysisFocus.from_question(
        "agent workflow skill tool rag memory 全都看看"
    )

    assert len(focus.dimensions) == (
        AnalysisFocus.MAX_DIMENSIONS
    )


def test_focus_ignores_unknown_dimensions():

    focus = AnalysisFocus(
        dimensions=["agents", "不存在", "workflow"],
        source="llm",
    )

    assert focus.dimensions == [
        "agents",
        "workflow",
    ]


def test_rank_orders_by_mention():

    focus = AnalysisFocus(
        dimensions=["workflow", "agents"],
        source="llm",
    )

    assert focus.rank("workflow") == 0

    assert focus.rank("agents") == 1

    # 不在重点里的排在最后。
    assert focus.rank("memory") > 1


def test_from_plan_reads_focus():

    focus = AnalysisFocus.from_plan(
        {
            "focus": {
                "dimensions": ["rag"],
                "notes": "关心检索",
                "source": "llm",
            }
        }
    )

    assert focus.dimensions == ["rag"]

    assert focus.notes == "关心检索"

    assert focus.source == "llm"


def test_from_plan_falls_back_for_legacy_runs():
    """
    旧 run 的 research_plan 没有 focus 字段时，
    退回用 question 做关键词匹配 ——
    历史报告也能有点侧重。
    """

    focus = AnalysisFocus.from_plan(
        {"question": "分析 workflow 编排"}
    )

    assert focus.dimensions == ["workflow"]

    assert focus.source == "keywords"


def test_from_plan_handles_broken_input():

    assert (
        AnalysisFocus.from_plan(None).is_focused
        is False
    )

    assert (
        AnalysisFocus.from_plan("x").is_focused
        is False
    )


# ----------------------------------------------------------------
# PlannerAgent
# ----------------------------------------------------------------


def test_planner_uses_llm_focus():

    result = run_planner(
        "我关心这个项目的多智能体怎么协作",
        FakeLLM(
            json.dumps(
                {
                    "dimensions": ["agents"],
                    "notes": "关心多智能体协作",
                },
                ensure_ascii=False,
            )
        ),
    )

    focus = result["research_plan"]["focus"]

    assert focus["dimensions"] == ["agents"]

    assert focus["source"] == "llm"

    assert focus["notes"] == "关心多智能体协作"


def test_planner_keeps_all_agents():
    """
    任务表必须保持 5 个 agent。

    少跑一个会让对应章节变成「真实数据不存在」，
    CriticAgent 也会报字段缺失。
    question 驱动的是重点，不是「跑不跑」。
    """

    result = run_planner(
        "分析项目的 agent",
        FakeLLM(
            json.dumps({"dimensions": ["agents"]})
        ),
    )

    assert result["tasks"] == list(
        PlannerAgent.TASKS
    )

    assert len(result["tasks"]) == 5


def test_planner_respects_llm_no_focus():

    result = run_planner(
        "分析这个项目",
        FakeLLM(
            json.dumps(
                {"dimensions": [], "notes": ""}
            )
        ),
    )

    focus = result["research_plan"]["focus"]

    assert focus["dimensions"] == []

    assert focus["source"] == "none"


def test_planner_falls_back_when_llm_unavailable():

    result = run_planner(
        "重点分析 workflow 编排",
        FakeLLM("", available=False),
    )

    focus = result["research_plan"]["focus"]

    assert focus["dimensions"] == ["workflow"]

    assert focus["source"] == "keywords"


def test_planner_falls_back_on_invalid_json():

    result = run_planner(
        "分析 rag 检索",
        FakeLLM("这不是 JSON"),
    )

    assert result["research_plan"]["focus"][
        "dimensions"
    ] == ["rag"]


def test_planner_falls_back_without_llm_tool():

    result = run_planner("看看 memory 记忆设计")

    assert result["research_plan"]["focus"][
        "dimensions"
    ] == ["memory"]


def test_planner_plan_version_is_bumped():

    result = run_planner("分析项目")

    assert result["research_plan"][
        "plan_version"
    ] == PlannerAgent.PLAN_VERSION


# ----------------------------------------------------------------
# 采集配额
# ----------------------------------------------------------------


def test_quotas_unchanged_without_focus():

    quotas = ArchitectureAnalysisSkill._quotas_for(
        AnalysisFocus.none()
    )

    assert quotas == (
        ArchitectureAnalysisSkill.DIMENSION_QUOTAS
    )


def test_focus_dimension_gets_more_quota():
    """
    重点维度拿更多文件配额。

    这是「调深度」的一半：
    问 agent 就该多读 agents 相关文件。
    """

    focus = AnalysisFocus(
        dimensions=["agents"],
        source="llm",
    )

    quotas = ArchitectureAnalysisSkill._quotas_for(
        focus
    )

    assert quotas["agents"] > (
        ArchitectureAnalysisSkill
        .DIMENSION_QUOTAS["agents"]
    )

    # 非重点维度仍然有配额 ——
    # 报告里那些章节还是要写的。
    assert quotas["workflow"] >= 1

    assert all(
        value >= 1 for value in quotas.values()
    )


def test_focus_dimensions_come_first():
    """
    重点维度必须排在配额表前面。

    _read_candidates 是按顺序取名额的，
    重点排在后面就会被先取完的维度挤掉。
    """

    focus = AnalysisFocus(
        dimensions=["memory"],
        source="llm",
    )

    quotas = ArchitectureAnalysisSkill._quotas_for(
        focus
    )

    assert next(iter(quotas)) == "memory"


def test_quota_total_is_bounded():

    for dimensions in (
        ["agents"],
        ["agents", "workflow"],
        ["agents", "workflow", "rag"],
    ):

        quotas = ArchitectureAnalysisSkill._quotas_for(
            AnalysisFocus(
                dimensions=dimensions,
                source="llm",
            )
        )

        assert sum(quotas.values()) <= (
            ArchitectureAnalysisSkill.MAX_MODULES
        )


# ----------------------------------------------------------------
# 报告渲染
# ----------------------------------------------------------------


def build_report_data(focus_dimensions=None):

    structure = {
        "available": True,
        "basis": "code+readme+topics",
        "dimensions": {
            name: {
                "declared": True,
                "declared_by": "code",
                "items": [f"class {name.title()}Thing"],
                "topics": [],
                "evidence": [],
                "code_evidence": [],
                "details": [
                    {
                        "kind": "class",
                        "name": f"{name.title()}Thing",
                        "signature": (
                            f"class {name.title()}Thing(Base)"
                        ),
                        "file_path": f"{name}.py",
                        "line": 10,
                        "methods": ["run"],
                        "calls": [],
                        "literals": [],
                    }
                ],
            }
            for name in AnalysisFocus.DIMENSIONS
        },
    }

    data = {
        "run_id": "run-1",
        "question": "分析项目的 agent",
        "repository": {
            "full_name": "a/b",
            "language": "Python",
            "topics": [],
            "html_url": "u",
            "license": {"name": "MIT"},
        },
        "technology_stack": {
            "frameworks": [],
            "llm": [],
            "database": [],
            "embedding": [],
            "deployment": [],
        },
        "project_structure": structure,
        "synthesis": {
            "available": True,
            "summary": {
                "one_line": "一句话。",
                "core_design": [],
                "technology_choices": [],
                "highlights": [],
                "risks": [],
                "use_cases": [],
            },
            "dimensions": {},
        },
    }

    if focus_dimensions is not None:

        data["research_plan"] = {
            "question": "分析项目的 agent",
            "focus": {
                "dimensions": focus_dimensions,
                "notes": "关心协作",
                "source": "llm",
            },
        }

    return data


def section(content, start, end):

    return content[
        content.index(start): content.index(end)
    ]


def test_focus_chapter_is_expanded():
    """重点章节要展开实现明细。"""

    content = ReportGenerationSkill._build_report(
        build_report_data(["agents"])
    )

    agents = section(
        content,
        "## 04 Agent 架构",
        "## 05 Workflow",
    )

    assert "**实现明细**" in agents

    assert "class AgentsThing(Base)" in agents

    # 措辞不能自相矛盾。
    assert "以上为本次展开的实现明细" in agents

    assert "未放入本报告" not in agents


def test_non_focus_chapter_is_compressed():
    """非重点章节压成一行，但不消失。"""

    content = ReportGenerationSkill._build_report(
        build_report_data(["agents"])
    )

    workflow = section(
        content,
        "## 05 Workflow",
        "## 06 Skill",
    )

    assert "本次未展开" in workflow

    assert "未按问题展开" in workflow

    # 不能整章删掉 —— 报告必须仍是完整的 01-11。
    assert "## 05 Workflow" in content

    assert "## 09 Memory" in content


def test_report_states_the_question_and_focus():
    """报告开头要写清问了什么、重点在哪。"""

    content = ReportGenerationSkill._build_report(
        build_report_data(["agents"])
    )

    head = content[: content.index("## 01")]

    assert "**本次问题**：分析项目的 agent" in head

    assert "**本次重点**：Agent 架构" in head


def test_report_unchanged_without_focus():
    """
    没有识别出重点时保持全量等深。

    这是对旧行为的兼容：
    泛泛地问「分析这个项目」不该
    让用户丢掉任何章节的细节。
    """

    content = ReportGenerationSkill._build_report(
        build_report_data(None)
    )

    for name in ("## 04 Agent 架构", "## 09 Memory"):

        assert name in content

    assert "本次未展开" not in content


def test_compressed_chapter_keeps_judgment():
    """压缩后仍保留综合判断，不丢结论。"""

    data = build_report_data(["agents"])

    data["synthesis"]["dimensions"] = {
        "workflow": "LangGraph 编排。"
    }

    content = ReportGenerationSkill._build_report(
        data
    )

    assert "**综合判断**：LangGraph 编排。" in (
        content
    )
