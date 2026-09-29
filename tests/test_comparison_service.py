"""
Comparison Service 测试。

fixture 使用 RunMemory.load() 的真实返回结构
（workflow_state / evidences），
不再使用真实系统中不存在的 project["analysis"]。

同时这里不再替换 ComparisonAgent，
而是让真实的 ComparisonAgent 参与测试，
以验证“服务 → Agent → 真实数据”整条链路。
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.schemas.comparison import (
    ComparisonCreateRequest,
)
from app.services.comparison_service import (
    ComparisonService,
)


EXECUTED_TASKS = [
    "repository_analysis_agent",
    "architecture_analysis_agent",
    "technology_analysis_agent",
    "evidence_analysis_agent",
    "critic_agent",
]

TECH_WITH_DATABASE = {
    "llm": [],
    "database": ["PostgreSQL"],
    "embedding": [],
    "deployment": [],
    "frameworks": [],
    "source_files": ["docker-compose.yml"],
}

TECH_EMPTY = {
    "llm": [],
    "database": [],
    "embedding": [],
    "deployment": [],
    "frameworks": [],
    "source_files": [],
}


def project_structure(
    agents=(),
    available=True,
):
    """
    构造被分析项目的自述结构。

    结构与 ArchitectureAnalysisSkill 的真实产出一致。
    """

    declared = bool(agents)

    def dimension(name, items):

        is_declared = bool(items)

        return {
            "declared": is_declared,
            "items": list(items),
            "topics": [],
            "evidence": [],
            "reason": (
                None
                if is_declared
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
            "agents": dimension("agents", agents),
            "workflow": dimension("workflow", ()),
            "skills": dimension("skills", ()),
            "tools": dimension("tools", ()),
            "rag": dimension("rag", ()),
            "memory": dimension("memory", ()),
            "extension": dimension(
                "extension", ()
            ),
        },
    }


def run_memory_payload(
    run_id,
    repository_id,
    repository_name,
    technology_stack,
    evidences=None,
    agents=(),
):
    """构造 RunMemory.load() 的真实返回结构。"""

    research_plan = {
        "tasks": list(EXECUTED_TASKS),
        "plan_version": 1,
        "analysis_type": "github_agent_project",
        "evidence_required": True,
    }

    return {
        "run_id": run_id,
        "status": "COMPLETED",
        "current_node": "end",
        "question": "分析这个项目",
        "repository": {
            "id": repository_id,
            "url": (
                "https://github.com/demo/"
                f"{repository_name}"
            ),
            "owner": "demo",
            "name": repository_name,
            "description": None,
            "language": "Python",
        },
        "research_plan": research_plan,
        "final_report": {
            "report": {
                "path": f"reports/{run_id}.md",
                "format": "markdown",
            },
            "content": "# report",
        },
        "agent_outputs": [],
        "task_results": [],
        "evidences": list(evidences or []),
        "workflow_state": {
            "status": "COMPLETED",
            "current_node": "end",
            "data": {
                "executed_tasks": list(
                    EXECUTED_TASKS
                ),
                "research_plan": research_plan,
                "repository": {
                    "language": "Python",
                    "size": 8586,
                },
                "architecture_analysis_agent": {
                    "files": [],
                    "modules": [],
                },
                "technology_stack": (
                    technology_stack
                ),
                "project_structure": project_structure(
                    agents=agents
                ),
            },
        },
    }


def real_evidence(evidence_id, content):
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


def install_fakes(
    monkeypatch,
    runs,
    memories,
):
    """替换 Service 依赖的 Repository 与 RunMemory。"""

    import app.services.comparison_service as module

    fake_repository = SimpleNamespace(
        get_by_id=AsyncMock(
            side_effect=runs
        )
    )

    fake_memory = SimpleNamespace(
        load=AsyncMock(
            side_effect=memories
        )
    )

    monkeypatch.setattr(
        module,
        "AnalysisRunRepository",
        lambda session: fake_repository,
    )

    monkeypatch.setattr(
        module,
        "RunMemory",
        lambda session: fake_memory,
    )

    return fake_repository, fake_memory


@pytest.mark.asyncio
async def test_create_comparison_with_real_runmemory_schema(
    monkeypatch,
):
    """
    ComparisonService 在真实 RunMemory 结构下
    必须产生真实业务结果。
    """

    session = SimpleNamespace()

    run_a = SimpleNamespace(
        id="run-a",
        repository_id=1,
        status="COMPLETED",
    )

    run_b = SimpleNamespace(
        id="run-b",
        repository_id=2,
        status="COMPLETED",
    )

    install_fakes(
        monkeypatch,
        runs=[run_a, run_b],
        memories=[
            run_memory_payload(
                "run-a",
                1,
                "project-a",
                TECH_WITH_DATABASE,
                evidences=[
                    real_evidence(
                        "evidence-real-1",
                        "Stores data in PostgreSQL.",
                    )
                ],
                agents=["Planner", "Critic"],
            ),
            # B 项目 README 没有声明 Agent
            run_memory_payload(
                "run-b",
                2,
                "project-b",
                TECH_EMPTY,
            ),
        ],
    )

    service = ComparisonService()

    result = await service.create_comparison(
        session,
        ComparisonCreateRequest(
            run_ids=["run-a", "run-b"]
        ),
    )

    assert result.status == "COMPLETED"

    assert len(result.projects) == 2

    assert (
        result.projects[0].repository_name
        == "project-a"
    )

    # Agent 维度来自被分析项目自己的自述结构。
    agent_dimension = result.comparison["agent"]

    # A 声明了 Agent，B 没有 → DIFFERENT
    assert agent_dimension["relation"] == "DIFFERENT"

    assert agent_dimension["project_a"]["value"][
        "items"
    ] == ["Critic", "Planner"]

    assert agent_dimension["project_a"]["value"][
        "declared"
    ] is True

    assert agent_dimension["project_b"]["value"][
        "declared"
    ] is False

    assert (
        agent_dimension["source"]
        == (
            "workflow_state.data."
            "project_structure.dimensions.agents"
        )
    )

    # database 维度来自真实 technology_stack。
    assert (
        result.comparison["database"]["relation"]
        == "DIFFERENT"
    )

    # evidence_based 由真实 Evidence 引用决定。
    assert result.evidence_based is True


@pytest.mark.asyncio
async def test_comparison_without_evidence_is_not_evidence_based(
    monkeypatch,
):
    """两个 Run 都没有 Evidence 时 evidence_based 必须为 False。"""

    session = SimpleNamespace()

    run_a = SimpleNamespace(
        id="run-a",
        repository_id=1,
        status="COMPLETED",
    )

    run_b = SimpleNamespace(
        id="run-b",
        repository_id=2,
        status="COMPLETED",
    )

    install_fakes(
        monkeypatch,
        runs=[run_a, run_b],
        memories=[
            run_memory_payload(
                "run-a",
                1,
                "project-a",
                TECH_EMPTY,
            ),
            run_memory_payload(
                "run-b",
                2,
                "project-b",
                TECH_EMPTY,
            ),
        ],
    )

    service = ComparisonService()

    result = await service.create_comparison(
        session,
        ComparisonCreateRequest(
            run_ids=["run-a", "run-b"]
        ),
    )

    assert result.evidence_based is False


@pytest.mark.asyncio
async def test_comparison_requires_two_runs(monkeypatch):
    """必须提供两个不同的 Run ID。"""

    service = ComparisonService()

    with pytest.raises(
        Exception,
        match="must be different",
    ):
        await service.create_comparison(
            SimpleNamespace(),
            ComparisonCreateRequest(
                run_ids=["run-a", "run-a"]
            ),
        )


@pytest.mark.asyncio
async def test_comparison_requires_completed_runs(
    monkeypatch,
):
    """未完成的 Analysis Run 不能参与比较。"""

    session = SimpleNamespace()

    run = SimpleNamespace(
        id="run-a",
        repository_id=1,
        status="ANALYZING",
    )

    import app.services.comparison_service as module

    fake_repository = SimpleNamespace(
        get_by_id=AsyncMock(
            return_value=run
        )
    )

    monkeypatch.setattr(
        module,
        "AnalysisRunRepository",
        lambda session: fake_repository,
    )

    service = ComparisonService()

    with pytest.raises(
        Exception,
        match="Only completed analysis runs",
    ):
        await service.create_comparison(
            session,
            ComparisonCreateRequest(
                run_ids=["run-a", "run-b"]
            ),
        )


@pytest.mark.asyncio
async def test_comparison_requires_different_repositories(
    monkeypatch,
):
    """两个 Run 必须来自不同仓库。"""

    session = SimpleNamespace()

    run_a = SimpleNamespace(
        id="run-a",
        repository_id=1,
        status="COMPLETED",
    )

    run_b = SimpleNamespace(
        id="run-b",
        repository_id=1,
        status="COMPLETED",
    )

    import app.services.comparison_service as module

    fake_repository = SimpleNamespace(
        get_by_id=AsyncMock(
            side_effect=[run_a, run_b]
        )
    )

    monkeypatch.setattr(
        module,
        "AnalysisRunRepository",
        lambda session: fake_repository,
    )

    service = ComparisonService()

    with pytest.raises(
        Exception,
        match="different repositories",
    ):
        await service.create_comparison(
            session,
            ComparisonCreateRequest(
                run_ids=["run-a", "run-b"]
            ),
        )
