"""
代码证据与 README 自述合并的测试。

覆盖：

1. 代码抽到的维度，declared_by 为 code / code+readme
2. 只有 README 声明的维度，declared_by 为 readme
3. 两侧都没有时 declared=False，且给出新原因
4. declared / items / topics / evidence / reason
   五个契约字段的类型与含义不变
   （报告各维度章按它们渲染）
5. 报告能渲染出代码证据与结论来源

全程使用假 Tool，不联网。
"""

import pytest

from app.core.exceptions import ToolError
from app.project_analysis.code_structure_extractor import (
    CodeStructureExtractor,
)
from app.skills.architecture_analysis_skill import (
    ArchitectureAnalysisSkill,
)
from app.skills.report_generation_skill import (
    ReportGenerationSkill,
)

TREE = (
    "src/app/main.py",
    "src/app/agents/invoice_agent.py",
    "src/app/graph/workflow.py",
    "src/app/tools/supplier_lookup.py",
    "src/app/rag/retriever.py",
)


SOURCES = {
    "src/app/agents/invoice_agent.py": (
        "class InvoiceAgent:\n"
        "    pass\n"
    ),
    "src/app/graph/workflow.py": (
        "from langgraph.graph import StateGraph\n"
        "\n"
        "graph = StateGraph(AgentState)\n"
        "graph.add_node('intake', intake_node)\n"
        "graph.add_edge('intake', 'approve')\n"
    ),
    "src/app/tools/supplier_lookup.py": (
        "class SupplierLookupTool:\n"
        "    pass\n"
    ),
    "src/app/rag/retriever.py": (
        "from qdrant_client import QdrantClient\n"
        "\n"
        "def retrieve_documents(query):\n"
        "    pass\n"
    ),
    "src/app/main.py": (
        "from fastapi import FastAPI\n"
        "\n"
        "app = FastAPI()\n"
    ),
}


# README 只声明了 workflow，
# 其余维度全靠代码抽取。
README = (
    "# Demo\n"
    "\n"
    "## Workflow\n"
    "- LangGraph state orchestration\n"
)


class FakeCodeSearch:
    """GitHub Code Search 对该仓库返回 0 条。"""

    async def execute(self, **kwargs):
        return []


class FakeRepositoryTool:

    async def get_tree(self, **kwargs):
        return [
            {"path": path, "type": "blob"}
            for path in TREE
        ]


class FakeFileReader:

    async def execute(
        self,
        owner,
        name,
        file_path,
        branch,
    ):
        if file_path == "README.md":
            return README

        if file_path in SOURCES:
            return SOURCES[file_path]

        raise ToolError(f"HTTP 404: {file_path}")


class FakeContext:

    def __init__(self):
        self.tools = {
            "github_code_search": FakeCodeSearch(),
            "github_repository": FakeRepositoryTool(),
            "file_reader": FakeFileReader(),
        }


@pytest.fixture
def structure():
    """跑一次真实的 ArchitectureAnalysisSkill。"""

    import asyncio

    skill = ArchitectureAnalysisSkill()

    result = asyncio.run(
        skill.execute(
            FakeContext(),
            {
                "owner": "demo",
                "repo": "demo",
                "branch": "main",
                "readme": README,
                "repository": {
                    "topics": [],
                    "description": "a demo",
                },
            },
        )
    )

    return result["project_structure"]


# ----------------------------------------------------------------
# 合并语义
# ----------------------------------------------------------------


def test_code_signals_declare_dimension(structure):
    """代码里有的维度必须被判为已声明。"""

    agents = structure["dimensions"]["agents"]

    assert agents["declared"] is True

    assert agents["declared_by"] == "code"

    assert any(
        "InvoiceAgent" in item
        for item in agents["items"]
    )


def test_code_evidence_carries_file_and_line(structure):
    """
    代码证据必须带文件与行号。

    这是本次改动的核心价值：
    从「README 里有这个词」
    变成「这个文件第 N 行确实这么写」。
    """

    workflow = structure["dimensions"]["workflow"]

    evidence = workflow["code_evidence"]

    assert evidence

    node_call = next(
        item
        for item in evidence
        if "add_node" in (item["text"] or "")
    )

    assert node_call["file_path"] == (
        "src/app/graph/workflow.py"
    )

    assert node_call["line_start"] == 4


def test_readme_and_code_combine(structure):
    """两侧都有时 declared_by 为 code+readme。"""

    workflow = structure["dimensions"]["workflow"]

    assert workflow["declared_by"] == "code+readme"

    # README 条目补在代码条目之后。
    assert "LangGraph state orchestration" in (
        workflow["items"]
    )


def test_langgraph_topic_alone_does_not_declare_agents(
    structure,
):
    """
    只有 LangGraph 而没有 Agent 类时，
    agents 维度不能被判为已声明。

    回归点：langgraph 曾经既算 workflow
    又算 agents，让任何 LangGraph 项目
    都凭空多出 agents 条目。
    """

    assert (
        "import langgraph.graph"
        not in structure["dimensions"]["agents"]["items"]
    )


def test_undeclared_dimension_keeps_reason(structure):
    """两侧都没有的维度必须给出原因。"""

    skills = structure["dimensions"]["skills"]

    assert skills["declared"] is False

    assert skills["declared_by"] is None

    assert skills["items"] == []

    assert "skills" in skills["reason"]


def test_contract_fields_keep_their_types(structure):
    """
    报告各维度章按这五个字段渲染，
    类型与含义都不能变。
    """

    for entry in structure["dimensions"].values():

        assert isinstance(
            entry["declared"],
            bool,
        )

        assert isinstance(entry["items"], list)

        assert isinstance(
            entry["topics"],
            list,
        )

        assert isinstance(
            entry["evidence"],
            list,
        )

        assert (
            entry["reason"] is None
            or isinstance(entry["reason"], str)
        )


def test_readme_evidence_keeps_line_numbers(structure):
    """
    README 证据的原有含义不变：
    仍然指向 README.md 的行号。
    """

    workflow = structure["dimensions"]["workflow"]

    readme_hit = [
        item
        for item in workflow["evidence"]
        if item["text"]
        == "- LangGraph state orchestration"
    ]

    assert readme_hit

    assert (
        readme_hit[0]["file_path"] == "README.md"
    )


def test_code_extraction_meta_is_reported(structure):
    """代码抽取的执行情况必须带出来。"""

    meta = structure["code_extraction"]

    assert meta["available"] is True

    assert meta["parsed_files"] == 5

    assert meta["unparsed"] == []


def test_basis_records_both_sources(structure):
    """basis 要说明结论来自代码与 README。"""

    assert structure["basis"] == (
        "code+readme+topics"
    )


# ----------------------------------------------------------------
# 按维度分配采集配额
# ----------------------------------------------------------------


def pick(paths):
    tree = [
        {"path": path, "type": "blob"}
        for path in paths
    ]

    return ArchitectureAnalysisSkill()._read_candidates(
        tree
    )


def test_every_dimension_gets_its_own_quota():
    """
    每个维度都要有独立名额。

    回归点：旧做法按「命中信号总数」全局排序，
    仓库目录结构会决定结果 ——
    agents/ 文件多就把 rag/ 挤掉，
    各模块详略极不均匀。
    """

    picked = pick(
        [
            "src/app/main.py",
            *[
                f"src/app/agents/a{i}.py"
                for i in range(10)
            ],
            *[
                f"src/app/graph/g{i}.py"
                for i in range(8)
            ],
            *[
                f"src/app/tools/t{i}.py"
                for i in range(3)
            ],
            "src/app/rag/r1.py",
            "src/app/rag/r2.py",
            "src/app/memory/m1.py",
            *[
                f"src/app/services/o{i}.py"
                for i in range(8)
            ],
        ]
    )

    dimensions = {
        dimension: sum(
            1
            for path in picked
            if dimension
            in CodeStructureExtractor.dimensions_for_path(
                path
            )
        )
        for dimension in (
            "workflow",
            "agents",
            "tools",
            "rag",
            "memory",
        )
    }

    # 即使 agents 文件是 rag 的 5 倍，
    # rag 也必须有样本。
    assert dimensions["rag"] >= 2

    assert dimensions["workflow"] >= 4

    assert dimensions["tools"] >= 3

    assert dimensions["memory"] >= 1


def test_quota_leftovers_backfill_the_budget():
    """
    配额之外的文件必须回填名额。

    否则「源码全在一个目录下」的仓库
    会只读到配额那么几个文件，
    其余名额白白浪费。
    """

    picked = pick(
        [
            *[
                f"src/app/agents/a{i}.py"
                for i in range(20)
            ],
            "src/app/main.py",
        ]
    )

    assert len(picked) == (
        ArchitectureAnalysisSkill.MAX_MODULES
    )


def test_low_priority_paths_lose_to_real_code():
    """
    名额不够时，测试 / 迁移目录优先被牺牲。

    注意它们是「最后才读」而不是「永不读」：
    名额够时仍会被读，
    因为多读一个文件总比空着名额好。
    """

    source = [
        f"src/app/services/s{i}.py"
        for i in range(
            ArchitectureAnalysisSkill.MAX_MODULES
        )
    ]

    picked = pick(
        source
        + [
            "tests/test_workflow.py",
            "alembic/versions/0001_init.py",
            "src/app/scripts/seed.py",
        ]
    )

    assert len(picked) == (
        ArchitectureAnalysisSkill.MAX_MODULES
    )

    assert "tests/test_workflow.py" not in picked

    assert (
        "alembic/versions/0001_init.py" not in picked
    )

    assert "src/app/scripts/seed.py" not in picked


def test_low_priority_paths_fill_spare_slots():
    """名额有剩时，低优先级路径仍应被读取。"""

    picked = pick(
        [
            "src/app/graph/workflow.py",
            "tests/test_workflow.py",
        ]
    )

    assert "src/app/graph/workflow.py" in picked

    assert "tests/test_workflow.py" in picked


# ----------------------------------------------------------------
# 报告渲染
# ----------------------------------------------------------------


def test_report_renders_anchors(structure):
    """
    默认报告要给证据锚点（文件:行号）。

    锚点是默认报告的「可回溯性」来源：
    要点可以归纳，锚点必须能逐条打开核对。
    """

    content = ReportGenerationSkill._build_report(
        {
            "project_structure": structure,
            "technology_stack": {
                "embedding": ["Qdrant"],
            },
        }
    )

    workflow = content[
        content.index("## 05 Workflow"):
        content.index("## 06 Skill")
    ]

    assert "**结论来源**：代码证据 + README 自述" in (
        workflow
    )

    assert "**证据锚点**" in workflow

    assert (
        "`src/app/graph/workflow.py:4`"
        in workflow
    )

    # README 出处也进锚点，与代码证据合并成一组。
    assert "`README.md:4`" in workflow


def test_default_report_shows_highlights_not_symbols():
    """
    默认报告要的是「要点」，不是符号清单。

    条目是 `builder.add_node('x', ...)` 这类原始符号，
    直接列出来只是堆符号；
    归纳成「图节点（3）：a、b、c」才是要点。
    """

    content = ReportGenerationSkill._build_report(
        {
            "project_structure": {
                "available": True,
                "basis": "code+readme+topics",
                "dimensions": {
                    "workflow": {
                        "declared": True,
                        "declared_by": "code",
                        "items": [
                            "StateGraph(...)",
                            "builder.add_node('intake', self._a)",
                            "builder.add_node('approve', self._b)",
                            "import langgraph.graph",
                            "路径 src/app/graph/",
                            "README 说了一句话",
                        ],
                        "topics": [],
                        "evidence": [],
                        "code_evidence": [],
                        "details": [],
                    },
                },
            }
        }
    )

    workflow = content[
        content.index("## 05 Workflow"):
        content.index("## 06 Skill")
    ]

    assert "**要点**" in workflow

    # 图调用被归纳成名字列表
    # （StateGraph 构造 + 两个 add_node）。
    assert "图结构（3）" in workflow

    assert "`StateGraph`" in workflow

    assert "`intake`" in workflow

    assert "`approve`" in workflow

    assert "依赖（1）：`langgraph.graph`" in workflow

    assert "目录（1）：`src/app/graph/`" in workflow

    # 原始符号不应再原样出现。
    assert "builder.add_node(" not in workflow


def test_default_report_points_to_deep_dive():
    """
    默认报告不放大块实现细节，
    但要给出深挖的入口。
    """

    content = ReportGenerationSkill._build_report(
        {
            "run_id": "run-123",
            "project_structure": {
                "available": True,
                "basis": "code+readme+topics",
                "dimensions": {
                    "workflow": {
                        "declared": True,
                        "declared_by": "code",
                        "items": ["StateGraph(...)"],
                        "topics": [],
                        "evidence": [],
                        "code_evidence": [],
                        "details": [
                            {
                                "kind": "graph",
                                "name": "duplicate_check",
                                "signature": "def f(self)",
                                "file_path": "a.py",
                                "line": 1,
                                "calls": [],
                                "literals": [],
                            }
                        ],
                    },
                },
            },
        }
    )

    workflow = content[
        content.index("## 05 Workflow"):
        content.index("## 06 Skill")
    ]

    # 实现明细的签名不进默认报告。
    assert "**实现细节**" not in workflow

    assert "def f(self)" not in workflow

    # 但必须指向深挖接口。
    assert "1 项实现明细" in workflow

    assert (
        "/analysis/run-123/deep-dive?module=workflow"
        in workflow
    )


def test_deep_dive_hint_uses_placeholder_without_run_id():
    """拿不到 run_id 时用占位符，不能渲染成 None。"""

    content = ReportGenerationSkill._build_report(
        {
            "project_structure": {
                "available": True,
                "basis": "code+readme+topics",
                "dimensions": {
                    "rag": {
                        "declared": True,
                        "declared_by": "code",
                        "items": ["def retrieve(q)"],
                        "topics": [],
                        "evidence": [],
                        "code_evidence": [],
                        "details": [
                            {
                                "kind": "function",
                                "name": "retrieve",
                                "signature": "def retrieve(q)",
                                "file_path": "a.py",
                                "line": 1,
                                "calls": [],
                                "literals": [],
                            }
                        ],
                    },
                },
            }
        }
    )

    rag = content[
        content.index("## 08 RAG"):
        content.index("## 09 Memory")
    ]

    assert "{run_id}" in rag

    assert "None" not in rag


def test_report_renders_path_signal_without_line():
    """
    路径信号没有行号，
    不能渲染成 `src/app/agents/:None`。
    """

    content = ReportGenerationSkill._build_report(
        {
            "project_structure": {
                "available": True,
                "basis": "code+readme+topics",
                "dimensions": {
                    "agents": {
                        "declared": True,
                        "declared_by": "code",
                        "items": ["路径 src/app/agents/"],
                        "topics": [],
                        "evidence": [],
                        "code_evidence": [
                            {
                                "file_path": (
                                    "src/app/agents/"
                                ),
                                "line_start": None,
                                "text": (
                                    "路径 src/app/agents/"
                                ),
                            }
                        ],
                    },
                },
            }
        }
    )

    agents = content[
        content.index("## 04 Agent 架构"):
        content.index("## 05 Workflow")
    ]

    assert "None" not in agents

    assert (
        "目录/文件名命中架构关键词："
        "`src/app/agents/`"
    ) in agents
