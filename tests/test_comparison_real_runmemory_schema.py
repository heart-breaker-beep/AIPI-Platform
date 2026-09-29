"""
Phase 13 真实结构回归测试。

背景：

修复前 ComparisonAgent 假设 project["analysis"] 存在，
而 RunMemory.load() 的真实返回中并没有这个 key，
导致 10 个维度里 9 个恒为 NOT_AVAILABLE，
evidence_ids 恒为空，evidence_based 恒为 True（硬编码）。

本文件用 RunMemory.load() 的真实结构作为 fixture，
锁住以下事实：

    1. Agent 维度不再因为缺少 analysis 而直接 NOT_AVAILABLE
    2. executed_tasks 可以被正确读取
    3. Evidence 的 id 可以被正确读取
    4. project["evidences"] 会被真正使用
    5. evidence_ids 不再全部为 0
    6. evidence_based 不再硬编码 True

fixture 结构取自当前工作区真实数据
（run d1d71c3e 的 RunMemory.load() 返回），
只对长文本与 id 做了缩短处理。
"""

import pytest

from app.agents.comparison_agent import (
    ComparisonAgent,
)


def project_structure(
    agents=(),
    agent_topics=(),
    workflow=(),
    tools=(),
    rag_topics=(),
    available=True,
):
    """
    构造被分析项目的自述结构。

    结构与 ArchitectureAnalysisSkill 的真实产出一致：
    7 个维度，每个含 declared / items / topics / evidence / reason。
    """

    def dimension(name, items, topics):

        declared = bool(items or topics)

        return {
            "declared": declared,
            "items": list(items),
            "topics": list(topics),
            "evidence": (
                [
                    {
                        "file_path": "README.md",
                        "line_start": 83,
                        "line_end": 83,
                        "text": f"- {name} ...",
                    }
                ]
                if declared
                else []
            ),
            "reason": (
                None
                if declared
                else f"没有 {name} 相关声明。"
            ),
        }

    return {
        "available": available,
        "basis": "readme+topics",
        "reason": (
            None if available else "没有可用 README。"
        ),
        "dimensions": {
            "agents": dimension(
                "agents", agents, agent_topics
            ),
            "workflow": dimension(
                "workflow", workflow, ()
            ),
            "skills": dimension("skills", (), ()),
            "tools": dimension("tools", tools, ()),
            "rag": dimension(
                "rag", (), rag_topics
            ),
            "memory": dimension("memory", (), ()),
            "extension": dimension(
                "extension", (), ()
            ),
        },
    }


def build_real_run(
    run_id,
    repository_id,
    repository_name,
    technology_stack,
    evidences=None,
    language="Python",
    size_kb=8586,
    agents=(),
    agent_topics=(),
    workflow=(),
    tools=(),
    rag_topics=(),
):
    """
    构造与 RunMemory.load() 完全一致的顶层结构。

    真实顶层 key：
        run_id / status / current_node / question
        repository / research_plan / final_report
        agent_outputs / task_results / evidences
        workflow_state
    """

    executed_tasks = [
        "repository_analysis_agent",
        "architecture_analysis_agent",
        "technology_analysis_agent",
        "evidence_analysis_agent",
        "critic_agent",
    ]

    research_plan = {
        "tasks": list(executed_tasks),
        "question": "分析这个 GitHub Agent 项目",
        "plan_version": 1,
        "analysis_type": "github_agent_project",
        "evidence_required": True,
    }

    return {
        "run_id": run_id,
        "status": "COMPLETED",
        "current_node": "end",
        "question": "分析这个 GitHub Agent 项目",

        # RunMemory 返回的是数据库 Repository 摘要。
        "repository": {
            "id": repository_id,
            "url": (
                "https://github.com/demo/"
                f"{repository_name}"
            ),
            "owner": "demo",
            "name": repository_name,
            "description": None,
            "language": language,
        },

        "research_plan": research_plan,

        "final_report": {
            "report": {
                "path": f"reports/{run_id}_analysis.md",
                "format": "markdown",
            },
            "content": "## report",
        },

        # 真实 run 的 agent_outputs 顺序：
        # planner / repository / architecture /
        # technology / evidence / critic / final_report
        "agent_outputs": [
            {
                "tasks": list(executed_tasks),
                "research_plan": research_plan,
            },
            {
                "readme": "# readme",
                "repository": {},
                "dependencies": {},
            },
            {
                "files": [],
                "modules": [],
            },
            {
                "technology_stack": technology_stack,
            },
            {
                "count": len(evidences or []),
                "evidence": [],
            },
            {
                "errors": [],
                "passed": True,
            },
            {
                "report": {"format": "markdown"},
                "content": "# report",
            },
        ],

        # 真实 run 中 analysis_tasks 表为空。
        "task_results": [],

        "evidences": list(evidences or []),

        "workflow_state": {
            "status": "COMPLETED",
            "current_node": "end",
            "errors": [],
            "retry_count": 0,
            "pause_reason": None,
            "human_approved": True,
            "checkpoint_version": 10,
            "data": {
                "run_id": run_id,
                "repository_id": repository_id,
                "repository": {
                    "language": language,
                    "size": size_kb,
                },
                # AIPI 自己的执行数据：
                # 真实 run 里有，但 Phase 13 不能用它比较项目。
                "executed_tasks": list(executed_tasks),
                "research_plan": research_plan,
                "technology_stack": technology_stack,
                "architecture_analysis_agent": {
                    "files": [],
                    "modules": [],
                },
                # 项目级事实（Phase 13 的真实来源）：
                # 由 ArchitectureAnalysisSkill 从被分析项目的
                # README / topics 确定性抽取。
                "project_structure": project_structure(
                    agents=agents,
                    agent_topics=agent_topics,
                    workflow=workflow,
                    tools=tools,
                    rag_topics=rag_topics,
                ),
                "critic_agent": {
                    "errors": [],
                    "passed": True,
                },
                "evidence_analysis_agent": {
                    "count": len(evidences or []),
                    "evidence": [],
                },
                "readme": "# readme",
                "question": "分析这个 GitHub Agent 项目",
            },
        },
    }


def real_evidence(
    evidence_id,
    content,
):
    """真实 Evidence 行的字段结构。"""

    return {
        "id": evidence_id,
        "source_type": "github",
        "file_path": "README.md",
        "line_start": 1,
        "line_end": 215,
        "content": content,
        "verification_status": "UNVERIFIED",
    }


# 与真实 run d1d71c3e 一致的 technology_stack：
# database 检测到 PostgreSQL，source_files 只拿到 docker-compose.yml。
TECH_A = {
    "llm": [],
    "database": ["PostgreSQL"],
    "embedding": [],
    "deployment": [],
    "frameworks": [],
    "source_files": ["docker-compose.yml"],
}

# 与真实 run 799049b1 一致：技术栈全部为空。
TECH_B = {
    "llm": [],
    "database": [],
    "embedding": [],
    "deployment": [],
    "frameworks": [],
    "source_files": [],
}

EVIDENCES_A = [
    real_evidence(
        "55c64c81-b22b-4098-81c0-08d0bc5e5355",
        "This project stores data in PostgreSQL.",
    ),
    real_evidence(
        "35e63b87-8ded-42f7-8389-c6f14ea8fb7a",
        "Deployment uses Docker.",
    ),
]


async def compare_two_real_runs():
    """执行一次真实结构下的比较。"""

    agent = ComparisonAgent(
        skill_registry=None
    )

    return await agent.execute(
        context=None,
        input_data={
            # 项目 A：README 自述了 Agent / Workflow / Tool / RAG
            "project_a": build_real_run(
                "d1d71c3e-a9b6-4073-8d3d-bbbfe0b11005",
                26,
                "Multi-Agent-Research-Assistant",
                TECH_A,
                evidences=EVIDENCES_A,
                agents=[
                    "Planner",
                    "Executor",
                    "Critic",
                ],
                agent_topics=["multi-agent"],
                workflow=["StateGraph"],
                tools=["web_search", "read_webpage"],
                rag_topics=["rag"],
            ),
            # 项目 B：README 没有声明这些能力
            "project_b": build_real_run(
                "799049b1-3d51-4c2f-bbe5-81930ce59a23",
                35,
                "enterprise-workflow-agent-platform",
                TECH_B,
            ),
        },
    )


def test_real_fixture_has_no_analysis_key():
    """
    fixture 必须与真实结构一致：

    有 workflow_state / evidences，
    没有 project["analysis"]。
    """

    project = build_real_run(
        "run-a",
        26,
        "repo-a",
        TECH_A,
    )

    assert "analysis" not in project

    assert "workflow_state" in project

    assert "evidences" in project

    assert "agent_outputs" in project

    assert "task_results" in project


@pytest.mark.asyncio
async def test_requirement_1_agent_dimension_is_available():
    """
    要求 1：
    Agent 维度不再因为缺少 analysis 而 NOT_AVAILABLE。
    """

    result = await compare_two_real_runs()

    agent_dimension = result["comparison"]["agent"]

    assert (
        agent_dimension["relation"]
        != "NOT_AVAILABLE"
    )

    assert (
        agent_dimension["project_a"]["available"]
        is True
    )

    assert (
        agent_dimension["project_b"]["available"]
        is True
    )


@pytest.mark.asyncio
async def test_requirement_2_project_structure_is_read():
    """
    要求 2：
    被分析项目的自述结构可以被正确读取。

    （Phase 13 之前这里读的是 executed_tasks，
      那是 AIPI 自己的执行数据。）
    """

    result = await compare_two_real_runs()

    value = result["comparison"]["agent"][
        "project_a"
    ]["value"]

    assert value["declared"] is True

    assert value["items"] == [
        "Critic",
        "Executor",
        "Planner",
    ]

    assert value["topics"] == ["multi-agent"]

    assert (
        result["comparison"]["agent"]["source"]
        == (
            "workflow_state.data."
            "project_structure.dimensions.agents"
        )
    )


@pytest.mark.asyncio
async def test_requirement_3_evidence_id_field_is_read():
    """
    要求 3：
    Evidence 使用 id 字段，可以被正确读取。
    """

    result = await compare_two_real_runs()

    database = result["comparison"]["database"]

    assert database["project_a"][
        "evidence_ids"
    ] == [
        "55c64c81-b22b-4098-81c0-08d0bc5e5355"
    ]


def total_evidence_ids(result, side):
    """统计某一侧被引用的 Evidence 总数。"""

    return sum(
        len(entry[side]["evidence_ids"])
        for entry in result["comparison"].values()
    )


@pytest.mark.asyncio
async def test_requirement_4_project_evidences_is_used():
    """
    要求 4：
    project["evidences"] 会被真正使用。

    两个项目的 evidences 不同，
    因此引用情况必须不同：
    项目 A 有 Evidence 且被引用，
    项目 B 的 evidences 为空，引用必须为 0。
    """

    result = await compare_two_real_runs()

    assert total_evidence_ids(
        result,
        "project_a",
    ) > 0

    assert (
        total_evidence_ids(
            result,
            "project_b",
        )
        == 0
    )

    assert (
        result["comparison"]["database"][
            "project_b"
        ]["evidence_ids"]
        == []
    )

    # deployment 维度在真实 run A 中为空列表，
    # 空值没有 token 可匹配，
    # 因此不会产生 Evidence 引用。
    assert (
        result["comparison"]["deployment"][
            "project_a"
        ]["value"]
        == []
    )

    assert (
        result["comparison"]["deployment"][
            "project_a"
        ]["evidence_ids"]
        == []
    )


@pytest.mark.asyncio
async def test_requirement_5_evidence_ids_not_all_empty():
    """
    要求 5：
    evidence_ids 不再全部为 0。

    修复前 10 个维度的 evidence_ids 全为 0。
    """

    result = await compare_two_real_runs()

    total = 0

    for dimension in result["comparison"].values():

        for side in (
            "project_a",
            "project_b",
        ):

            total += len(
                dimension[side]["evidence_ids"]
            )

    assert total > 0


@pytest.mark.asyncio
async def test_requirement_6_evidence_based_is_computed():
    """
    要求 6：
    evidence_based 不再硬编码 True，而是由真实引用决定。
    """

    with_evidence = await compare_two_real_runs()

    assert with_evidence["evidence_based"] is True

    agent = ComparisonAgent(
        skill_registry=None
    )

    without_evidence = await agent.execute(
        context=None,
        input_data={
            "project_a": build_real_run(
                "run-a",
                26,
                "repo-a",
                TECH_A,
                evidences=[],
            ),
            "project_b": build_real_run(
                "run-b",
                35,
                "repo-b",
                TECH_B,
                evidences=[],
            ),
        },
    )

    assert without_evidence["evidence_based"] is False


@pytest.mark.asyncio
async def test_all_ten_dimensions_are_comparable():
    """
    Phase 13 修复后 10 个维度全部可比较。

    修复前：只有 1 个维度可用，
    另外 6 个恒为 NOT_AVAILABLE、2 个语义错误。
    """

    result = await compare_two_real_runs()

    usable = [
        dimension
        for dimension, entry in (
            result["comparison"].items()
        )
        if entry["project_a"]["available"]
        or entry["project_b"]["available"]
    ]

    assert sorted(usable) == sorted(
        result["comparison"].keys()
    )

    assert len(usable) == 10


@pytest.mark.asyncio
async def test_undeclared_capability_is_reported_not_invented():
    """
    B 项目没有声明 skill / memory / extension 时，
    如实返回 declared=False，而不是编造内容，
    也不是用 AIPI 自己的 Skill/Memory 顶上。
    """

    result = await compare_two_real_runs()

    for dimension in (
        "skill",
        "memory",
        "extension",
    ):

        entry = result["comparison"][dimension]

        # 数据是可用的（确实做了判断）……
        assert entry["project_b"]["available"] is True

        # ……但结论是「未声明」，不是编造。
        assert (
            entry["project_b"]["value"]["declared"]
            is False
        )

        assert entry["project_b"]["value"][
            "items"
        ] == []

        # 两个项目都未声明 → SAME
        assert entry["relation"] == "SAME"


@pytest.mark.asyncio
async def test_database_dimension_is_different_between_real_runs():
    """
    真实数据下 database 维度应该能区分两个项目。

    run A 检测到 PostgreSQL，
    run B 技术栈为空。
    """

    result = await compare_two_real_runs()

    assert (
        result["comparison"]["database"][
            "relation"
        ]
        == "DIFFERENT"
    )

    assert (
        result["comparison"]["database"][
            "project_a"
        ]["value"]
        == ["PostgreSQL"]
    )
