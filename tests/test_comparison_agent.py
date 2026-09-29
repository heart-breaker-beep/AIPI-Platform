"""
Comparison Agent 测试。

重要：

本文件所有 fixture 都模拟 RunMemory.load() 的
真实返回结构，不再使用 project["analysis"]
这种真实系统中并不存在的结构。

真实结构（顶层 key）：

    run_id / status / current_node / question
    repository / research_plan / final_report
    agent_outputs / task_results / evidences / workflow_state
"""

import pytest

from app.agents.comparison_agent import (
    ComparisonAgent,
)

# Phase 13 文档 16.3 定义的比较维度。
PHASE13_DIMENSIONS = [
    "agent",
    "workflow",
    "skill",
    "tool",
    "rag",
    "memory",
    "database",
    "deployment",
    "code_complexity",
    "extension",
]

EXECUTED_TASKS = [
    "repository_analysis_agent",
    "architecture_analysis_agent",
    "technology_analysis_agent",
    "evidence_analysis_agent",
    "critic_agent",
]

RESEARCH_PLAN = {
    "tasks": list(EXECUTED_TASKS),
    "plan_version": 1,
    "analysis_type": "github_agent_project",
    "evidence_required": True,
}


def real_project(
    run_id="run-a",
    repository_id=26,
    repository_name="project-a",
    executed_tasks=None,
    research_plan=None,
    technology_stack=None,
    architecture=None,
    evidences=None,
    language="Python",
    size_kb=8586,
    question="分析这个项目",
):
    """
    构造一个与 RunMemory.load() 真实返回结构一致的 project。

    注意：刻意不包含 project["analysis"]。
    """

    plan = (
        RESEARCH_PLAN
        if research_plan is None
        else research_plan
    )

    return {
        "run_id": run_id,
        "status": "COMPLETED",
        "current_node": "end",
        "question": question,
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
        "research_plan": plan,
        "final_report": {
            "report": {
                "path": f"reports/{run_id}.md",
                "format": "markdown",
            },
            "content": "# report",
        },
        "agent_outputs": [
            {
                "dependencies": {},
                "readme": "# readme",
                "repository": {},
            },
        ],
        "task_results": [],
        "evidences": list(
            evidences or []
        ),
        "workflow_state": {
            "status": "COMPLETED",
            "current_node": "end",
            "data": {
                "executed_tasks": list(
                    EXECUTED_TASKS
                    if executed_tasks is None
                    else executed_tasks
                ),
                "research_plan": plan,
                "repository": {
                    "language": language,
                    "size": size_kb,
                },
                "architecture_analysis_agent": (
                    architecture
                    if architecture is not None
                    else {
                        "files": [],
                        "modules": [],
                    }
                ),
                "technology_stack": (
                    technology_stack
                    if technology_stack is not None
                    else {
                        "llm": [],
                        "database": [],
                        "embedding": [],
                        "deployment": [],
                        "frameworks": [],
                        "source_files": [],
                    }
                ),
            },
        },
    }


def real_evidence(
    evidence_id,
    content,
    file_path="README.md",
):
    """构造一条与真实 Evidence 行结构一致的记录。"""

    return {
        "id": evidence_id,
        "source_type": "github",
        "file_path": file_path,
        "line_start": 1,
        "line_end": 10,
        "content": content,
        "verification_status": "UNVERIFIED",
    }


async def run_compare(project_a, project_b):
    """执行一次比较。"""

    agent = ComparisonAgent(
        skill_registry=None
    )

    return await agent.execute(
        context=None,
        input_data={
            "project_a": project_a,
            "project_b": project_b,
        },
    )


def test_dimensions_match_phase13_document():
    """比较维度必须与 Phase 13 文档一致。"""

    assert list(
        ComparisonAgent.DIMENSIONS
    ) == PHASE13_DIMENSIONS


def test_fixture_has_no_fake_analysis_schema():
    """
    回归保护：fixture 不得再出现
    真实系统中不存在的 project["analysis"]。
    """

    project = real_project()

    assert "analysis" not in project

    assert "workflow_state" in project

    assert "evidences" in project


@pytest.mark.asyncio
async def test_agent_dimension_reads_executed_tasks():
    """Agent 维度必须读取真实 executed_tasks。"""

    same = await run_compare(
        real_project("run-a"),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    agent_dimension = same["comparison"]["agent"]

    assert agent_dimension["relation"] == "SAME"

    assert (
        agent_dimension["project_a"]["value"]
        == {
            "count": 5,
            "agents": EXECUTED_TASKS,
        }
    )

    assert (
        agent_dimension["project_a"]["available"]
        is True
    )

    assert (
        agent_dimension["source"]
        == "workflow_state.data.executed_tasks"
    )

    different = await run_compare(
        real_project("run-a"),
        real_project(
            "run-b",
            repository_id=35,
            executed_tasks=[
                "repository_analysis_agent",
                "critic_agent",
            ],
        ),
    )

    assert (
        different["comparison"]["agent"][
            "relation"
        ]
        == "DIFFERENT"
    )


@pytest.mark.asyncio
async def test_workflow_dimension_uses_research_plan():
    """
    Workflow 维度读取真实 research_plan。

    不同提问不应影响该维度：
    research_plan["question"] 属于 Run 元数据，
    不是被分析项目的属性。
    """

    result = await run_compare(
        real_project(
            "run-a",
            question="第一个完全不同的问题",
        ),
        real_project(
            "run-b",
            repository_id=35,
            question="第二个完全不同的问题",
        ),
    )

    workflow = result["comparison"]["workflow"]

    assert workflow["relation"] == "SAME"

    assert (
        workflow["project_a"]["value"]
        == RESEARCH_PLAN
    )

    assert (
        workflow["source"]
        == "workflow_state.data.research_plan"
    )


@pytest.mark.asyncio
async def test_run_status_does_not_create_false_evidence():
    """
    回归保护：Run 执行状态不能污染 Evidence 归因。

    workflow_state.status == "COMPLETED"
    这类 Run 元数据若进入维度值，
    token "completed" 会与 README Evidence 巧合匹配，
    产生看起来合理、实际无意义的 Evidence 引用。
    """

    # Evidence 内容里刻意包含 "completed" 与 "end"。
    result = await run_compare(
        real_project(
            "run-a",
            evidences=[
                real_evidence(
                    "evidence-real-1",
                    "The analysis was completed "
                    "and reached the end.",
                ),
            ],
        ),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    # workflow 维度值只有 research_plan，
    # 不含 status / current_node，因此不应引用 Evidence。
    assert (
        result["comparison"]["workflow"][
            "project_a"
        ]["evidence_ids"]
        == []
    )

    # agent 维度同理：Agent 名称不会命中 Evidence。
    assert (
        result["comparison"]["agent"][
            "project_a"
        ]["evidence_ids"]
        == []
    )

    # 没有任何真实引用，因此 evidence_based 必须为 False。
    assert result["evidence_based"] is False


@pytest.mark.asyncio
async def test_database_dimension_uses_technology_stack():
    """Database 维度读取真实 technology_stack.database。"""

    result = await run_compare(
        real_project(
            "run-a",
            technology_stack={
                "database": ["PostgreSQL"],
                "deployment": [],
                "embedding": [],
                "llm": [],
                "frameworks": [],
                "source_files": [
                    "docker-compose.yml"
                ],
            },
        ),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    database = result["comparison"]["database"]

    assert database["relation"] == "DIFFERENT"

    assert (
        database["project_a"]["value"]
        == ["PostgreSQL"]
    )

    assert database["project_b"]["value"] == []

    assert (
        database["source"]
        == (
            "workflow_state.data."
            "technology_stack.database"
        )
    )


@pytest.mark.asyncio
async def test_rag_dimension_uses_embedding_field():
    """RAG 维度读取 technology_stack.embedding（向量库检测）。"""

    result = await run_compare(
        real_project(
            "run-a",
            technology_stack={
                "database": [],
                "deployment": [],
                "embedding": ["Qdrant"],
                "llm": [],
                "frameworks": [],
                "source_files": [],
            },
        ),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    rag = result["comparison"]["rag"]

    assert rag["relation"] == "DIFFERENT"

    assert rag["project_a"]["value"] == ["Qdrant"]

    assert (
        rag["source"]
        == (
            "workflow_state.data."
            "technology_stack.embedding"
        )
    )


@pytest.mark.asyncio
async def test_deployment_dimension_uses_technology_stack():
    """Deployment 维度读取真实 technology_stack.deployment。"""

    result = await run_compare(
        real_project(
            "run-a",
            technology_stack={
                "database": [],
                "deployment": ["Docker"],
                "embedding": [],
                "llm": [],
                "frameworks": [],
                "source_files": [],
            },
        ),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    deployment = result["comparison"]["deployment"]

    assert deployment["relation"] == "DIFFERENT"

    assert deployment["project_a"]["value"] == [
        "Docker"
    ]


@pytest.mark.asyncio
async def test_code_complexity_uses_repository_and_architecture():
    """代码复杂度维度读取真实 repository / architecture 数据。"""

    result = await run_compare(
        real_project(
            "run-a",
            language="Python",
            size_kb=8586,
            architecture={
                "files": ["a.py", "b.py"],
                "modules": [{"file_path": "a.py"}],
            },
        ),
        real_project(
            "run-b",
            repository_id=35,
            language="Go",
            size_kb=120,
        ),
    )

    complexity = result["comparison"][
        "code_complexity"
    ]

    assert complexity["relation"] == "DIFFERENT"

    value_a = complexity["project_a"]["value"]

    assert value_a["language"] == "Python"

    assert value_a["size_kb"] == 8586

    assert value_a["file_count"] == 2

    assert value_a["module_count"] == 1

    assert complexity["project_b"]["value"][
        "language"
    ] == "Go"


@pytest.mark.asyncio
async def test_unavailable_dimensions_explain_missing_data():
    """
    skill / tool / memory / extension
    在真实数据中确实不存在，
    必须返回 NOT_AVAILABLE 并说明原因。
    """

    result = await run_compare(
        real_project("run-a"),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    for dimension in (
        "skill",
        "tool",
        "memory",
        "extension",
    ):

        entry = result["comparison"][dimension]

        assert entry["relation"] == "NOT_AVAILABLE"

        assert (
            entry["project_a"]["available"]
            is False
        )

        reason = entry["project_a"][
            "unavailable_reason"
        ]

        assert "真实数据不存在" in reason


@pytest.mark.asyncio
async def test_missing_workflow_state_is_unavailable():
    """
    缺少 workflow_state 时必须是
    “真实数据缺失”，而不是读错了字段名。
    """

    project_without_state = {
        "run_id": "run-a",
        "status": "COMPLETED",
        "repository": {"id": 1},
        "evidences": [],
    }

    result = await run_compare(
        project_without_state,
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    assert (
        result["comparison"]["agent"]["relation"]
        == "ONE_SIDE_UNAVAILABLE"
    )

    assert (
        "executed_tasks"
        in result["comparison"]["agent"][
            "project_a"
        ]["unavailable_reason"]
    )


@pytest.mark.asyncio
async def test_fake_analysis_schema_is_ignored():
    """
    project["analysis"] 不再被读取。

    即使传入旧结构，也不会产生有效维度值。
    """

    legacy_project = {
        "run_id": "run-a",
        "status": "COMPLETED",
        "repository": {"id": 1},
        "evidences": [],
        "analysis": {
            "agents": {
                "count": 99,
                "evidence_ids": [
                    "fake-evidence-id"
                ],
            },
            "database": {
                "type": "FakeDB",
                "evidence_ids": [
                    "fake-evidence-id"
                ],
            },
        },
    }

    result = await run_compare(
        legacy_project,
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    assert (
        result["comparison"]["agent"]["relation"]
        == "ONE_SIDE_UNAVAILABLE"
    )

    assert (
        result["comparison"]["database"][
            "project_a"
        ]["value"]
        is None
    )

    # 关键：假 evidence id 绝不能出现在结果里。
    assert "fake-evidence-id" not in str(
        result
    )


@pytest.mark.asyncio
async def test_evidence_ids_come_from_real_evidences():
    """
    evidence_ids 必须来自 project["evidences"][*]["id"]。

    真实 Evidence 使用 id 字段，
    而不是 evidence_id / evidence_ids。
    """

    result = await run_compare(
        real_project(
            "run-a",
            technology_stack={
                "database": ["PostgreSQL"],
                "deployment": [],
                "embedding": [],
                "llm": [],
                "frameworks": [],
                "source_files": [],
            },
            evidences=[
                real_evidence(
                    "evidence-real-1",
                    "This project stores data in "
                    "PostgreSQL.",
                ),
                real_evidence(
                    "evidence-real-2",
                    "Unrelated content about CSS.",
                ),
            ],
        ),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    evidence_ids = (
        result["comparison"]["database"][
            "project_a"
        ]["evidence_ids"]
    )

    assert evidence_ids == ["evidence-real-1"]

    assert (
        result["comparison"]["agent"][
            "project_a"
        ]["evidence_ids"]
        == []
    )


@pytest.mark.asyncio
async def test_evidence_ids_are_never_invented():
    """引用的 Evidence ID 必须全部存在于真实 evidences 中。"""

    evidences = [
        real_evidence(
            "evidence-real-1",
            "Uses PostgreSQL.",
        ),
    ]

    result = await run_compare(
        real_project(
            "run-a",
            technology_stack={
                "database": ["PostgreSQL"],
                "deployment": [],
                "embedding": [],
                "llm": [],
                "frameworks": [],
                "source_files": [],
            },
            evidences=evidences,
        ),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    known_ids = {
        evidence["id"]
        for evidence in evidences
    }

    for dimension in result["comparison"].values():

        for side in (
            "project_a",
            "project_b",
        ):

            for evidence_id in dimension[
                side
            ]["evidence_ids"]:

                assert evidence_id in known_ids


@pytest.mark.asyncio
async def test_evidence_based_is_false_without_evidence():
    """
    evidence_based 不再硬编码。

    没有任何 Evidence 引用时必须为 False。
    """

    result = await run_compare(
        real_project("run-a"),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    assert result["evidence_based"] is False


@pytest.mark.asyncio
async def test_evidence_based_is_true_with_real_evidence():
    """存在真实 Evidence 引用时必须为 True。"""

    result = await run_compare(
        real_project(
            "run-a",
            technology_stack={
                "database": ["PostgreSQL"],
                "deployment": [],
                "embedding": [],
                "llm": [],
                "frameworks": [],
                "source_files": [],
            },
            evidences=[
                real_evidence(
                    "evidence-real-1",
                    "Backed by PostgreSQL.",
                ),
            ],
        ),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    assert result["evidence_based"] is True


@pytest.mark.asyncio
async def test_evidence_based_not_triggered_by_dimensions_alone():
    """
    evidence_based 不能因为“有 dimensions”而变 True。
    """

    result = await run_compare(
        real_project("run-a"),
        real_project(
            "run-b",
            repository_id=35,
        ),
    )

    assert len(result["comparison"]) == 10

    assert result["evidence_based"] is False
