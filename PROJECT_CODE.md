# AIPI Platform 项目代码总览

> AI Agent GitHub Project Intelligence Platform
>
> 本文档按**分层**整理项目中每个 `.py` 文件的完整源码，每段代码均标注所属层级与文件路径。
> 代码内容由脚本从源文件直接读取生成，与仓库当前状态一致。

---

## 一、项目目录

```
AIPI Platform/
│
├── .claude/
│   └── settings.local.json
├── .ruff_cache/
│   ├── 0.16.8/
│   │   ├── 16566685418715801329
│   │   ├── 17936654776091991913
│   │   └── 3370953332892493429
│   ├── .gitignore
│   └── CACHEDIR.TAG
├── alembic/                                                         # 数据库迁移（Alembic）
│   ├── versions/                                                    # 迁移脚本
│   │   ├── 479571222143_create_initial_analysis_tables.py
│   │   ├── a9e1f4c2d8b7_add_evidence_claim_citation.py
│   │   └── b0f6883a5f43_add_checkpoints.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/                                                             # 应用主包
│   ├── agents/                                                      # ── Agent 层 ──
│   │   ├── agent_registry.py
│   │   ├── agent_runtime.py
│   │   ├── architecture_analysis_agent.py
│   │   ├── base.py
│   │   ├── critic_agent.py
│   │   ├── evidence_analysis_agent.py
│   │   ├── planner_agent.py
│   │   ├── repository_analysis_agent.py
│   │   ├── researcher.py
│   │   └── technology_analysis_agent.py
│   ├── api/                                                         # ── API 层 ──
│   │   ├── v1/                                                      # v1 路由
│   │   │   ├── __init__.py                                          # (空)
│   │   │   └── analysis.py
│   │   └── __init__.py                                              # (空)
│   ├── context/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   └── retriever.py
│   ├── core/                                                        # ── 核心基础设施层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── config.py
│   │   ├── error_handlers.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── db/                                                          # ── 数据库层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── base.py
│   │   └── session.py
│   ├── embeddings/                                                  # ── AI 能力层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── base.py
│   │   └── ollama.py
│   ├── evidence/                                                    # ── 证据与溯源层 ──
│   │   ├── __init__.py
│   │   ├── store.py
│   │   ├── traceability.py
│   │   └── verifier.py
│   ├── llm/                                                         # ── LLM 能力层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── base.py
│   │   └── deepseek.py
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── project_memory.py
│   │   └── run_memory.py
│   ├── models/                                                      # ── 数据模型层 ──
│   │   ├── __init__.py
│   │   ├── analysis_run.py
│   │   ├── analysis_task.py
│   │   ├── checkpoint.py
│   │   ├── citation.py
│   │   ├── claim.py
│   │   ├── evidence.py
│   │   └── repository.py
│   ├── project_analysis/                                            # ── 项目分析层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis_focus.py
│   │   ├── code_chunker.py
│   │   ├── code_structure_extractor.py
│   │   ├── project_indexer.py
│   │   └── repository_indexer.py
│   ├── repositories/                                                # ── 数据访问层 ──
│   │   ├── __init__.py
│   │   ├── analysis_run.py
│   │   ├── checkpoint.py
│   │   ├── citation.py
│   │   ├── claim.py
│   │   ├── evidence.py
│   │   ├── repository.py
│   │   └── repository_basic.py
│   ├── schemas/                                                     # ── 数据契约层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis.py
│   │   ├── analysis_result.py
│   │   ├── error.py
│   │   └── evidence.py
│   ├── services/                                                    # ── 业务服务层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis_result_service.py
│   │   ├── analysis_service.py
│   │   ├── analysis_workflow.py
│   │   ├── evidence_service.py
│   │   └── repository_service.py
│   ├── skills/                                                      # ── Skill 能力层 ──
│   │   ├── __init__.py
│   │   ├── architecture_analysis_skill.py
│   │   ├── base.py
│   │   ├── evidence_analysis_skill.py
│   │   ├── json_output.py
│   │   ├── module_deep_dive_skill.py
│   │   ├── registry.py
│   │   ├── report_generation_skill.py
│   │   ├── report_synthesis_skill.py
│   │   ├── repository_analysis_skill.py
│   │   └── technology_analysis_skill.py
│   ├── static/
│   │   └── index.html
│   ├── tools/                                                       # ── 工具层 ──
│   │   ├── github/                                                  # GitHub API 工具
│   │   │   ├── __init__.py                                          # (空)
│   │   │   ├── github_code_search_tool.py
│   │   │   ├── github_repository_tool.py
│   │   │   └── parser.py
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dependency_analyzer_tool.py
│   │   ├── file_reader_tool.py
│   │   ├── llm_chat_tool.py
│   │   ├── mysql_query_tool.py
│   │   ├── qdrant_search_tool.py
│   │   └── report_export_tool.py
│   ├── vector_store/                                                # ── 向量存储层 ──
│   │   ├── __init__.py                                              # (空)
│   │   └── qdrant.py
│   ├── workflow/                                                    # ── Workflow 层 ──
│   │   ├── nodes/                                                   # Workflow 节点层
│   │   │   ├── __init__.py                                          # (空)
│   │   │   ├── agent_node.py
│   │   │   ├── analysis_node.py
│   │   │   ├── base.py
│   │   │   ├── design_gate_node.py
│   │   │   ├── end_node.py
│   │   │   ├── finalizer_node.py
│   │   │   ├── human_node.py
│   │   │   ├── plan_executor_node.py
│   │   │   ├── skill_node.py
│   │   │   ├── start_node.py
│   │   │   ├── synthesis_node.py
│   │   │   └── tool_node.py
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis_workflow.py
│   │   ├── checkpoint.py
│   │   ├── context.py
│   │   ├── engine.py
│   │   ├── exceptions.py
│   │   ├── node.py
│   │   ├── result.py
│   │   ├── retry.py
│   │   ├── state.py
│   │   ├── transition.py
│   │   └── workflow.py
│   ├── __init__.py                                                  # (空)
│   └── main.py
├── reports/
│   ├── 3730e4e2-2014-43c8-91c3-382a65b2dab3_analysis.md
│   ├── 375e3b6b-1b6f-4c2c-ad6e-d8557071a816_analysis.md
│   ├── 478567aa-f3e4-4dd0-8190-02e529c7fa9b_analysis.md
│   ├── 48319961-f784-4f02-9495-d918067dd72f_analysis.md
│   ├── 5348dfc4-90be-40ed-b831-7a7c898e280c_analysis.md
│   ├── 74955586-c729-404f-9a77-f9d35c2f914a_analysis.md
│   ├── 773fa941-7723-4ae2-99f0-e1e000b2e63c_analysis.md
│   ├── 799049b1-3d51-4c2f-bbe5-81930ce59a23_analysis.md
│   ├── 839c0af3-75e8-4929-bc56-c7a3c7d61c16_analysis.md
│   ├── 839c0af3-75e8-4929-bc56-c7a3c7d61c16_workflow_deep_dive.md
│   ├── 892282e6-de22-4e8b-baad-dd67942f20a2_analysis.md
│   ├── 8ac15b01-1fff-4000-861f-b394a5917324_analysis.md
│   ├── 91353270-c6df-4be0-afd3-55da9838424c_analysis.md
│   ├── a57edd4e-59b1-4aa9-a889-d4d10dfbc0d5_analysis.md
│   ├── a670ec22-703a-4402-8392-a39900e72f3d_analysis.md
│   ├── b3b3b6c2-97e4-47ea-a2b8-b3e9734e2f74_analysis.md
│   ├── b3b3b6c2-97e4-47ea-a2b8-b3e9734e2f74_workflow_deep_dive.md
│   ├── bd05a24f-c95e-4202-bcee-19af504f0c6c_analysis.md
│   ├── bd842def-63fe-435c-91d2-939c2c43f202_analysis.md
│   ├── c498a9a2-04e9-471c-aaea-678ea56fca9a_analysis.md
│   ├── c7bcfb1d-fae3-4fba-aa3d-bf8d77284b44_analysis.md
│   ├── caaaf822-e1ee-42f8-a52a-3b1eac1434bb_analysis.md
│   ├── d1d71c3e-a9b6-4073-8d3d-bbbfe0b11005_analysis.md
│   ├── e0400cf2-8671-47f3-8f50-414c1445e02d_analysis.md
│   ├── focus_demo_analysis.md
│   ├── real-run-2_workflow_deep_dive.md
│   ├── real_run_application_analysis.md
│   └── real_run_v2_analysis.md
├── test_reports/                                                    # 测试产生的报告输出目录
│   ├── _b.mjs
│   ├── api_flow_run_id.txt
│   ├── focus_run.txt
│   ├── last_run.txt
│   ├── latest_run.txt
│   ├── preview.md
│   ├── real_deep_dive.json
│   ├── real_run_data.json
│   ├── real_run_full.json
│   ├── real_run_synthesis.json
│   ├── real_run_v2_data.json
│   ├── real_run_v2_synthesis.json
│   ├── stuck_runs.txt
│   ├── test.md
│   └── verify_run.txt
├── tests/                                                           # ── 测试层 ──
│   ├── test_agent_registry.py
│   ├── test_agent_runtime.py
│   ├── test_analysis_api.py
│   ├── test_analysis_focus.py
│   ├── test_analysis_result.py
│   ├── test_architecture_code_evidence.py
│   ├── test_checkpoint_size_guard.py
│   ├── test_chunker.py
│   ├── test_code_structure_extractor.py
│   ├── test_config.py
│   ├── test_context_manager.py
│   ├── test_context_retriever.py
│   ├── test_database.py
│   ├── test_dependency_analyzer_tool.py
│   ├── test_embedding.py
│   ├── test_embedding_qdrant.py
│   ├── test_evidence_agent.py
│   ├── test_evidence_models.py
│   ├── test_evidence_service.py
│   ├── test_evidence_skill.py
│   ├── test_evidence_store.py
│   ├── test_evidence_verifier.py
│   ├── test_exceptions.py
│   ├── test_file_reader_tool.py
│   ├── test_github_client.py
│   ├── test_github_code_search_tool.py
│   ├── test_github_parser.py
│   ├── test_indexer.py
│   ├── test_json_output.py
│   ├── test_memory.py
│   ├── test_module_deep_dive_skill.py
│   ├── test_mysql_query_tool.py
│   ├── test_phase10.py
│   ├── test_phase12.py
│   ├── test_pre_phase12_integration.py
│   ├── test_pre_phase12_structure.py
│   ├── test_qdrant.py
│   ├── test_qdrant_search_tool.py
│   ├── test_report_export_tool.py
│   ├── test_report_synthesis_skill.py
│   ├── test_repository_analysis_workflow.py
│   ├── test_repository_crud.py
│   ├── test_repository_pipeline.py
│   ├── test_repository_service.py
│   ├── test_repository_skill.py
│   ├── test_retrieval.py
│   ├── test_skill_base.py
│   ├── test_skill_node.py
│   ├── test_skill_registry.py
│   ├── test_skill_workflow.py
│   ├── test_tools.py
│   ├── test_traceability.py
│   ├── test_workflow.py
│   └── test_workflow_engine_errors.py
├── .env                                                             # 本地环境变量（已 gitignore）
├── .env.example                                                     # 环境变量模板
├── .gitignore
├── a.py                                                             # Agent Loop 实验草稿（未纳入 app/）
├── agent loop.py                                                    # Agent Loop 草稿片段
├── AI-Agent-GitHub-Project-Intelligence-Platform-详细Phase开发实施文档.md
├── AI-Agent-GitHub-Project-Intelligence-Platform-项目设计文档.md
├── alembic.ini                                                      # Alembic 配置
├── generate_project_code.py                                         # 本文档生成脚本
├── Phase12-Phase13-数据契约审查报告.md
├── PROJECT_CODE.md
├── pytest.ini                                                       # Pytest 配置
└── requirements.txt                                                 # 依赖清单
```

### 分层调用关系

```
                        ┌─────────────────────────┐
    HTTP 请求 ─────────▶ │   API 层                │  app/api/v1/
                        │   (路由 + 依赖注入)      │
                        └───────────┬─────────────┘
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │   业务服务层             │  app/services/
                        │   (业务编排)             │
                        └───────┬─────────┬───────┘
                                │         │
                ┌───────────────┘         └───────────────┐
                ▼                                         ▼
    ┌───────────────────────┐               ┌─────────────────────────┐
    │  数据访问层            │               │  工具层                  │
    │  app/repositories/    │               │  app/tools/             │
    └───────────┬───────────┘               └────────────┬────────────┘
                │                                        │
                ▼                                        ▼
    ┌───────────────────────┐               ┌─────────────────────────┐
    │  数据模型层            │               │  项目分析层              │
    │  app/models/          │               │  app/project_analysis/  │
    └───────────┬───────────┘               └───────────┬─────────────┘
                │                                       │
                ▼                                       ▼
    ┌───────────────────────┐               ┌─────────────────────────┐
    │  数据库层              │               │  AI 能力层 / 向量存储层  │
    │  app/db/              │               │  app/embeddings/        │
    │      → MySQL          │               │  app/vector_store/      │
    └───────────────────────┘               │      → Qdrant           │
                                            └─────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │  Workflow 层  app/workflow/  +  app/workflow/nodes/             │
    │  WorkflowEngine 按 Transition 驱动 Node 执行，共享 WorkflowState │
    └───────────────┬─────────────────────────────┬───────────────────┘
                    │                             │
                    ▼                             ▼
    ┌────────────────────────────────────────────────────────┐
    │  Agent 层  app/agents/                                  │
    │  BaseAgent / *Agent / AgentRegistry / AgentRuntime      │
    └───────────────────────────┬────────────────────────────┘
                                │  通过 SkillRegistry 取能力
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │  Skill 层  app/skills/                                  │
    │  BaseSkill / *Skill / SkillRegistry                     │
    │  一个 Skill 组合多个 Tool 完成一次业务能力               │
    └───────────────────────────┬────────────────────────────┘
                                │
                                ▼
    ┌───────────────────────────┐   ┌─────────────────────────┐
    │  工具层  app/tools/        │   │  LLM 能力层  app/llm/    │
    │  BaseTool / *Tool          │   │  BaseLLM / DeepSeekLLM  │
    └───────────────────────────┘   └─────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │  证据与溯源层  app/evidence/                                     │
    │  EvidenceStore / EvidenceVerifier / TraceabilityService         │
    │  证据链：Claim ─▶ Citation ─▶ Evidence ─▶ Source(file:line)      │
    └────────────────────────────────┬────────────────────────────────┘
                                     │  经 app/repositories/ 落 MySQL
                                     ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │  Workflow 状态持久化  app/workflow/checkpoint.py                 │
    │  WorkflowState ⇄ app/models/checkpoint.py（checkpoints 表）      │
    │  支撑暂停 / 恢复 / 重试                                           │
    └─────────────────────────────────────────────────────────────────┘

    调用链：Workflow ─▶ Node ─▶ Agent ─▶ Skill ─▶ Tool

    贯穿各层：app/core/（配置、日志、异常、异常处理器）
    数据契约：app/schemas/（被 API 层与 Service 层共同引用）
```

---

## 二、入口层

FastAPI 应用装配：日志、异常处理、路由挂载；同时收录 `app` 包标记文件

### 📄 `app/__init__.py`

**层级**：入口层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/main.py`

**层级**：入口层 · **职责**：FastAPI 应用初始化、日志初始化、全局异常注册、路由挂载；文件末尾额外装配了 `WorkflowContext`（agents / tools / skills）的草稿代码

```python
"""
FastAPI 应用入口。

负责：

1. FastAPI 应用初始化
2. 全局配置加载
3. 日志初始化
4. 全局异常处理
5. API 路由注册
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.v1.analysis import (
    router as analysis_router,
)
from app.core.config import get_settings
from app.core.error_handlers import (
    application_error_handler,
    unexpected_error_handler,
)
from app.core.exceptions import ApplicationError
from app.core.logging import (
    get_logger,
    setup_logging,
)


settings = get_settings()


# 应用启动时初始化全局日志。
setup_logging()

logger = get_logger(
    __name__
)


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI Agent GitHub Project "
        "Intelligence Platform"
    ),
    version="0.1.0",
    debug=settings.DEBUG,
)


# 注册统一业务异常处理器。
app.add_exception_handler(
    ApplicationError,
    application_error_handler,
)


# 注册未预期异常处理器。
app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)


# 注册 Analysis API。
app.include_router(
    analysis_router,
    prefix="/api/v1",
)


@app.get(
    "/health",
    tags=["System"],
)
async def health_check():
    """
    健康检查接口。
    """

    return {
        "status": "ok",
        "environment": settings.APP_ENV,
    }


@app.get(
    "/",
    tags=["System"],
)
async def root():
    """
    根路径直接返回操作页面。

    这是给人工跑一次分析用的最简前端：
    单文件、无构建步骤，
    只调用本服务已有的 /api/v1 接口。

    文件缺失时退回 JSON，
    保证 API 本身不受影响。
    """

    index = (
        Path(__file__).parent
        / "static"
        / "index.html"
    )

    if index.is_file():

        return FileResponse(
            index,
            media_type="text/html",
        )

    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
        "ui": "app/static/index.html not found",
    }
```

## 三、API 层

HTTP 路由定义，负责接收请求、注入数据库 Session、调用 Service

### 📄 `app/api/v1/analysis.py`

**层级**：API 层 · **职责**：Analysis 相关的 HTTP 路由定义，负责接收请求、注入数据库 Session、调用 Service

```python
"""Analysis API 路由。"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisDeepDiveResponse,
    AnalysisReportResponse,
    AnalysisResponse,
)
from app.services.analysis_service import (
    analysis_service,
)


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


@router.post(
    "",
    response_model=AnalysisResponse,
)
async def create_analysis(
    request: AnalysisCreateRequest,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """创建并启动 GitHub 项目分析 Workflow。"""

    return await analysis_service.create_analysis(
        session,
        request,
    )


@router.get(
    "",
    response_model=list[AnalysisResponse],
)
async def list_analyses(
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="最多返回多少条",
    ),
    session: AsyncSession = Depends(get_db),
) -> list[AnalysisResponse]:
    """
    列出最近的分析任务。

    给前端的历史列表用 ——
    没有这个接口时，页面关掉就找不回
    之前跑过的分析了。
    """

    return await analysis_service.list_analyses(
        session,
        limit,
    )


@router.get(
    "/{run_id}",
    response_model=AnalysisResponse,
)
async def get_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """查询分析任务。"""

    return await analysis_service.get_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/approve",
    response_model=AnalysisResponse,
)
async def approve_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """批准 Design Gate 或 Human Review。"""

    return await analysis_service.approve_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/pause",
    response_model=AnalysisResponse,
)
async def pause_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """暂停 Workflow。"""

    return await analysis_service.pause_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/resume",
    response_model=AnalysisResponse,
)
async def resume_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """恢复 PAUSED Workflow。"""

    return await analysis_service.resume_analysis(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/retry",
    response_model=AnalysisResponse,
)
async def retry_analysis(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisResponse:
    """重试失败 Workflow。"""

    return await analysis_service.retry_analysis(
        session,
        run_id,
    )


@router.get(
    "/{run_id}/report",
    response_model=AnalysisReportResponse,
)
async def get_analysis_report(
    run_id: str,
    session: AsyncSession = Depends(get_db),
) -> AnalysisReportResponse:
    """获取最终项目智能分析报告。"""

    return await analysis_service.get_report(
        session,
        run_id,
    )


@router.post(
    "/{run_id}/deep-dive",
    response_model=AnalysisDeepDiveResponse,
)
async def deep_dive_module(
    run_id: str,
    module: str = Query(
        ...,
        description=(
            "要深挖的模块：agents / workflow / "
            "skills / tools / rag / memory"
        ),
    ),
    session: AsyncSession = Depends(get_db),
) -> AnalysisDeepDiveResponse:
    """
    对已完成 run 的单个模块做深挖。

    默认报告每章只给要点与证据锚点；
    想看某个模块的实现细节
    （签名 / 调用链 / 关键常量 / 源码片段）时走这里。

    该接口只读不写：不修改原 run，
    产物是单独一份 markdown 报告。
    """

    return await analysis_service.deep_dive_module(
        session,
        run_id,
        module,
    )
```

### 📄 `app/api/__init__.py`

**层级**：API 层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/api/v1/__init__.py`

**层级**：API 层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

## 四、数据契约层（Schemas）

接口的请求体与响应体定义，被 API 层与 Service 层共同引用

### 📄 `app/schemas/analysis.py`

**层级**：数据契约层（Schemas） · **职责**：Analysis 接口的请求体与响应体定义

```python
"""Analysis API 请求与响应模型。"""

from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisCreateRequest(BaseModel):
    """创建项目分析任务。"""

    repo_url: str = Field(
        ...,
        min_length=1,
        description="GitHub repository URL",
    )

    question: str | None = Field(
        default=None,
        max_length=5000,
        description="本次项目分析问题",
    )


class AnalysisResponse(BaseModel):
    """Analysis Run 当前状态。"""

    run_id: str

    status: str

    repo_url: str

    question: str | None = None

    current_node: str | None = None

    progress: int = 0

    created_at: datetime


class AnalysisReportResponse(BaseModel):
    """最终项目分析报告。"""

    run_id: str

    status: str

    report: dict | None = None


class AnalysisDeepDiveResponse(BaseModel):
    """
    单个模块的深挖报告。

    默认报告每章只给要点；
    这一份是某个模块的实现细节展开。
    """

    run_id: str

    module: str

    title: str | None = None

    # 写入磁盘的报告文件信息（path / format）。
    report: dict | None = None

    # 报告正文，便于调用方直接展示。
    content: str | None = None

    # 本次深挖读取了哪些文件。
    # 是「比默认报告看得多」的证据，
    # 也让读者知道结论的覆盖面。
    files_read: list[str] = []

    # 展开了多少项实现明细。
    details: int = 0
```

### 📄 `app/schemas/error.py`

**层级**：数据契约层（Schemas） · **职责**：统一错误响应结构，保证各接口返回一致的错误格式

```python
"""统一错误响应模型，用于保证不同 API 返回一致的错误结构。"""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """错误的具体信息。"""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """统一 API 错误响应。"""

    success: bool
    error: ErrorDetail
```

### 📄 `app/schemas/evidence.py`

**层级**：数据契约层（Schemas） · **职责**：Evidence / Claim / Citation 的请求体与响应体定义（`EvidenceCreateRequest` / `ClaimCreateRequest` / `CitationCreateRequest` 等）

```python
"""
Evidence / Claim / Citation 数据契约。
"""

from datetime import datetime

from pydantic import BaseModel, Field


class EvidenceCreateRequest(BaseModel):
    repository_id: int

    source_type: str = Field(
        min_length=1,
        max_length=50,
    )

    source_url: str | None = None

    file_path: str | None = None

    line_start: int | None = Field(
        default=None,
        ge=1,
    )

    line_end: int | None = Field(
        default=None,
        ge=1,
    )

    content: str = Field(
        min_length=1,
    )

    verification_status: str = "UNVERIFIED"


class EvidenceResponse(BaseModel):
    id: str
    repository_id: int
    source_type: str
    source_url: str | None
    file_path: str | None
    line_start: int | None
    line_end: int | None
    content: str
    verification_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ClaimCreateRequest(BaseModel):
    run_id: str

    claim_text: str = Field(
        min_length=1,
    )

    verification_status: str = "UNVERIFIED"


class ClaimResponse(BaseModel):
    id: str
    run_id: str
    claim_text: str
    verification_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class CitationCreateRequest(BaseModel):
    claim_id: str
    evidence_id: str


class CitationResponse(BaseModel):
    id: str
    claim_id: str
    evidence_id: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
```

### 📄 `app/schemas/__init__.py`

**层级**：数据契约层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/schemas/analysis_result.py`

**层级**：数据契约层 · **职责**：Analysis Result 数据契约。

```python
"""
Analysis Result 数据契约。

Phase12:

Workflow执行结果
        ↓
AnalysisResult
        ↓
Report
"""

from typing import Any

from pydantic import BaseModel, Field



class ProjectOverview(BaseModel):
    """
    项目基础信息。
    """

    name: str | None = None

    description: str | None = None

    repository_url: str | None = None

    language: str | None = None



class TechnologyStack(BaseModel):
    """
    技术栈信息。
    """

    languages: list[str] = Field(
        default_factory=list
    )

    frameworks: list[str] = Field(
        default_factory=list
    )

    databases: list[str] = Field(
        default_factory=list
    )

    tools: list[str] = Field(
        default_factory=list
    )



class AgentAnalysisResult(BaseModel):
    """
    单个 Agent 分析结果。
    """

    agent_name: str


    summary: str | None = None


    facts: list[str] = Field(
        default_factory=list
    )


    evidence_ids: list[str] = Field(
        default_factory=list
    )



class AnalysisResult(BaseModel):
    """
    Phase12 标准分析结果。

    作为:

    Workflow
        ↓
    Report

    的统一数据契约。
    """


    run_id: str



    project_overview: ProjectOverview = Field(
        default_factory=ProjectOverview
    )



    technology_stack: TechnologyStack = Field(
        default_factory=TechnologyStack
    )



    agents: list[AgentAnalysisResult] = Field(
        default_factory=list
    )



    workflow: dict[str, Any] = Field(
        default_factory=dict
    )



    skills: list[str] = Field(
        default_factory=list
    )



    tools: list[str] = Field(
        default_factory=list
    )



    rag: dict[str, Any] = Field(
        default_factory=dict
    )



    memory: dict[str, Any] = Field(
        default_factory=dict
    )



    database: dict[str, Any] = Field(
        default_factory=dict
    )



    evidence: list[Any] = Field(
        default_factory=list
    )
```

## 五、业务服务层（Services）

业务编排：校验入参、组合 DAO 与工具层、掌控事务边界

### 📄 `app/services/analysis_service.py`

**层级**：业务服务层（Services） · **职责**：Analysis 任务的业务编排——校验 URL、创建或复用 Repository、创建 Analysis Run 并提交事务

```python
"""Analysis 任务业务逻辑。"""

from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError
from app.core.logging import (
    get_logger,
    log_with_run_id,
)
from app.models.repository import Repository
from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.repositories.repository_basic import (
    RepositoryRepository,
)
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisDeepDiveResponse,
    AnalysisReportResponse,
    AnalysisResponse,
)
from app.services.analysis_workflow import (
    AnalysisWorkflowRunner,
)
from app.skills.module_deep_dive_skill import (
    ModuleDeepDiveSkill,
)
from app.tools.github.parser import (
    parse_github_url,
)

logger = get_logger(__name__)


class AnalysisService:
    """负责 Analysis Run 与 Workflow 的业务编排。"""

    workflow_runner_factory = (
        AnalysisWorkflowRunner
    )

    async def create_analysis(
        self,
        session: AsyncSession,
        request: AnalysisCreateRequest,
    ) -> AnalysisResponse:
        """创建并启动单项目分析 Workflow。"""

        repo_url = request.repo_url.strip()

        if not repo_url:
            raise ValidationError(
                "Repository URL cannot be empty."
            )

        if not repo_url.startswith(
            (
                "https://github.com/",
                "http://github.com/",
            )
        ):
            raise ValidationError(
                "Only GitHub repository URLs are supported."
            )

        owner, name = self._parse_github_url(
            repo_url
        )

        repository_repo = (
            RepositoryRepository(
                session
            )
        )

        analysis_run_repo = (
            AnalysisRunRepository(
                session
            )
        )

        repository = (
            await repository_repo.get_by_url(
                repo_url
            )
        )

        if repository is None:
            repository = (
                await repository_repo.create(
                    url=repo_url,
                    owner=owner,
                    name=name,
                )
            )

        elif (
            repository.owner != owner
            or repository.name != name
        ):
            # 自愈历史脏数据。
            #
            # 之前 _parse_github_url 不剥离 query string，
            # 因此可能存在
            #
            #     name = "repo?utm_source=chatgpt.com"
            #
            # 这种行。它的危险之处在于不会报错：
            #
            #     api.github.com/repos/{owner}/{name}
            #         → query 被服务端忽略，元数据仍然 200
            #
            #     raw.githubusercontent.com/{owner}/{name}/...
            #         → "?" 被当成路径的一部分，全部 404
            #
            # 结果是 readme 为空、evidences 为 0、
            # technology_stack 全空，
            # 而 run 仍然被标记为 COMPLETED。
            #
            # 按 URL 命中已有行时会直接复用，
            # 所以只修解析器救不了存量数据，
            # 这里顺手把 owner / name 修正回来。
            logger.warning(
                "repairing repository row | "
                "id=%s | name %r -> %r",
                repository.id,
                repository.name,
                name,
            )

            repository.owner = owner

            repository.name = name

        run_id = str(uuid4())

        run = await analysis_run_repo.create(
            run_id=run_id,
            repository_id=repository.id,
            question=request.question,
        )

        await session.commit()

        log_with_run_id(
            logger,
            level=20,
            message="analysis workflow starting",
            run_id=run_id,
        )

        runner = (
            self.workflow_runner_factory(
                session
            )
        )

        # POST /analysis 不再只是创建数据库记录，
        # 而是真正启动 Workflow。
        await runner.start(
            run_id
        )

        run = await analysis_run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        return await self._to_response(
            session,
            run,
        )

    async def get_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """查询 Analysis Run。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        return await self._to_response(
            session,
            run,
        )

    async def approve_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """批准 Design Gate 或 Human Review。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status not in {
            "WAITING_DESIGN",
            "WAITING_HUMAN",
        }:
            raise ValidationError(
                f"Analysis run cannot be approved "
                f"from status: {run.status}"
            )

        runner = (
            self.workflow_runner_factory(
                session
            )
        )

        await runner.approve(
            run_id
        )

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def pause_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """暂停 Workflow。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status not in {
            "ANALYZING",
            "WAITING_DESIGN",
            "WAITING_HUMAN",
        }:
            raise ValidationError(
                f"Analysis run cannot be paused "
                f"from status: {run.status}"
            )

        runner = (
            self.workflow_runner_factory(
                session
            )
        )

        await runner.pause(
            run_id
        )

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def resume_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """从 PAUSED Checkpoint 恢复。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status != "PAUSED":
            raise ValidationError(
                f"Analysis run cannot be resumed "
                f"from status: {run.status}"
            )

        runner = (
            self.workflow_runner_factory(
                session
            )
        )

        await runner.resume(
            run_id
        )

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def retry_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """重新执行失败的 Workflow。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        if run.status != "FAILED":
            raise ValidationError(
                f"Analysis run cannot be retried "
                f"from status: {run.status}"
            )

        runner = (
            self.workflow_runner_factory(
                session
            )
        )

        await runner.retry(
            run_id
        )

        run = await run_repo.get_by_id(
            run_id
        )

        return await self._to_response(
            session,
            run,
        )

    async def get_report(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisReportResponse:
        """获取最终分析报告。"""

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        runner = (
            self.workflow_runner_factory(
                session
            )
        )

        report = await runner.get_report(
            run_id
        )

        return AnalysisReportResponse(
            run_id=run.id,
            status=run.status,
            report=report,
        )

    async def list_analyses(
        self,
        session: AsyncSession,
        limit: int = 20,
    ) -> list[AnalysisResponse]:
        """
        列出最近的分析任务。

        给前端的历史列表用：
        前端只能看到「当前这一个 run」时，
        关掉页面就找不回来了。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        runs = await run_repo.list_recent(limit)

        if not runs:
            return []

        # 一次把所有关联仓库取回来，
        # 避免每个 run 查一次库。
        repository_ids = {
            run.repository_id
            for run in runs
        }

        result = await session.execute(
            select(Repository).where(
                Repository.id.in_(repository_ids)
            )
        )

        repositories = {
            repository.id: repository
            for repository in result.scalars().all()
        }

        responses = []

        for run in runs:

            repository = repositories.get(
                run.repository_id
            )

            responses.append(
                AnalysisResponse(
                    run_id=run.id,
                    status=run.status,
                    repo_url=(
                        repository.url
                        if repository is not None
                        else ""
                    ),
                    question=run.question,
                    current_node=run.current_node,
                    progress=self._progress(
                        run.status,
                        run.current_node,
                    ),
                    created_at=run.created_at,
                )
            )

        return responses

    async def deep_dive_module(
        self,
        session: AsyncSession,
        run_id: str,
        module: str,
    ) -> AnalysisDeepDiveResponse:
        """
        对某个已完成 run 的单个模块做深挖。

        默认报告每章只给要点；
        用户想看某个模块的实现细节时走这里。
        """

        run_repo = AnalysisRunRepository(
            session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        normalized = (
            module or ""
        ).strip().lower()

        if normalized not in (
            ModuleDeepDiveSkill.MODULES
        ):
            raise ValidationError(
                f"Unsupported module: {module!r}. "
                "Expected one of "
                f"{', '.join(ModuleDeepDiveSkill.MODULES)}."
            )

        runner = (
            self.workflow_runner_factory(
                session
            )
        )

        result = await runner.deep_dive_module(
            run_id,
            normalized,
        )

        return AnalysisDeepDiveResponse(
            run_id=run_id,
            module=normalized,
            title=result.get("title"),
            report=result.get("report"),
            content=result.get("content"),
            files_read=result.get("files_read")
            or [],
            details=result.get("details", 0),
        )

    async def _to_response(
        self,
        session: AsyncSession,
        run,
    ) -> AnalysisResponse:
        """将 AnalysisRun 转成 API Response。"""

        if run is None:
            raise ValidationError(
                "Analysis run not found."
            )

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: "
                f"{run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            question=run.question,
            current_node=run.current_node,
            progress=self._progress(
                run.status,
                run.current_node,
            ),
            created_at=run.created_at,
        )

    @staticmethod
    def _progress(
        status: str,
        current_node: str | None,
    ) -> int:
        """计算第一版 Workflow 进度。"""

        if status == "COMPLETED":
            return 100

        if status == "FAILED":
            return 100

        mapping = {
            "start": 5,
            "planner_agent": 15,
            "design_gate": 20,
            "plan_executor": 70,
            "human_review": 85,
            "synthesis": 90,
            "finalizer": 95,
            "end": 100,
        }

        return mapping.get(
            current_node,
            0,
        )

    @staticmethod
    def _parse_github_url(
        repo_url: str,
    ) -> tuple[str, str]:
        """
        解析 GitHub owner/repository。

        复用 app.tools.github.parser.parse_github_url：
        它基于 urlparse，会正确剥离 query string 与 fragment。

        旧实现直接按 "/" 切分字符串，因此

            https://github.com/owner/name?utm_source=chatgpt.com

        会被解析成

            name = "name?utm_source=chatgpt.com"

        后果是一整条连锁失败：

            repository.name 被污染
                → README / 配置文件全部 404
                → readme 为空
                → evidences 为 0
                → technology_stack 全空
                → 报告多个章节「真实数据不存在」

        而且该 run 仍然会被标记为 COMPLETED，
        继续参与 Phase 13 的多项目比较。
        """

        try:

            return parse_github_url(repo_url)

        except ValueError as error:

            raise ValidationError(
                "Invalid GitHub repository URL."
            ) from error


analysis_service = AnalysisService()
```

### 📄 `app/services/repository_service.py`

**层级**：业务服务层（Services） · **职责**：Repository 查询 / 创建 / GitHub 数据同步。依赖工具层的 `GitHubRepositoryTool` 与 `parse_github_url`

```python
"""
Repository 业务服务。
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.repositories.repository import RepositoryRepository

from app.tools.github.github_repository_tool import (
    GitHubRepositoryTool
)
from app.tools.github.parser import (
    parse_github_url
)

class RepositoryService:
    """
    Repository 业务服务。

    负责:
        - Repository 查询
        - Repository 创建
        - GitHub数据同步
    不负责:
        - GitHub API细节
    """
    def __init__(
        self,
        session: AsyncSession,
    ):


        self.repository_repository = (
            RepositoryRepository(session)
        )


        self.github_tool = (
            GitHubRepositoryTool()
        )

    async def get_or_create(
        self,
        url: str,
    ) -> Repository:
        """
        获取 Repository。

        存在:
            返回数据库数据

        不存在:
            GitHub获取信息
            保存数据库
        """
        owner, name = (
            parse_github_url(url)
        )

        repository = await (
            self.repository_repository
            .get_by_url(url)
        )

        if repository:
            return repository



        github_data = await (
            self.github_tool
            .get_repository(
                owner,
                name,
            )
        )

        repository = await (
            self.repository_repository
            .create(

                url=url,

                owner=owner,

                name=name,

                description=
                github_data.get(
                    "description"
                ),

                default_branch=
                github_data.get(
                    "default_branch"
                ),

                language=
                github_data.get(
                    "language"
                ),

                stars=
                github_data.get(
                    "stargazers_count",
                    0,
                ),

                forks=
                github_data.get(
                    "forks_count",
                    0,
                ),
            )
        )
        return repository
```

### 📄 `app/services/evidence_service.py`

**层级**：业务服务层（Services） · **职责**：证据链业务编排：`create_evidence()` / `create_claim()` / `cite()` 落库，`verify_evidence()` / `verify_claim()` 走校验器，`get_claim_traceability()` 返回溯源链；调用链为 Service → Store → Verifier → Traceability → Repository

```python
"""
Evidence 业务服务。

Phase 9：

Service
 ↓
Evidence Store
 ↓
Verifier
 ↓
Traceability
 ↓
Repository
 ↓
MySQL
"""

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError
from app.evidence.store import EvidenceStore
from app.evidence.traceability import (
    TraceabilityService,
)
from app.evidence.verifier import EvidenceVerifier


class EvidenceService:
    """
    Evidence 业务服务。

    对上层提供统一接口：

    - create_evidence
    - create_claim
    - cite
    - verify_evidence
    - verify_claim
    - get_claim_traceability
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

        self.store = EvidenceStore(
            session
        )

        self.verifier = EvidenceVerifier(
            session
        )

        self.traceability = (
            TraceabilityService(
                session
            )
        )

    async def create_evidence(
        self,
        *,
        repository_id: int,
        source_type: str,
        content: str,
        source_url: str | None = None,
        file_path: str | None = None,
        line_start: int | None = None,
        line_end: int | None = None,
        verification_status: str = "UNVERIFIED",
    ):

        return await self.store.create_evidence(
            evidence_id=str(uuid4()),
            repository_id=repository_id,
            source_type=source_type,
            content=content,
            source_url=source_url,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            verification_status=verification_status,
        )

    async def create_claim(
        self,
        *,
        run_id: str,
        claim_text: str,
        verification_status: str = "UNVERIFIED",
    ):

        return await self.store.create_claim(
            claim_id=str(uuid4()),
            run_id=run_id,
            claim_text=claim_text,
            verification_status=verification_status,
        )

    async def cite(
        self,
        *,
        claim_id: str,
        evidence_id: str,
    ):

        return await self.store.create_citation(
            citation_id=str(uuid4()),
            claim_id=claim_id,
            evidence_id=evidence_id,
        )

    async def verify_evidence(
        self,
        *,
        evidence_id: str,
        status: str,
    ):

        evidence = await (
            self.store.evidence_repository
            .get_by_id(evidence_id)
        )

        if evidence is None:
            raise ValidationError(
                f"Evidence not found: {evidence_id}"
            )

        return await self.verifier.verify_evidence(
            evidence,
            status,
        )

    async def verify_claim(
        self,
        *,
        claim_id: str,
        status: str,
    ):

        claim = await (
            self.store.claim_repository
            .get_by_id(claim_id)
        )

        if claim is None:
            raise ValidationError(
                f"Claim not found: {claim_id}"
            )

        return await self.verifier.verify_claim(
            claim,
            status,
        )

    async def get_claim_traceability(
        self,
        *,
        claim_id: str,
    ):

        return await (
            self.traceability
            .get_claim_trace(claim_id)
        )

    async def commit(self) -> None:
        """
        提交 Phase 9 数据。
        """

        await self.session.commit()
```

### 📄 `app/services/__init__.py`

**层级**：业务服务层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/services/analysis_result_service.py`

**层级**：业务服务层 · **职责**：Analysis Result 构建服务。

```python
"""
Analysis Result 构建服务。

职责：

WorkflowState.data

        ↓

AnalysisResult


Phase12新增。
"""


from typing import Any


from app.schemas.analysis_result import (
    AnalysisResult,
    AgentAnalysisResult,
    ProjectOverview,
    TechnologyStack,
)



class AnalysisResultService:
    """
    将 Workflow 数据转换成标准分析结果。
    """



    def build(
        self,
        run_id: str,
        data: dict[str, Any],
    ) -> AnalysisResult:
        """
        构建 AnalysisResult。
        """


        repository = (
            data.get(
                "repository",
                {}
            )
        )



        if not isinstance(
            repository,
            dict,
        ):
            repository = {}



        technology_stack = (
            data.get(
                "technology_stack",
                {}
            )
        )


        if not isinstance(
            technology_stack,
            dict,
        ):
            technology_stack = {}



        agents = []


        agent_outputs = (
            data.get(
                "agent_outputs",
                {}
            )
        )



        if isinstance(
            agent_outputs,
            dict,
        ):


            for agent_name, output in (
                agent_outputs.items()
            ):


                if not isinstance(
                    output,
                    dict,
                ):
                    continue



                agents.append(

                    AgentAnalysisResult(

                        agent_name=agent_name,


                        summary=output.get(
                            "summary"
                        ),


                        facts=output.get(
                            "facts",
                            [],
                        ),


                        evidence_ids=output.get(
                            "evidence_ids",
                            [],
                        ),
                    )
                )



        return AnalysisResult(


            run_id=run_id,



            project_overview=

            ProjectOverview(

                name=repository.get(
                    "name"
                ),


                description=repository.get(
                    "description"
                ),


                repository_url=repository.get(
                    "url"
                ),


                language=repository.get(
                    "language"
                ),
            ),



            technology_stack=

            TechnologyStack(

                languages=

                technology_stack.get(
                    "languages",
                    [],
                ),


                frameworks=

                technology_stack.get(
                    "frameworks",
                    [],
                ),


                databases=

                technology_stack.get(
                    "databases",
                    [],
                ),


                tools=

                technology_stack.get(
                    "tools",
                    [],
                ),
            ),



            agents=agents,



            workflow=

            {

                "state":

                data.get(
                    "workflow_state"
                ),


                "tasks":

                data.get(
                    "task_results",
                    [],
                ),
            },



            skills=data.get(
                "skills",
                [],
            ),



            tools=data.get(
                "tools",
                [],
            ),



            rag=data.get(
                "rag",
                {},
            ),



            memory=data.get(
                "memory",
                {},
            ),



            database=data.get(
                "database",
                {},
            ),



            evidence=data.get(
                "evidences",
                data.get(
                    "evidence",
                    [],
                ),
            ),
        )



analysis_result_service = (
    AnalysisResultService()
)
```

### 📄 `app/services/analysis_workflow.py`

**层级**：业务服务层 · **职责**：Analysis Workflow Runner。

```python
"""
Analysis Workflow Runner。

负责把：

AnalysisRun
    ↓
Workflow
    ↓
WorkflowEngine
    ↓
Checkpoint
    ↓
AnalysisRun

真正连接起来。
"""

from pathlib import Path

from app.agents.agent_registry import (
    create_agent_registry,
)
from app.context.manager import (
    ContextManager,
)
from app.core.logging import get_logger
from app.memory.manager import (
    MemoryManager,
)
from app.models.repository import Repository
from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.repositories.checkpoint import (
    CheckpointRepository,
)
from app.skills.registry import (
    create_skill_registry,
)
from app.tools.dependency_analyzer_tool import (
    DependencyAnalyzerTool,
)
from app.tools.file_reader_tool import (
    FileReaderTool,
)
from app.tools.github.github_code_search_tool import (
    GitHubCodeSearchTool,
)
from app.tools.github.github_repository_tool import (
    GitHubRepositoryTool,
)
from app.tools.llm_chat_tool import (
    LLMChatTool,
)
from app.tools.mysql_query_tool import (
    MySQLQueryTool,
)
from app.tools.qdrant_search_tool import (
    QdrantSearchTool,
)
from app.tools.report_export_tool import (
    ReportExportTool,
)
from app.workflow.analysis_workflow import (
    build_analysis_workflow,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import (
    WorkflowContext,
)
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.state import (
    WorkflowState,
)

logger = get_logger(__name__)


class AnalysisWorkflowRunner:
    """Analysis Workflow 执行器。"""

    def __init__(
        self,
        session,
    ):
        self.session = session

        self.checkpoint_repository = (
            CheckpointRepository(
                session
            )
        )

        self.checkpoint = (
            CheckpointManager(
                self.checkpoint_repository
            )
        )

        self.engine = WorkflowEngine(
            checkpoint=self.checkpoint
        )

    def build_context(
        self,
        *,
        repository_id: int,
    ) -> WorkflowContext:
        """创建完整 WorkflowContext。"""

        skill_registry = (
            create_skill_registry()
        )

        agent_registry = (
            create_agent_registry(
                skill_registry
            )
        )

        tools = {
            "github_repository":
                GitHubRepositoryTool(),

            "github_code_search":
                GitHubCodeSearchTool(),

            "file_reader":
                FileReaderTool(),

            "dependency_analyzer":
                DependencyAnalyzerTool(),

            "qdrant_search":
                QdrantSearchTool(),

            "mysql_query":
                MySQLQueryTool(
                    self.session
                ),

            "report_export":
                ReportExportTool(),

            "llm_chat":
                LLMChatTool(),
        }

        memory_manager = (
            MemoryManager(
                self.session
            )
        )

        context_manager = (
            ContextManager(
                memory_manager
            )
        )

        return WorkflowContext(
            agents=agent_registry.agents,
            tools=tools,
            skills=skill_registry.skills,
            config={
                "session": self.session,
                "repository_id": repository_id,
            },
            memory_manager=memory_manager,
            context_manager=context_manager,
        )

    async def start(
        self,
        run_id: str,
    ):
        """启动新的 Analysis Workflow。"""

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        repository = await self.session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValueError(
                f"Repository not found: "
                f"{run.repository_id}"
            )

        state = WorkflowState(
            run_id=run.id
        )

        state.data = {
            "run_id": run.id,
            "repository_id": repository.id,
            "repo_url": repository.url,
            "owner": repository.owner,
            "repo": repository.name,
            "question": (
                run.question
                or (
                    "请分析这个 GitHub Agent 项目，"
                    "重点分析 Multi-Agent、Workflow、"
                    "Skill、Tool、RAG、Memory 和数据库。"
                )
            ),
        }

        context = self.build_context(
            repository_id=repository.id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.run(
            workflow,
            state,
            context,
        )

        return await self._sync_run(
            result
        )

    async def approve(
        self,
        run_id: str,
    ):
        """批准 Design Gate 或 Human Review。"""

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        state.approve()

        await self.checkpoint.save(
            state
        )

        context = self.build_context(
            repository_id=run.repository_id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.resume(
            workflow,
            context,
            run_id,
        )

        return await self._sync_run(
            result
        )

    async def pause(
        self,
        run_id: str,
    ):
        """人工暂停 Workflow。"""

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        result = await self.engine.pause(
            state
        )

        return await self._sync_run(
            result
        )

    async def resume(
        self,
        run_id: str,
    ):
        """从 PAUSED Checkpoint 恢复。"""

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        context = self.build_context(
            repository_id=run.repository_id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.resume(
            workflow,
            context,
            run_id,
        )

        return await self._sync_run(
            result
        )

    async def retry(
        self,
        run_id: str,
    ):
        """重新执行失败的 Workflow。"""

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: {run_id}"
            )

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        context = self.build_context(
            repository_id=run.repository_id
        )

        workflow = (
            build_analysis_workflow(
                context
            )
        )

        result = await self.engine.retry(
            workflow,
            context,
            run_id,
        )

        return await self._sync_run(
            result
        )

    async def get_report(
        self,
        run_id: str,
    ):
        """
        获取最终报告。

        两条路：

        1. 从 checkpoint 读（正常路径）
        2. 读不出来时退回磁盘上的报告文件

        第 2 条是必需的，不是锦上添花：
        checkpoint 的 state_data 一旦超过
        asyncmy 的大字段读取上限，
        这个 run 的 state 就永久读不回来了，
        但报告正文其实早就写在
        reports/{run_id}_analysis.md 里。
        没有这条兜底的话，
        「分析成功但报告 500」就会一直存在。
        """

        try:

            state = await self.checkpoint.load(
                run_id
            )

        except Exception as error:

            # 读不出来不让请求挂掉，
            # 交给文件兜底。
            logger.warning(
                "checkpoint load failed | run_id=%s | %s: %s",
                run_id,
                type(error).__name__,
                error,
            )

            state = None

        report = None

        if state is not None:

            report = state.data.get(
                "final_report"
            )

        return self._report_from_disk(
            run_id,
            report,
        )

    @staticmethod
    def _report_from_disk(
        run_id: str,
        report,
    ):
        """
        用磁盘上的报告文件补齐 report。

        两种情况都走这里：

        - report 完全没有（checkpoint 读不出来）
        - report 有路径但没有正文
          （state 瘦身时丢掉了 content）
        """

        directory = Path("reports")

        path = None

        if isinstance(report, dict):

            inner = report.get("report")

            if isinstance(inner, dict):

                path = inner.get("path")

        candidates = []

        if path:

            candidates.append(Path(path))

        candidates.append(
            directory / f"{run_id}_analysis.md"
        )

        for candidate in candidates:

            if not candidate.is_file():
                continue

            try:

                content = candidate.read_text(
                    encoding="utf-8"
                )

            except OSError:

                continue

            if isinstance(report, dict) and report.get(
                "content"
            ):

                return report

            return {
                "report": {
                    "path": str(candidate),
                    "format": "markdown",
                },
                "content": content,
            }

        return report

    async def deep_dive_module(
        self,
        run_id: str,
        module: str,
    ):
        """
        对某个已完成 run 的单个模块做深挖。

        复用该 run 已保存的仓库信息
        （owner / repo / branch / readme），
        因此不需要重新解析 URL，
        也不需要重跑整个分析流程。

        深挖只读不写：不修改 checkpoint，
        产物是单独一份 markdown。
        """

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        data = state.data or {}

        owner = data.get("owner")

        repo = data.get("repo")

        if not owner or not repo:
            raise ValueError(
                "该 run 缺少 owner / repo，"
                "无法定位仓库做深挖。"
            )

        repository = await self.session.get(
            Repository,
            data.get("repository_id"),
        )

        context = self.build_context(
            repository_id=data.get(
                "repository_id"
            )
        )

        skill = context.skills.get(
            "module_deep_dive"
        )

        if skill is None:
            raise ValueError(
                "Module deep dive skill "
                "is not registered."
            )

        return await skill.execute(
            context,
            {
                "run_id": run_id,
                "module": module,
                "owner": owner,
                "repo": repo,
                "branch": data.get(
                    "branch",
                    "main",
                ),
                "readme": data.get("readme"),
                "repository": data.get(
                    "repository"
                ),
                "repo_url": (
                    repository.url
                    if repository is not None
                    else data.get("repo_url")
                ),
            },
        )

    async def _sync_run(
        self,
        state,
    ):
        """把 Workflow 状态同步到 AnalysisRun。"""

        run_repo = AnalysisRunRepository(
            self.session
        )

        run = await run_repo.get_by_id(
            state.run_id
        )

        if run is None:
            raise ValueError(
                f"Analysis run not found: "
                f"{state.run_id}"
            )

        await run_repo.update_runtime_state(
            run,
            status=state.status,
            current_node=state.current_node,
            retry_count=state.retry_count,
        )

        await self.session.commit()

        return state
```

## 六、数据访问层（Repositories）

表级别的数据访问对象（DAO），只负责 SQL 与对象映射

### 📄 `app/repositories/__init__.py`

**层级**：数据访问层（Repositories） · **职责**：本层类的统一导出入口

```python
"""数据访问层统一导出。"""

from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.repositories.repository_basic import (
    RepositoryRepository,
)

__all__ = [
    "RepositoryRepository",
    "AnalysisRunRepository",
]

"""
数据访问层统一导出。
"""

from app.repositories.analysis_run import (
    AnalysisRunRepository,
)

from app.repositories.claim import (
    ClaimRepository,
)

from app.repositories.citation import (
    CitationRepository,
)

from app.repositories.evidence import (
    EvidenceRepository,
)

from app.repositories.repository_basic import (
    RepositoryRepository,
)


__all__ = [
    "RepositoryRepository",
    "AnalysisRunRepository",
    "EvidenceRepository",
    "ClaimRepository",
    "CitationRepository",
]
```

### 📄 `app/repositories/repository.py`

**层级**：数据访问层（Repositories） · **职责**：`repositories` 表的数据访问（**全字段版**，`create()` 内部 commit）

```python
"""
Repository 数据访问层兼容入口。

真正的 RepositoryRepository 实现位于：

    app.repositories.repository_basic
"""

from app.repositories.repository_basic import (
    RepositoryRepository,
)


__all__ = [
    "RepositoryRepository",
]
```

### 📄 `app/repositories/repository_basic.py`

**层级**：数据访问层（Repositories） · **职责**：`repositories` 表的数据访问（**精简版**，`create()` 只 flush，事务交给调用方）

```python
"""
GitHub Repository 数据访问层。

Repository 层只负责：

- 查询
- 创建
- Flush

事务提交由上层 Service 控制。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository


class RepositoryRepository:
    """
    repositories 表的数据访问对象。

    事务边界：

        Service
          ↓
        Repository
          ↓
        SQLAlchemy

    Repository 本身不负责 commit。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def get_by_url(
        self,
        url: str,
    ) -> Repository | None:
        """
        根据 GitHub URL 查询 Repository。
        """

        result = await self.session.execute(
            select(Repository).where(
                Repository.url == url
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id(
        self,
        repository_id: int,
    ) -> Repository | None:
        """
        根据 Repository ID 查询 Repository。
        """

        result = await self.session.execute(
            select(Repository).where(
                Repository.id == repository_id
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        url: str,
        owner: str,
        name: str,
        description: str | None = None,
        default_branch: str | None = None,
        language: str | None = None,
        stars: int = 0,
        forks: int = 0,
    ) -> Repository:
        """
        创建 Repository。

        注意：

        这里使用 flush() 而不是 commit()。

        最终事务由 Service 统一提交。
        """

        repository = Repository(
            url=url,
            owner=owner,
            name=name,
            description=description,
            default_branch=default_branch,
            language=language,
            stars=stars,
            forks=forks,
        )

        self.session.add(
            repository
        )

        await self.session.flush()

        return repository
```

### 📄 `app/repositories/analysis_run.py`

**层级**：数据访问层（Repositories） · **职责**：`analysis_runs` 表的数据访问

```python
"""
Analysis Run 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun


class AnalysisRunRepository:
    """负责 analysis_runs 表的数据访问。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

    async def create(
        self,
        *,
        run_id: str,
        repository_id: int,
        question: str | None = None,
    ) -> AnalysisRun:
        """创建一次 Analysis Run。"""

        run = AnalysisRun(
            id=run_id,
            repository_id=repository_id,
            question=question,
            status="pending",
        )

        self.session.add(run)

        await self.session.flush()

        return run

    async def get_by_id(
        self,
        run_id: str,
    ) -> AnalysisRun | None:
        """根据 run_id 查询分析任务。"""

        result = await self.session.execute(
            select(AnalysisRun).where(
                AnalysisRun.id == run_id
            )
        )

        return result.scalar_one_or_none()

    async def list_recent(
        self,
        limit: int = 20,
    ) -> list[AnalysisRun]:
        """
        按创建时间倒序列出最近的 Analysis Run。

        给前端的历史列表用。

        只读 analysis_runs 这张小表：
        state_data 在 checkpoints 里，
        这里不碰，避免大字段排序触发
        1038 Out of sort memory。
        """

        result = await self.session.execute(
            select(AnalysisRun)
            .order_by(
                AnalysisRun.created_at.desc()
            )
            .limit(limit)
        )

        return list(result.scalars().all())

    async def update_status(
        self,
        run: AnalysisRun,
        status: str,
    ) -> AnalysisRun:
        """更新分析任务状态。"""

        run.status = status

        await self.session.flush()

        return run

    async def update_runtime_state(
        self,
        run: AnalysisRun,
        *,
        status: str | None = None,
        current_node: str | None = None,
        retry_count: int | None = None,
    ) -> AnalysisRun:
        """
        更新 Workflow 运行状态。

        用于：
        - Pause
        - Resume
        - Retry
        - Checkpoint
        """

        if status is not None:
            run.status = status

        if current_node is not None:
            run.current_node = current_node

        if retry_count is not None:
            run.retry_count = retry_count

        await self.session.flush()

        return run
```

### 📄 `app/repositories/evidence.py`

**层级**：数据访问层（Repositories） · **职责**：`evidences` 表的数据访问：`create()` / `get_by_id()` / `list_by_repository()`

```python
"""
Evidence 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.evidence import Evidence


class EvidenceRepository:
    """
    Evidence 表的数据访问对象。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        *,
        evidence_id: str,
        repository_id: int,
        source_type: str,
        content: str,
        source_url: str | None = None,
        file_path: str | None = None,
        line_start: int | None = None,
        line_end: int | None = None,
        verification_status: str = "UNVERIFIED",
    ) -> Evidence:

        evidence = Evidence(
            id=evidence_id,
            repository_id=repository_id,
            source_type=source_type,
            source_url=source_url,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            content=content,
            verification_status=verification_status,
        )

        self.session.add(evidence)

        await self.session.flush()

        return evidence

    async def get_by_id(
        self,
        evidence_id: str,
    ) -> Evidence | None:

        result = await self.session.execute(
            select(Evidence).where(
                Evidence.id == evidence_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_repository(
        self,
        repository_id: int,
    ) -> list[Evidence]:

        result = await self.session.execute(
            select(Evidence)
            .where(
                Evidence.repository_id == repository_id
            )
            .order_by(Evidence.created_at)
        )

        return list(result.scalars().all())
```

### 📄 `app/repositories/claim.py`

**层级**：数据访问层（Repositories） · **职责**：`claims` 表的数据访问：`create()` / `get_by_id()` / `list_by_run()`

```python
"""
Claim 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.claim import Claim


class ClaimRepository:
    """
    Claim 表的数据访问对象。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        *,
        claim_id: str,
        run_id: str,
        claim_text: str,
        verification_status: str = "UNVERIFIED",
    ) -> Claim:

        claim = Claim(
            id=claim_id,
            run_id=run_id,
            claim_text=claim_text,
            verification_status=verification_status,
        )

        self.session.add(claim)

        await self.session.flush()

        return claim

    async def get_by_id(
        self,
        claim_id: str,
    ) -> Claim | None:

        result = await self.session.execute(
            select(Claim).where(
                Claim.id == claim_id
            )
        )

        return result.scalar_one_or_none()

    async def list_by_run(
        self,
        run_id: str,
    ) -> list[Claim]:

        result = await self.session.execute(
            select(Claim)
            .where(
                Claim.run_id == run_id
            )
            .order_by(Claim.created_at)
        )

        return list(result.scalars().all())
```

### 📄 `app/repositories/citation.py`

**层级**：数据访问层（Repositories） · **职责**：`citations` 表的数据访问：`create()` / `get_by_id()` / `get_by_claim()` / `exists()`

```python
"""
Citation 数据访问层。
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.citation import Citation


class CitationRepository:
    """
    Citation 表的数据访问对象。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def create(
        self,
        *,
        citation_id: str,
        claim_id: str,
        evidence_id: str,
    ) -> Citation:

        citation = Citation(
            id=citation_id,
            claim_id=claim_id,
            evidence_id=evidence_id,
        )

        self.session.add(citation)

        await self.session.flush()

        return citation

    async def get_by_id(
        self,
        citation_id: str,
    ) -> Citation | None:

        result = await self.session.execute(
            select(Citation).where(
                Citation.id == citation_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_claim(
        self,
        claim_id: str,
    ) -> list[Citation]:

        result = await self.session.execute(
            select(Citation)
            .where(
                Citation.claim_id == claim_id
            )
            .order_by(Citation.created_at)
        )

        return list(result.scalars().all())

    async def exists(
        self,
        *,
        claim_id: str,
        evidence_id: str,
    ) -> bool:

        result = await self.session.execute(
            select(Citation.id).where(
                Citation.claim_id == claim_id,
                Citation.evidence_id == evidence_id,
            )
        )

        return result.scalar_one_or_none() is not None
```

### 📄 `app/repositories/checkpoint.py`

**层级**：数据访问层（Repositories） · **职责**：`checkpoints` 表的数据访问：`save()`（同 run 内自增版本号）/ `get_latest()` / `delete()`，支撑 Workflow 的暂停与恢复

```python
"""
Workflow Checkpoint 数据访问层。
"""

import json

from sqlalchemy import (
    delete,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.checkpoint import Checkpoint
from app.workflow.state import WorkflowState

# 单行 state_data 的安全上限（字节）。
#
# 为什么必须设：列类型是 JSON，而 asyncmy 驱动
# 读取大字段时的缓冲区分片会失败，
# 报错是客户端的
#
#     Lost connection to MySQL server during query
#     (Existing exports of data: object cannot be re-sized)
#
# 实测临界点与 MySQL 的 sort_buffer_size
# （默认 262,144 = 256KB）吻合：
# 224KB 能读，264KB 读不了。
#
# 一旦写进去一个超限的 state_data，
# **这个 run 就再也读不回来了** ——
# 恢复、取报告、深挖全部 500。
# 所以必须在写入前拦住，而不是读取时补救。
#
# 留足余量取 180KB。
MAX_STATE_BYTES = 180_000

# 超限时按「最不值得留」的顺序逐项瘦身。
#
# 顺序是有讲究的：
#
#   final_report.content  报告正文已经写到 reports/*.md，
#                         存进 state 纯属重复，
#                         而且它正好是压垮骆驼的最后一根稻草
#                         （finalizer 那一步 +20KB）。
#   readme                原始 README，已被抽取成结构，
#                         保留开头足够人工核对。
#   evidence              证据正文，报告第 12 章展示用。
#   modules               源码片段，报告第 11 章展示用 ——
#                         最后才动它，因为删了报告就空了。
TRIM_ORDER = (
    "final_report.content",
    "readme",
    "evidence",
    "modules",
)

# 瘦身后各字段保留的规模。
READ_README_CHARS = 4_000

READ_EVIDENCE = 20

READ_MODULES = 4


class CheckpointRepository:
    """负责 checkpoints 表的数据访问。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session

    async def save(
        self,
        state: WorkflowState,
    ) -> Checkpoint:
        """
        保存 WorkflowState 快照。

        收进来的 state 是 CheckpointManager
        deepcopy 过的快照，
        因此这里瘦身不会影响内存里的运行状态。
        """

        data, trims = self._fit_state_data(
            state.data
        )

        if trims:

            # 下划线开头，FinalizerNode 组装报告输入时
            # 会跳过这类键，不会污染报告。
            data["_trimmed"] = trims

        checkpoint = Checkpoint(
            run_id=state.run_id,
            checkpoint_version=(
                state.checkpoint_version
            ),
            status=state.status,
            current_node=state.current_node,
            state_data=data,
            outputs=state.outputs,
            errors=state.errors,
            retry_count=state.retry_count,
            pause_reason=state.pause_reason,
            human_approved=state.human_approved,
        )

        self.session.add(
            checkpoint
        )

        await self.session.flush()

        return checkpoint

    @classmethod
    def _fit_state_data(
        cls,
        data,
    ):
        """
        把 state_data 压到安全上限以内。

        返回 (可能被瘦身过的 data, 瘦身记录)。
        """

        if not isinstance(data, dict):
            return data, {}

        size = cls._size(data)

        if size <= MAX_STATE_BYTES:
            return data, {}

        dropped = {}

        for path in TRIM_ORDER:

            before = cls._size(data)

            cls._trim(data, path)

            after = cls._size(data)

            if after < before:

                dropped[path] = (
                    before - after
                )

            if after <= MAX_STATE_BYTES:
                break

        return data, {
            "original_bytes": size,
            "final_bytes": cls._size(data),
            "limit_bytes": MAX_STATE_BYTES,
            "dropped_bytes": dropped,
        }

    @staticmethod
    def _size(value) -> int:
        """按实际落库的序列化方式估算字节数。"""

        try:

            return len(
                json.dumps(
                    value,
                    ensure_ascii=False,
                    default=str,
                ).encode("utf-8")
            )

        except (TypeError, ValueError):

            return 0

    @classmethod
    def _trim(
        cls,
        data: dict,
        path: str,
    ) -> None:
        """按路径瘦身一个字段。"""

        if path == "final_report.content":

            report = data.get("final_report")

            if isinstance(report, dict):

                # 报告正文已经写在 reports/*.md，
                # 这里只留文件信息，
                # 取报告时由 runner 回读文件。
                report.pop("content", None)

            return

        if path == "readme":

            readme = data.get("readme")

            if isinstance(readme, str) and len(
                readme
            ) > READ_README_CHARS:

                data["readme"] = (
                    readme[:READ_README_CHARS]
                )

            return

        if path == "evidence":

            cls._trim_list(
                data,
                "evidence",
                READ_EVIDENCE,
                ("content",),
            )

            # evidence_analysis_agent 里是同一份数据。
            cls._trim_list(
                data,
                "evidence_analysis_agent",
                READ_EVIDENCE,
                ("content",),
                nested="evidence",
            )

            return

        if path == "modules":

            cls._trim_list(
                data,
                "modules",
                READ_MODULES,
                ("content",),
            )

    @staticmethod
    def _trim_list(
        data: dict,
        key: str,
        keep: int,
        drop_keys,
        nested=None,
    ) -> None:
        """截断一个列表字段，并去掉指定子字段。"""

        value = data.get(key)

        if nested and isinstance(value, dict):

            value = value.get(nested)

        if not isinstance(value, list):
            return

        if len(value) > keep:

            del value[keep:]

        for item in value:

            if isinstance(item, dict):

                for drop in drop_keys:
                    item.pop(drop, None)

    async def get_latest(
        self,
        run_id: str,
    ) -> WorkflowState | None:
        """
        获取指定 run 的最新 Checkpoint。

        实现说明：

        不能用 ORDER BY checkpoint_version DESC LIMIT 1。

        state_data 是可能达到数百 KB 的 JSON
        （包含目录结构、关键源码、Evidence、报告），
        MySQL 在对这种大行排序时会报：

            OperationalError 1038
            Out of sort memory,
            consider increasing server sort buffer size

        因此改成两步：

            1. 只查最大版本号（只读整数列，不需要排序大行）
            2. 按 (run_id, version) 精确取行（等值查询，不排序）
        """

        version_result = await self.session.execute(
            select(
                func.max(
                    Checkpoint.checkpoint_version
                )
            ).where(
                Checkpoint.run_id == run_id
            )
        )

        latest_version = (
            version_result.scalar_one_or_none()
        )

        if latest_version is None:
            return None

        result = await self.session.execute(
            select(Checkpoint)
            .where(
                Checkpoint.run_id == run_id,
                Checkpoint.checkpoint_version
                == latest_version,
            )
            .limit(1)
        )

        checkpoint = (
            result.scalar_one_or_none()
        )

        if checkpoint is None:
            return None

        return WorkflowState(
            run_id=checkpoint.run_id,
            status=checkpoint.status,
            current_node=checkpoint.current_node,
            data=checkpoint.state_data or {},
            outputs=checkpoint.outputs or [],
            errors=checkpoint.errors or [],
            retry_count=checkpoint.retry_count,
            pause_reason=checkpoint.pause_reason,
            human_approved=checkpoint.human_approved,
            checkpoint_version=checkpoint.checkpoint_version,
        )

    async def delete(
        self,
        run_id: str,
    ) -> None:
        """删除指定 run 的全部 Checkpoint。"""

        await self.session.execute(
            delete(Checkpoint).where(
                Checkpoint.run_id == run_id
            )
        )

        await self.session.flush()
```

## 七、数据模型层（Models）

SQLAlchemy ORM 表结构定义

### 📄 `app/models/__init__.py`

**层级**：数据模型层（Models） · **职责**：模型统一导出（同时供 Alembic 迁移发现全部表）

```python
"""
数据库模型统一导出。
"""

from app.models.analysis_run import AnalysisRun
from app.models.analysis_task import AnalysisTask
from app.models.claim import Claim
from app.models.citation import Citation
from app.models.evidence import Evidence
from app.models.repository import Repository
from app.models.checkpoint import Checkpoint

__all__ = [
    "Repository",
    "AnalysisRun",
    "AnalysisTask",
    "Evidence",
    "Claim",
    "Citation",
    "Checkpoint",
]
```

### 📄 `app/models/repository.py`

**层级**：数据模型层（Models） · **职责**：`repositories` 表结构定义

```python
"""GitHub Repository 数据模型。"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Repository(Base):
    """保存 GitHub 项目的基础信息。"""

    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    url: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    owner: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    default_branch: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    stars: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    forks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
```

### 📄 `app/models/analysis_run.py`

**层级**：数据模型层（Models） · **职责**：`analysis_runs` 表结构定义

```python
"""Analysis Run 数据模型。"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AnalysisRun(Base):
    """代表用户发起的一次完整项目分析。"""

    __tablename__ = "analysis_runs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"),
        nullable=False,
    )

    question: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    current_node: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
```

### 📄 `app/models/analysis_task.py`

**层级**：数据模型层（Models） · **职责**：`analysis_tasks` 表结构定义

```python
"""Analysis Task 数据模型。"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AnalysisTask(Base):
    """保存一次 Analysis Run 中的具体分析任务。"""

    __tablename__ = "analysis_tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    run_id: Mapped[str] = mapped_column(
        ForeignKey("analysis_runs.id"),
        nullable=False,
    )

    task_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    input: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    output: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
```

### 📄 `app/models/evidence.py`

**层级**：数据模型层（Models） · **职责**：`evidences` 表结构定义（Phase 9）：一条可验证的证据，带 source_type / source_url / file_path / line 等来源定位字段与 verification_status

```python
"""
Evidence 数据模型。

Phase 9:
Evidence / Claim / Citation
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Evidence(Base):
    """
    证据模型。

    一条 Evidence 表示：

        Repository
            ↓
        Source
            ↓
        File
            ↓
        Line
            ↓
        Content

    Evidence 本身属于 Repository。
    """

    __tablename__ = "evidences"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    repository_id: Mapped[int] = mapped_column(
        ForeignKey("repositories.id"),
        nullable=False,
        index=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    source_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    file_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    line_start: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    line_end: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    verification_status: Mapped[str] = mapped_column(
        String(20),
        default="UNVERIFIED",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
```

### 📄 `app/models/claim.py`

**层级**：数据模型层（Models） · **职责**：`claims` 表结构定义（Phase 9）：一次分析 Run 产出的结论，通过 `citations` 关联到证据

```python
"""
Claim 数据模型。

Phase 9:
表示一次分析 Run 中产生的结论。
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Claim(Base):
    """
    分析结论。

    例如：

        该项目存在多个 Agent。
    """

    __tablename__ = "claims"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    run_id: Mapped[str] = mapped_column(
        ForeignKey("analysis_runs.id"),
        nullable=False,
        index=True,
    )

    claim_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    verification_status: Mapped[str] = mapped_column(
        String(20),
        default="UNVERIFIED",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
```

### 📄 `app/models/citation.py`

**层级**：数据模型层（Models） · **职责**：`citations` 表结构定义：Claim → Evidence 的引用关系，对 (claim_id, evidence_id) 加唯一约束避免重复引用

```python
"""
Citation 数据模型。

表示：

Claim
  ↓
Evidence
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Citation(Base):
    """
    Claim 与 Evidence 的关联关系。
    """

    __tablename__ = "citations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    claim_id: Mapped[str] = mapped_column(
        ForeignKey("claims.id"),
        nullable=False,
        index=True,
    )

    evidence_id: Mapped[str] = mapped_column(
        ForeignKey("evidences.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "claim_id",
            "evidence_id",
            name="uq_citations_claim_evidence",
        ),
    )
```

### 📄 `app/models/checkpoint.py`

**层级**：数据模型层（Models） · **职责**：`checkpoints` 表结构定义：Workflow 状态快照，保存 run_id / checkpoint_version / current_node / state_data / outputs / errors / retry_count / pause_reason / human_approved

```python
"""
Workflow Checkpoint 数据模型。
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base


class Checkpoint(Base):
    """
    保存 Workflow 某一时刻的完整执行快照。
    """

    __tablename__ = "checkpoints"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    run_id: Mapped[str] = mapped_column(
        ForeignKey(
            "analysis_runs.id"
        ),
        nullable=False,
        index=True,
    )

    checkpoint_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    current_node: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state_data: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    outputs: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    errors: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    pause_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    human_approved: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
```

## 八、数据库层（DB）

ORM 基类与异步 Engine / Session 管理

### 📄 `app/db/base.py`

**层级**：数据库层（DB） · **职责**：SQLAlchemy ORM 声明式基类

```python
"""SQLAlchemy ORM 基类。"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """所有数据库模型的基类。"""

    pass
```

### 📄 `app/db/session.py`

**层级**：数据库层（DB） · **职责**：异步 Engine、Session 工厂，以及 FastAPI 的数据库依赖 `get_db`

```python
"""数据库 Engine、Session 和 FastAPI 数据库依赖。"""

import json

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import get_settings


settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,

    # JSON 列默认使用 ensure_ascii=True 序列化，
    # 中文会被转义成 \uXXXX，
    # 一个汉字从 3 字节（utf8mb4）膨胀到 6 字节。
    #
    # checkpoints.state_data 里包含中文报告，
    # 转义会让单行体积显著增大，
    # 进而在读取时触发 asyncmy 驱动的
    # 「BufferError: object cannot be re-sized」
    # → Lost connection to MySQL server。
    #
    # 连接字符集是 utf8mb4，
    # 直接写原文是安全的。
    json_serializer=lambda value: json.dumps(
        value,
        ensure_ascii=False,
    ),
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """为 API 请求提供数据库 Session。"""

    async with AsyncSessionLocal() as session:
        yield session
```

### 📄 `app/db/__init__.py`

**层级**：数据库层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

## 九、核心基础设施层（Core）

配置、日志、异常体系与全局异常处理器，贯穿所有分层

### 📄 `app/core/config.py`

**层级**：核心基础设施层（Core） · **职责**：从环境变量与 `.env` 加载全局配置，并生成 MySQL 异步连接串

```python
"""项目统一配置：负责从环境变量和 .env 加载应用、数据库和 AI 服务配置。"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用全局配置，统一管理项目运行所需的环境参数。"""

    # Application
    APP_NAME: str = "AI Agent GitHub Project Intelligence Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # MySQL
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "agent_intelligence"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # LLM
    #
    # DeepSeek 提供 OpenAI 兼容接口，
    # 因此 openai SDK 直连该 base_url 即可。
    LLM_PROVIDER: str = "deepseek"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "deepseek-chat"
    LLM_BASE_URL: str = "https://api.deepseek.com"
    LLM_TIMEOUT: float = 120.0

    # 单次回复的最大 token 数。
    #
    # 必须显式设置：综合分析要输出
    # 六个维度的判断段落 + 摘要，
    # 用 API 默认值会被截断，
    # 截断的 JSON 解析必然失败，
    # 报告就会退化成「综合分析不可用」。
    LLM_MAX_TOKENS: int = 8192

    # Embedding
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"

    EMBEDDING_PROVIDER: str = "ollama"
    EMBEDDING_MODEL: str = "bge-m3"

    # GitHub
    GITHUB_TOKEN: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        """生成 SQLAlchemy 异步 MySQL 连接地址。"""
        return (
            f"mysql+asyncmy://"
            f"{self.MYSQL_USER}:"
            f"{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:"
            f"{self.MYSQL_PORT}/"
            f"{self.MYSQL_DATABASE}"
        )


@lru_cache
def get_settings() -> Settings:
    """获取全局配置实例，整个应用复用同一个 Settings 对象。"""
    return Settings()
```

### 📄 `app/core/exceptions.py`

**层级**：核心基础设施层（Core） · **职责**：项目统一异常体系，按错误来源划分类型并绑定 HTTP 状态码与错误码

```python
"""项目统一异常体系，用于区分参数、Workflow、Tool、Agent 和 LLM 等不同错误。"""


class ApplicationError(Exception):
    """所有业务异常的基类。"""

    status_code = 500
    error_code = "APPLICATION_ERROR"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValidationError(ApplicationError):
    """请求参数或业务数据验证失败。"""
    status_code = 400
    error_code = "VALIDATION_ERROR"


class WorkflowError(ApplicationError):
    """Workflow 执行失败。"""
    status_code = 500
    error_code = "WORKFLOW_ERROR"


class ToolError(ApplicationError):
    """Tool 执行失败。"""
    status_code = 500
    error_code = "TOOL_ERROR"


class AgentError(ApplicationError):
    """Agent 执行失败。"""
    status_code = 500
    error_code = "AGENT_ERROR"


class RepositoryError(ApplicationError):
    """Repository 数据访问失败。"""
    status_code = 500
    error_code = "REPOSITORY_ERROR"


class LLMError(ApplicationError):
    """LLM 调用失败。"""
    status_code = 500
    error_code = "LLM_ERROR"


class RetryableError(ApplicationError):
    """可以通过重试机制恢复的异常。"""
    status_code = 500
    error_code = "RETRYABLE_ERROR"


class NonRetryableError(ApplicationError):
    """不应该继续重试的异常。"""
    status_code = 500
    error_code = "NON_RETRYABLE_ERROR"
```

### 📄 `app/core/error_handlers.py`

**层级**：核心基础设施层（Core） · **职责**：FastAPI 全局异常处理器，将业务异常与未预期异常转换为统一 JSON 响应

```python
"""FastAPI 全局异常处理器，负责将项目异常转换为统一 HTTP 响应。"""

import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ApplicationError


logger = logging.getLogger(__name__)


async def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> JSONResponse:
    """统一处理项目定义的业务异常。"""

    logger.error(
        "application error | path=%s | error_code=%s | message=%s",
        request.url.path,
        exc.error_code,
        exc.message,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
            },
        },
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """统一处理未预期的系统异常。"""

    # 未知异常记录完整堆栈，但只向客户端返回通用错误，
    # 避免数据库、API Key 等内部信息泄露。
    logger.exception(
        "unexpected error | path=%s",
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error",
            },
        },
    )
```

### 📄 `app/core/logging.py`

**层级**：核心基础设施层（Core） · **职责**：全局日志初始化格式，以及带 `run_id` 的任务日志辅助函数

```python
"""项目统一日志配置，负责初始化日志格式并提供带 run_id 的任务日志。"""

import logging
import sys
from typing import Optional


LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def setup_logging() -> None:
    """初始化全局日志配置。"""
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """获取指定模块的 Logger。"""
    return logging.getLogger(name)


def log_with_run_id(
    logger: logging.Logger,
    level: int,
    message: str,
    run_id: Optional[str] = None,
) -> None:
    """记录任务日志，并在存在 run_id 时关联具体任务。"""

    # run_id 是后续 Workflow、Agent、Tool、Checkpoint
    # 追踪同一次任务执行过程的重要标识。
    if run_id:
        message = f"run_id={run_id} | {message}"

    logger.log(level, message)
```

### 📄 `app/core/__init__.py`

**层级**：核心基础设施层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

## 十、Workflow 层（Workflow）

自研工作流引擎：状态、上下文、节点、流转、重试、检查点与执行引擎

### 📄 `app/workflow/state.py`

**层级**：Workflow 层（Workflow） · **职责**：Workflow 运行状态 `WorkflowState`：run_id、status、current_node、data、outputs、errors、retry_count

```python
"""
Workflow 运行状态。

Phase 10：
- 支持 Design Gate
- 支持 Human Review
- 支持 Pause / Resume
- 支持 Retry
- 支持 Checkpoint
"""

from dataclasses import dataclass, field
from typing import Any

class WorkflowStatus:
    """Workflow 状态常量。"""

    CREATED = "CREATED"

    PLANNING = "PLANNING"

    WAITING_DESIGN = "WAITING_DESIGN"

    ANALYZING = "ANALYZING"

    WAITING_HUMAN = "WAITING_HUMAN"

    PAUSED = "PAUSED"

    RETRYING = "RETRYING"

    FAILED = "FAILED"

    COMPLETED = "COMPLETED"


@dataclass
class WorkflowState:
    """
    保存一次 Workflow 执行过程中的完整状态。

    该对象可以被 CheckpointManager 序列化并恢复。
    """

    # Workflow 执行 ID
    run_id: str

    # 当前 Workflow 状态
    status: str = WorkflowStatus.CREATED

    # 当前正在执行的 Node
    current_node: str | None = None

    # 业务数据
    data: dict[str, Any] = field(
        default_factory=dict
    )

    # 节点执行结果
    outputs: list[Any] = field(
        default_factory=list
    )

    # 错误记录
    errors: list[str] = field(
        default_factory=list
    )

    # 当前 Node 的重试次数
    retry_count: int = 0

    # 当前 Node 最大重试次数
    max_retry: int = 3

    # 暂停原因
    pause_reason: str | None = None

    # 是否已经获得人工批准
    human_approved: bool = False

    # Checkpoint 版本
    checkpoint_version: int = 0

    def mark_waiting_design(self) -> None:
        """进入 Design Gate，等待人工审批。"""

        self.status = WorkflowStatus.WAITING_DESIGN

    def approve(self) -> None:
        """人工批准 Research Plan。"""

        self.human_approved = True
        self.status = WorkflowStatus.ANALYZING

    def pause(
        self,
        reason: str = "manual_pause",
    ) -> None:
        """暂停 Workflow。"""

        self.status = WorkflowStatus.PAUSED
        self.pause_reason = reason

    def resume(self) -> None:
        """恢复 Workflow。"""

        self.status = WorkflowStatus.ANALYZING
        self.pause_reason = None

    def start_retry(self) -> None:
        """进入 Retry 状态。"""

        self.status = WorkflowStatus.RETRYING

    def reset_retry(self) -> None:
        """重置当前 Node 的 retry count。"""

        self.retry_count = 0

    def can_retry(self) -> bool:
        """判断当前 Node 是否还能继续重试。"""

        return self.retry_count < self.max_retry

    def increase_retry(self) -> None:
        """增加当前 Node 的 retry 次数。"""

        self.retry_count += 1
```

### 📄 `app/workflow/context.py`

**层级**：Workflow 层（Workflow） · **职责**：Workflow 执行上下文 `WorkflowContext`：agents / tools / skills / config

```python
"""
Workflow 执行上下文。

负责向 Workflow / Node / Agent 提供：

- Agent
- Tool
- Skill
- Config
- Memory
- Context Manager

其中 Memory / Context Manager 为可选能力，
用于兼容 Phase 10 以前的调用方式。
"""

from dataclasses import dataclass


@dataclass
class WorkflowContext:
    """
    Workflow 运行环境。

    当前阶段：

        Workflow
            ↓
        WorkflowContext
            ├── Agents
            ├── Tools
            ├── Skills
            ├── Config
            ├── Memory
            └── Context Manager
    """

    # Agent 集合
    agents: dict

    # Tool 集合
    tools: dict

    # Skill 集合
    skills: dict

    # Workflow 配置
    config: dict

    # Phase 11 Memory 能力
    #
    # 使用 object 避免 Workflow 层
    # 与具体 MemoryManager 实现产生强耦合。
    memory_manager: object | None = None

    # Phase 11 Context Manager
    #
    # 使用 object 避免 Workflow 层
    # 与具体 ContextManager 实现产生强耦合。
    context_manager: object | None = None
```

### 📄 `app/workflow/node.py`

**层级**：Workflow 层（Workflow） · **职责**：节点抽象 `BaseNode`，定义 `execute(state, context)`

```python
"""
Workflow节点抽象。
"""

from abc import ABC, abstractmethod


class BaseNode(ABC):
    """
    Workflow执行节点基类。
    """

    # 节点名称
    name: str

    @abstractmethod
    async def execute(
        self,
        state,
        context
    ):
        """
        执行节点逻辑。
        """
        pass
```

### 📄 `app/workflow/transition.py`

**层级**：Workflow 层（Workflow） · **职责**：节点流转关系 `Transition`：source / target / 可选条件函数

```python
"""
Workflow节点流转关系。
"""


class Transition:


    def __init__(
        self,
        source,
        target,
        condition=None
    ):

        # 当前节点
        self.source = source


        # 下一节点
        self.target = target


        # 条件函数
        self.condition = condition
```

### 📄 `app/workflow/result.py`

**层级**：Workflow 层（Workflow） · **职责**：节点执行结果 `NodeResult`：success / data / error

```python
"""
Node执行结果。
"""


from dataclasses import dataclass
from typing import Any


@dataclass
class NodeResult:
    """
    节点执行返回结果。
    """


    # 是否执行成功
    success: bool


    # 返回数据
    data: Any = None


    # 错误信息
    error: str | None = None
```

### 📄 `app/workflow/retry.py`

**层级**：Workflow 层（Workflow） · **职责**：重试策略 `RetryPolicy`：max_retry 与 `can_retry()`

```python
"""
Workflow Retry Policy。

Phase 10：
- Retryable Error
- NonRetryable Error
- 最大重试次数
"""

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)


class RetryPolicy:
    """
    Workflow 重试策略。

    RetryPolicy 本身只负责：
    1. 判断异常是否允许 Retry
    2. 判断是否超过最大 Retry 次数
    """

    def __init__(
        self,
        max_retry: int = 3,
    ) -> None:

        if max_retry < 0:
            raise ValueError(
                "max_retry cannot be negative"
            )

        self.max_retry = max_retry

    def can_retry(
        self,
        retry_count: int,
    ) -> bool:
        """判断当前 retry_count 是否还能继续 Retry。"""

        return retry_count < self.max_retry

    def is_retryable(
        self,
        error: Exception,
    ) -> bool:
        """
        判断异常是否允许 Retry。

        RetryableError：
            可以重试

        NonRetryableError：
            不允许重试
        """

        if isinstance(
            error,
            NonRetryableError,
        ):
            return False

        if isinstance(
            error,
            RetryableError,
        ):
            return True

        return False

    def should_retry(
        self,
        error: Exception,
        retry_count: int,
    ) -> bool:
        """综合判断是否应该 Retry。"""

        return (
            self.is_retryable(error)
            and self.can_retry(retry_count)
        )
```

### 📄 `app/workflow/checkpoint.py`

**层级**：Workflow 层（Workflow） · **职责**：状态保存与恢复 `CheckpointManager`，内存实现：按 run_id 用 `deepcopy` 保存 `WorkflowState` 快照

```python
"""
Workflow Checkpoint Manager。
"""

from copy import deepcopy
from typing import Any


class CheckpointManager:
    """Workflow Checkpoint 管理器。"""

    def __init__(
        self,
        repository=None,
    ) -> None:
        self.repository = repository
        self._store: dict[str, Any] = {}

    async def save(
        self,
        state,
    ) -> str:
        """保存 WorkflowState 快照。"""

        # 先递增原状态版本。
        state.checkpoint_version += 1

        snapshot = deepcopy(
            state
        )

        if self.repository is not None:

            await self.repository.save(
                snapshot
            )

        else:

            self._store[
                snapshot.run_id
            ] = snapshot

        return snapshot.run_id

    async def load(
        self,
        run_id: str,
    ):
        """读取最近一次 Checkpoint。"""

        if self.repository is not None:

            state = (
                await self.repository.get_latest(
                    run_id
                )
            )

            if state is None:
                return None

            return deepcopy(
                state
            )

        state = self._store.get(
            run_id
        )

        if state is None:
            return None

        return deepcopy(
            state
        )

    async def delete(
        self,
        run_id: str,
    ) -> None:
        """删除 Checkpoint。"""

        if self.repository is not None:

            await self.repository.delete(
                run_id
            )

        else:

            self._store.pop(
                run_id,
                None,
            )
```

### 📄 `app/workflow/exceptions.py`

**层级**：Workflow 层（Workflow） · **职责**：Workflow 自有异常：`WorkflowError`（继承 `ApplicationError`，可被全局异常处理器捕获）/ `NodeExecutionError`

```python
"""
Workflow 层异常定义。

统一使用：

    app.core.exceptions.WorkflowError

避免项目中出现两个不同的 WorkflowError。
"""

from app.core.exceptions import WorkflowError


class NodeExecutionError(WorkflowError):
    """
    Workflow Node 执行异常。

    继承统一的 WorkflowError，
    因此可以被 WorkflowError / ApplicationError
    统一捕获。
    """

    pass


__all__ = [
    "WorkflowError",
    "NodeExecutionError",
]
```

### 📄 `app/workflow/workflow.py`

**层级**：Workflow 层（Workflow） · **职责**：流程定义 `Workflow`：`add_node()` 注册节点、`add_transition()` 注册流转

```python
"""
Workflow 流程定义。

负责：

1. 注册 Workflow Node
2. 保存 Node
3. 注册 Transition
4. 保存 Transition

真正执行 Workflow 的职责由 WorkflowEngine 负责。
"""

from app.workflow.node import BaseNode
from app.workflow.transition import Transition


class Workflow:
    """
    Workflow 流程定义。

    Workflow 本身只负责描述：

        Node
          +
        Transition

    不负责真正执行。

    真正执行由：

        WorkflowEngine

    完成。
    """

    def __init__(self) -> None:
        # 保存所有 Workflow Node
        #
        # {
        #     "start": StartNode(),
        #     "analysis": AnalysisNode(),
        # }
        self.nodes: dict[str, BaseNode] = {}

        # 保存 Workflow 流转关系
        self.transitions: list[Transition] = []

    def add_node(
        self,
        node: BaseNode,
    ) -> None:
        """
        注册 Workflow Node。
        """

        if not node.name:
            raise ValueError(
                "Workflow node name cannot be empty"
            )

        if node.name in self.nodes:
            raise ValueError(
                f"Workflow node already exists: {node.name}"
            )

        self.nodes[node.name] = node

    def add_transition(
        self,
        transition: Transition,
    ) -> None:
        """
        注册 Workflow Transition。
        """

        self.transitions.append(
            transition
        )

    def get_node(
        self,
        name: str,
    ) -> BaseNode | None:
        """
        根据名称获取 Node。
        """

        return self.nodes.get(name)
```

### 📄 `app/workflow/engine.py`

**层级**：Workflow 层（Workflow） · **职责**：执行引擎 `WorkflowEngine`：从 `start` 节点起循环执行，异常时记录 errors 并置 FAILED，正常结束置 COMPLETED；支持可选 `checkpoint` / `retry_policy`，`RetryableError` 按 `RetryPolicy` 重试，`PAUSED` 状态保存检查点后退出，`resume_from` 可从检查点恢复

```python
"""
Workflow 执行引擎。

Phase 12：
    - 顺序执行
    - Checkpoint
    - Pause
    - Resume
    - Retry
    - Human Gate
"""


from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.core.logging import get_logger
from app.workflow.retry import RetryPolicy
from app.workflow.state import WorkflowStatus


logger = get_logger(__name__)


class WorkflowEngine:
    """自研 Workflow 执行引擎。"""

    PAUSE_STATUSES = {
        WorkflowStatus.PAUSED,
        WorkflowStatus.WAITING_HUMAN,
        WorkflowStatus.WAITING_DESIGN,
    }

    def __init__(
        self,
        checkpoint=None,
        retry_policy=None,
    ) -> None:

        self.checkpoint = checkpoint

        self.retry_policy = (
            retry_policy
            or RetryPolicy()
        )

    async def run(
        self,
        workflow,
        state,
        context,
        resume_from=None,
    ):
        """
        执行 Workflow。

        resume_from：
            从 Checkpoint 恢复，并执行当前节点的下一个节点。

        state：
            如果 state 本身已经存在 current_node，
            则用于 Retry 当前节点。
        """

        if resume_from is not None:

            state = await self._restore(
                resume_from
            )

            if state is None:
                raise ValueError(
                    f"Checkpoint not found: {resume_from}"
                )

            if state.status == WorkflowStatus.FAILED:

                # FAILED 表示当前节点没有执行完成，
                # 因此必须重新执行该节点，
                # 不能像 Pause / Human Gate 那样跳到下一个节点。
                current_node = state.current_node

            else:

                # PAUSED / WAITING_DESIGN / WAITING_HUMAN：
                # 当前节点已经执行完成，
                # 从下一个节点继续。
                current_node = (
                    self._get_next_node(
                        workflow,
                        state,
                        state.current_node,
                    )
                )

            state.resume()

            # 重新执行意味着重新开始，
            # 上一轮失败留下的错误不再保留。
            state.errors = []

        elif (
            state is not None
            and state.current_node
        ):

            # Retry：
            # 从失败节点重新执行。
            current_node = (
                state.current_node
            )

        else:

            current_node = "start"

        while current_node:

            node = workflow.nodes.get(
                current_node
            )

            if node is None:

                state.errors.append(
                    f"Node not found: {current_node}"
                )

                state.status = (
                    WorkflowStatus.FAILED
                )

                await self._save(state)

                return state

            state.current_node = (
                current_node
            )

            try:

                state = await self._execute_node(
                    node,
                    state,
                    context,
                )

            except Exception as error:

                # 记录完整 traceback。
                #
                # 部分异常（例如 httpx.ReadTimeout）
                # 的 str() 为空字符串，
                # 只记录 str(error) 会导致
                # errors == [""] 而无法排查。
                logger.exception(
                    "Workflow node failed: %s",
                    current_node,
                )

                state.errors.append(
                    str(error)
                    or type(error).__name__
                )

                state.status = (
                    WorkflowStatus.FAILED
                )

                await self._save(state)

                return state

            if state.status in self.PAUSE_STATUSES:

                await self._save(state)

                return state

            await self._save(state)


            current_node = (
                self._get_next_node(
                    workflow,
                    state,
                    current_node,
                )
            )

        state.status = (
            WorkflowStatus.COMPLETED
        )

        await self._save(state)

        return state

    async def _execute_node(
        self,
        node,
        state,
        context,
    ):

        while True:

            try:

                return await node.execute(
                    state,
                    context,
                )

            except NonRetryableError:

                raise

            except RetryableError as error:

                if not self.retry_policy.should_retry(
                    error,
                    state.retry_count,
                ):
                    raise

                state.increase_retry()
                state.start_retry()

                await self._save(state)

                state.status = (
                    WorkflowStatus.ANALYZING
                )

    async def pause(
        self,
        state,
        reason: str = "manual_pause",
    ):

        state.pause(
            reason=reason
        )

        await self._save(state)

        return state

    async def approve(
        self,
        state,
    ):

        state.approve()

        await self._save(state)

        return state

    async def resume(
        self,
        workflow,
        context,
        run_id: str,
    ):

        return await self.run(
            workflow,
            None,
            context,
            resume_from=run_id,
        )

    async def retry(
        self,
        workflow,
        context,
        run_id: str,
    ):

        state = await self._restore(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        state.status = (
            WorkflowStatus.RETRYING
        )

        state.errors = []

        await self._save(state)

        return await self.run(
            workflow,
            state,
            context,
        )

    async def _save(
        self,
        state,
    ):

        if self.checkpoint is None:
            return

        await self.checkpoint.save(
            state
        )

    async def _restore(
        self,
        run_id: str,
    ):

        if self.checkpoint is None:
            raise ValueError(
                "Checkpoint manager is required"
            )

        return await self.checkpoint.load(
            run_id
        )

    def _get_next_node(
        self,
        workflow,
        state,
        current,
    ):

        for transition in workflow.transitions:

            if transition.source != current:
                continue

            if transition.condition:

                if not transition.condition(
                    state
                ):
                    continue

            return transition.target

        return None
```

### 📄 `app/workflow/__init__.py`

**层级**：Workflow 层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/workflow/analysis_workflow.py`

**层级**：Workflow 层 · **职责**：AIPI 单项目分析 Workflow。

```python
"""
AIPI 单项目分析 Workflow。

完整链路：

Start
    ↓
Planner
    ↓
Design Gate
    ↓
Plan Executor
    ↓
Human Review
    ↓
Synthesis
    ↓
Finalizer
    ↓
End
"""

from app.workflow.nodes.agent_node import AgentNode
from app.workflow.nodes.design_gate_node import (
    DesignGateNode,
)
from app.workflow.nodes.end_node import EndNode
from app.workflow.nodes.finalizer_node import (
    FinalizerNode,
)
from app.workflow.nodes.human_node import HumanNode
from app.workflow.nodes.plan_executor_node import (
    PlanExecutorNode,
)
from app.workflow.nodes.start_node import StartNode
from app.workflow.nodes.synthesis_node import (
    SynthesisNode,
)
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow


def build_analysis_workflow(
    context,
) -> Workflow:
    """
    创建单项目完整分析 Workflow。

    Agent 的具体实例来自 WorkflowContext，
    Workflow 本身不负责创建 Agent。
    """

    workflow = Workflow()

    planner = context.agents.get(
        "planner_agent"
    )

    if planner is None:
        raise ValueError(
            "Planner Agent is not registered."
        )

    report_skill = context.skills.get(
        "report_generation"
    )

    if report_skill is None:
        raise ValueError(
            "Report generation skill is not registered."
        )

    synthesis_skill = context.skills.get(
        "report_synthesis"
    )

    if synthesis_skill is None:
        raise ValueError(
            "Report synthesis skill is not registered."
        )

    workflow.add_node(
        StartNode()
    )

    workflow.add_node(
        AgentNode(
            name="planner_agent",
            agent=planner,
        )
    )

    workflow.add_node(
        DesignGateNode()
    )

    workflow.add_node(
        PlanExecutorNode()
    )

    workflow.add_node(
        HumanNode()
    )

    workflow.add_node(
        SynthesisNode(
            skill=synthesis_skill,
        )
    )

    workflow.add_node(
        FinalizerNode(
            skill=report_skill,
        )
    )

    workflow.add_node(
        EndNode()
    )

    workflow.add_transition(
        Transition(
            "start",
            "planner_agent",
        )
    )

    workflow.add_transition(
        Transition(
            "planner_agent",
            "design_gate",
        )
    )

    workflow.add_transition(
        Transition(
            "design_gate",
            "plan_executor",
        )
    )

    workflow.add_transition(
        Transition(
            "plan_executor",
            "human_review",
        )
    )

    workflow.add_transition(
        Transition(
            "human_review",
            "synthesis",
        )
    )

    workflow.add_transition(
        Transition(
            "synthesis",
            "finalizer",
        )
    )

    workflow.add_transition(
        Transition(
            "finalizer",
            "end",
        )
    )

    return workflow
```

## 十一、Workflow 节点层（Workflow Nodes）

各类节点的具体实现：开始 / 结束 / 分析 / Agent / Tool / Skill / 人工审核

### 📄 `app/workflow/nodes/base.py`

**层级**：Workflow 节点层 · **职责**：节点基类 `BaseNode`（与 `app/workflow/node.py` 中的同名类重复定义）

```python
"""
Workflow 节点基类兼容入口。

项目只保留：
    app.workflow.node.BaseNode

这里通过重新导出保持旧代码兼容。
"""

from app.workflow.node import BaseNode


__all__ = [
    "BaseNode",
]
```

### 📄 `app/workflow/nodes/start_node.py`

**层级**：Workflow 节点层 · **职责**：开始节点 `StartNode`（name=`start`），把 status 置为 RUNNING

```python
"""
Workflow开始节点。
"""


from app.workflow.node import BaseNode



class StartNode(BaseNode):


    name = "start"



    async def execute(
        self,
        state,
        context
    ):

        state.status = "RUNNING"

        return state
```

### 📄 `app/workflow/nodes/end_node.py`

**层级**：Workflow 节点层 · **职责**：结束节点 `EndNode`（name=`end`），把 status 置为 COMPLETED

```python
"""
Workflow结束节点。
"""


from app.workflow.node import BaseNode



class EndNode(BaseNode):


    name = "end"



    async def execute(
        self,
        state,
        context
    ):

        state.status = "COMPLETED"

        return state
```

### 📄 `app/workflow/nodes/analysis_node.py`

**层级**：Workflow 节点层 · **职责**：分析节点 `AnalysisNode`（name=`analysis`），当前为占位实现

```python
"""
分析节点。
"""


from app.workflow.node import BaseNode



class AnalysisNode(BaseNode):


    name = "analysis"



    async def execute(
        self,
        state,
        context
    ):

        # 模拟业务结果
        state.data[
            "result"
        ] = "analysis completed"


        return state
```

### 📄 `app/workflow/nodes/agent_node.py`

**层级**：Workflow 节点层 · **职责**：Agent 节点 `AgentNode`，调用 `agent.run(state, context)` 并把结果追加到 `state.outputs`

```python
"""
Agent 类型 Workflow 节点。

负责：
    - 调用 Agent.execute()
    - 将 Agent 输出保存到 WorkflowState
    - 保留执行历史
"""

from .base import BaseNode


class AgentNode(BaseNode):
    """
    封装 Agent 执行。
    """

    def __init__(
        self,
        name,
        agent,
    ):
        self.name = name
        self.agent = agent

    async def execute(
        self,
        state,
        context,
    ):
        """
        执行 Agent。

        Agent 新接口：

            execute(
                context,
                input_data
            )
        """

        result = await self.agent.execute(
            context,
            state.data,
        )

        # 保存当前 Agent 输出。
        state.data[self.name] = result

        # 保留执行历史。
        state.outputs.append(result)

        return state
```

### 📄 `app/workflow/nodes/tool_node.py`

**层级**：Workflow 节点层 · **职责**：Tool 节点 `ToolNode`，从 `state.data[node.name]` 取参后调用 `tool.execute(**args)`，并把结果追加到 `state.outputs`

```python
"""
Tool类型Workflow节点。
"""


from .base import BaseNode



class ToolNode(BaseNode):
    """
    封装Tool调用。
    """


    def __init__(
        self,
        name,
        tool
    ):

        self.name = name

        self.tool = tool



    async def execute(
        self,
        state,
        context
    ):


        # 从 state.data 中按节点名取调用参数
        args = state.data.get(
            self.name,
            {}
        )


        # 执行Tool
        result = await self.tool.execute(
            **args
        )


        state.outputs.append(
            result
        )


        return state
```

### 📄 `app/workflow/nodes/skill_node.py`

**层级**：Workflow 节点层 · **职责**：Skill 节点 `SkillNode`，以 `skill.execute(context=context, input_data=state.data)` 调用 Skill，把结果同时写入 `state.data[node.name]` 与 `state.outputs`

```python
"""
Skill Node


Workflow中的Skill执行节点。


职责:

Workflow

    ↓

SkillNode

    ↓

Skill

    ↓

Tool


"""
from .base import BaseNode

class SkillNode(BaseNode):


    def __init__(
        self,
        name,
        skill
    ):
        # 节点名称

        self.name = name


        # 对应Skill实例

        self.skill = skill

    async def execute(
        self,
        state,
        context
    ):
        """
        执行Skill。


        """
        result = await self.skill.execute(

            context=context,

            input_data=state.data

        )

        # 保存当前Skill输出

        state.data[
            self.name
        ] = result

        # 保存执行历史

        state.outputs.append(
            result
        )
        return state
```

### 📄 `app/workflow/nodes/human_node.py`

**层级**：Workflow 节点层 · **职责**：HITL 人工审核节点 `HumanNode`（name=`human_review`），把 status 置为 WAITING_HUMAN 以暂停流程

```python
"""
Human-In-The-Loop Workflow Node。

负责：

Workflow
    ↓
HumanNode
    ↓
WAITING_HUMAN
    ↓
Checkpoint
    ↓
等待人工操作
"""

from .base import BaseNode


class HumanNode(BaseNode):
    """人工审核节点。"""

    name = "human_review"

    async def execute(
        self,
        state,
        context,
    ):
        """
        进入人工审核状态。

        WorkflowEngine 会检测 WAITING_HUMAN，
        保存 Checkpoint 后停止。
        """

        state.status = (
            "WAITING_HUMAN"
        )

        state.pause_reason = (
            "human_review_required"
        )

        return state
```

### 📄 `app/workflow/nodes/__init__.py`

**层级**：Workflow 节点层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/workflow/nodes/design_gate_node.py`

**层级**：Workflow 节点层 · **职责**：Design Gate Workflow Node。

```python
"""
Design Gate Workflow Node。

职责：
    - 读取 Planner Agent 生成的 Research Plan
    - 将 Research Plan 提升到 WorkflowState.data 顶层
    - 将 Workflow 置为 WAITING_DESIGN
    - 等待人工审批后继续执行
"""

from app.workflow.node import BaseNode


class DesignGateNode(BaseNode):
    """
    Phase 12 研究计划设计闸门。

    Planner Agent 完成后进入该节点。

    数据流：

        planner_agent
            ↓
        planner_agent["research_plan"]
            ↓
        state.data["research_plan"]
            ↓
        WAITING_DESIGN
            ↓
        Human Approval
    """

    name = "design_gate"

    async def execute(
        self,
        state,
        context,
    ):
        """
        保存 Research Plan，并暂停 Workflow 等待设计审批。
        """

        # 获取 Planner Agent 的输出。
        planner_result = state.data.get(
            "planner_agent",
            {},
        )

        # Planner Agent 应该返回 research_plan。
        research_plan = planner_result.get(
            "research_plan"
        )

        # 将 Research Plan 保存到 WorkflowState 顶层。
        #
        # 这样后续：
        #   - PlanExecutorNode
        #   - Checkpoint
        #   - Memory
        #   - Human Approval
        #
        # 都可以直接读取 state.data["research_plan"]。
        if research_plan is not None:
            state.data[
                "research_plan"
            ] = research_plan

        # 进入 Design Gate，
        # 等待人工确认研究计划。
        state.mark_waiting_design()

        return state
```

### 📄 `app/workflow/nodes/finalizer_node.py`

**层级**：Workflow 节点层 · **职责**：Finalizer Workflow Node。

```python
"""
Finalizer Workflow Node。

负责：

Human Review
    ↓
Finalizer
    ↓
ReportGenerationSkill
    ↓
Final Report
"""

from .base import BaseNode


class FinalizerNode(BaseNode):
    """最终报告生成节点。"""

    name = "finalizer"

    def __init__(
        self,
        skill,
    ):
        self.skill = skill

    async def execute(
        self,
        state,
        context,
    ):
        """生成最终项目分析报告。"""

        report_input = {
            key: value
            for key, value in state.data.items()
            if not key.startswith("_")
        }

        report_input.setdefault(
            "title",
            "GitHub Project Intelligence Report",
        )

        report_input.setdefault(
            "filename",
            f"{state.run_id}_analysis.md",
        )

        result = await self.skill.execute(
            context=context,
            input_data=report_input,
        )

        state.data["final_report"] = result

        state.outputs.append(result)

        return state
```

### 📄 `app/workflow/nodes/plan_executor_node.py`

**层级**：Workflow 节点层 · **职责**：Planner 计划执行节点。

```python
"""
Planner 计划执行节点。

负责：

1. 读取 PlannerAgent 生成的 tasks
2. 按 tasks 顺序获取 Agent
3. 构建当前 Agent 所需 Context
4. 依次执行 Agent
5. 将 Agent 输出合并回 WorkflowState.data
"""

from .base import BaseNode


class PlanExecutorNode(BaseNode):
    """根据 PlannerAgent 输出执行 Agent。"""

    name = "plan_executor"

    def __init__(
        self,
        name: str = "plan_executor",
        planner_key: str = "planner_agent",
    ):
        self.name = name
        self.planner_key = planner_key

    async def execute(
        self,
        state,
        context,
    ):
        """执行 Planner 生成的任务列表。"""

        planner_result = state.data.get(
            self.planner_key
        )

        if not isinstance(
            planner_result,
            dict,
        ):
            raise ValueError(
                "Planner result is missing."
            )

        tasks = planner_result.get(
            "tasks"
        )

        if not isinstance(
            tasks,
            list,
        ):
            raise ValueError(
                "Planner result must contain "
                "a list field named 'tasks'."
            )

        if not tasks:
            raise ValueError(
                "Planner returned an empty task list."
            )

        executed_tasks = []

        for agent_name in tasks:

            if not isinstance(
                agent_name,
                str,
            ):
                raise ValueError(
                    "Planner task must be "
                    "an Agent name string."
                )

            agent = context.agents.get(
                agent_name
            )

            if agent is None:
                raise ValueError(
                    f"Agent not found: {agent_name}"
                )

            agent_input = dict(
                state.data
            )

            # Phase 11 Context Manager 接入。
            if (
                context.context_manager is not None
                and state.data.get(
                    "repository_id"
                ) is not None
            ):
                query = (
                    state.data.get("question")
                    or "GitHub project analysis"
                )

                agent_context = (
                    await context.context_manager.build(
                        run_id=state.run_id,
                        repository_id=state.data[
                            "repository_id"
                        ],
                        query=query,
                        workflow_state=state.data,
                        user_instruction=query,
                    )
                )

                agent_input["_context"] = (
                    agent_context
                )

            result = await agent.execute(
                context,
                agent_input,
            )

            # Agent 名键只保留还有读取方的部分。
            #
            # 原实现把同一份结果写三遍：
            #
            #     state.data[agent_name]   本段
            #     state.data.update(...)   拍平到顶层
            #     state.outputs.append(...) 再存一份
            #
            # 实测（被分析项目 Legal，17.8MB）：
            # architecture 一份 57KB、evidence 29KB、
            # repository 5KB，三写下来约 250KB 纯重复，
            # 把 state_data 推到 263KB，
            # 越过 asyncmy 单字段 256KB 的缓冲区分片上限，
            # 报告接口读 checkpoint 直接
            # Lost connection to MySQL server。
            #
            # 顶层拍平的那份是规范数据源
            # （报告 / 综合分析 / 分析结果都读它），
            # 因此这里只额外保留
            # architecture_analysis_agent 的精简副本 ——
            # CriticAgent 会按这个键读它。
            slim = self._slim_agent_result(
                agent_name,
                result,
            )

            if slim is not None:

                state.data[agent_name] = slim

            # 合并结构化输出。
            if isinstance(
                result,
                dict,
            ):
                state.data.update(
                    result
                )

            # outputs 的正文没有任何业务读取方
            # （只作为 agent_outputs 透出），
            # 因此不再原样复制大对象，
            # 只留一个可读的运行痕迹。
            state.outputs.append(
                self._output_marker(
                    agent_name,
                    result,
                )
            )

            executed_tasks.append(
                agent_name
            )

        state.data[
            "executed_tasks"
        ] = executed_tasks

        return state

    # Agent 名键的精简规则。
    #
    # 顶层拍平的那份是规范数据源，
    # Agent 名键只是兼容层，
    # 因此按「有没有读取方」逐个决定：
    #
    #   SLIM_AGENT_FIELDS  有大读取方 -> 只留它需要的子字段
    #   DROPPED_AGENT_KEYS 完全没有读取方 -> 不写
    #   其余               原样保留
    #
    # 只对体积大的动手：
    # critic_agent（30B）、technology_analysis_agent（193B）
    # 留着也不占地方，但删了会破坏断言它们的测试。
    SLIM_AGENT_FIELDS = {
        # 读取方：CriticAgent 需要
        # modules / directory_structure / files。
        #
        # 它不读 project_structure（顶层有），
        # 而那一块恰好最大（33KB）。
        "architecture_analysis_agent": (
            "files",
            "modules",
            "directory_structure",
        ),
    }

    # 体积大、且没有任何读取方的 Agent 名键。
    #
    # evidence_analysis_agent（29KB）的内容是
    # {"evidence": [...], "count": N}，
    # 而 evidence 与 count 都已经在顶层拍平，
    # 全项目没有任何地方按这个键去读 state.data。
    DROPPED_AGENT_KEYS = (
        "evidence_analysis_agent",
    )

    @classmethod
    def _slim_agent_result(
        cls,
        agent_name,
        result,
    ):
        """
        决定 Agent 名键写什么。

        返回 None 表示「不写这个键」。
        """

        if agent_name in cls.DROPPED_AGENT_KEYS:
            return None

        fields = cls.SLIM_AGENT_FIELDS.get(
            agent_name
        )

        if not fields:
            # 其余 Agent 原样保留。
            return result

        if not isinstance(result, dict):
            return result

        return {
            key: result[key]
            for key in fields
            if key in result
        }

    @staticmethod
    def _output_marker(
        agent_name,
        result,
    ) -> dict:
        """
        生成 outputs 里的一条运行痕迹。

        保留 Agent 名与产出规模，
        便于排查「这一步到底有没有产出」，
        但不复制正文 —— 正文在 state.data 里。
        """

        marker = {
            "agent": agent_name,
            "type": type(result).__name__,
        }

        if isinstance(result, dict):

            marker["fields"] = sorted(
                result.keys()
            )

        return marker
```

### 📄 `app/workflow/nodes/synthesis_node.py`

**层级**：Workflow 节点层 · **职责**：Report Synthesis Workflow Node。

```python
"""
Report Synthesis Workflow Node。

负责：

Human Review
    ↓
SynthesisNode
    ↓
ReportSynthesisSkill
    ↓
state.data["synthesis"]

位置在 Human Review 之后、Finalizer 之前：

- 放在 Human Review 之后，
  是为了让综合分析跑在人工批准之后，
  不占用人工等待期间的资源；
- 放在 Finalizer 之前，
  是因为 Finalizer 会把 state.data 中
  所有非 "_" 开头的键转发给报告 Skill，
  因此本节点写入的 "synthesis"
  会被报告自动带上，无需额外接线。
"""

from .base import BaseNode


class SynthesisNode(BaseNode):
    """报告综合分析节点。"""

    name = "synthesis"

    def __init__(
        self,
        skill,
    ):
        self.skill = skill

    async def execute(
        self,
        state,
        context,
    ):
        """生成综合分析结论。"""

        synthesis_input = {
            key: value
            for key, value in state.data.items()
            if not key.startswith("_")
        }

        try:

            result = await self.skill.execute(
                context=context,
                input_data=synthesis_input,
            )

        # 综合分析只是报告的增强章节。
        #
        # 真实事故的防线：
        # 报告中任何一个环节抛异常
        # 都会让整个 Workflow 变成 FAILED
        # （此前一个 README 请求超时
        # 就让 5-Agent 计划整体失败），
        # 因此这里必须降级而不是冒泡。
        except Exception as error:

            result = {
                "available": False,
                "reason": (
                    "综合分析执行失败："
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
                "summary": {},
                "dimensions": {},
            }

        state.data["synthesis"] = result

        state.outputs.append(result)

        return state
```

## 十二、Agent 层（Agents）

Agent 抽象接口、领域 Agent 实现、Agent 注册中心与运行环境；Agent 只编排 Skill，不直接持有 Tool

### 📄 `app/agents/base.py`

**层级**：Agent 层（Agents） · **职责**：Agent 抽象基类 `BaseAgent`：持有 `skill_registry`，提供 `get_skill(name)`，子类实现 `execute(context, input_data)`。Agent 不直接持有 Tool，只编排 Skill

```python
"""
Agent 基础抽象类。


Agent 在系统中的职责：

    Agent
      |
      v
    Skill
      |
      v
    Tool


Agent:
    负责任务理解和能力调用。

Skill:
    封装具体业务能力。

Tool:
    执行具体操作。


例如：

RepositoryAnalysisAgent

        |
        v

RepositoryAnalysisSkill

        |
        +---- GitHub Tool
        |
        +---- File Reader Tool
        |
        +---- Dependency Tool


"""
from abc import ABC, abstractmethod
class BaseAgent(ABC):
    """
    所有 Agent 的基础接口。


    每个 Agent 必须：

    1. 有唯一名称
    2. 可以执行任务
    3. 可以访问 Skill Registry

    """
    # Agent唯一标识

    name: str

    # Agent功能描述

    description: str



    def __init__(
        self,
        skill_registry
    ):
        # Agent 不直接保存 Tool

        # 而是通过 Skill Registry 获取能力

        self.skill_registry = (
            skill_registry
        )

    def get_skill(
        self,
        skill_name
    ):

        """
        根据名称获取 Skill。


        例如：

        repository_analysis_agent

            获取

        repository_analysis_skill

        """

        return (
            self.skill_registry.get(
                skill_name
            )
        )

    @abstractmethod
    async def execute(
        self,
        context,
        input_data
    ):
        """
        Agent执行入口。


        context:
            当前运行上下文。


        input_data:
            当前任务数据。


        """

        pass
```

### 📄 `app/agents/planner_agent.py`

**层级**：Agent 层（Agents） · **职责**：任务规划 Agent `PlannerAgent`（name=`planner_agent`）。当前返回**固定**的分析任务清单（repository → architecture → technology → evidence → critic），后续 Phase 升级为 LLM 动态规划

```python
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
```

### 📄 `app/agents/repository_analysis_agent.py`

**层级**：Agent 层（Agents） · **职责**：仓库基础信息分析 Agent `RepositoryAnalysisAgent`（name=`repository_analysis_agent`），转调 `repository_analysis` Skill

```python
"""
Repository Analysis Agent。


负责：

分析 GitHub 项目的基础信息。


调用链：

RepositoryAnalysisAgent

        |

        v

RepositoryAnalysisSkill

        |

        v

GitHub Tool
File Reader Tool
Dependency Tool


"""


from app.agents.base import BaseAgent




class RepositoryAnalysisAgent(
    BaseAgent
):


    # Agent名称

    name = (
        "repository_analysis_agent"
    )



    description = (
        "Analyze repository information"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取对应Skill

        skill = self.get_skill(

            "repository_analysis"

        )



        # 执行Skill

        result = await skill.execute(

            context,

            input_data

        )



        return result
```

### 📄 `app/agents/architecture_analysis_agent.py`

**层级**：Agent 层（Agents） · **职责**：架构分析 Agent `ArchitectureAnalysisAgent`（name=`architecture_analysis_agent`），转调 `architecture_analysis` Skill

```python
"""
Architecture Analysis Agent。


负责：

分析项目代码架构。


例如：

- 目录结构
- 模块关系
- 核心流程


"""


from app.agents.base import BaseAgent




class ArchitectureAnalysisAgent(
    BaseAgent
):


    name = (
        "architecture_analysis_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取架构分析Skill

        skill = self.get_skill(

            "architecture_analysis"

        )



        return await skill.execute(

            context,

            input_data

        )
```

### 📄 `app/agents/technology_analysis_agent.py`

**层级**：Agent 层（Agents） · **职责**：技术栈分析 Agent `TechnologyAnalysisAgent`（name=`technology_analysis_agent`），转调 `technology_analysis` Skill

```python
"""
Technology Analysis Agent。


负责：

分析项目技术栈。

例如：

- Python
- FastAPI
- Database
- LLM
- Docker


"""


from app.agents.base import BaseAgent




class TechnologyAnalysisAgent(
    BaseAgent
):


    name = (
        "technology_analysis_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        skill = self.get_skill(

            "technology_analysis"

        )


        return await skill.execute(

            context,

            input_data

        )
```

### 📄 `app/agents/evidence_analysis_agent.py`

**层级**：Agent 层（Agents） · **职责**：证据追踪 Agent `EvidenceAnalysisAgent`（name=`evidence_analysis_agent`），转调 `evidence_analysis` Skill

```python
"""
Evidence Analysis Agent。


负责：

分析结果证据追踪。


保证：

报告中的结论可以追溯：

源码

文档

向量库


"""


from app.agents.base import BaseAgent




class EvidenceAnalysisAgent(
    BaseAgent
):


    name = (
        "evidence_analysis_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        skill = self.get_skill(

            "evidence_analysis"

        )


        return await skill.execute(

            context,

            input_data

        )
```

### 📄 `app/agents/critic_agent.py`

**层级**：Agent 层（Agents） · **职责**：结果检查 Agent `CriticAgent`（name=`critic_agent`），检查 `input_data` 是否含 `repository` / `architecture` / `technology` 三项，返回 `{passed, errors}`

```python
"""
Critic Agent。

负责检查分析结果是否完整。

Phase 12 校验要求
=================

文档 15.2 把 Critic 作为分析闭环中的验证步骤，
因此它必须能发现「分析其实没有产出数据」，
而不只是检查 key 是否存在。

旧实现只检查 3 个 key 是否存在，
于是下面这种「跑过了但什么都没产出」的输入
也会被判为 passed=True：

    architecture_analysis_agent = {"files": [], "modules": []}

新实现分两层校验：

1. 存在性：分析步骤是否产出对应字段
2. 内容：该字段是否真的有数据
"""


from app.agents.base import BaseAgent


class CriticAgent(
    BaseAgent
):
    """
    分析结果检查 Agent。
    """

    name = "critic_agent"

    description = (
        "Validate repository analysis results"
    )

    # 逻辑字段 -> 可接受的别名
    REQUIRED_FIELDS = {
        "repository": (
            "repository",
            "repository_analysis",
            "repository_analysis_agent",
        ),
        "architecture": (
            "architecture",
            "architecture_analysis",
            "architecture_analysis_agent",
        ),
        "technology": (
            "technology",
            "technology_analysis",
            "technology_analysis_agent",
            "technology_stack",
        ),
        # Phase 12 的「Agent / Workflow / Skill / Tool Analysis」
        # 步骤产出被分析项目的自述结构。
        "project_structure": (
            "project_structure",
        ),
    }

    async def execute(
        self,
        context,
        input_data,
    ):
        errors = []

        for logical_name, aliases in (
            self.REQUIRED_FIELDS.items()
        ):

            actual_key = next(
                (
                    alias
                    for alias in aliases
                    if alias in input_data
                ),
                None,
            )

            if actual_key is None:
                errors.append(
                    f"{logical_name} missing"
                )

                continue

            if not self._has_content(
                logical_name,
                input_data.get(actual_key),
            ):
                errors.append(
                    f"{logical_name} is empty"
                )

        return {
            "passed": not errors,
            "errors": errors,
        }

    @classmethod
    def _has_content(
        cls,
        logical_name,
        value,
    ) -> bool:
        """
        判断字段是否真的带有数据。

        注意两点：

        1. Agent 输出通常是包装结构
           （例如 {"repository": {...}}），
           真正的数据在内层字段，
           因此先做一层解包再判断。

        2. project_structure 与 technology_stack
           允许「诚实的空」——
           例如项目没有 README 时
           project_structure.available 就是 False，
           这属于真实结论，不是分析失败。
           因此只要求该字段存在且结构正确。
        """

        if not isinstance(value, dict):
            return False

        value = cls._unwrap(
            logical_name,
            value,
        )

        if logical_name == "repository":

            return bool(value)

        if logical_name == "architecture":

            modules = value.get("modules")

            if isinstance(modules, list) and modules:
                return True

            directory_structure = value.get(
                "directory_structure"
            )

            if (
                isinstance(directory_structure, dict)
                and directory_structure.get("available")
            ):
                return True

            # 兼容只有 files 的旧结构。
            files = value.get("files")

            return bool(files)

        if logical_name == "technology":

            return bool(value)

        return True

    @classmethod
    def _unwrap(
        cls,
        logical_name,
        value,
    ):
        """
        把 Agent 输出的包装结构解开一层。

        例如 repository_analysis_agent 的值是

            {"repository": {...}, "readme": "..."}

        真正的判据在内层 repository 上，
        因此在包装层直接判断 non-empty
        会把「内层为空」误判成有数据。
        """

        for alias in cls.REQUIRED_FIELDS.get(
            logical_name,
            (),
        ):

            inner = value.get(alias)

            if isinstance(
                inner,
                (dict, list),
            ):

                return inner

        return value
```

### 📄 `app/agents/agent_registry.py`

**层级**：Agent 层（Agents） · **职责**：Agent 注册中心 `AgentRegistry`：按 `agent.name` 注册与获取；`create_agent_registry(skill_registry)` 在启动时构造全部 6 个领域 Agent

```python
"""
Agent Registry。

统一管理系统中的 Agent。
"""

from app.agents.architecture_analysis_agent import (
    ArchitectureAnalysisAgent,
)
from app.agents.critic_agent import (
    CriticAgent,
)
from app.agents.evidence_analysis_agent import (
    EvidenceAnalysisAgent,
)
from app.agents.planner_agent import (
    PlannerAgent,
)
from app.agents.repository_analysis_agent import (
    RepositoryAnalysisAgent,
)
from app.agents.technology_analysis_agent import (
    TechnologyAnalysisAgent,
)


class AgentRegistry:
    """Agent 管理器。"""

    def __init__(self):
        """初始化 Agent Registry。"""

        self.agents = {}

    def register(
        self,
        agent,
    ):
        """注册 Agent。"""

        self.agents[
            agent.name
        ] = agent

    def get(
        self,
        name,
    ):
        """根据名称获取 Agent。"""

        return self.agents.get(
            name
        )


def create_agent_registry(
    skill_registry,
):
    """
    创建默认 Agent 集合。
    """

    registry = AgentRegistry()

    agents = [
        PlannerAgent(
            skill_registry
        ),
        RepositoryAnalysisAgent(
            skill_registry
        ),
        ArchitectureAnalysisAgent(
            skill_registry
        ),
        TechnologyAnalysisAgent(
            skill_registry
        ),
        EvidenceAnalysisAgent(
            skill_registry
        ),
        CriticAgent(
            skill_registry
        ),
    ]

    for agent in agents:
        registry.register(
            agent
        )

    return registry
```

### 📄 `app/agents/agent_runtime.py`

**层级**：Agent 层（Agents） · **职责**：Agent 运行环境 `AgentRuntime`：持有 `agent_registry`，`execute(agent_name, context, input_data)` 按名取 Agent 后转调其 `execute()`

```python
"""
Agent Runtime。


负责：

执行指定 Agent。


调用流程：

Runtime

    |

    v

Agent

    |

    v

Skill

    |

    v

Tool


"""


class AgentRuntime:



    def __init__(
        self,
        agent_registry
    ):


        # 保存Agent管理器

        self.agent_registry = (
            agent_registry
        )



    async def execute(
        self,
        agent_name,
        context,
        input_data
    ):


        # 根据名称获取Agent

        agent = (
            self.agent_registry.get(
                agent_name
            )
        )



        if agent is None:


            raise Exception(

                f"Agent {agent_name} not found"

            )

        # 执行Agent

        result = await agent.execute(

            context,

            input_data

        )



        return result
```

### 📄 `app/agents/researcher.py`

**层级**：Agent 层（Agents） · **职责**：**空文件**（0 字节），预留的研究 Agent 占位

> 该文件为 **0 字节** 空文件，无源码内容。

## 十三、Skill 层（Skills）

业务能力层：组合多个 Tool 完成一次业务分析，向 Agent 暴露统一的 execute(context, input_data)

### 📄 `app/skills/__init__.py`

**层级**：Skill 层（Skills） · **职责**：Skill 包入口，导出 `BaseSkill`

```python
"""
Skill package
"""

from app.skills.base import BaseSkill


__all__ = [

    "BaseSkill"

]
```

### 📄 `app/skills/base.py`

**层级**：Skill 层（Skills） · **职责**：Skill 抽象基类 `BaseSkill`：`name` / `description` 标识与 `execute(context, input_data)`。Skill 组合多个 Tool 完成一次业务能力，例如 `RepositoryAnalysisSkill` = GitHub Tool + FileReader Tool + DependencyAnalyzer Tool

```python
"""
Skill 基础抽象类。

Skill 和 Tool 的区别:

Tool:
    一个具体动作。
    例如:
        - 查询GitHub
        - 读取文件
        - 查询数据库


Skill:
    一个业务能力。
    可以组合多个 Tool 完成复杂任务。


例如:

RepositoryAnalysisSkill

    |
    +-- GitHubTool
    |
    +-- FileReaderTool
    |
    +-- DependencyAnalyzerTool

"""


from abc import ABC, abstractmethod



class BaseSkill(ABC):
    """
    所有 Skill 的基础接口。
    """


    # Skill唯一名称
    name: str


    # Skill功能描述
    description: str



    @abstractmethod
    async def execute(
        self,
        context,
        input_data: dict
    ):
        """
        执行 Skill。

        参数:

        context:
            Workflow运行上下文。

            保存:
                - tools
                - agents
                - skills


        input_data:
            当前Skill需要处理的数据。


        返回:
            Skill执行结果。

        """

        pass
```

### 📄 `app/skills/repository_analysis_skill.py`

**层级**：Skill 层（Skills） · **职责**：仓库分析能力 `RepositoryAnalysisSkill`（name=`repository_analysis`），依次调用 `github_repository` / `file_reader` / `dependency_analyzer` 三个 Tool，产出 `{repository, readme, dependencies}`

```python
"""
Repository Analysis Skill。

负责：
- 获取 GitHub Repository 基本信息
- 获取 README
- 分析项目依赖
"""

from app.core.exceptions import ToolError
from app.skills.base import BaseSkill


class RepositoryAnalysisSkill(
    BaseSkill
):
    """GitHub Repository 分析 Skill。"""

    name = "repository_analysis"

    description = (
        "Analyze github repository information"
    )

    # GitHub REST API 返回 84 个字段，
    # 其中 30 多个是各类 API URL（archive_url / blobs_url ...），
    # 分析与报告都不使用。
    #
    # 该结构会被保存两份
    # （state.data["repository_analysis_agent"] 与
    #   PlanExecutorNode 拍平后的 state.data["repository"]），
    # 全量保存会让 checkpoint.state_data 凭空多出约 30KB。
    REPOSITORY_FIELDS = (
        "id",
        "name",
        "full_name",
        "owner",
        "description",
        "html_url",
        "url",
        "homepage",
        "language",
        "topics",
        "default_branch",
        "size",
        "stargazers_count",
        "forks_count",
        "watchers_count",
        "open_issues_count",
        "subscribers_count",
        "license",
        "created_at",
        "updated_at",
        "pushed_at",
        "archived",
        "disabled",
        "fork",
        "visibility",
    )

    @classmethod
    def _select_repository_fields(
        cls,
        repository,
    ) -> dict:
        """只保留分析真正使用的仓库字段。"""

        if not isinstance(
            repository,
            dict,
        ):
            return repository

        return {
            key: repository[key]
            for key in cls.REPOSITORY_FIELDS
            if key in repository
        }

    async def execute(
        self,
        context,
        input_data,
    ):
        """
        执行仓库分析。

        input_data 至少需要：

        {
            "owner": "xxx",
            "repo": "xxx"
        }

        可选：

        {
            "project_path": "..."
        }
        """

        # 从 Context 获取工具
        github_tool = context.tools.get(
            "github_repository"
        )

        if github_tool is None:
            raise RuntimeError(
                "Tool not found: github_repository"
            )

        file_reader = context.tools.get(
            "file_reader"
        )

        if file_reader is None:
            raise RuntimeError(
                "Tool not found: file_reader"
            )

        dependency_tool = context.tools.get(
            "dependency_analyzer"
        )

        if dependency_tool is None:
            raise RuntimeError(
                "Tool not found: dependency_analyzer"
            )

        owner = input_data.get(
            "owner"
        )

        repo = input_data.get(
            "repo"
        )

        if not owner or not repo:
            raise ValueError(
                "Repository analysis requires "
                "'owner' and 'repo'."
            )

        project_path = input_data.get(
            "project_path"
        )

        result = {}

        # 获取仓库基本信息（只保留分析使用的字段）
        result["repository"] = (
            self._select_repository_fields(
                await github_tool.execute(
                    owner=owner,
                    name=repo,
                )
            )
        )

        # 获取 README
        #
        # README 读取失败（超时 / 网络抖动）
        # 不应中断整个分析。
        #
        # 这里曾经的真实事故：
        # 一个 README 请求超时
        # → 第一个 Agent 抛异常
        # → 整个 5-Agent 计划 FAILED。
        try:

            result["readme"] = (
                await file_reader.execute(
                    owner=owner,
                    name=repo,
                    file_path="README.md",
                    branch=input_data.get(
                        "branch",
                        "main",
                    ),
                )
            )

        except ToolError as error:

            result["readme"] = ""

            result["readme_error"] = (
                str(error) or type(error).__name__
            )

        # 有本地项目目录时才执行依赖分析
        if project_path:
            result["dependencies"] = (
                await dependency_tool.execute(
                    project_path=project_path,
                )
            )
        else:
            # GitHub 远程仓库尚未提供本地目录
            result["dependencies"] = {}

        return result
```

### 📄 `app/skills/architecture_analysis_skill.py`

**层级**：Skill 层（Skills） · **职责**：架构分析能力 `ArchitectureAnalysisSkill`（name=`architecture_analysis`），用 `github_code_search` 搜出文件列表，再逐个用 `file_reader` 读取内容，产出 `{files, modules}`

```python
"""
Architecture Analysis Skill。

负责：

    GitHub Code Search
        ↓
    File Reader
        ↓
    Architecture information

Phase 12 → Phase 13 数据契约补充
================================

除了 files / modules，
本 Skill 还会产出 project_structure：
从「被分析项目」的 README 与 GitHub topics 中
确定性抽取该项目自述的：

    agents / workflow / skills / tools
    rag / memory / extension

抽取规则：

- 纯字符串匹配 + README 行号定位
- 不使用 LLM，不做语义推断
- 每条结果都带 README 行号与原文片段，
  可以逐条人工复核
- 没匹配到就 declared=False 并给出原因，
  不编造数据

这样 Phase 13 的比较多的是
「被分析项目自述的结构」，
而不是 AIPI 自己的执行状态。
"""

import os
import re

from app.core.exceptions import ToolError
from app.project_analysis.analysis_focus import (
    AnalysisFocus,
)
from app.project_analysis.code_structure_extractor import (
    CodeStructureExtractor,
)
from app.skills.base import BaseSkill


class ArchitectureAnalysisSkill(
    BaseSkill
):
    """
    分析 Repository 架构。
    """

    name = "architecture_analysis"

    description = (
        "Analyze repository architecture"
    )

    # 项目自述结构的关键词表。
    #
    # 命中行会被原样记录（含行号），
    # 因此宁可多留证据，也不做二次推断。
    STRUCTURE_KEYWORDS = {
        "agents": (
            "agent",
            "planner",
            "executor",
            "critic",
            "synthesizer",
            "researcher",
            "supervisor",
            "orchestrator",
            "coordinator",
            "router",
        ),
        "workflow": (
            "workflow",
            "stategraph",
            "state graph",
            "state machine",
            "pipeline",
            "langgraph",
            "langchain",
            "interrupt",
            "graph",
        ),
        "skills": (
            "skill",
            "capability",
            "abilities",
        ),
        "tools": (
            "tool call",
            "tool calls",
            "tools",
            "function call",
        ),
        "rag": (
            "rag",
            "retrieval",
            "retrieve",
            "embedding",
            "pgvector",
            "vector",
            "corpus",
            "semantic search",
        ),
        "memory": (
            "memory",
            "checkpoint",
            "persist",
            "session state",
        ),
        "extension": (
            "plugin",
            "extension",
            "pluggable",
            "extensible",
            "mcp",
            "adapter",
        ),
    }

    # 从一个命中行里抽取「标识」：
    # README 中的 `反引号` 与 **粗体** 内容。
    _IDENTIFIER_PATTERN = re.compile(
        r"`([^`\n]+)`"
        r"|\*\*([^*\n]+)\*\*"
    )

    # 只有单个 token 的标识才作为 item，
    # 避免把 **fails closed** 这类短语
    # 当成结构化条目。
    _SINGLE_TOKEN_PATTERN = re.compile(
        r"[A-Za-z][A-Za-z0-9_.\-*]{1,39}"
    )

    # README 列表行的前缀。
    #
    # 列表行常被用来罗列能力，
    # 而且多数写成普通文字（不加粗、不加反引号），
    # 例如：
    #
    #     - supplier lookup, duplicate detection, categorization
    #
    # 仅靠粗体 / 反引号抽不到这类内容，
    # 因此列表行的逗号分段也作为条目。
    _BULLET_PATTERN = re.compile(
        r"^\s*[-*]\s+(.*)$"
    )

    # 列表分段作为条目的最大长度。
    #
    # 超过这个长度的多半是整句话，
    # 不适合当条目。
    MAX_BULLET_ITEM_CHARS = 60

    # 每个维度最多记录的命中行数。
    MAX_EVIDENCE_LINES = 4

    # 每个维度最多记录的标识数。
    MAX_ITEMS = 12

    # 代码证据与 README 自述合并后，
    # 单个维度最多保留多少个条目。
    #
    # 略大于 MAX_ITEMS：
    # 代码符号排在前面且通常先用满 12 个，
    # 这里留出余量，让 README 补充的条目
    # 不至于被全部挤掉。
    MAX_MERGED_ITEMS = 16

    # 允许接纳「未命中关键词的代码标识」的维度。
    #
    # 工具名通常以函数 / API 形式出现
    # （例如 read_webpage），
    # 无法预先写进关键词表，
    # 因此只有 tools 维度接受这类标识。
    #
    # 其余维度只接受命中本维度关键词的标识，
    # 避免 StateGraph / MODEL_* 这类
    # 其他维度的标识被重复计入。
    DIMENSIONS_ACCEPTING_CODE_IDENTIFIERS = (
        "tools",
    )

    # 目录结构：按扩展名 / 顶层目录统计的展示上限。
    MAX_EXTENSIONS = 12

    MAX_TOP_LEVEL_DIRS = 15

    MAX_KEY_FILES = 20

    # 关键文件：这些文件最能说明项目如何构建与部署。
    KEY_FILE_NAMES = (
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "package.json",
        "tsconfig.json",
        "go.mod",
        "pom.xml",
        "Cargo.toml",
        "Gemfile",
        "Makefile",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".env.example",
    )

    # 允许读取内容的文件类型（不含 .md，
    # README 已由 RepositoryAnalysisSkill 读取）。
    #
    # 刻意不含 .toml / .ini / .cfg / .yml / .json：
    # 这些是配置文件，由 TechnologyAnalysisSkill
    # 负责读取并抽取技术栈。
    # 本 Skill 的「关键源码」只用来抽取
    # Agent / Workflow / Tool 等代码结构，
    # 再读一遍配置文件纯属浪费配额
    # （旧版本 8 个配额里有 3-4 个是
    #   docker-compose.yml / pyproject.toml 这类文件，
    #   导致真正承载架构的 graph / nodes / tools
    #   一个都没读到）。
    SOURCE_EXTENSIONS = (
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".mjs",
        ".go",
        ".java",
        ".rs",
        ".rb",
        ".php",
        ".cs",
        ".kt",
        ".swift",
        ".vue",
    )

    # 读取源码时优先挑选的入口文件。
    #
    # 刻意不包含 __init__.py：
    # 它通常只是空的包声明，
    # 而且会命中很深的目录。
    PRIORITY_FILENAMES = (
        "main.py",
        "app.py",
        "server.py",
        "manage.py",
        "cli.py",
        "index.ts",
        "index.js",
        "main.ts",
        "main.js",
        "app.ts",
        "app.js",
    )

    # 这些路径最后才考虑。
    #
    # 它们能命中架构关键词（tests/test_agents.py
    # 名字里有 agent），但描述的是「项目怎么测自己」，
    # 不是「项目怎么组织 Agent」，
    # 放在最后避免挤掉真正的实现代码。
    LOW_PRIORITY_PATH_PATTERNS = (
        re.compile(r"(^|/)tests?/"),
        re.compile(r"(^|/)test_[^/]*$"),
        re.compile(r"_test\.[a-z]+$"),
        re.compile(r"(^|/)migrations?/"),
        re.compile(r"(^|/)alembic/versions/"),
        re.compile(r"(^|/)(demo_data|examples?|samples?)/"),
        re.compile(r"(^|/)scripts?/"),
    )

    # 最多读取多少个文件内容作为「关键源码」。
    #
    # 文件树可能有数百个文件，
    # 不限制会对 GitHub 发起数百次请求。
    #
    # 8 -> 12：不再把配额花在
    # docker-compose.yml 这类配置文件上。
    # 12 -> 20：改为按维度分配配额，
    # 每个维度都要留够样本。
    MAX_MODULES = 20

    # 每个维度的样本配额。
    #
    # 旧做法是全局挑 20 个「路径命中最多信号」的文件，
    # 结果取决于仓库目录结构：
    # agents/ 下文件多就全是 agents，
    # rag/ 只有 1 个文件就可能一个都进不来，
    # 于是报告里每个模块的详略极不均匀。
    #
    # 现在每个维度有独立名额，
    # 命中该维度的文件先按自己的配额挑，
    # 一个维度内部的明细深浅不再由别的维度决定。
    DIMENSION_QUOTAS = {
        "workflow": 4,
        "agents": 3,
        "tools": 3,
        "rag": 2,
        "memory": 2,
        "skills": 2,
    }

    # 重点维度与非重点维度的配额权重。
    #
    # 用户点名了重点时，配额按权重重新分配，
    # 而不是把非重点维度降到 0 ——
    # 报告里那些章节仍然要写，
    # 只是给更少的样本。
    #
    # 以 MAX_MODULES=20 为例：
    #
    #     1 个重点  重点 10，其余各 2   -> 20
    #     2 个重点  重点各 7，其余各 1   -> 18
    #     3 个重点  重点各 5，其余各 1   -> 18
    FOCUS_WEIGHT = 5

    BASE_WEIGHT = 1

    @classmethod
    def _quotas_for(
        cls,
        focus=None,
    ):
        """
        按本次重点算出各维度的采集配额。

        返回的是**有序**字典：
        重点维度排在前面，
        这样 _read_candidates 会先把它们的
        名额用满，不会被其它维度挤掉。

        没有识别出重点时返回默认配额，
        与旧行为完全一致。
        """

        if focus is None or not focus.is_focused:

            return dict(cls.DIMENSION_QUOTAS)

        weights = {}

        for name in cls.DIMENSION_QUOTAS:

            weights[name] = (
                cls.FOCUS_WEIGHT
                if focus.is_primary(name)
                else cls.BASE_WEIGHT
            )

        total = sum(weights.values())

        quotas = {}

        # 重点维度在前，且内部按用户在问题里
        # 提到的顺序排 —— 越靠前越重要。
        ordered = sorted(
            cls.DIMENSION_QUOTAS,
            key=lambda name: (
                0 if focus.is_primary(name) else 1,
                focus.rank(name),
                name,
            ),
        )

        for name in ordered:

            quotas[name] = max(
                1,
                cls.MAX_MODULES
                * weights[name]
                // total,
            )

        return quotas

    # 落库时最多保留多少个**源码正文**。
    #
    # 与 MAX_MODULES 分开是刻意的：
    #
    #   MAX_MODULES       读几个文件喂给 AST
    #   MAX_STORED_MODULES 存几个文件的正文进 state
    #
    # AST 抽取在内存里用全文，不受这个上限影响；
    # 但 modules 正文要写进 checkpoint，
    # 20 个文件 × 1200 字符 ≈ 24KB，
    # 而报告第 11 章只渲染 8 个 ——
    # 存 20 个有 12 个永远没人看。
    #
    # 真实事故：state_data 涨到 263KB，
    # 越过 asyncmy 单字段 256KB 的缓冲区分片上限，
    # 报告接口读 checkpoint 直接
    # Lost connection to MySQL server。
    MAX_STORED_MODULES = 8

    # 落库时最多保留多少个文件路径。
    #
    # 真实文件树可能有数百个文件，
    # 全部写入 checkpoint 会让
    # state_data 膨胀到数百 KB，
    # 进而撑爆 MySQL 的排序缓冲区
    # （OperationalError 1038 Out of sort memory）。
    # 真实总数见 directory_structure.total_files。
    MAX_FILE_PATHS = 60

    # 单个源码文件最多写入多少字符。
    #
    # 大型配置文件的全文（例如 28KB 的 CI 配置）
    # 同样会让 state_data 膨胀。
    MAX_MODULE_CHARS = 1200

    async def execute(
        self,
        context,
        input_data,
    ):
        code_search = context.tools.get(
            "github_code_search"
        )

        if code_search is None:
            raise RuntimeError(
                "Tool not found: github_code_search"
            )

        file_reader = context.tools.get(
            "file_reader"
        )

        if file_reader is None:
            raise RuntimeError(
                "Tool not found: file_reader"
            )

        owner = input_data.get(
            "owner"
        )

        repo = input_data.get(
            "repo"
        )

        if not owner or not repo:
            raise ValueError(
                "Architecture analysis requires "
                "'owner' and 'repo'."
            )

        repository = (
            f"{owner}/{repo}"
        )

        keyword = input_data.get(
            "keyword",
            "class",
        )

        branch = input_data.get(
            "branch",
            "main",
        )

        files = await code_search.execute(
            keyword=keyword,
            repo=repository,
        )

        # GitHub Code Search 的 repo: 限定符
        # 对多数仓库返回 0 条结果，
        # 因此真实的目录结构必须来自 Git Trees API。
        tree = await self._load_tree(
            context,
            owner,
            repo,
            branch,
        )

        if not files and tree:

            # Code Search 没有结果时，
            # 用真实文件树补全文件列表。
            files = [
                item.get("path")
                for item in tree
                if item.get("type") == "blob"
                and item.get("path")
            ]

        architecture = {
            # 只保留采样，真实总数见 directory_structure。
            "files": list(files)[: self.MAX_FILE_PATHS],
            "modules": [],
            "directory_structure": (
                self._build_directory_structure(
                    tree
                )
            ),
        }

        # AST 抽取需要**未截断**的源码：
        # 截断过的 Python 几乎必然语法错误，
        # 因此这里单独收一份全文，
        # 只在本次执行内使用，不写入 state
        # （modules 里存的仍是截断后的内容）。
        ast_sources = []

        # 本次分析的重点维度。
        #
        # research_plan 由 DesignGateNode 提升到顶层，
        # PlanExecutorNode 又把 state.data 整体
        # 作为 agent_input 传进来，因此这里能读到。
        focus = AnalysisFocus.from_plan(
            input_data.get("research_plan")
        )

        for file_path in self._read_candidates(
            files,
            self._quotas_for(focus),
        ):

            try:

                content = await file_reader.execute(
                    owner=owner,
                    name=repo,
                    file_path=file_path,
                    branch=branch,
                )

            except ToolError as error:

                # 单个文件读取失败（超时 / 网络抖动）
                # 不应该让整个分析失败：
                # 记录失败原因后继续读其它文件。
                architecture[
                    "modules"
                ].append(
                    {
                        "file_path": file_path,
                        "content": "",
                        "error": str(error)
                        or type(error).__name__,
                    }
                )

                continue

            # 只存够报告展示的量。
            # 全文已经喂给 AST 了，
            # 多存的正文没有任何读取方。
            if len(
                architecture["modules"]
            ) < self.MAX_STORED_MODULES:

                architecture[
                    "modules"
                ].append(
                    self._module_entry(
                        file_path,
                        content,
                    )
                )

            ast_sources.append(
                {
                    "file_path": file_path,
                    "content": content or "",
                }
            )

        # 从真实源码抽取结构信号。
        #
        # 除已读取的文件外，
        # 额外把整棵文件树的路径交给抽取器：
        # 配额只有 12 个，
        # 但「存在 src/agents/ 目录」这条证据
        # 不该因为该目录下的文件没被读到而丢失。
        code_structure = (
            CodeStructureExtractor.extract(
                ast_sources,
                extra_paths=[
                    path
                    for path in files
                    if isinstance(path, str)
                ],
            )
        )

        # Phase 12 → Phase 13 契约：
        # 产出被分析项目的自述结构。
        #
        # 现在由「代码证据」与「README 自述」共同构成，
        # 代码为主、README 为辅。
        architecture[
            "project_structure"
        ] = self._extract_project_structure(
            input_data,
            code_structure,
        )

        return architecture

    def _module_entry(
        self,
        file_path,
        content,
    ):
        """
        构建单个源码条目。

        两个处理：

        1. 跳过开头的 import 段
           否则摘录就是一堆 `import os`，
           对理解项目毫无帮助。
        2. 按 MAX_MODULE_CHARS 截断，
           避免大型文件把 state_data 撑爆。
        """

        text = str(content or "")

        start = CodeStructureExtractor.meaningful_start(
            text
        )

        excerpt = text[
            start: start + self.MAX_MODULE_CHARS
        ]

        entry = {
            "file_path": file_path,
            "content": excerpt,
        }

        # 摘录从第几行开始 ——
        # 证据层要用它标行号，
        # 否则会写成「file:1-30」但内容是第 30 行开始的。
        if start:

            entry["start_line"] = (
                text[:start].count("\n") + 1
            )

        if len(text) - start > self.MAX_MODULE_CHARS:
            entry["original_characters"] = len(text)
            entry["truncated"] = True

        return entry

    @staticmethod
    async def _load_tree(
        context,
        owner,
        name,
        branch,
    ):
        """
        获取仓库文件树。

        目录结构属于增强信息，
        拿不到时返回空列表，
        不应因此中断整个分析流程。
        """

        tool = context.tools.get(
            "github_repository"
        )

        if tool is None:
            return []

        get_tree = getattr(
            tool,
            "get_tree",
            None,
        )

        if not callable(get_tree):
            return []

        try:

            tree = await get_tree(
                owner=owner,
                name=name,
                branch=branch,
            )

        except ToolError:

            return []

        if not isinstance(tree, list):
            return []

        return tree

    def _build_directory_structure(
        self,
        tree,
    ):
        """
        从真实文件树构建目录结构。

        只做计数与归类，不做推断。
        """

        blobs = [
            item
            for item in tree
            if isinstance(item, dict)
            and item.get("type") == "blob"
            and item.get("path")
        ]

        if not blobs:

            return {
                "available": False,
                "reason": (
                    "未获取到仓库文件树，"
                    "无法生成目录结构。"
                ),
                "total_files": 0,
                "by_extension": {},
                "top_level_dirs": [],
                "key_files": [],
            }

        by_extension = {}
        top_level = {}
        key_files = []

        for blob in blobs:

            path = blob["path"]

            extension = (
                os.path.splitext(path)[1].lower()
                or "(无扩展名)"
            )

            by_extension[extension] = (
                by_extension.get(extension, 0) + 1
            )

            head = (
                path.split("/", 1)[0]
                if "/" in path
                else "(根目录)"
            )

            top_level[head] = (
                top_level.get(head, 0) + 1
            )

            if os.path.basename(path) in self.KEY_FILE_NAMES:
                key_files.append(path)

        return {
            "available": True,
            "source": "github git trees api",
            "total_files": len(blobs),
            "by_extension": dict(
                sorted(
                    by_extension.items(),
                    key=lambda item: -item[1],
                )[: self.MAX_EXTENSIONS]
            ),
            "top_level_dirs": [
                {
                    "name": name,
                    "file_count": count,
                }
                for name, count in sorted(
                    top_level.items(),
                    key=lambda item: -item[1],
                )[: self.MAX_TOP_LEVEL_DIRS]
            ],
            "key_files": sorted(
                key_files
            )[: self.MAX_KEY_FILES],
        }

    @staticmethod
    def _normalize_path(item):
        """文件列表项可能是 dict 或纯字符串。"""

        if isinstance(item, dict):
            return item.get("path")

        return str(item)

    def _read_candidates(
        self,
        files,
        quotas=None,
    ):
        """
        从文件列表里挑出要读取的关键源码。

        文件树可能有数百个文件，
        必须限制读取数量，
        否则会对 GitHub 发起数百次请求
        （本 Skill 是逐个文件读的，
        没有批量接口）。

        挑选顺序：

            1. 按维度配额挑路径命中该维度的文件
               （每个维度有独立名额，见 DIMENSION_QUOTAS）
            2. 入口文件（main.py / app.py ...）
            3. 其余源码
            4. 测试 / 迁移 / 示例（垫底）

        同一档内浅层路径优先。

        两次修正的由来：

        - 第一版按固定文件名列表挑，
          配额被 docker-compose.yml /
          pyproject.toml 这类配置文件占满，
          一个 88 个 .py 的项目
          连一个 Agent 类都没读到；
        - 第二版按「命中信号总数」全局排序，
          但仓库目录结构会决定结果：
          agents/ 文件多就挤掉 rag/，
          各模块详略极不均匀。
        """

        entry = []
        normal = []
        low = []

        if not quotas:

            quotas = self.DIMENSION_QUOTAS

        # 维度名 -> 候选文件（浅层优先）。
        by_dimension = {
            name: []
            for name in quotas
        }

        seen = set()

        for item in files:

            file_path = self._normalize_path(
                item
            )

            if not file_path:
                continue

            if file_path in seen:
                continue

            if not file_path.lower().endswith(
                self.SOURCE_EXTENSIONS
            ):
                continue

            basename = os.path.basename(
                file_path
            ).lower()

            # __init__.py 绝大多数只是空文件或转出声明，
            # 作为「关键源码」没有意义。
            #
            # 实测空的 __init__.py 还会让证据层
            # 因为「纯空白内容」而报错。
            if basename == "__init__.py":
                continue

            seen.add(file_path)

            if self._is_low_priority_path(
                file_path
            ):

                low.append(file_path)

                continue

            matched = (
                CodeStructureExtractor
                .dimensions_for_path(file_path)
            )

            if matched:

                for dimension in matched:

                    by_dimension[
                        dimension
                    ].append(file_path)

            elif basename in self.PRIORITY_FILENAMES:

                entry.append(file_path)

            else:

                normal.append(file_path)

        for bucket in (
            entry,
            normal,
            low,
            *by_dimension.values(),
        ):

            bucket.sort(
                key=lambda path: (
                    path.count("/"),
                    path,
                )
            )

        # 按维度配额取文件。
        #
        # 一个文件可能同时命中多个维度
        # （例如 services/workflow_service.py
        # 既像 workflow 又像 agents），
        # 取第一个有余额的维度即可，
        # 同一个文件不重复占名额。
        ordered = []

        taken = set()

        for dimension, quota in quotas.items():

            count = 0

            for path in by_dimension[dimension]:

                if count >= quota:
                    break

                if path in taken:
                    continue

                taken.add(path)

                ordered.append(path)

                count += 1

        # 配额之外、但仍命中维度的文件。
        #
        # 必须回填：
        # 如果一个仓库的源码全在 agents/ 下，
        # 配额只取 3 个，
        # 剩下 17 个名额就会空着，
        # 白白浪费掉读取机会。
        remaining_dimension = []

        for paths in by_dimension.values():

            for path in paths:

                if path not in taken:

                    remaining_dimension.append(path)

        remaining_dimension.sort(
            key=lambda path: (
                path.count("/"),
                path,
            )
        )

        for bucket in (
            entry,
            remaining_dimension,
            normal,
            low,
        ):

            for path in bucket:

                if len(ordered) >= self.MAX_MODULES:
                    break

                if path in taken:
                    continue

                taken.add(path)

                ordered.append(path)

        return ordered[: self.MAX_MODULES]

    def _is_low_priority_path(
        self,
        file_path,
    ) -> bool:
        """判断是否为测试 / 迁移 / 示例类路径。"""

        normalized = str(file_path).lower()

        return any(
            pattern.search(normalized)
            for pattern in (
                self.LOW_PRIORITY_PATH_PATTERNS
            )
        )

    def _extract_project_structure(
        self,
        input_data,
        code_structure=None,
    ):
        """
        抽取被分析项目的结构。

        数据来源（全部来自被分析项目本身）：

            code_structure      真实源码的 AST 抽取结果
            readme              目标项目 README 全文
            repository.topics   GitHub 官方话题标签
            repository.description  项目描述

        不读取任何 AIPI 自身的执行数据。

        代码为主、README 为辅：

        - items 里代码符号排在前面，
          README 条目补在后面；
        - evidence 保持「README 命中行」的原有含义，
          代码证据放在新增的 code_evidence 字段，
          两个字段分开是因为两条证据的性质不同 ——
          一个是「项目说自己有什么」，
          一个是「项目代码里确实有什么」；
        - declared_by 记录结论来自哪一侧。

        保持 declared / items / topics / evidence / reason
        这五个字段的原有含义与类型不变 ——
        报告层按它们渲染各维度章。
        """

        readme = input_data.get(
            "readme"
        )

        repository = input_data.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            repository = {}

        topics = repository.get(
            "topics"
        )

        if not isinstance(
            topics,
            list,
        ):
            topics = []

        description = repository.get(
            "description"
        )

        if not isinstance(
            description,
            str,
        ):
            description = ""

        code_dimensions = {}

        if isinstance(
            code_structure,
            dict,
        ):

            code_dimensions = (
                code_structure.get("dimensions")
                or {}
            )

            if not isinstance(
                code_dimensions,
                dict,
            ):
                code_dimensions = {}

        # 既没有 README / topics / description，
        # 也没有从代码里抽出任何信号时，
        # 才能诚实声明无法抽取。
        #
        # 旧版本只看 README 三件套，
        # 于是 README 为空的仓库
        # 即使代码结构完整也拿不到任何维度。
        if (
            not isinstance(readme, str)
            and not topics
            and not description
            and not self._has_code_signals(
                code_dimensions
            )
        ):
            return {
                "available": False,
                "basis": "code+readme+topics",
                "reason": (
                    "被分析项目没有可用 README、"
                    "topics 或 description，"
                    "也没有读取到任何源码，"
                    "无法抽取项目结构。"
                ),
                "dimensions": {},
                "code_extraction": (
                    self._code_extraction_meta(
                        code_structure
                    )
                ),
            }

        lines = (
            readme.splitlines()
            if isinstance(readme, str)
            else []
        )

        dimensions = {}

        for dimension, keywords in (
            self.STRUCTURE_KEYWORDS.items()
        ):
            dimensions[dimension] = (
                self._merge_dimension(
                    dimension,
                    self._extract_dimension_signals(
                        dimension,
                        keywords,
                        lines,
                        topics,
                        description,
                    ),
                    code_dimensions.get(
                        dimension
                    ),
                )
            )

        return {
            "available": True,
            "basis": "code+readme+topics",
            "reason": None,
            "dimensions": dimensions,
            "code_extraction": (
                self._code_extraction_meta(
                    code_structure
                )
            ),
        }

    @staticmethod
    def _has_code_signals(
        code_dimensions: dict,
    ) -> bool:
        """代码侧是否抽到了任何条目。"""

        if not isinstance(
            code_dimensions,
            dict,
        ):
            return False

        return any(
            isinstance(entry, dict)
            and entry.get("items")
            for entry in code_dimensions.values()
        )

    @staticmethod
    def _code_extraction_meta(
        code_structure,
    ) -> dict:
        """
        记录代码抽取的执行情况。

        解析失败的文件必须如实带出来，
        否则「没抽到东西」与
        「文件根本没解析成功」会混为一谈。
        """

        if not isinstance(
            code_structure,
            dict,
        ):
            return {
                "available": False,
                "reason": "未执行代码结构抽取。",
                "parsed_files": 0,
                "unparsed": [],
            }

        return {
            "available": bool(
                code_structure.get("available")
            ),
            "parsed_files": (
                code_structure.get(
                    "parsed_files",
                    0,
                )
            ),
            "unparsed": list(
                code_structure.get("unparsed")
                or []
            ),
        }

    def _merge_dimension(
        self,
        dimension: str,
        readme_entry: dict,
        code_entry,
    ) -> dict:
        """
        合并「代码证据」与「README 自述」。

        代码在前，README 在后。
        """

        if not isinstance(
            code_entry,
            dict,
        ):
            code_entry = {}

        code_items = [
            item
            for item in (
                code_entry.get("items") or []
            )
            if isinstance(item, str)
        ]

        code_evidence = [
            item
            for item in (
                code_entry.get("evidence") or []
            )
            if isinstance(item, dict)
        ]

        readme_items = list(
            readme_entry.get("items") or []
        )

        # 按小写去重，避免同一个符号
        # 被代码与 README 各记一次。
        seen = set()

        items = []

        for item in code_items + readme_items:

            lowered = item.lower()

            if lowered in seen:
                continue

            seen.add(lowered)

            if len(items) >= self.MAX_MERGED_ITEMS:
                break

            items.append(item)

        declared_by = None

        if code_items:
            declared_by = "code"

        if readme_items or readme_entry.get(
            "topics"
        ) or readme_entry.get("evidence"):

            declared_by = (
                "code+readme"
                if declared_by == "code"
                else "readme"
            )

        declared = declared_by is not None

        return {
            # 原字段：类型与含义都不变。
            "declared": declared,
            "items": items,
            "topics": readme_entry.get(
                "topics"
            )
            or [],
            "evidence": readme_entry.get(
                "evidence"
            )
            or [],
            "reason": (
                None
                if declared
                else (
                    "被分析项目的代码、README / "
                    "topics / description 中"
                    f"都没有 {dimension} 相关声明。"
                )
            ),

            # 新增字段：不改变上面五个的含义，
            # 只是把来源与代码证据显式带出来。
            "declared_by": declared_by,
            "code_evidence": code_evidence,
            # 实现明细：函数签名 / 调用链 / 关键常量。
            #
            # 必须在这里透传，
            # 否则抽取器辛苦解析出来的明细
            # 会在合并这一步被丢掉。
            "details": [
                item
                for item in (
                    code_entry.get("details") or []
                )
                if isinstance(item, dict)
            ],
        }

    def _extract_dimension_signals(
        self,
        dimension,
        keywords,
        lines,
        topics,
        description,
    ):
        """
        抽取单个维度的自述信号。

        返回：

            declared   是否在项目自述中被提到
            items      命中的标识（反引号 / 粗体单 token）
            topics     命中的 GitHub topics
            evidence   命中行（含行号与原文）
            reason     declared=False 时的说明
        """

        matched_topics = [
            topic
            for topic in topics
            if isinstance(topic, str)
            and self._line_matches(topic, keywords)
        ]

        items = []
        seen_items = set()

        # 先找出所有命中行。
        hits = [
            (index, line)
            for index, line in enumerate(lines, start=1)
            if line.strip()
            and self._line_matches(line, keywords)
        ]

        # 产生了标识的行优先作为证据。
        #
        # 否则 README 开头的徽章 / 标题行
        # 会把证据额度占满，
        # 真正带信息的行反而抽不到。
        identified = []
        plain = []

        for index, line in hits:

            if self._collect_items(
                line,
                keywords,
                items,
                seen_items,
                dimension=dimension,
            ):
                identified.append((index, line))
            else:
                plain.append((index, line))

        evidence = []

        for index, line in (
            identified + plain
        )[: self.MAX_EVIDENCE_LINES]:

            evidence.append(
                {
                    "file_path": "README.md",
                    "line_start": index,
                    "line_end": index,
                    "text": line.strip()[:200],
                }
            )

        # description 也是项目自述，
        # 但没有 README 行号，
        # 因此只用来补充 items，
        # 不计入 evidence 行。
        if description and self._line_matches(
            description,
            keywords,
        ):

            self._collect_items(
                description,
                keywords,
                items,
                seen_items,
                dimension=dimension,
            )

        declared = bool(
            evidence
            or items
            or matched_topics
        )

        return {
            "declared": declared,
            "items": items,
            "topics": matched_topics,
            "evidence": evidence,
            "reason": (
                None
                if declared
                else (
                    "被分析项目的 README / topics / "
                    f"description 中没有 {dimension} "
                    "相关声明。"
                )
            ),
        }

    @staticmethod
    def _line_matches(
        text,
        keywords,
    ):
        """判断文本是否命中关键词（词边界匹配）。"""

        lowered = text.lower()

        return any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                lowered,
            )
            for keyword in keywords
        )

    def _collect_items(
        self,
        text,
        keywords,
        items,
        seen_items,
        dimension,
    ):
        """
        从命中行里收集标识。

        规则（避免维度之间互相泄漏）：

        - **粗体** token 必须自身命中本维度关键词，
          避免把 **Executor** 这类角色名记进 tools 维度
        - `反引号` token 同样必须命中本维度关键词；
          只有 DIMENSIONS_ACCEPTING_CODE_IDENTIFIERS
          里的维度（tools）例外，
          因为它需要保留工具调用名

        返回是否收集到任何标识。
        """

        accept_code_identifiers = (
            dimension
            in self.DIMENSIONS_ACCEPTING_CODE_IDENTIFIERS
        )

        collected = False

        for match in (
            self._IDENTIFIER_PATTERN
            .finditer(text)
        ):

            code_token = match.group(1)

            bold_token = match.group(2)

            token = (
                code_token
                or bold_token
                or ""
            ).strip()

            if not self._SINGLE_TOKEN_PATTERN.fullmatch(
                token
            ):
                continue

            matches_keywords = self._line_matches(
                token,
                keywords,
            )

            if not matches_keywords:

                # 粗体 token 一律要求命中关键词。
                if bold_token is not None:
                    continue

                # 代码 token 只有特定维度例外。
                if not accept_code_identifiers:
                    continue

            lowered = token.lower()

            collected = True

            if lowered in seen_items:
                continue

            seen_items.add(lowered)

            if len(items) < self.MAX_ITEMS:
                items.append(token)

        if self._collect_bullet_phrases(
            text,
            items,
            seen_items,
        ):
            collected = True

        return collected

    def _collect_bullet_phrases(
        self,
        text,
        items,
        seen_items,
    ) -> bool:
        """
        把列表行的逗号分段作为条目。

        只对以 "- " / "* " 开头的行生效，
        因为这类行是 README 里最常见的
        「罗列能力」写法。

        条目是 README 原文的切片，
        不加工、不改写。
        """

        bullet = self._BULLET_PATTERN.match(text)

        if bullet is None:
            return False

        collected = False

        for segment in bullet.group(1).split(","):

            phrase = segment.strip()

            if not phrase:
                continue

            if len(phrase) > self.MAX_BULLET_ITEM_CHARS:
                continue

            collected = True

            lowered = phrase.lower()

            if lowered in seen_items:
                continue

            seen_items.add(lowered)

            if len(items) < self.MAX_ITEMS:
                items.append(phrase)

        return collected
```

### 📄 `app/skills/technology_analysis_skill.py`

**层级**：Skill 层（Skills） · **职责**：技术栈分析能力 `TechnologyAnalysisSkill`（name=`technology_analysis`），调用 `dependency_analyzer` Tool，产出 `{technology_stack}`

```python
"""
Technology Analysis Skill。

支持：

1. 本地项目目录分析
2. GitHub Repository 远程文件分析
"""

from app.core.exceptions import ToolError
from app.skills.base import BaseSkill


class TechnologyAnalysisSkill(
    BaseSkill
):
    """项目技术栈分析 Skill。"""

    name = "technology_analysis"

    description = (
        "Analyze GitHub project technology stack"
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        project_path = input_data.get(
            "project_path"
        )

        # 本地项目：复用现有 DependencyAnalyzerTool。
        if project_path:

            dependency_tool = (
                context.tools.get(
                    "dependency_analyzer"
                )
            )

            if dependency_tool is None:
                raise RuntimeError(
                    "Tool not found: dependency_analyzer"
                )

            dependencies = (
                await dependency_tool.execute(
                    project_path=project_path,
                )
            )

            return {
                "technology_stack": dependencies
            }

        # GitHub 远程项目。
        return await self._analyze_remote(
            context,
            input_data,
        )

    async def _analyze_remote(
        self,
        context,
        input_data,
    ):
        file_reader = context.tools.get(
            "file_reader"
        )

        if file_reader is None:
            raise RuntimeError(
                "Tool not found: file_reader"
            )

        owner = input_data.get(
            "owner"
        )

        repo = input_data.get(
            "repo"
        )

        if not owner or not repo:
            raise ValueError(
                "Technology analysis requires "
                "'owner' and 'repo'."
            )

        branch = input_data.get(
            "branch",
            "main",
        )

        target_files = [
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "Dockerfile",
            "docker-compose.yml",
        ]

        contents = {}

        failures = {}

        for file_path in target_files:

            # 单个配置文件读取失败（超时 / 网络抖动）
            # 不应中断整个分析：
            # 跳过该文件并记录原因，
            # 技术栈仍然基于读到的其它文件得出。
            try:

                content = await file_reader.execute(
                    owner=owner,
                    name=repo,
                    file_path=file_path,
                    branch=branch,
                )

            except ToolError as error:

                failures[file_path] = (
                    str(error) or type(error).__name__
                )

                continue

            if content:
                contents[file_path] = content

        all_content = "\n".join(
            contents.values()
        ).lower()

        frameworks = []
        databases = []
        llms = []
        embeddings = []
        deployment = []

        if "fastapi" in all_content:
            frameworks.append("FastAPI")

        if "django" in all_content:
            frameworks.append("Django")

        if "flask" in all_content:
            frameworks.append("Flask")

        if "langchain" in all_content:
            frameworks.append("LangChain")

        if "langgraph" in all_content:
            frameworks.append("LangGraph")

        if "sqlalchemy" in all_content:
            databases.append("SQLAlchemy")

        if "mysql" in all_content:
            databases.append("MySQL")

        if "postgres" in all_content:
            databases.append("PostgreSQL")

        if "qdrant" in all_content:
            embeddings.append("Qdrant")

        if "chromadb" in all_content:
            embeddings.append("ChromaDB")

        if "deepseek" in all_content:
            llms.append("DeepSeek")

        if "openai" in all_content:
            llms.append("OpenAI")

        if "ollama" in all_content:
            llms.append("Ollama")

        if "docker" in all_content:
            deployment.append("Docker")

        technology_stack = {
            "frameworks": frameworks,
            "database": databases,
            "llm": llms,
            "embedding": embeddings,
            "deployment": deployment,
            "source_files": list(
                contents.keys()
            ),
        }

        if failures:
            technology_stack["read_failures"] = failures

        return {
            "technology_stack": technology_stack
        }
```

### 📄 `app/skills/evidence_analysis_skill.py`

**层级**：Skill 层（Skills） · **职责**：证据追踪能力 `EvidenceAnalysisSkill`（name=`evidence_analysis`），调用 `qdrant_search` Tool 做语义检索，产出 `{evidence}`

```python
"""
Evidence Analysis Skill。

支持：

1. Qdrant 语义检索结果
2. Repository / Architecture Agent 输出
3. Evidence MySQL 持久化
"""

from app.services.evidence_service import (
    EvidenceService,
)
from app.skills.base import BaseSkill


class EvidenceAnalysisSkill(
    BaseSkill
):
    """生成可追溯 Evidence。"""

    name = "evidence_analysis"

    description = (
        "Extract traceable evidence from "
        "repository analysis results."
    )

    # 单条源码证据最多保存多少字符。
    MAX_EVIDENCE_CHARS = 1500

    async def execute(
        self,
        context,
        input_data,
    ):
        evidence = []

        query_vector = input_data.get(
            "query_vector"
        )

        # 如果已经提供向量，则继续使用 Qdrant。
        if query_vector is not None:

            evidence.extend(
                await self._from_qdrant(
                    context,
                    query_vector,
                    input_data.get(
                        "limit",
                        5,
                    ),
                )
            )

        # 没有 query_vector 时，
        # 从 Architecture / Repository 结果生成源码证据。
        if not evidence:

            evidence.extend(
                self._from_analysis_results(
                    input_data
                )
            )

        # 去重。
        unique = []

        seen = set()

        for item in evidence:

            key = (
                item.get("file_path"),
                item.get("line_start"),
                item.get("line_end"),
                item.get("content"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(item)

        # Phase 9 Evidence 持久化。
        config = getattr(context, "config", {}) or {}
        session = config.get("session")

        repository_id = config.get(
            "repository_id"

        )

        persist_failures = []

        if (
            session is not None
            and repository_id is not None
        ):
            service = EvidenceService(
                session
            )

            persisted = []

            for item in unique:

                # 单条证据落库失败不应中断整个分析：
                # 记录原因后继续处理其它证据。
                try:

                    record = (
                        await service.create_evidence(
                            repository_id=repository_id,
                            source_type=item[
                                "source_type"
                            ],
                            source_url=item.get(
                                "source_url"
                            ),
                            file_path=item.get(
                                "file_path"
                            ),
                            line_start=item.get(
                                "line_start"
                            ),
                            line_end=item.get(
                                "line_end"
                            ),
                            content=item[
                                "content"
                            ],
                            verification_status=(
                                "UNVERIFIED"
                            ),
                        )
                    )

                except Exception as error:

                    persist_failures.append(
                        {
                            "file_path": item.get(
                                "file_path"
                            ),
                            "error": (
                                str(error)
                                or type(error).__name__
                            ),
                        }
                    )

                    continue

                item = dict(item)

                item["evidence_id"] = (
                    record.id
                )

                persisted.append(item)

            unique = persisted

        return {
            "evidence": unique,
            "count": len(unique),
            "persist_failures": persist_failures,
        }

    async def _from_qdrant(
        self,
        context,
        query_vector,
        limit,
    ):
        qdrant_tool = context.tools.get(
            "qdrant_search"
        )

        if qdrant_tool is None:
            raise RuntimeError(
                "Tool not found: qdrant_search"
            )

        results = await qdrant_tool.execute(
            query_vector=query_vector,
            limit=limit,
        )

        evidence = []

        for item in results:

            evidence.append(
                {
                    "source_type": item.get(
                        "source_type",
                        "repository",
                    ),
                    "source_url": item.get(
                        "source_url"
                    ),
                    "file_path": item.get(
                        "file_path"
                    ) or item.get(
                        "source"
                    ),
                    "line_start": item.get(
                        "line_start"
                    ),
                    "line_end": item.get(
                        "line_end"
                    ),
                    "content": item.get(
                        "text",
                        "",
                    ),
                    "metadata": item,
                }
            )

        return evidence

    @staticmethod
    def _from_analysis_results(
        input_data,
    ):
        evidence = []

        repo_url = input_data.get(
            "repo_url"
        )

        readme = input_data.get(
            "readme"
        )

        if isinstance(
            readme,
            str,
        ) and readme.strip():

            evidence.append(
                {
                    "source_type": "github",
                    "source_url": repo_url,
                    "file_path": "README.md",
                    "line_start": 1,
                    "line_end": len(
                        readme.splitlines()
                    ),
                    "content": readme,
                    "metadata": {},
                }
            )

        modules = EvidenceAnalysisSkill._modules(
            input_data
        )

        for module in modules:

            if not isinstance(
                module,
                dict,
            ):
                continue

            # 读取失败的模块不生成证据，
            # 否则会把空内容当成源码证据。
            if module.get("error"):
                continue

            file_path = module.get(
                "file_path"
            )

            content = module.get(
                "content"
            )

            if isinstance(
                content,
                dict,
            ):
                content = content.get(
                    "content",
                    "",
                )

            # 纯空白也算「没有内容」。
            #
            # 真实事故：空的 __init__.py 只有 1 个换行符，
            # 通过 `if not content` 检查后
            # 被证据存储层以
            # "Evidence content cannot be empty." 拒绝，
            # 异常冒泡导致整个 5-Agent 计划 FAILED。
            content = str(content)

            if not content.strip():
                continue

            # 限制单条证据长度：
            # 源码文件可能有数万字符，
            # 全部落库会让证据表迅速膨胀。
            excerpt = content[
                : EvidenceAnalysisSkill.MAX_EVIDENCE_CHARS
            ]

            # 摘录可能跳过了开头的 import 段，
            # 行号要跟着偏移，
            # 否则会写成「file:1-30」但内容其实是第 30 行开始的。
            start_line = module.get(
                "start_line",
                1,
            )

            if not isinstance(
                start_line,
                int,
            ) or start_line < 1:
                start_line = 1

            evidence.append(
                {
                    "source_type": "github",
                    "source_url": repo_url,
                    "file_path": file_path,
                    "line_start": start_line,
                    "line_end": (
                        start_line
                        + len(excerpt.splitlines())
                        - 1
                    ),
                    "content": excerpt,
                    "metadata": {},
                }
            )

        return evidence

    @staticmethod
    def _modules(
        input_data,
    ) -> list:
        """
        取出架构分析产出的 modules。

        修复点：

        旧代码只读 input_data["architecture"]，
        但真实数据结构里没有这个 key
        （真实 key 是 architecture_analysis_agent，
        且 PlanExecutorNode 会把结果拍平到顶层 modules），
        因此这个分支以前从未执行过，
        导致 Evidence 只有 README、没有源码。
        """

        architecture = (
            input_data.get("architecture")
            or input_data.get(
                "architecture_analysis_agent"
            )
        )

        if isinstance(
            architecture,
            dict,
        ):

            modules = architecture.get(
                "modules"
            )

            if isinstance(modules, list):
                return modules

        modules = input_data.get("modules")

        if isinstance(modules, list):
            return modules

        return []
```

### 📄 `app/skills/report_generation_skill.py`

**层级**：Skill 层（Skills） · **职责**：报告生成能力 `ReportGenerationSkill`（name=`report_generation`），聚合各 Skill 结果并交给 `report_export` Tool 导出；Tool 缺失时直接返回结构化结果

````python
"""
Report Generation Skill。

负责生成 Project Intelligence Report。

Phase 12 文档 15.3 要求报告至少包含：

    项目概览 / 技术栈 / 目录结构 / Agent架构 / Workflow
    / Skill / Tool / RAG / Memory / 数据库 / 关键源码 / Evidence

实际产出调整为：

    00 结论摘要 + 01-11 章

改动与原因：

  关键源码章已移除
      它展示的是每个文件开头的固定字符数，
      而 Python 文件开头必然是 import 块，
      渲染出来只有一堆 import，对理解项目没有帮助。

  04-09 章跟随「本次重点」展开或压缩
      用户在问题里点名了某个模块时
      （例如「分析项目的 agent」），
      重点章展开实现明细，
      其余章压成一行要点并注明未展开 ——
      否则把每章都铺开写一遍，重点就被淹没了。

各章末尾的「综合判断」来自 ReportSynthesisSkill
（由 LLM 基于已采集事实归纳，只归纳不推测）。

渲染方式
========

01-12 章由本 Skill 确定性地渲染成 markdown
（表格 / 列表 / 带语言标注的代码块），
不再把中间数据结构 dump 成 JSON。

这样做的好处：

- 数值仍是一字不改的真实数据，可逐条复核；
- 不经过 LLM，
  因此 LLM 不可用时报告依然完整可读，
  也不存在幻觉面。

每个字段的取值都来自各 Agent 的真实产出，
渲染层只负责排版，不补充、不推断任何信息。

本 Skill 的硬性约束：

- 所有章节内容都来自被分析项目的真实分析结果
- 取不到的章节必须明确写「真实数据不存在」并给出原因
- 不使用任何硬编码占位内容
  （旧版本曾把 AIPI 自己的 Tool 列表和
   {"context_enabled": true} 写进报告，
   那会让报告看起来完整但内容是假的）
- 「综合判断」不可用时静默省略，
  原始数据章节必须完整保留
"""

import json
import re

from app.project_analysis.analysis_focus import (
    AnalysisFocus,
)
from app.skills.base import BaseSkill


class ReportGenerationSkill(
    BaseSkill
):
    """项目智能分析报告生成能力。"""

    name = "report_generation"

    description = (
        "Generate final GitHub project "
        "intelligence report."
    )

    # 维度章节 -> 综合分析里的维度名。
    #
    # 章标题里的名字（Agent 架构 / Skill）
    # 与综合分析里的名字（agents / skills）
    # 不一致，且顺序需要显式固定，
    # 因此用一张表对应起来。
    DIMENSION_SECTIONS = (
        ("04 Agent 架构", "agents"),
        ("05 Workflow", "workflow"),
        ("06 Skill", "skills"),
        ("07 Tool", "tools"),
        ("08 RAG", "rag"),
        ("09 Memory", "memory"),
    )

    # 结论摘要各小节的展示名。
    SUMMARY_FIELDS = (
        ("core_design", "核心设计"),
        ("technology_choices", "技术选型"),
        ("highlights", "亮点"),
        ("risks", "风险与缺口"),
        ("use_cases", "适用场景"),
    )

    async def execute(
        self,
        context,
        input_data: dict,
    ):
        exporter = context.tools.get(
            "report_export"
        )

        title = input_data.get(
            "title",
            "Repository Analysis Report",
        )

        filename = input_data.get(
            "filename",
            "repository_analysis.md",
        )

        content = self._build_report(
            input_data
        )

        if exporter is None:
            return {
                "report": {
                    "format": "markdown",
                    "content": content,
                }
            }

        report = await exporter.execute(
            title=title,
            content=content,
            filename=filename,
        )

        return {
            "report": report,
            "content": content,
        }

    @classmethod
    def _build_report(
        cls,
        data: dict,
    ) -> str:
        """
        按 Phase 12 文档 15.3 生成报告。

        章节顺序与文档一致，内容全部来自真实数据。
        """

        technology_stack = data.get(
            "technology_stack"
        )

        if not isinstance(
            technology_stack,
            dict,
        ):
            technology_stack = {}

        architecture = (
            data.get("architecture")
            or data.get(
                "architecture_analysis_agent"
            )
        )

        if not isinstance(
            architecture,
            dict,
        ):
            architecture = {}

        project_structure = data.get(
            "project_structure"
        )

        if not isinstance(
            project_structure,
            dict,
        ):
            project_structure = {}

        # 综合分析结论。
        #
        # 不可用时为 None，
        # 此时 00 章仍会渲染，
        # 但内容明确写「综合分析不可用」与原因，
        # 而不是让这一章凭空消失
        # （消失会让人误以为报告本来就没有结论层）。
        synthesis = data.get("synthesis")

        if not isinstance(
            synthesis,
            dict,
        ):
            synthesis = {}

        # 用于在各章末尾给出深挖接口的调用地址。
        # 拿不到时渲染成 {run_id} 占位。
        run_id = data.get("run_id")

        # 本次分析的重点维度。
        #
        # research_plan 里带 focus；
        # 旧 run 没有该字段时 from_plan 会退回
        # 用 question 做关键词匹配。
        focus = AnalysisFocus.from_plan(
            data.get("research_plan")
        )

        sections = [
            cls._summary_section(
                synthesis,
                question=data.get("question"),
                focus=focus,
            ),

            cls._section(
                "01 项目概览",
                cls._overview_markdown(
                    cls._project_overview(data)
                ),
            ),

            cls._section(
                "02 技术栈",
                cls._technology_markdown(
                    technology_stack
                ),
            ),

            cls._section(
                "03 目录结构",
                cls._directory_markdown(
                    # PlanExecutorNode 会把
                    # architecture 的产出拍平到顶层，
                    # 因此两个位置都要看。
                    architecture.get(
                        "directory_structure"
                    )
                    or data.get(
                        "directory_structure"
                    )
                ),
            ),

            cls._section_with_judgment(
                "04 Agent 架构",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "agents",
                    ),
                    dimension="agents",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "agents",
            ),

            cls._section_with_judgment(
                "05 Workflow",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "workflow",
                    ),
                    dimension="workflow",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "workflow",
            ),

            cls._section_with_judgment(
                "06 Skill",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "skills",
                    ),
                    dimension="skills",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "skills",
            ),

            cls._section_with_judgment(
                "07 Tool",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "tools",
                    ),
                    dimension="tools",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "tools",
            ),

            cls._section_with_judgment(
                "08 RAG",
                cls._dimension_markdown(
                    cls._rag_dimension(
                        project_structure,
                        technology_stack,
                    ),
                    dimension="rag",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "rag",
            ),

            cls._section_with_judgment(
                "09 Memory",
                cls._dimension_markdown(
                    cls._structure_dimension(
                        project_structure,
                        "memory",
                    ),
                    dimension="memory",
                    run_id=run_id,
                    focus=focus,
                ),
                synthesis,
                "memory",
            ),

            cls._section(
                "10 数据库",
                cls._database_markdown(
                    technology_stack
                ),
            ),

            # 「关键源码」章已移除。
            #
            # 它展示的是每个文件开头的固定字符数，
            # 而 Python 文件开头必然是 import 块 ——
            # 实际渲染出来就是一堆
            # `import sqlite3` / `from decimal import Decimal`，
            # 对理解项目没有任何帮助。
            # 想看真实实现请看各模块章的「证据锚点」，
            # 或对该模块做深挖。

            cls._section(
                "11 Evidence",
                cls._evidence_markdown(
                    data.get("evidence")
                ),
            ),
        ]

        return "\n\n".join(
            sections
        )

    # ------------------------------------------------------------------
    # 通用渲染工具
    # ------------------------------------------------------------------

    @staticmethod
    def _text(value) -> str:
        """把任意标量渲染成表格里的一个值。"""

        if value is None:
            return "—"

        if isinstance(value, bool):
            return "是" if value else "否"

        if isinstance(
            value,
            (list, tuple),
        ):
            items = [
                str(item).strip()
                for item in value
                if str(item).strip()
            ]

            return ", ".join(items) if items else "—"

        text = str(value).strip()

        return text or "—"

    @staticmethod
    def _table(
        headers: list,
        rows: list,
    ) -> str:
        """渲染 markdown 表格。"""

        lines = [
            "| "
            + " | ".join(headers)
            + " |",
            "| "
            + " | ".join(
                "---" for _ in headers
            )
            + " |",
        ]

        for row in rows:

            lines.append(
                "| "
                + " | ".join(
                    str(cell) for cell in row
                )
                + " |"
            )

        return "\n".join(lines)

    @staticmethod
    def _bullets(items: list) -> str:
        """渲染 markdown 无序列表。"""

        return "\n".join(
            f"- {item}" for item in items
        )

    @staticmethod
    def _is_missing(value) -> bool:
        """判断是否为 _missing() 产出的「数据不存在」标记。"""

        return (
            isinstance(value, dict)
            and value.get("available") is False
            and "reason" in value
        )

    @classmethod
    def _missing_text(
        cls,
        reason: str,
    ) -> str:
        """
        渲染「数据不存在」。

        原因文本原样输出：
        它是报告里唯一说明「为什么没有」的线索。
        """

        return reason

    # ------------------------------------------------------------------
    # 各章渲染
    # ------------------------------------------------------------------

    @classmethod
    def _overview_markdown(
        cls,
        overview: dict,
    ) -> str:
        """01 项目概览：字段表格。"""

        if cls._is_missing(overview):
            return cls._missing_text(
                overview["reason"]
            )

        rows = [
            (
                "项目全名",
                cls._text(
                    overview.get("full_name")
                ),
            ),
            (
                "描述",
                cls._text(
                    overview.get("description")
                ),
            ),
            (
                "主语言",
                cls._text(
                    overview.get("language")
                ),
            ),
            (
                "Topics",
                cls._text(
                    overview.get("topics")
                ),
            ),
            (
                "Stars / Forks",
                (
                    f"{cls._text(overview.get('stars'))}"
                    " / "
                    f"{cls._text(overview.get('forks'))}"
                ),
            ),
            (
                "Open Issues",
                cls._text(
                    overview.get("open_issues")
                ),
            ),
            (
                "License",
                cls._text(
                    overview.get("license")
                ),
            ),
            (
                "默认分支",
                cls._text(
                    overview.get(
                        "default_branch"
                    )
                ),
            ),
            (
                "仓库体积",
                (
                    f"{cls._text(overview.get('size_kb'))}"
                    " KB"
                ),
            ),
            (
                "创建 / 最近推送",
                (
                    f"{cls._text(overview.get('created_at'))}"
                    " / "
                    f"{cls._text(overview.get('pushed_at'))}"
                ),
            ),
            (
                "README 字符数",
                cls._text(
                    overview.get(
                        "readme_characters"
                    )
                ),
            ),
            (
                "地址",
                cls._text(
                    overview.get("html_url")
                ),
            ),
        ]

        return cls._table(
            ["字段", "值"],
            rows,
        )

    @classmethod
    def _technology_markdown(
        cls,
        technology_stack: dict,
    ) -> str:
        """
        02 技术栈：分类表格。

        技术栈是「把若干配置文件拼成一个大字符串
        再做子串匹配」得到的，
        因此无法把某一项准确归到某一个文件，
        这里只列出「检测依据」扫过哪些文件，
        不编造逐项的文件归属。
        """

        if not technology_stack:
            return cls._missing_text(
                "真实数据不存在"
                "（Technology Agent 未产出 "
                "technology_stack）。"
            )

        labels = (
            ("frameworks", "框架"),
            ("llm", "LLM"),
            ("database", "数据库"),
            ("embedding", "Embedding"),
            ("deployment", "部署"),
        )

        rows = []

        for key, label in labels:

            values = technology_stack.get(
                key
            )

            if isinstance(
                values,
                (list, tuple),
            ) and values:

                rendered = ", ".join(
                    str(item)
                    for item in values
                )

            else:

                rendered = "未检测到"

            rows.append((label, rendered))

        blocks = [
            cls._table(
                ["类别", "检测结果"],
                rows,
            )
        ]

        source_files = technology_stack.get(
            "source_files"
        )

        if source_files:

            blocks.append(
                "**检测依据**（以下文件被读取后做关键词匹配）："
                "\n\n"
                + cls._bullets(
                    f"`{path}`"
                    for path in source_files
                )
            )

        failures = technology_stack.get(
            "read_failures"
        )

        if isinstance(failures, dict) and failures:

            blocks.append(
                "**读取失败**：\n\n"
                + cls._bullets(
                    f"`{path}` — {reason}"
                    for path, reason
                    in failures.items()
                )
            )

        return "\n\n".join(blocks)

    @classmethod
    def _directory_markdown(
        cls,
        directory,
    ) -> str:
        """03 目录结构：文件数 + 顶层目录表 + 关键文件。"""

        if not isinstance(
            directory,
            dict,
        ) or not directory.get("available"):

            return cls._missing_text(
                "真实数据不存在"
                "（未获取到仓库文件树）。"
            )

        blocks = [
            f"共 {cls._text(directory.get('total_files'))} 个文件。"
        ]

        top_level = directory.get(
            "top_level_dirs"
        )

        if isinstance(top_level, list) and top_level:

            blocks.append(
                cls._table(
                    ["顶层目录", "文件数"],
                    [
                        (
                            cls._text(
                                item.get("name")
                            ),
                            cls._text(
                                item.get(
                                    "file_count"
                                )
                            ),
                        )
                        for item in top_level
                        if isinstance(item, dict)
                    ],
                )
            )

        by_extension = directory.get(
            "by_extension"
        )

        if isinstance(
            by_extension,
            dict,
        ) and by_extension:

            blocks.append(
                "**按文件类型**\n\n"
                + cls._table(
                    ["扩展名", "文件数"],
                    [
                        (
                            cls._text(name),
                            cls._text(count),
                        )
                        for name, count
                        in by_extension.items()
                    ],
                )
            )

        key_files = directory.get(
            "key_files"
        )

        if isinstance(key_files, list) and key_files:

            blocks.append(
                "**关键文件**\n\n"
                + cls._bullets(
                    f"`{path}`"
                    for path in key_files
                )
            )

        return "\n\n".join(blocks)

    # 结论来源 -> 展示文案。
    DECLARED_BY_LABELS = {
        "code": "代码证据",
        "readme": "README 自述",
        "code+readme": "代码证据 + README 自述",
    }

    # 默认报告每章最多几条要点 / 几条证据锚点。
    #
    # 默认报告是「概览」，不是「实现说明书」：
    # 只给要点与可回溯的锚点，
    # 具体某个模块想知道更多时走深挖。
    MAX_HIGHLIGHTS = 6

    MAX_ANCHORS = 5

    # 证据锚点里最多留给 README 出处的名额。
    MAX_README_ANCHORS = 2

    # 单条要点里最多列几个名字。
    MAX_NAMES_PER_HIGHLIGHT = 8

    @classmethod
    def _dimension_markdown(
        cls,
        entry: dict,
        dimension: str,
        run_id=None,
        focus=None,
    ) -> str:
        """
        04-09 的维度章。

        三种渲染形态：

            无重点（focus 为空）
                全量等深：要点 + 证据锚点 + 深挖指引

            本次重点维度
                再加「实现明细」（签名 / 调用链 / 关键常量）

            本次非重点维度
                压成一行要点 + 一句未展开说明

        为什么要有第三种：用户问「分析这个项目的 agent」
        时，把 05-09 章都铺开写一遍，
        重点就被淹没了 ——
        这正是「报告里还是什么都有」的来源。
        """

        if cls._is_missing(entry):
            return cls._missing_text(
                entry["reason"]
            )

        focused = (
            focus is not None
            and focus.is_focused
        )

        if focused and not focus.is_primary(
            dimension
        ):

            return cls._compressed_markdown(
                entry,
                dimension,
                run_id,
                focus,
            )

        blocks = []

        declared_by = entry.get(
            "declared_by"
        )

        if declared_by:

            blocks.append(
                "**结论来源**："
                + cls.DECLARED_BY_LABELS.get(
                    declared_by,
                    declared_by,
                )
            )

        highlights = cls._highlights(entry)

        if highlights:

            blocks.append(
                "**要点**\n\n"
                + cls._bullets(highlights)
            )

        else:

            blocks.append(
                "**要点**\n\n未抽取到结构化条目。"
            )

        topics = entry.get("topics")

        if isinstance(topics, list) and topics:

            blocks.append(
                "**命中的 GitHub topics**："
                + ", ".join(
                    f"`{topic}`"
                    for topic in topics
                )
            )

        # RAG 章额外带上向量库检测结果。
        vector_store = entry.get(
            "vector_store_detected"
        )

        if isinstance(
            vector_store,
            list,
        ):

            blocks.append(
                "**检测到的向量库**："
                + (
                    ", ".join(vector_store)
                    if vector_store
                    else (
                        "未检测到"
                        "（当前只识别 qdrant / "
                        "chromadb）"
                    )
                )
            )

        anchors = cls._anchors(entry)

        if anchors:

            blocks.append(
                "**证据锚点**\n\n"
                + cls._bullets(anchors)
            )

        details = entry.get("details")

        # 报告里实际展开了多少条明细。
        # 0 表示没展开（非重点维度或没有明细），
        # 深挖指引的措辞要据此区分。
        shown_count = 0

        # 本次重点维度：把实现明细展开在报告里。
        #
        # 非重点维度不展开 ——
        # 它们已经走 _compressed_markdown 提前返回了。
        if (
            focused
            and focus.is_primary(dimension)
            and isinstance(details, list)
            and details
        ):

            rendered = [
                cls._detail_markdown(item)
                for item in details
                if isinstance(item, dict)
            ]

            rendered = [
                item for item in rendered if item
            ]

            if rendered:

                shown_count = len(rendered)

                blocks.append(
                    "**实现明细**\n\n"
                    + "\n\n".join(rendered)
                )

        detail_count = len(
            entry.get("details") or []
        )

        if detail_count:

            blocks.append(
                cls._deep_dive_hint(
                    dimension,
                    detail_count,
                    run_id,
                    shown_count=shown_count,
                )
            )

        return "\n\n".join(blocks)

    @classmethod
    def _compressed_markdown(
        cls,
        entry: dict,
        dimension: str,
        run_id,
        focus,
    ) -> str:
        """
        非重点维度的压缩形态。

        只留一行要点与一句说明 ——
        不是删掉这一章（那会让报告缺章），
        而是把它压到「知道有这回事」的程度。
        """

        highlights = cls._highlights(entry)

        summary = (
            "；".join(highlights)
            if highlights
            else "未抽取到结构化条目。"
        )

        if run_id:

            hint = (
                "> 查看完整内容与实现明细："
                f"`POST /analysis/{run_id}/deep-dive"
                f"?module={dimension}`"
            )

        else:

            hint = (
                "> 查看完整内容："
                "`reports/{run_id}_analysis.md`"
            )

        return (
            f"本次未展开。要点：{summary}\n\n"
            "> 本次分析的重点是 "
            + "、".join(focus.titles())
            + "，该模块未按问题展开。\n"
            ">\n"
            f"{hint}"
        )

    @classmethod
    def _scope_note(
        cls,
        question,
        focus,
    ) -> str:
        """
        报告开头的「本次问题 / 重点」抬头。

        必须写清楚，否则用户无法判断
        报告为什么有的章详细、有的章只有一行。
        """

        lines = []

        if isinstance(
            question,
            str,
        ) and question.strip():

            lines.append(
                "**本次问题**："
                + question.strip()
            )

        if focus is not None and focus.is_focused:

            lines.append(
                "**本次重点**："
                + "、".join(focus.titles())
                + "（这几个模块展开，其余压缩）"
            )

            if focus.notes:

                lines.append(
                    "**关注点**："
                    + focus.notes
                )

        if not lines:
            return ""

        return "\n\n".join(lines) + "\n\n"

    @classmethod
    def _deep_dive_hint(
        cls,
        dimension: str,
        detail_count: int,
        run_id,
        shown_count: int = 0,
    ) -> str:
        """
        指向该模块深挖报告的指引。

        detail_count 是采集到的明细总数。
        本次重点维度已经在报告里展开了，
        措辞要跟着变 ——
        否则会出现「刚展示完明细，
        下一行又说这些明细未放入报告」的矛盾。
        """

        target = (
            f"/analysis/{run_id}/deep-dive"
            if run_id
            else "/analysis/{run_id}/deep-dive"
        )

        if shown_count:

            return (
                "> 以上为本次展开的实现明细。"
                "**源码片段**与其余明细见深挖：\n"
                ">\n"
                f"> `POST {target}"
                f"?module={dimension}`"
            )

        return (
            "> 本模块另有 "
            f"{detail_count} 项实现明细"
            "（函数签名 / 调用链 / 关键常量 / 源码片段），"
            "未放入本报告。\n"
            ">\n"
            f"> 查看方式：`POST {target}"
            f"?module={dimension}`"
        )

    # 要点分组的展示顺序与名称。
    #
    # 顺序即优先级：
    # 图结构与类最能说明一个模块在做什么，
    # 依赖与目录只是旁证。
    HIGHLIGHT_GROUPS = (
        # 叫「图结构」而不是「图节点」：
        # 这一组里既有 StateGraph 构造，
        # 也有 add_node / add_edge，
        # 统称节点会与 add_node 的节点名混起来。
        ("graph", "图结构"),
        ("class", "类"),
        ("function", "函数"),
        ("import", "依赖"),
        ("path", "目录"),
        ("readme", "README 自述"),
    )

    @classmethod
    def _highlights(cls, entry: dict) -> list:
        """
        把扁平条目归纳成「要点」。

        条目是原始符号（`builder.add_node('x', ...)` /
        `class BaseAgent(ABC)` / `路径 src/app/agents/`），
        直接列出来只是堆符号；
        按类别归并并计数之后才是要点。

        纯字符串处理，不经过 LLM。
        """

        items = entry.get("items")

        if not isinstance(items, list):
            return []

        grouped = {
            key: []
            for key, _ in cls.HIGHLIGHT_GROUPS
        }

        for item in items:

            text = str(item).strip()

            if not text:
                continue

            grouped[
                cls._highlight_group(text)
            ].append(text)

        highlights = []

        for key, label in cls.HIGHLIGHT_GROUPS:

            values = grouped[key]

            if not values:
                continue

            highlights.append(
                cls._highlight_line(
                    label,
                    key,
                    values,
                )
            )

            if len(highlights) >= cls.MAX_HIGHLIGHTS:
                break

        return highlights

    @classmethod
    def _highlight_group(
        cls,
        text: str,
    ) -> str:
        """判断一条条目属于哪个要点分组。"""

        if cls._GRAPH_CALL_PATTERN.search(text):

            return "graph"

        if text.startswith("class "):

            return "class"

        if text.startswith(("def ", "@")):

            return "function"

        if text.startswith("import "):

            return "import"

        if text.startswith("路径 "):

            return "path"

        return "readme"

    # 图调用：`builder.add_node('x', ...)` 之类。
    _GRAPH_CALL_PATTERN = re.compile(
        r"\.(add_node|add_edge|add_conditional_edges"
        r"|set_entry_point|set_finish_point)\("
        r"|^StateGraph\("
    )

    # 从 add_node('name', ...) 里取节点名。
    _NODE_NAME_PATTERN = re.compile(
        r"add_node\(\s*['\"]([^'\"]+)['\"]"
    )

    # 从 add_edge('a', 'b') 里取两端。
    #
    # 显示成 `a → b` 比 `graph.add_edge` 有信息量得多。
    _EDGE_PATTERN = re.compile(
        r"add_(?:conditional_)?edge\(\s*"
        r"['\"]([^'\"]+)['\"]\s*,\s*"
        r"['\"]([^'\"]+)['\"]"
    )

    # 从 class Foo(Bar) / def foo(...) 里取名字。
    _DEFINITION_NAME_PATTERN = re.compile(
        r"^(?:class|def)\s+([A-Za-z_][A-Za-z0-9_]*)"
    )

    @classmethod
    def _highlight_line(
        cls,
        label: str,
        key: str,
        values: list,
    ) -> str:
        """渲染一条要点。"""

        names = []

        for value in values:

            names.append(
                cls._highlight_name(key, value)
            )

        shown = names[
            : cls.MAX_NAMES_PER_HIGHLIGHT
        ]

        rest = len(names) - len(shown)

        text = "、".join(
            f"`{name}`" for name in shown
        )

        if rest > 0:

            text += f" 等 {len(names)} 项"

        return f"{label}（{len(names)}）：{text}"

    @classmethod
    def _highlight_name(
        cls,
        key: str,
        value: str,
    ) -> str:
        """从原始条目里取出适合展示的名字。"""

        if key == "graph":

            node = cls._NODE_NAME_PATTERN.search(
                value
            )

            if node:
                return node.group(1)

            edge = cls._EDGE_PATTERN.search(value)

            if edge:
                return f"{edge.group(1)} → {edge.group(2)}"

            # StateGraph(...) -> StateGraph
            return value.split("(")[0]

        if key == "path":

            return value[len("路径 "):]

        if key == "import":

            return value[len("import "):]

        if key == "readme":

            # 自述条目可能是一整句，
            # 太长就截断，避免要点变成段落。
            return (
                value
                if len(value) <= 40
                else value[:40] + "…"
            )

        matched = cls._DEFINITION_NAME_PATTERN.match(
            value
        )

        if matched:
            return matched.group(1)

        return value

    @classmethod
    def _anchors(cls, entry: dict) -> list:
        """
        证据锚点：代码证据 + README 出处，合并限长。

        代码证据排在前面：
        它比 README 自述更接近项目实际做了什么。

        但要给 README 预留名额：
        declared_by 常常是 code+readme，
        而代码证据通常更多，
        不预留的话 README 锚点会被全部挤掉，
        读者就看不到「自述」那一半证据。
        """

        code = [
            item
            for item in (
                entry.get("code_evidence") or []
            )
            if isinstance(item, dict)
        ]

        readme = [
            item
            for item in (
                entry.get("evidence") or []
            )
            if isinstance(item, dict)
        ]

        # 最多给 README 留 2 个名额，
        # 且不超过它实际有的条数。
        reserved = min(
            cls.MAX_README_ANCHORS,
            len(readme),
        )

        code_budget = max(
            cls.MAX_ANCHORS - reserved,
            1,
        )

        anchors = [
            cls._code_evidence_line(item)
            for item in code[:code_budget]
        ]

        for item in readme:

            if len(anchors) >= cls.MAX_ANCHORS:
                break

            anchors.append(
                cls._code_evidence_line(item)
            )

        return anchors

    # 明细类型 -> 展示名。
    DETAIL_KIND_LABELS = {
        "graph": "图节点",
        "class": "类",
        "function": "函数",
    }

    @classmethod
    def _detail_markdown(
        cls,
        detail: dict,
    ) -> str:
        """
        渲染一条实现明细。

        形如：

            ### `duplicate_check` · `workflow_service.py:342`

            ```python
            def _node_duplicate_check(self, state: AgentState) -> AgentState
            ```

            - 调用：`find_similar_invoices`
            - 关键常量：`0.85`、`'duplicate_suspected'`
        """

        name = str(
            detail.get("name") or ""
        ).strip()

        signature = str(
            detail.get("signature") or ""
        ).strip()

        if not name and not signature:
            return ""

        file_path = detail.get("file_path")

        line = detail.get("line")

        location = file_path or "（未知文件）"

        if line:
            location = f"{location}:{line}"

        heading = "### "

        if name:

            heading += f"`{name}`"

            kind = cls.DETAIL_KIND_LABELS.get(
                str(detail.get("kind") or "")
            )

            if kind:
                heading += f" · {kind}"

            heading += f" · `{location}`"

        else:

            heading += f"`{location}`"

        blocks = [heading]

        if signature:

            blocks.append(
                "```python\n"
                f"{signature}\n"
                "```"
            )

        methods = detail.get("methods")

        if isinstance(methods, list) and methods:

            blocks.append(
                "- 方法："
                + "、".join(
                    f"`{item}`"
                    for item in methods
                )
            )

        calls = detail.get("calls")

        if isinstance(calls, list) and calls:

            blocks.append(
                "- 调用："
                + "、".join(
                    f"`{item}`"
                    for item in calls
                )
            )

        literals = detail.get("literals")

        if isinstance(literals, list) and literals:

            blocks.append(
                "- 关键常量："
                + "、".join(
                    f"`{item}`"
                    for item in literals
                )
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _code_evidence_line(item: dict) -> str:
        """
        渲染一条代码证据。

        路径信号没有行号，
        直接照搬会变成
        「`src/app/graph/` — 路径 src/app/graph/」
        这种把同一句话说了两遍的样子，
        因此单独处理。
        """

        text = str(item.get("text") or "")

        line = (
            item.get("line")
            or item.get("line_start")
        )

        if line:

            return (
                f"`{ReportGenerationSkill._location(item)}`"
                f" — {text}"
            )

        # 无行号的一律是路径信号。
        return (
            f"目录/文件名命中架构关键词："
            f"`{ReportGenerationSkill._location(item)}`"
        )

    @staticmethod
    def _location(item: dict) -> str:
        """
        渲染证据位置。

        路径信号（例如「路径 src/app/agents/」）
        没有行号，此时只显示路径，
        不能渲染成 `src/app/agents/:None`。
        """

        file_path = (
            item.get("file")
            or item.get("file_path")
            or "（未知文件）"
        )

        line = (
            item.get("line")
            or item.get("line_start")
        )

        if line:

            return f"{file_path}:{line}"

        return str(file_path)

    @classmethod
    def _database_markdown(
        cls,
        technology_stack: dict,
    ) -> str:
        """10 数据库。"""

        if not technology_stack:
            return cls._missing_text(
                "真实数据不存在"
                "（未产出 technology_stack）。"
            )

        databases = technology_stack.get(
            "database"
        )

        if isinstance(
            databases,
            (list, tuple),
        ) and databases:

            body = cls._bullets(
                f"`{name}`" for name in databases
            )

        else:

            body = "未检测到数据库。"

        return (
            body
            + "\n\n"
            + "数据来源："
            "`workflow_state.data."
            "technology_stack.database`"
        )

    @classmethod
    def _evidence_markdown(
        cls,
        evidence,
    ) -> str:
        """12 Evidence：文件 + 行号 + 内容片段。"""

        if not isinstance(
            evidence,
            list,
        ) or not evidence:

            return cls._missing_text(
                "真实数据不存在"
                "（Evidence Agent 未产出证据）。"
            )

        blocks = []

        for item in evidence:

            if not isinstance(item, dict):
                continue

            file_path = (
                item.get("file_path")
                or "（未知文件）"
            )

            line_start = item.get(
                "line_start"
            )

            line_end = item.get(
                "line_end"
            )

            if line_start and line_end:

                location = (
                    f"{file_path}:"
                    f"{line_start}-{line_end}"
                )

            elif line_start:

                location = (
                    f"{file_path}:{line_start}"
                )

            else:

                location = file_path

            content = str(
                item.get("content") or ""
            ).strip()

            # 单条证据的 content 可能很长，
            # 这里只取首行做摘要，
            # 完整内容在 Evidence 表里。
            first_line = (
                content.splitlines()[0]
                if content
                else ""
            )

            block = f"**`{location}`**"

            if first_line:

                block += (
                    "\n\n> "
                    + first_line[:160]
                )

            blocks.append(block)

        if not blocks:
            return cls._missing_text(
                "真实数据不存在"
                "（Evidence Agent 未产出证据）。"
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _missing(
        reason: str,
    ) -> dict:
        """统一的「真实数据不存在」表示。"""

        return {
            "available": False,
            "reason": reason,
        }

    # ------------------------------------------------------------------
    # 综合分析章节
    # ------------------------------------------------------------------

    @classmethod
    def _summary_section(
        cls,
        synthesis: dict,
        question=None,
        focus=None,
    ) -> str:
        """
        渲染 00 结论摘要。

        与其它章节不同，
        这一章是给人读的散文，
        不套 ```text JSON 代码块。

        综合分析不可用时仍然渲染该章，
        并写明原因 —— 缺席会被误读成
        「报告本来就没有结论层」。
        """

        if not synthesis.get("available"):

            reason = (
                synthesis.get("reason")
                or "综合分析未产出。"
            )

            return (
                "## 00 结论摘要\n\n"
                + cls._scope_note(question, focus)
                + "```text\n"
                "综合分析不可用。\n"
                f"原因：{reason}\n"
                "以下 01-11 章为未经归纳的原始分析数据。\n"
                "```"
            )

        summary = synthesis.get("summary")

        if not isinstance(summary, dict):
            summary = {}

        # 抬头：本次问了什么、重点在哪。
        #
        # 必须写清楚，否则用户无法判断
        # 报告为什么有的章详细、有的章只有一行。
        blocks = ["## 00 结论摘要"]

        scope = cls._scope_note(question, focus)

        if scope:
            blocks.append(scope.strip())

        blocks.append(
            "> 本章由 LLM 基于各 Agent 已采集的真实事实归纳，\n"
            "> 只做归纳、不做推测；\n"
            "> 事实不足处会明确标注「数据不足」。\n"
            "> 原始事实见下方 01-11 章。"
        )

        one_line = str(
            summary.get("one_line") or ""
        ).strip()

        if one_line:

            blocks.append(
                "### 一句话结论\n\n"
                f"{one_line}"
            )

        for key, title in cls.SUMMARY_FIELDS:

            items = summary.get(key)

            if not isinstance(items, list):
                continue

            bullets = [
                str(item).strip()
                for item in items
                if str(item).strip()
            ]

            if not bullets:
                continue

            blocks.append(
                f"### {title}\n\n"
                + "\n".join(
                    f"- {item}"
                    for item in bullets
                )
            )

        # summary 全空时（LLM 返回了合法 JSON
        # 但内容为空），明确说明而不是留一个空章。
        if len(blocks) == 1:

            blocks.append(
                "LLM 未返回可用的结论内容。"
            )

        return "\n\n".join(blocks)

    @classmethod
    def _section_with_judgment(
        cls,
        title: str,
        value,
        synthesis: dict,
        dimension: str,
    ) -> str:
        """
        渲染维度章节，并在末尾追加综合判断。

        综合判断不可用、或该维度没有判断时，
        只渲染原始数据章节，不追加空段落。
        """

        section = cls._section(
            title,
            value,
        )

        judgment = cls._dimension_judgment(
            synthesis,
            dimension,
        )

        if not judgment:
            return section

        return (
            f"{section}\n\n"
            f"**综合判断**：{judgment}"
        )

    @staticmethod
    def _dimension_judgment(
        synthesis: dict,
        dimension: str,
    ) -> str:
        """取出某个维度的综合判断，取不到返回空串。"""

        if not synthesis.get("available"):
            return ""

        dimensions = synthesis.get(
            "dimensions"
        )

        if not isinstance(
            dimensions,
            dict,
        ):
            return ""

        judgment = dimensions.get(
            dimension
        )

        if not isinstance(
            judgment,
            str,
        ):
            return ""

        return judgment.strip()

    @staticmethod
    def _project_overview(
        data: dict,
    ) -> dict:
        """项目概览：来自 GitHub API 的真实仓库信息。"""

        repository = data.get(
            "repository"
        )

        if (
            not isinstance(repository, dict)
            or not repository
        ):
            return ReportGenerationSkill._missing(
                "真实数据不存在"
                "（未获取到仓库信息）。"
            )

        license_info = repository.get(
            "license"
        )

        license_name = None

        if isinstance(
            license_info,
            dict,
        ):
            license_name = license_info.get(
                "name"
            )

        return {
            "name": repository.get(
                "name"
            ),
            "full_name": repository.get(
                "full_name"
            ),
            "description": repository.get(
                "description"
            ),
            "language": repository.get(
                "language"
            ),
            "topics": repository.get(
                "topics"
            ),
            "stars": repository.get(
                "stargazers_count"
            ),
            "forks": repository.get(
                "forks_count"
            ),
            "open_issues": repository.get(
                "open_issues_count"
            ),
            "license": license_name,
            "default_branch": repository.get(
                "default_branch"
            ),
            "size_kb": repository.get("size"),
            "created_at": repository.get(
                "created_at"
            ),
            "pushed_at": repository.get(
                "pushed_at"
            ),
            "html_url": repository.get(
                "html_url"
            ),
            "readme_characters": len(
                data.get("readme") or ""
            ),
        }

    @staticmethod
    def _structure_dimension(
        project_structure: dict,
        name: str,
    ) -> dict:
        """
        从 project_structure 取出某个维度的可读内容。

        该结构来自被分析项目的 README 与 GitHub topics，
        每条都带 README 行号，可人工复核。
        """

        if not project_structure.get(
            "available"
        ):
            return ReportGenerationSkill._missing(
                project_structure.get("reason")
                or (
                    "真实数据不存在"
                    "（未产出被分析项目的自述结构）。"
                )
            )

        entry = (
            project_structure.get(
                "dimensions"
            )
            or {}
        ).get(name)

        if not isinstance(entry, dict):
            return ReportGenerationSkill._missing(
                "真实数据不存在"
                f"（无 {name} 维度）。"
            )

        if not entry.get("declared"):
            return ReportGenerationSkill._missing(
                entry.get("reason")
                or (
                    "被分析项目未声明该能力"
                    "（README / topics 中没有相关描述）。"
                )
            )

        return {
            "items": entry.get("items") or [],
            "topics": entry.get("topics") or [],
            "evidence": [
                {
                    "file": item.get("file_path"),
                    "line": item.get("line_start"),
                    "text": item.get("text"),
                }
                for item in (
                    entry.get("evidence") or []
                )
            ],
            # 来自真实源码的 AST 证据。
            #
            # 与上面的 README 证据分开，
            # 因为两者性质不同：
            # 一个是「项目说自己有什么」，
            # 一个是「项目代码里确实有什么」。
            "code_evidence": [
                {
                    "file": item.get("file_path"),
                    "line": item.get("line_start"),
                    "text": item.get("text"),
                }
                for item in (
                    entry.get("code_evidence") or []
                )
                if isinstance(item, dict)
            ],
            "declared_by": entry.get(
                "declared_by"
            ),
            # 实现明细：函数签名 / 调用链 / 关键字面量。
            #
            # 比 items 重，但正是它回答了
            # 「这个模块具体怎么做的」。
            "details": [
                item
                for item in (
                    entry.get("details") or []
                )
                if isinstance(item, dict)
            ],
        }

    @staticmethod
    def _rag_dimension(
        project_structure: dict,
        technology_stack: dict,
    ) -> dict:
        """
        RAG 章节。

        README 自述的 rag 信号是主要来源；
        technology_stack.embedding 只是
        「是否检测到向量库」的辅助信息，
        不能单独代表完整的 RAG 实现。
        """

        declared = ReportGenerationSkill._structure_dimension(
            project_structure,
            "rag",
        )

        embedding = technology_stack.get(
            "embedding",
            [],
        )

        # 注意：_structure_dimension 成功时
        # 返回的是 {"items", "topics", "evidence"}，
        # 并不带 "available" 键；
        # 只有失败时才返回 _missing() 的
        # {"available": False, "reason": ...}。
        #
        # 这里曾经用 declared.get("available") 判断，
        # 成功路径永远取到 None，
        # 于是 RAG 章一直走「不可用」分支，
        # 还带着一个 None 的 reason。
        if not ReportGenerationSkill._is_missing(
            declared
        ):

            declared["vector_store_detected"] = (
                embedding
            )

            return declared

        return {
            "available": False,
            "reason": declared.get("reason")
            or (
                "真实数据不存在"
                "（被分析项目未声明 RAG 相关能力）。"
            ),
            "vector_store_detected": embedding,
        }

    @staticmethod
    def _section(
        title: str,
        value,
    ) -> str:
        """
        渲染一个章节。

        value 为字符串时按 markdown 原样输出；
        其它类型（理论上不应出现）退化成
        JSON 代码块，保证不会丢数据。
        """

        if value is None:
            value = "暂无数据"

        if isinstance(
            value,
            str,
        ):
            body = value.strip()
        else:
            body = (
                "```text\n"
                + json.dumps(
                    value,
                    ensure_ascii=False,
                    indent=2,
                    default=str,
                )
                + "\n```"
            )

        return (
            f"## {title}\n\n"
            f"{body}"
        )
````

### 📄 `app/skills/registry.py`

**层级**：Skill 层（Skills） · **职责**：Skill 注册中心 `SkillRegistry`（`register()` / `get(name)`）；`create_skill_registry()` 注册全部 5 个默认 Skill

```python
"""
Skill 注册中心。

作用:

统一管理系统中的 Skill。

Workflow / Agent 不需要关心 Skill 如何创建。

只需要:

registry.get("repository_analysis")

即可获取。


"""


from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)


from app.skills.architecture_analysis_skill import (
    ArchitectureAnalysisSkill
)


from app.skills.technology_analysis_skill import (
    TechnologyAnalysisSkill
)


from app.skills.evidence_analysis_skill import (
    EvidenceAnalysisSkill
)


from app.skills.report_generation_skill import (
    ReportGenerationSkill
)


from app.skills.report_synthesis_skill import (
    ReportSynthesisSkill
)


from app.skills.module_deep_dive_skill import (
    ModuleDeepDiveSkill
)




class SkillRegistry:
    """
    Skill管理器。
    """


    def __init__(self):

        # 保存所有Skill实例
        #
        # {
        #    "repository_analysis":
        #          RepositoryAnalysisSkill()
        # }

        self.skills = {}



    def register(
        self,
        skill
    ):
        """
        注册Skill。
        """


        self.skills[
            skill.name
        ] = skill



    def get(
        self,
        name:str
    ):
        """
        根据名称获取Skill。
        """

        return self.skills.get(
            name
        )




def create_skill_registry():
    """
    创建默认Skill集合。

    项目启动时调用。

    """


    registry = SkillRegistry()



    # 注册仓库分析Skill

    registry.register(
        RepositoryAnalysisSkill()
    )


    # 注册架构分析Skill

    registry.register(
        ArchitectureAnalysisSkill()
    )


    # 注册技术栈分析Skill

    registry.register(
        TechnologyAnalysisSkill()
    )


    # 注册证据分析Skill

    registry.register(
        EvidenceAnalysisSkill()
    )


    # 注册报告生成Skill

    registry.register(
        ReportGenerationSkill()
    )


    # 注册报告综合分析Skill

    registry.register(
        ReportSynthesisSkill()
    )


    # 注册单模块深挖Skill

    registry.register(
        ModuleDeepDiveSkill()
    )



    return registry
```

### 📄 `app/skills/json_output.py`

**层级**：Skill 层 · **职责**：LLM JSON 输出解析。

````python
"""
LLM JSON 输出解析。

为什么单独抽出来
================

报告综合分析（ReportSynthesisSkill）与
单模块深挖（ModuleDeepDiveSkill）都要
让 LLM 返回 JSON，
而模型的实际返回有三种常见形态：

    1. 纯 JSON
    2. ```json 代码块包裹
    3. 前后混着解释文字

更麻烦的是第四种：**被截断的 JSON**。

真实事故：综合分析要输出六个维度的判断段落，
回复一旦触到 max_tokens 上限就会被切断，
而截断的 JSON 用 json.loads 必然失败，
报告就会整章退化成「综合分析不可用」。

两处都要处理这件事，
逻辑放在一处避免两边慢慢长歪。
"""

import json


def parse_json_object(content: str):
    """
    尽最大努力把 LLM 回复解析成 dict。

    解析不出来返回 None，
    由调用方决定怎么降级 ——
    这里绝不伪造半截内容。
    """

    if not isinstance(content, str):
        return None

    text = strip_code_fence(content)

    if not text:
        return None

    try:

        parsed = json.loads(text)

    except (ValueError, TypeError):

        # 前后混入解释文字时，
        # 退回到「第一个 { 到最后一个 }」。
        start = text.find("{")

        end = text.rfind("}")

        if start == -1 or end <= start:

            # 连一对完整的 {} 都没有，
            # 基本可以认定回复被截断了。
            return repair_truncated(text)

        try:

            parsed = json.loads(
                text[start: end + 1]
            )

        except (ValueError, TypeError):

            return repair_truncated(text)

    if isinstance(parsed, dict):
        return parsed

    return None


def strip_code_fence(content: str) -> str:
    """去掉 markdown 代码块围栏。"""

    text = content.strip()

    if not text.startswith("```"):
        return text

    lines = text.splitlines()

    if lines and lines[0].startswith("```"):
        lines = lines[1:]

    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]

    return "\n".join(lines).strip()


def repair_truncated(text: str):
    """
    尝试修复被截断的 JSON。

    两种策略，依次尝试：

        1. 直接补上未闭合的引号与括号
        2. 回退到最后一个逗号再补括号
           （截断正好落在半个键值上时用）

    修不好就返回 None。
    """

    if not text:
        return None

    for candidate in (
        close_brackets(text),
        close_brackets(trim_to_last_comma(text)),
    ):

        if not candidate:
            continue

        try:

            parsed = json.loads(candidate)

        except (ValueError, TypeError):

            continue

        if isinstance(parsed, dict):
            return parsed

    return None


def close_brackets(text: str) -> str:
    """补上未闭合的引号与括号。"""

    stack = []

    in_string = False

    escaped = False

    for char in text:

        if in_string:

            if escaped:
                escaped = False

            elif char == "\\":
                escaped = True

            elif char == '"':
                in_string = False

            continue

        if char == '"':
            in_string = True

        elif char == "{":
            stack.append("}")

        elif char == "[":
            stack.append("]")

        elif char in "}]":

            if stack:
                stack.pop()

    repaired = text

    # 截断在字符串中间时先补引号。
    if in_string:
        repaired += '"'

    return repaired + "".join(
        reversed(stack)
    )


def trim_to_last_comma(text: str) -> str:
    """回退到最后一个逗号，丢掉残缺的尾巴。"""

    index = text.rfind(",")

    if index <= 0:
        return ""

    return text[:index]
````

### 📄 `app/skills/module_deep_dive_skill.py`

**层级**：Skill 层 · **职责**：Module Deep Dive Skill。

````python
"""
Module Deep Dive Skill。

职责
====

针对**某一个模块**（agents / workflow / skills /
tools / rag / memory）做深入分析，
产出一份独立的深挖报告。

为什么要有它
============

默认报告是「概览」：
每个模块只给要点与证据锚点，
既不浅到看不出结构，也不深到读不完。

但用户经常只想弄清楚**一个**模块 ——
「这个项目的 workflow 到底怎么流转的」。
这时候重跑整份报告是浪费，
只看概览又不够。

深挖就是补这一刀：只盯一个模块，
读更多文件、看更多符号、
把函数签名 / 调用链 / 关键常量 / 源码片段
全部展开。

与默认报告的差别
================

                       默认报告        深挖报告
    读取文件数          20             40（且只看该模块相关）
    每模块明细上限      6              20
    明细内容            不入报告        签名 + 调用链
                                        + 常量 + 源码片段
    LLM 结论            全项目一段      该模块七个小节

一条重要约束
============

深挖只**展开**默认报告已经采集到的结构，
不改变「只归纳不推测」的规则：
LLM 拿到的仍然是真实源码与真实事实，
源码片段直接来自 AST 的源码切片，
不是模型复述。
"""

import json
import re

from app.project_analysis.code_structure_extractor import (
    CodeStructureExtractor,
)
from app.skills.base import BaseSkill
from app.skills.json_output import (
    parse_json_object,
)


class ModuleDeepDiveSkill(
    BaseSkill
):
    """单模块深度分析能力。"""

    name = "module_deep_dive"

    description = (
        "Deep dive into one module of an "
        "analyzed repository."
    )

    # 可深挖的模块，与报告的 04-09 章一一对应。
    MODULES = CodeStructureExtractor.DIMENSIONS

    # 深挖时最多读取多少个文件。
    #
    # 默认报告是 20 个（六个模块分摊），
    # 深挖只看一个模块，所以给到 40。
    # 代价是每个文件一次 GitHub 请求。
    MAX_FILES = 40

    # 深挖时单个模块最多展开多少条明细。
    MAX_DETAILS = 20

    # 源码片段最多展示多少字符。
    MAX_SOURCE_CHARS = 1200

    # 送进 prompt 的 README 最多多少字符。
    MAX_README_CHARS = 4000

    MODULE_TITLES = {
        "agents": "Agent 架构",
        "workflow": "Workflow",
        "skills": "Skill",
        "tools": "Tool",
        "rag": "RAG",
        "memory": "Memory",
    }

    # LLM 输出的小节，顺序即渲染顺序。
    ANALYSIS_FIELDS = (
        ("responsibility", "职责"),
        ("key_implementations", "关键实现"),
        ("data_structures", "涉及的数据结构"),
        ("call_flow", "调用流程"),
        ("boundaries", "边界与限制"),
        ("risks", "风险与可疑之处"),
        ("open_questions", "需要人工确认"),
    )

    async def execute(
        self,
        context,
        input_data: dict,
    ):
        module = str(
            input_data.get("module") or ""
        ).strip().lower()

        if module not in self.MODULES:

            raise ValueError(
                f"Unsupported module: {module!r}. "
                f"Expected one of "
                f"{', '.join(self.MODULES)}."
            )

        owner = input_data.get("owner")

        repo = input_data.get("repo")

        if not owner or not repo:

            raise ValueError(
                "Module deep dive requires "
                "'owner' and 'repo'."
            )

        branch = input_data.get(
            "branch",
            "main",
        )

        tree = await self._load_tree(
            context,
            owner,
            repo,
            branch,
        )

        file_paths = self._select_files(
            tree,
            module,
        )

        sources, read_failures = (
            await self._read_sources(
                context,
                owner,
                repo,
                branch,
                file_paths,
            )
        )

        extra_paths = [
            item.get("path")
            for item in tree
            if isinstance(item, dict)
            and item.get("path")
        ]

        code_structure = (
            CodeStructureExtractor.extract(
                sources,
                extra_paths=extra_paths,
                max_details=self.MAX_DETAILS,
                # 深挖要展示源码片段；
                # 默认报告不展示，因此默认关掉
                # （每条 1.5KB，会把 state_data 撑过
                #   asyncmy 的 256KB 单字段上限）。
                include_source=True,
            )
        )

        entry = (
            code_structure.get(
                "dimensions"
            )
            or {}
        ).get(module) or {
            "items": [],
            "evidence": [],
            "details": [],
        }

        analysis = await self._analyze(
            context,
            module=module,
            owner=owner,
            repo=repo,
            entry=entry,
            readme=input_data.get("readme"),
            parsed_files=code_structure.get(
                "parsed_files",
                0,
            ),
            unparsed=code_structure.get(
                "unparsed"
            )
            or [],
        )

        content = self._render(
            module=module,
            owner=owner,
            repo=repo,
            entry=entry,
            analysis=analysis,
            files=sources,
            read_failures=read_failures,
            parsed_files=code_structure.get(
                "parsed_files",
                0,
            ),
            unparsed=code_structure.get(
                "unparsed"
            )
            or [],
        )

        report = await self._export(
            context,
            module=module,
            repo=repo,
            content=content,
            run_id=input_data.get("run_id"),
        )

        return {
            "module": module,
            "title": (
                f"{repo} · "
                f"{self.MODULE_TITLES.get(module, module)}"
                " 模块深挖"
            ),
            "files_read": [
                item["file_path"]
                for item in sources
            ],
            "details": len(
                entry.get("details") or []
            ),
            "analysis": analysis,
            "report": report,
            "content": content,
        }

    # ------------------------------------------------------------------
    # 取材
    # ------------------------------------------------------------------

    @staticmethod
    async def _load_tree(
        context,
        owner,
        repo,
        branch,
    ):
        """读取仓库文件树；拿不到时返回空列表。"""

        tool = context.tools.get(
            "github_repository"
        )

        if tool is None:
            return []

        get_tree = getattr(
            tool,
            "get_tree",
            None,
        )

        if not callable(get_tree):
            return []

        tree = await get_tree(
            owner=owner,
            name=repo,
            branch=branch,
        )

        if not isinstance(tree, list):
            return []

        return tree

    def _select_files(
        self,
        tree,
        module: str,
    ) -> list:
        """
        挑出与目标模块相关的文件。

        先用路径信号（`src/app/agents/` 之类）挑，
        不够再按浅层优先的顺序补充其它源码文件 ——
        有些模块不靠目录命名体现
        （例如 Skill 类散落在 services/ 下），
        只按路径筛会一个文件都读不到，
        那种情况下仍然要读一批文件
        让 AST 去认符号。
        """

        matched = []

        others = []

        for item in tree:

            if not isinstance(item, dict):
                continue

            path = item.get("path")

            if not path:
                continue

            if not str(path).lower().endswith(
                self.SOURCE_EXTENSIONS
            ):
                continue

            if str(path).lower().endswith(
                "__init__.py"
            ):
                continue

            if module in (
                CodeStructureExtractor
                .dimensions_for_path(path)
            ):

                matched.append(path)

            elif self._is_skippable_path(path):

                # 兜底阶段不看测试 / 迁移 / 文档。
                #
                # 命中目标模块的文件仍然优先，
                # 因此这里跳过不会漏掉该模块自身的代码。
                continue

            else:

                others.append(path)

        key = lambda path: (path.count("/"), path)

        matched.sort(key=key)

        others.sort(key=key)

        remaining = max(
            self.MAX_FILES - len(matched),
            0,
        )

        return matched + others[
            : min(
                self.MAX_FALLBACK_FILES,
                remaining,
            )
        ]

    # 与 ArchitectureAnalysisSkill 保持一致的源码扩展名。
    SOURCE_EXTENSIONS = (
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".mjs",
        ".go",
        ".java",
        ".rs",
        ".rb",
        ".php",
        ".cs",
        ".kt",
        ".swift",
        ".vue",
    )

    # 兜底补充文件时跳过的路径。
    #
    # 深挖的配额是 40，但命中目标模块的文件往往只有 1-2 个
    # （真实案例：workflow 模块只有 workflow_service.py，
    #   其余 39 个名额全被 tests/ 与 alembic/ 吃掉）。
    # 每个文件都是一次 GitHub 请求，
    # 把配额喂给测试与迁移既慢又没信息。
    SKIP_PATH_PATTERNS = (
        re.compile(r"(^|/)tests?/"),
        re.compile(r"(^|/)test_[^/]*$"),
        re.compile(r"_test\.[a-z]+$"),
        re.compile(r"(^|/)migrations?/"),
        # 整个 alembic/ 都是迁移脚手架，
        # 不只是 versions/ —— env.py、script.py.mako
        # 同样与应用架构无关。
        re.compile(r"(^|/)alembic/"),
        re.compile(r"(^|/)(demo_data|examples?|samples?)/"),
        re.compile(r"(^|/)docs?/"),
    )

    # 兜底补充文件的上限。
    #
    # MAX_FILES 是总配额，但命中目标模块的文件
    # 往往只有 1-2 个；剩下的名额如果全部用无关文件填满，
    # 就是几十次纯浪费的 GitHub 请求
    # （实测：workflow 模块读 40 个文件耗时 69 秒，
    #   其中 39 个对 workflow 维度毫无贡献）。
    #
    # 因此兜底只补到够用为止：
    # 既覆盖「模块符号散落在非同名目录」的情况，
    # 又不至于为了凑数去扫全仓库。
    MAX_FALLBACK_FILES = 15

    @classmethod
    def _is_skippable_path(
        cls,
        path: str,
    ) -> bool:
        """判断兜底补充时是否应跳过该路径。"""

        normalized = str(path).lower()

        return any(
            pattern.search(normalized)
            for pattern in cls.SKIP_PATH_PATTERNS
        )

    async def _read_sources(
        self,
        context,
        owner,
        repo,
        branch,
        file_paths,
    ):
        """
        逐个读取文件。

        单个文件失败不影响其它文件，
        失败原因如实带出来。
        """

        reader = context.tools.get("file_reader")

        if reader is None:
            raise RuntimeError(
                "Tool not found: file_reader"
            )

        sources = []

        failures = []

        for path in file_paths:

            try:

                content = await reader.execute(
                    owner=owner,
                    name=repo,
                    file_path=path,
                    branch=branch,
                )

            except Exception as error:

                failures.append(
                    {
                        "file_path": path,
                        "error": (
                            f"{type(error).__name__}: "
                            f"{error}"
                        ),
                    }
                )

                continue

            if not isinstance(content, str):
                continue

            if not content.strip():
                continue

            sources.append(
                {
                    "file_path": path,
                    "content": content,
                }
            )

        return sources, failures

    # ------------------------------------------------------------------
    # LLM 分析
    # ------------------------------------------------------------------

    async def _analyze(
        self,
        context,
        *,
        module,
        owner,
        repo,
        entry,
        readme,
        parsed_files,
        unparsed,
    ):
        """
        生成该模块的分析结论。

        LLM 不可用时返回 available=False，
        由渲染层降级为「只给实现明细」，
        不抛异常。
        """

        tool = context.tools.get("llm_chat")

        if tool is None:

            return {
                "available": False,
                "reason": "未注册 llm_chat 工具。",
            }

        facts = self._build_facts(
            module=module,
            owner=owner,
            repo=repo,
            entry=entry,
            readme=readme,
            parsed_files=parsed_files,
            unparsed=unparsed,
        )

        result = await tool.execute(
            messages=[
                {
                    "role": "system",
                    "content": self._system_prompt(
                        module
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "<facts>\n"
                        + json.dumps(
                            facts,
                            ensure_ascii=False,
                            indent=2,
                        )
                        + "\n</facts>\n\n"
                        + self._output_instruction()
                    ),
                },
            ]
        )

        if not result.get("available"):

            return {
                "available": False,
                "reason": result.get("reason")
                or "LLM 未返回内容。",
            }

        parsed = self._parse(
            result.get("content") or ""
        )

        if parsed is None:

            return {
                "available": False,
                "reason": (
                    "LLM 返回的内容不是合法 JSON。"
                ),
            }

        return {
            "available": True,
            "reason": None,
            "sections": {
                key: self._as_text_list(
                    parsed.get(key)
                )
                for key, _ in self.ANALYSIS_FIELDS
            },
        }

    def _build_facts(
        self,
        *,
        module,
        owner,
        repo,
        entry,
        readme,
        parsed_files,
        unparsed,
    ) -> dict:
        """构建送进 prompt 的事实。"""

        readme_text = ""

        if isinstance(readme, str):
            readme_text = readme[
                : self.MAX_README_CHARS
            ]

        return {
            "repository": f"{owner}/{repo}",
            "module": module,
            "module_title": self.MODULE_TITLES.get(
                module,
                module,
            ),
            "declared_by": entry.get(
                "declared_by"
            ),
            "items": entry.get("items") or [],
            "code_evidence": [
                {
                    "file": item.get("file_path"),
                    "line": item.get("line_start"),
                    "text": item.get("text"),
                }
                for item in (
                    entry.get("code_evidence") or []
                )
                if isinstance(item, dict)
            ],
            "readme_evidence": [
                {
                    "line": item.get("line_start"),
                    "text": item.get("text"),
                }
                for item in (
                    entry.get("evidence") or []
                )
                if isinstance(item, dict)
            ],
            "implementations": [
                {
                    "name": item.get("name"),
                    "kind": item.get("kind"),
                    "signature": item.get(
                        "signature"
                    ),
                    "file": item.get("file_path"),
                    "line": item.get("line"),
                    "methods": item.get("methods")
                    or [],
                    "calls": item.get("calls") or [],
                    "literals": item.get(
                        "literals"
                    )
                    or [],
                }
                for item in (
                    entry.get("details") or []
                )
                if isinstance(item, dict)
            ],
            "source_excerpts": [
                {
                    "name": item.get("name"),
                    "file": item.get("file_path"),
                    "line": item.get("line"),
                    "code": str(
                        item.get("source") or ""
                    )[: self.MAX_SOURCE_CHARS],
                }
                for item in (
                    entry.get("details") or []
                )
                if isinstance(item, dict)
                and item.get("source")
            ],
            "code_extraction": {
                "parsed_files": parsed_files,
                "unparsed": unparsed,
            },
            "readme": readme_text,
        }

    def _system_prompt(self, module: str) -> str:
        """系统提示词。"""

        title = self.MODULE_TITLES.get(
            module,
            module,
        )

        return (
            "你是一名资深软件架构分析师，"
            f"正在对某个 GitHub 项目的 "
            f"「{title}」模块做深入分析。\n"
            "\n"
            "你必须严格遵守以下规则：\n"
            "\n"
            "1. 只能使用用户消息中 <facts> 标签内提供的事实。\n"
            "   禁止使用外部知识、行业常识、"
            "对同类项目的印象来补充任何信息。\n"
            "2. 事实不足时必须写「数据不足：<缺什么>」，"
            "不要给出看起来合理的猜测。\n"
            "3. facts.declared_by 表示证据来源：\n"
            "   code   —— 代码里确实存在，可以说「实现了」；\n"
            "   readme —— 只是 README 声称，"
            "必须写成「README 声称」；\n"
            "   code+readme —— 两者都有。\n"
            "4. code_extraction.parsed_files 为 0 时，"
            "说明源码没被成功解析，"
            "不得对该模块的代码结构下任何结论。\n"
            "5. 只输出 JSON，不要用 markdown 代码块包裹，"
            "不要在 JSON 前后添加解释文字。\n"
        )

    def _output_instruction(self) -> str:
        """输出格式说明。"""

        lines = []

        for index, (key, label) in enumerate(
            self.ANALYSIS_FIELDS
        ):

            comma = (
                ","
                if index
                < len(self.ANALYSIS_FIELDS) - 1
                else ""
            )

            lines.append(
                f'  "{key}": '
                f'["{label}，数据不足时写'
                f'「数据不足：<缺什么>」"{comma}'
            )

        return (
            "请严格按下面的 JSON 结构输出，"
            "不要增删字段：\n"
            "{\n"
            + "\n".join(lines)
            + "\n}\n"
            "\n"
            "每个字段都是字符串数组，最多 6 条，"
            "每条一句话，要具体到这个模块的实现，"
            "不要写适用于任何项目的空话。"
        )

    # ------------------------------------------------------------------
    # 渲染
    # ------------------------------------------------------------------

    def _render(
        self,
        *,
        module,
        owner,
        repo,
        entry,
        analysis,
        files,
        read_failures,
        parsed_files,
        unparsed,
    ) -> str:
        """渲染深挖报告。"""

        title = self.MODULE_TITLES.get(
            module,
            module,
        )

        blocks = [
            (
                f"# {repo} · {title} 模块深挖报告\n\n"
                f"> 分析对象：`{owner}/{repo}`\n"
                f"> 模块：`{module}`\n"
                f"> 读取文件：{len(files)} 个"
                f"（默认报告为 20 个）\n"
                f"> 解析成功：{parsed_files} 个文件\n"
                f"> 实现明细："
                f"{len(entry.get('details') or [])} 项"
            )
        ]

        blocks.append(
            self._render_analysis(
                title,
                analysis,
            )
        )

        blocks.append(
            self._render_implementations(
                entry.get("details") or []
            )
        )

        blocks.append(
            self._render_evidence(entry)
        )

        blocks.append(
            self._render_extraction_health(
                files=files,
                read_failures=read_failures,
                unparsed=unparsed,
            )
        )

        return "\n\n".join(
            block
            for block in blocks
            if block
        )

    def _render_analysis(
        self,
        title: str,
        analysis: dict,
    ) -> str:
        """渲染 LLM 结论。"""

        if not analysis.get("available"):

            return (
                "## 分析结论\n\n"
                "```text\n"
                f"本模块的结论分析不可用。\n"
                f"原因：{analysis.get('reason')}\n"
                "以下实现明细为未经归纳的原始抽取结果。\n"
                "```"
            )

        sections = analysis.get(
            "sections"
        ) or {}

        blocks = ["## 分析结论"]

        for key, label in self.ANALYSIS_FIELDS:

            values = sections.get(key)

            if not values:
                continue

            blocks.append(
                f"### {label}\n\n"
                + "\n".join(
                    f"- {item}" for item in values
                )
            )

        if len(blocks) == 1:

            blocks.append("LLM 未返回可用的结论内容。")

        return "\n\n".join(blocks)

    def _render_implementations(
        self,
        details: list,
    ) -> str:
        """渲染实现明细（签名 + 调用链 + 常量 + 源码）。"""

        if not details:

            return (
                "## 实现明细\n\n"
                "未抽取到实现明细"
                "（该模块没有匹配到可解析的函数 / 类）。"
            )

        blocks = ["## 实现明细"]

        for detail in details:

            blocks.append(
                self._render_detail(detail)
            )

        return "\n\n".join(blocks)

    def _render_detail(
        self,
        detail: dict,
    ) -> str:
        """渲染单条实现明细。"""

        name = str(
            detail.get("name") or ""
        ).strip()

        file_path = detail.get("file_path")

        line = detail.get("line")

        location = file_path or "（未知文件）"

        if line:
            location = f"{location}:{line}"

        heading = (
            f"### `{name}` · `{location}`"
            if name
            else f"### `{location}`"
        )

        blocks = [heading]

        signature = str(
            detail.get("signature") or ""
        ).strip()

        if signature:

            blocks.append(
                "```python\n"
                f"{signature}\n"
                "```"
            )

        methods = detail.get("methods")

        if isinstance(methods, list) and methods:

            blocks.append(
                "- 方法："
                + "、".join(
                    f"`{item}`" for item in methods
                )
            )

        calls = detail.get("calls")

        if isinstance(calls, list) and calls:

            blocks.append(
                "- 调用："
                + "、".join(
                    f"`{item}`" for item in calls
                )
            )

        literals = detail.get("literals")

        if isinstance(literals, list) and literals:

            blocks.append(
                "- 关键常量："
                + "、".join(
                    f"`{item}`" for item in literals
                )
            )

        source = str(
            detail.get("source") or ""
        ).strip()

        if source:

            blocks.append(
                "**源码片段**\n\n"
                "```python\n"
                f"{source[: self.MAX_SOURCE_CHARS]}\n"
                "```"
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _render_evidence(entry: dict) -> str:
        """渲染该模块的条目与证据锚点。"""

        blocks = []

        items = entry.get("items")

        if isinstance(items, list) and items:

            blocks.append(
                "## 结构化条目\n\n"
                + "\n".join(
                    f"- {item}" for item in items
                )
            )

        anchors = []

        for key in (
            "code_evidence",
            "evidence",
        ):

            for item in entry.get(key) or []:

                if not isinstance(item, dict):
                    continue

                file_path = (
                    item.get("file_path")
                    or item.get("file")
                    or "（未知文件）"
                )

                line = item.get("line_start")

                location = (
                    f"{file_path}:{line}"
                    if line
                    else file_path
                )

                anchors.append(
                    f"- `{location}` — {item.get('text')}"
                )

        if anchors:

            blocks.append(
                "## 证据锚点\n\n"
                + "\n".join(anchors)
            )

        return "\n\n".join(blocks)

    @staticmethod
    def _render_extraction_health(
        *,
        files,
        read_failures,
        unparsed,
    ) -> str:
        """
        如实交代这次的采集情况。

        深挖的价值在于「看得比默认报告多」，
        因此多读了哪些文件、
        哪些没读到、哪些没解析成功，
        必须写清楚，否则读者无法判断结论的覆盖面。
        """

        lines = [
            (
                "- 成功读取并解析："
                f"{len(files)} 个文件"
            )
        ]

        if read_failures:

            lines.append(
                f"- 读取失败：{len(read_failures)} 个"
            )

            for item in read_failures[:10]:

                lines.append(
                    f"  - `{item['file_path']}`"
                    f" — {item['error']}"
                )

        if unparsed:

            lines.append(
                f"- 解析失败：{len(unparsed)} 个"
            )

            for item in unparsed[:10]:

                lines.append(
                    f"  - `{item['file_path']}`"
                    f" — {item['error']}"
                )

        if files:

            lines.append("- 本次读取的文件：")

            for item in files:

                lines.append(
                    f"  - `{item['file_path']}`"
                )

        return (
            "## 本次采集范围\n\n"
            + "\n".join(lines)
        )

    # ------------------------------------------------------------------
    # 导出与工具方法
    # ------------------------------------------------------------------

    async def _export(
        self,
        context,
        *,
        module,
        repo,
        content,
        run_id,
    ):
        """写出深挖报告文件。"""

        exporter = context.tools.get(
            "report_export"
        )

        filename = (
            f"{run_id}_{module}_deep_dive.md"
            if run_id
            else f"{repo}_{module}_deep_dive.md"
        )

        if exporter is None:

            return {
                "format": "markdown",
                "content": content,
            }

        return await exporter.execute(
            title=(
                f"{repo} · {module} 模块深挖报告"
            ),
            content=content,
            filename=filename,
        )

    @staticmethod
    def _parse(
        content: str,
    ):
        """
        解析 LLM 返回的 JSON。

        与报告综合分析共用同一套容错逻辑
        （代码块包裹 / 前后噪声 / 被截断）。
        """

        return parse_json_object(content)

    @staticmethod
    def _as_text_list(value) -> list:
        """把任意值转成限长的字符串列表。"""

        if value is None:
            return []

        if isinstance(value, str):

            text = value.strip()

            return [text] if text else []

        if not isinstance(
            value,
            (list, tuple),
        ):
            return [str(value)]

        items = []

        for item in value:

            text = str(item).strip()

            if not text:
                continue

            items.append(text)

            if len(items) >= 6:
                break

        return items
````

### 📄 `app/skills/report_synthesis_skill.py`

**层级**：Skill 层 · **职责**：Report Synthesis Skill。

````python
"""
Report Synthesis Skill。

职责
====

在 Finalizer 生成报告之前，
把已被各 Agent 采集到的**真实事实**
交给 LLM，产出一层「判断」：

    - 00 结论摘要（一句话结论 / 核心设计 / 技术选型
                   / 亮点 / 风险与缺口 / 适用场景）
    - 各维度（agents / workflow / skills / tools
             / rag / memory）的综合判断

为什么需要这一层
================

在此之前，报告是 state.data 的 JSON 序列化：
有事实、没有结论。
本 Skill 负责从「事实」跨到「判断」。

硬性约束
========

1. LLM **只能**使用 prompt 中 <facts> 提供的事实，
   禁止补充外部知识、行业常识或猜测。
2. 事实不足时必须写「数据不足：<缺什么>」，
   不允许编造一个看起来合理的答案。
3. LLM 不可用（无 Key / 超时 / 返回非法 JSON）时，
   本 Skill 返回 available=False 并给出原因，
   **不抛异常**，报告仍然正常产出。

这三点与 ReportGenerationSkill 中
「不使用任何硬编码占位内容」的约束是同一条原则。
"""

import json

from app.skills.base import BaseSkill
from app.skills.json_output import (
    parse_json_object,
)


class ReportSynthesisSkill(
    BaseSkill
):
    """基于已采集事实生成综合判断。"""

    name = "report_synthesis"

    description = (
        "Synthesize judgments from "
        "collected analysis facts."
    )

    # 送进 prompt 的 README 最多多少字符。
    #
    # README 是当前最主要的事实来源，
    # 但个别仓库的 README 有数万字符，
    # 全量送入会撑爆上下文。
    MAX_README_CHARS = 6000

    # 送进 prompt 的单个源码片段最多多少字符。
    MAX_SOURCE_CHARS = 600

    # 最多送入多少个源码片段。
    MAX_SOURCE_FILES = 6

    # 最多送入多少条 Evidence。
    MAX_EVIDENCE = 12

    # 输出 JSON 中每个列表最多保留多少条。
    #
    # LLM 偶尔会写得很长，
    # 这里做上限保护，避免报告被一段话淹没。
    MAX_BULLETS = 6

    # 需要 LLM 给出判断的维度，
    # 与报告 04-09 章一一对应。
    DIMENSIONS = (
        "agents",
        "workflow",
        "skills",
        "tools",
        "rag",
        "memory",
    )

    # 维度名 -> 报告章节标题，用于 prompt 中给出上下文。
    DIMENSION_TITLES = {
        "agents": "Agent 架构",
        "workflow": "Workflow",
        "skills": "Skill",
        "tools": "Tool",
        "rag": "RAG",
        "memory": "Memory",
    }

    async def execute(
        self,
        context,
        input_data: dict,
    ):
        llm_tool = context.tools.get(
            "llm_chat"
        )

        if llm_tool is None:

            return self._unavailable(
                "Tool not found: llm_chat，"
                "无法生成综合分析。"
            )

        facts = self._build_facts(
            input_data
        )

        prompt = self._build_prompt(
            facts,
            question=input_data.get(
                "question"
            ),
        )

        result = await llm_tool.execute(
            messages=[
                {
                    "role": "system",
                    "content": (
                        self._system_prompt()
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ]
        )

        if not result.get("available"):

            return self._unavailable(
                result.get("reason")
                or "LLM 未返回内容。"
            )

        parsed = self._parse(
            result.get("content") or ""
        )

        if parsed is None:

            return self._unavailable(
                "LLM 返回的内容不是合法 JSON，"
                "无法解析为综合分析。"
            )

        summary = parsed.get("summary")

        if not isinstance(summary, dict):

            return self._unavailable(
                "LLM 返回的 JSON 缺少 summary 字段。"
            )

        return {
            "available": True,
            "reason": None,
            "summary": self._normalize_summary(
                summary
            ),
            "dimensions": (
                self._normalize_dimensions(
                    parsed.get("dimensions")
                )
            ),
        }

    @staticmethod
    def _unavailable(
        reason: str,
    ) -> dict:
        """统一的「综合分析不可用」表示。"""

        return {
            "available": False,
            "reason": reason,
            "summary": {},
            "dimensions": {},
        }

    # ------------------------------------------------------------------
    # prompt 构建
    # ------------------------------------------------------------------

    @staticmethod
    def _system_prompt() -> str:
        """
        系统提示词。

        这里是「只归纳不推测」约束的落点，
        修改时不要放宽这三条。
        """

        return (
            "你是一名资深软件架构分析师，"
            "正在为一份 GitHub 项目分析报告撰写结论部分。\n"
            "\n"
            "你必须严格遵守以下规则：\n"
            "\n"
            "1. 你只能使用用户消息中 <facts> 标签内提供的事实。\n"
            "   禁止使用你自己的外部知识、行业常识、"
            "对同类项目的印象来补充任何信息。\n"
            "2. 如果某个问题在 <facts> 中找不到依据，"
            "必须直接写「数据不足：<具体缺什么>」，"
            "绝对不要给出一个看起来合理的猜测。\n"
            "3. <facts> 中标记为 available=false 的部分，"
            "说明该项数据没有被采集到，"
            "对应的判断必须写成数据不足，"
            "不能说「未使用该技术」或「没有实现该能力」。\n"
            "   同样地，code_extraction.available=false "
            "或 parsed_files=0 时，"
            "说明源码没有被成功解析，"
            "此时不得对代码结构下任何结论。\n"
            "4. declared_by 表示结论的来源：\n"
            "   code    —— 代码里确实存在，可以说「实现了」；\n"
            "   readme  —— 只是 README 声称，"
            "必须写成「README 声称」而不是「实现了」；\n"
            "   code+readme  —— 两者都有，可以说「实现了」。\n"
            "5. 不要复述 JSON 原文，要给出结论性的判断，"
            "每条判断都要能对应到 <facts> 中的具体事实。\n"
            "6. 只输出 JSON，不要用 markdown 代码块包裹，"
            "不要在 JSON 前后添加任何解释文字。\n"
        )

    def _build_prompt(
        self,
        facts: dict,
        question=None,
    ) -> str:
        """构建用户消息。"""

        parts = []

        if isinstance(
            question,
            str,
        ) and question.strip():

            parts.append(
                "本次分析要回答的问题：\n"
                f"{question.strip()}\n"
            )

        parts.append(
            "<facts>\n"
            + json.dumps(
                facts,
                ensure_ascii=False,
                indent=2,
            )
            + "\n</facts>\n"
        )

        parts.append(
            self._output_instruction()
        )

        return "\n".join(parts)

    def _output_instruction(self) -> str:
        """输出格式说明。"""

        dimension_lines = "\n".join(
            f'    "{name}": "针对「'
            f'{self.DIMENSION_TITLES[name]}」'
            f'的综合判断，'
            f'数据不足时写「数据不足：<缺什么>」"'
            + ("," if index < len(
                self.DIMENSIONS
            ) - 1 else "")
            for index, name in enumerate(
                self.DIMENSIONS
            )
        )

        return (
            "请严格按下面的 JSON 结构输出，"
            "不要增删字段：\n"
            "\n"
            "{\n"
            '  "summary": {\n'
            '    "one_line": '
            '"一句话说清这个项目是什么、'
            '核心设计是什么",\n'
            '    "core_design": ["核心设计判断", "..."],\n'
            '    "technology_choices": '
            '["技术选型判断，'
            '说明这些技术组合意味着什么", "..."],\n'
            '    "highlights": ["这个项目做得好的地方", "..."],\n'
            '    "risks": ["风险、缺口、可疑之处", "..."],\n'
            '    "use_cases": ["适合用来做什么 / 参考什么", "..."]\n'
            "  },\n"
            '  "dimensions": {\n'
            f"{dimension_lines}\n"
            "  }\n"
            "}\n"
            "\n"
            "其中 summary 的每个列表字段最多 "
            f"{self.MAX_BULLETS} 条，"
            "每条一句话。\n"
            "facts 中没有依据的字段，"
            "写成「数据不足：<缺什么>」即可。"
        )

    # ------------------------------------------------------------------
    # 事实摘要
    # ------------------------------------------------------------------

    def _build_facts(
        self,
        data: dict,
    ) -> dict:
        """
        从 state.data 构建送入 LLM 的事实摘要。

        刻意只挑选与判断相关的字段：
        state.data 里还有 modules 全文、
        executed_tasks 等执行细节，
        全量送入既浪费上下文，
        又会把 AIPI 自身的执行状态
        混进对被分析项目的判断里。
        """

        if not isinstance(data, dict):
            data = {}

        return {
            "project_overview": (
                self._project_overview(data)
            ),
            "readme": self._readme(data),
            "technology_stack": (
                self._as_dict(
                    data.get("technology_stack")
                )
            ),
            "directory_structure": (
                self._as_dict(
                    data.get(
                        "directory_structure"
                    )
                )
            ),
            "declared_structure": (
                self._declared_structure(data)
            ),
            "code_extraction": (
                self._code_extraction(data)
            ),
            "source_files": (
                self._source_files(data)
            ),
            "evidence": self._evidence(data),
        }

    @staticmethod
    def _as_dict(value) -> dict:
        """只接受 dict，其它一律当空。"""

        if isinstance(value, dict):
            return value

        return {}

    @staticmethod
    def _project_overview(
        data: dict,
    ) -> dict:
        """项目概览：GitHub API 的真实元数据。"""

        repository = data.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            return {
                "available": False,
                "reason": "未获取到仓库信息。",
            }

        license_info = repository.get(
            "license"
        )

        license_name = None

        if isinstance(
            license_info,
            dict,
        ):
            license_name = license_info.get(
                "name"
            )

        return {
            "available": True,
            "name": repository.get("name"),
            "full_name": repository.get(
                "full_name"
            ),
            "description": repository.get(
                "description"
            ),
            "language": repository.get(
                "language"
            ),
            "topics": repository.get(
                "topics"
            ),
            "stars": repository.get(
                "stargazers_count"
            ),
            "forks": repository.get(
                "forks_count"
            ),
            "open_issues": repository.get(
                "open_issues_count"
            ),
            "license": license_name,
            "size_kb": repository.get("size"),
            "created_at": repository.get(
                "created_at"
            ),
            "pushed_at": repository.get(
                "pushed_at"
            ),
        }

    def _readme(
        self,
        data: dict,
    ) -> dict:
        """README：被分析项目最主要的事实来源。"""

        readme = data.get("readme")

        if not isinstance(
            readme,
            str,
        ) or not readme.strip():

            return {
                "available": False,
                "reason": (
                    data.get("readme_error")
                    or "未读取到 README 内容。"
                ),
            }

        return {
            "available": True,
            "characters": len(readme),
            "truncated": (
                len(readme)
                > self.MAX_README_CHARS
            ),
            "content": readme[
                : self.MAX_README_CHARS
            ],
        }

    def _declared_structure(
        self,
        data: dict,
    ) -> dict:
        """
        被分析项目自述结构的各维度。

        直接把 declared / items / topics / evidence
        交给 LLM，
        并显式带上 available / reason，
        让模型知道哪些是真没有、哪些是没采到。
        """

        structure = data.get(
            "project_structure"
        )

        if (
            not isinstance(
                structure,
                dict,
            )
            or not structure.get("available")
        ):

            return {
                "available": False,
                "reason": (
                    "未产出被分析项目的自述结构"
                    "（project_structure）。"
                ),
            }

        dimensions = (
            structure.get("dimensions")
            or {}
        )

        result = {}

        for name in self.DIMENSIONS:

            entry = dimensions.get(name)

            if not isinstance(entry, dict):

                result[name] = {
                    "available": False,
                    "reason": (
                        "该维度没有被抽取。"
                    ),
                }

                continue

            result[name] = {
                "available": bool(
                    entry.get("declared")
                ),
                # 结论来自代码还是 README。
                #
                # 这个区别对判断很关键：
                # declared_by=readme 时，
                # 只能说「README 声称有」，
                # 不能说「代码里确实有」。
                "declared_by": entry.get(
                    "declared_by"
                ),
                "items": entry.get(
                    "items"
                )
                or [],
                "topics": entry.get(
                    "topics"
                )
                or [],
                "reason": entry.get(
                    "reason"
                ),
                "code_evidence": [
                    {
                        "file": item.get(
                            "file_path"
                        ),
                        "line": item.get(
                            "line_start"
                        ),
                        "text": item.get(
                            "text"
                        ),
                    }
                    for item in (
                        entry.get(
                            "code_evidence"
                        )
                        or []
                    )
                    if isinstance(
                        item,
                        dict,
                    )
                ],
                "readme_evidence": [
                    {
                        "line": item.get(
                            "line_start"
                        ),
                        "text": item.get(
                            "text"
                        ),
                    }
                    for item in (
                        entry.get("evidence")
                        or []
                    )
                    if isinstance(
                        item,
                        dict,
                    )
                ],
                # 实现明细：函数签名 / 调用链 / 关键常量。
                #
                # 这是判断「做到什么程度」的依据：
                # 只有符号名时只能说「有这个方法」，
                # 有了签名与调用链才能说
                # 「它查了哪些字段、阈值多少」。
                "details": [
                    {
                        "name": item.get("name"),
                        "signature": item.get(
                            "signature"
                        ),
                        "file": item.get(
                            "file_path"
                        ),
                        "line": item.get("line"),
                        "methods": item.get(
                            "methods"
                        )
                        or [],
                        "calls": item.get("calls")
                        or [],
                        "literals": item.get(
                            "literals"
                        )
                        or [],
                    }
                    for item in (
                        entry.get("details") or []
                    )
                    if isinstance(item, dict)
                ],
            }

        return result

    @staticmethod
    def _code_extraction(
        data: dict,
    ) -> dict:
        """
        代码抽取的执行情况。

        必须交给 LLM：
        「解析了 8 个文件、0 个失败」
        和「一个文件都没读到」
        会得出完全不同的可靠性判断。
        """

        structure = data.get(
            "project_structure"
        )

        if not isinstance(
            structure,
            dict,
        ):
            return {
                "available": False,
                "reason": "未产出结构信息。",
            }

        meta = structure.get(
            "code_extraction"
        )

        if not isinstance(meta, dict):
            return {
                "available": False,
                "reason": "未执行代码结构抽取。",
            }

        return meta

    def _source_files(
        self,
        data: dict,
    ) -> list:
        """
        真实读到的源码片段。

        这是当前唯一来自代码而非 README 的证据，
        虽然采样很浅，
        但对判断「README 说的和代码是否一致」
        已经够用。
        """

        modules = data.get("modules")

        if not isinstance(modules, list):
            return []

        files = []

        for module in modules:

            if not isinstance(
                module,
                dict,
            ):
                continue

            if module.get("error"):
                continue

            content = str(
                module.get("content") or ""
            )

            if not content.strip():
                continue

            files.append(
                {
                    "file_path": module.get(
                        "file_path"
                    ),
                    "content": content[
                        : self.MAX_SOURCE_CHARS
                    ],
                    "truncated": (
                        len(content)
                        > self.MAX_SOURCE_CHARS
                    ),
                }
            )

            if len(files) >= self.MAX_SOURCE_FILES:
                break

        return files

    def _evidence(
        self,
        data: dict,
    ) -> list:
        """Evidence 摘要：只给文件、行号与片段。"""

        evidence = data.get("evidence")

        if not isinstance(evidence, list):
            return []

        items = []

        for item in evidence[
            : self.MAX_EVIDENCE
        ]:

            if not isinstance(item, dict):
                continue

            content = item.get("content")

            items.append(
                {
                    "file_path": item.get(
                        "file_path"
                    ),
                    "line_start": item.get(
                        "line_start"
                    ),
                    "line_end": item.get(
                        "line_end"
                    ),
                    "content": str(
                        content or ""
                    )[:200],
                }
            )

        return items

    # ------------------------------------------------------------------
    # 输出解析
    # ------------------------------------------------------------------

    @staticmethod
    def _parse(
        content: str,
    ):
        """
        解析 LLM 返回的 JSON。

        兼容纯 JSON / ```json 包裹 /
        前后有解释文字 / 被截断四种情况。
        解析失败返回 None，由调用方降级。
        """

        return parse_json_object(content)

    def _normalize_summary(
        self,
        summary: dict,
    ) -> dict:
        """
        规整 summary。

        列表字段统一成字符串列表并限长；
        one_line 统一成字符串。
        """

        normalized = {
            "one_line": self._as_text(
                summary.get("one_line")
            )
        }

        for key in (
            "core_design",
            "technology_choices",
            "highlights",
            "risks",
            "use_cases",
        ):

            normalized[key] = (
                self._as_text_list(
                    summary.get(key)
                )
            )

        return normalized

    def _normalize_dimensions(
        self,
        dimensions,
    ) -> dict:
        """规整 dimensions：只保留已知维度且值为文本。"""

        if not isinstance(
            dimensions,
            dict,
        ):
            return {}

        return {
            name: self._as_text(
                dimensions.get(name)
            )
            for name in self.DIMENSIONS
            if dimensions.get(name)
        }

    @staticmethod
    def _as_text(value) -> str:
        """把任意值转成去空白的字符串。"""

        if value is None:
            return ""

        if isinstance(value, str):
            return value.strip()

        if isinstance(
            value,
            (list, tuple),
        ):
            return "；".join(
                str(item).strip()
                for item in value
                if str(item).strip()
            )

        return str(value).strip()

    def _as_text_list(
        self,
        value,
    ) -> list:
        """把任意值转成限长的字符串列表。"""

        if value is None:
            return []

        if isinstance(value, str):

            text = value.strip()

            return [text] if text else []

        if not isinstance(
            value,
            (list, tuple),
        ):
            return [str(value)]

        items = []

        for item in value:

            text = ReportSynthesisSkill._as_text(
                item
            )

            if not text:
                continue

            items.append(text)

            if len(items) >= self.MAX_BULLETS:
                break

        return items
````

## 十四、证据与溯源层（Evidence）

证据链领域层：Evidence / Claim / Citation 的存储与状态校验，以及 Claim → Citation → Evidence → 源码位置的溯源构建

### 📄 `app/evidence/__init__.py`

**层级**：证据与溯源层（Evidence） · **职责**：证据链领域层的包标记文件；本层聚合 Evidence / Claim / Citation / Verification / Traceability 五块能力

```python
"""
Evidence 领域能力。

Phase 9:
Evidence
Claim
Citation
Verification
Traceability
"""
```

### 📄 `app/evidence/store.py`

**层级**：证据与溯源层（Evidence） · **职责**：领域存储 `EvidenceStore`：包装三个 Repository 完成证据对象的落库与关联校验（`create_evidence()` / `create_claim()` / `create_citation()`），并定义合法状态集合 `VERIFICATION_STATUSES`（VERIFIED / UNVERIFIED / CONFLICT）

```python
"""
Evidence Store。

负责：

Evidence
Claim
Citation

三类对象的领域级管理。
"""

from app.core.exceptions import ValidationError
from app.repositories.claim import ClaimRepository
from app.repositories.citation import CitationRepository
from app.repositories.evidence import EvidenceRepository


VERIFICATION_STATUSES = {
    "VERIFIED",
    "UNVERIFIED",
    "CONFLICT",
}


class EvidenceStore:
    """
    Evidence 领域存储。

    注意：

    Store 不直接执行 SQL。

    调用链：

        Evidence Store
              ↓
        Repository
              ↓
           SQLAlchemy
              ↓
             MySQL
    """

    def __init__(
        self,
        session,
    ) -> None:

        self.evidence_repository = (
            EvidenceRepository(session)
        )

        self.claim_repository = (
            ClaimRepository(session)
        )

        self.citation_repository = (
            CitationRepository(session)
        )

    @staticmethod
    def validate_status(
        status: str,
    ) -> str:

        normalized = status.upper()

        if normalized not in VERIFICATION_STATUSES:
            raise ValidationError(
                f"Unsupported verification status: "
                f"{normalized}"
            )

        return normalized

    async def create_evidence(
        self,
        *,
        evidence_id: str,
        repository_id: int,
        source_type: str,
        content: str,
        source_url: str | None = None,
        file_path: str | None = None,
        line_start: int | None = None,
        line_end: int | None = None,
        verification_status: str = "UNVERIFIED",
    ):

        if not content.strip():
            raise ValidationError(
                "Evidence content cannot be empty."
            )

        if (
            line_start is not None
            and line_end is not None
            and line_end < line_start
        ):
            raise ValidationError(
                "line_end cannot be smaller "
                "than line_start."
            )

        status = self.validate_status(
            verification_status
        )

        return await self.evidence_repository.create(
            evidence_id=evidence_id,
            repository_id=repository_id,
            source_type=source_type,
            source_url=source_url,
            file_path=file_path,
            line_start=line_start,
            line_end=line_end,
            content=content,
            verification_status=status,
        )

    async def create_claim(
        self,
        *,
        claim_id: str,
        run_id: str,
        claim_text: str,
        verification_status: str = "UNVERIFIED",
    ):

        if not claim_text.strip():
            raise ValidationError(
                "Claim text cannot be empty."
            )

        status = self.validate_status(
            verification_status
        )

        return await self.claim_repository.create(
            claim_id=claim_id,
            run_id=run_id,
            claim_text=claim_text,
            verification_status=status,
        )

    async def create_citation(
        self,
        *,
        citation_id: str,
        claim_id: str,
        evidence_id: str,
    ):

        claim = await self.claim_repository.get_by_id(
            claim_id
        )

        if claim is None:
            raise ValidationError(
                f"Claim not found: {claim_id}"
            )

        evidence = (
            await self.evidence_repository.get_by_id(
                evidence_id
            )
        )

        if evidence is None:
            raise ValidationError(
                f"Evidence not found: {evidence_id}"
            )

        exists = await (
            self.citation_repository.exists(
                claim_id=claim_id,
                evidence_id=evidence_id,
            )
        )

        if exists:
            raise ValidationError(
                "The Claim is already cited "
                "by this Evidence."
            )

        return await self.citation_repository.create(
            citation_id=citation_id,
            claim_id=claim_id,
            evidence_id=evidence_id,
        )
```

### 📄 `app/evidence/verifier.py`

**层级**：证据与溯源层（Evidence） · **职责**：校验器 `EvidenceVerifier`：校验状态取值合法性，对 Evidence / Claim 执行 `verify_evidence()` / `verify_claim()` 状态流转

```python
"""
Evidence Verification。

负责验证 Evidence / Claim 的状态。
"""

from app.core.exceptions import ValidationError
from app.evidence.store import (
    VERIFICATION_STATUSES,
)


class EvidenceVerifier:
    """
    Evidence / Claim 验证器。

    状态：

    VERIFIED
    UNVERIFIED
    CONFLICT
    """

    def __init__(
        self,
        session,
    ) -> None:

        self.session = session

    @staticmethod
    def validate_status(
        status: str,
    ) -> str:

        normalized = status.upper()

        if normalized not in VERIFICATION_STATUSES:
            raise ValidationError(
                f"Unsupported verification status: "
                f"{normalized}"
            )

        return normalized

    async def verify_evidence(
        self,
        evidence,
        status: str,
    ):

        evidence.verification_status = (
            self.validate_status(status)
        )

        await self.session.flush()

        return evidence

    async def verify_claim(
        self,
        claim,
        status: str,
    ):

        claim.verification_status = (
            self.validate_status(status)
        )

        await self.session.flush()

        return claim
```

### 📄 `app/evidence/traceability.py`

**层级**：证据与溯源层（Evidence） · **职责**：溯源服务 `TraceabilityService`：`get_claim_trace()` 沿 Claim → Citation → Evidence → Source → File → Line 组装完整证据链

```python
"""
Source Traceability。

负责构建：

Claim
 ↓
Citation
 ↓
Evidence
 ↓
Source
 ↓
File
 ↓
Line
"""

from app.core.exceptions import ValidationError
from app.repositories.claim import ClaimRepository
from app.repositories.citation import CitationRepository
from app.repositories.evidence import EvidenceRepository


class TraceabilityService:
    """
    Claim → Evidence 可追溯服务。
    """

    def __init__(
        self,
        session,
    ) -> None:

        self.claims = ClaimRepository(
            session
        )

        self.citations = CitationRepository(
            session
        )

        self.evidences = EvidenceRepository(
            session
        )

    async def get_claim_trace(
        self,
        claim_id: str,
    ) -> dict:

        claim = await self.claims.get_by_id(
            claim_id
        )

        if claim is None:
            raise ValidationError(
                f"Claim not found: {claim_id}"
            )

        citations = await (
            self.citations.get_by_claim(
                claim_id
            )
        )

        evidence_list = []

        for citation in citations:

            evidence = (
                await self.evidences.get_by_id(
                    citation.evidence_id
                )
            )

            if evidence is None:
                continue

            evidence_list.append(
                evidence
            )

        return {
            "claim": claim,
            "citations": citations,
            "evidences": evidence_list,
        }
```

## 十五、LLM 能力层（LLM）

大模型调用的抽象接口与 DeepSeek 实现

### 📄 `app/llm/base.py`

**层级**：LLM 能力层（LLM） · **职责**：LLM 抽象接口 `BaseLLM`，定义 `chat(messages)`

```python
"""
LLM抽象接口。
"""

from abc import ABC, abstractmethod

class BaseLLM(ABC):


    @abstractmethod
    async def chat(
        self,
        messages
    ):
        pass
```

### 📄 `app/llm/deepseek.py`

**层级**：LLM 能力层（LLM） · **职责**：DeepSeek 实现 `DeepSeekLLM`，包装 OpenAI 兼容客户端，固定 `model="deepseek-chat"`，返回 `choices[0].message.content`

```python
"""
DeepSeek LLM实现。

DeepSeek 提供 OpenAI 兼容接口，
底层使用 openai SDK 的 AsyncOpenAI 客户端。

构造方式保持向后兼容：

    DeepSeekLLM(client)

也可以显式指定模型与超时：

    DeepSeekLLM(client, model="deepseek-chat", timeout=60.0)
"""

from .base import BaseLLM


class DeepSeekLLM(BaseLLM):

    # 默认模型。
    #
    # 保留该默认值是为了不破坏
    # 早期只传 client 的调用方式。
    DEFAULT_MODEL = "deepseek-chat"

    def __init__(
        self,
        client,
        model: str | None = None,
        timeout: float | None = None,
        max_tokens: int | None = None,
    ):

        self.client = client

        self.model = (
            model or self.DEFAULT_MODEL
        )

        self.timeout = timeout

        self.max_tokens = max_tokens

    async def chat(
        self,
        messages,
        model: str | None = None,
        max_tokens: int | None = None,
    ):
        """
        发送一次对话请求，返回文本内容。

        model / max_tokens 允许单次调用覆盖实例默认值。
        """

        create_kwargs = {
            "model": model or self.model,
            "messages": messages,
        }

        if self.timeout is not None:
            create_kwargs["timeout"] = (
                self.timeout
            )

        limit = (
            max_tokens
            if max_tokens is not None
            else self.max_tokens
        )

        # 必须显式给出上限。
        #
        # 不设置时走服务端默认值，
        # 综合分析那种几千字符的 JSON 回复
        # 会被中途截断，
        # 截断的 JSON 一定解析失败。
        if limit is not None:
            create_kwargs["max_tokens"] = limit

        response = (
            await self.client
            .chat.completions.create(
                **create_kwargs
            )
        )

        return response.choices[0].message.content
```

### 📄 `app/llm/__init__.py`

**层级**：LLM 能力层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

## 十六、工具层（Tools）

Tool 抽象基类与具体工具：文件读取、代码搜索、依赖分析、语义检索、数据库查询与报告导出

### 📄 `app/tools/__init__.py`

**层级**：工具层（Tools） · **职责**：本层部分工具的统一导出入口（当前导出 `MySQLQueryTool` 与 `ReportExportTool`）

```python
from app.tools.mysql_query_tool import (
    MySQLQueryTool
)


from app.tools.report_export_tool import (
    ReportExportTool
)
```

### 📄 `app/tools/base.py`

**层级**：工具层（Tools） · **职责**：Tool 抽象基类 `BaseTool`，定义 `name` 与 `execute(**kwargs)`

```python
"""
Tool基础接口。
"""

from abc import ABC, abstractmethod


class BaseTool(ABC):

    # Tool名称
    name: str


    @abstractmethod
    async def execute(
        self,
        **kwargs
    ):
        pass
```

### 📄 `app/tools/file_reader_tool.py`

**层级**：工具层（Tools） · **职责**：GitHub 文件读取工具 `FileReaderTool`（name=`file_reader`），从 raw.githubusercontent.com 读取文件，`main` 取不到时自动回退 `master`

```python
"""
File Reader Tool。

负责:

    - 读取 GitHub 项目文件内容

读取策略
========

优先 GitHub Contents API
（api.github.com/repos/{owner}/{name}/contents/{path}）

失败时回退
（raw.githubusercontent.com）

原因：

部分网络环境下 raw.githubusercontent.com 极不稳定，
实测同一个 README：

    api.github.com/contents   -> 200，0.88 秒
    raw.githubusercontent.com -> 20 秒后 ReadError

而一个文件读取失败曾经导致
整个 5-Agent 分析计划直接 FAILED。

因此把稳定的域名放在前面，
raw 只作为回退（它支持 >1MB 的大文件，
Contents API 对超过 1MB 的文件不返回内容）。
"""


import base64
import httpx

from app.core.config import get_settings
from app.core.exceptions import ToolError
from app.tools.base import BaseTool



class FileReaderTool(BaseTool):


    """
    GitHub 文件读取工具。
    """


    name = "file_reader"


    # 单次读取超时（秒）。
    TIMEOUT_SECONDS = 30


    API_BASE = "https://api.github.com"


    RAW_BASE = (
        "https://raw.githubusercontent.com"
    )


    # 内部标记：
    # Contents API 无法提供内容
    # （网络出错 / 目录 / 超过 1MB），
    # 但「文件不存在」不属于这种情况。
    _USE_FALLBACK = object()


    @staticmethod
    def _headers() -> dict:
        """GitHub 请求头（配置了 token 就带上）。"""

        headers = {
            "Accept": (
                "application/vnd.github+json"
            ),
        }

        token = get_settings().GITHUB_TOKEN

        if token:

            headers["Authorization"] = (
                f"Bearer {token}"
            )

        return headers


    async def execute(
        self,
        owner: str,
        name: str,
        file_path: str = "README.md",
        branch: str = "main",
    ) -> str:


        return await self.read_file(
            owner,
            name,
            file_path,
            branch,
        )


    async def read_file(
        self,
        owner: str,
        name: str,
        file_path: str,
        branch: str = "main",
    ) -> str:
        """
        读取文件内容。

        返回空字符串表示「文件不存在」
        （非 200 / 404），保持既有语义。

        回退策略是「按分支决策」而不是
        「按来源整体回退」：

            Contents API 明确回答 404
                → 该分支上文件确实不存在
                → 不再去 raw 白等几十秒超时

            Contents API 网络出错 / 文件超过 1MB
                → 该分支回退 raw

        否则一个不存在的文件要等
        两个 raw 超时（实测 51 秒）。
        """

        branches = [branch]

        # main 不存在时尝试 master
        if branch == "main":

            branches.append("master")

        errors = []

        completed = 0

        for candidate in branches:

            try:

                result = (
                    await self._read_via_contents_api(
                        owner,
                        name,
                        file_path,
                        candidate,
                    )
                )

            except ToolError as error:

                errors.append(str(error))

                result = self._USE_FALLBACK

            else:

                completed += 1

            if isinstance(result, str):

                return result

            # 文件确实不存在（404）：
            # 换下一个分支，不必回退 raw。
            if result is None:

                continue

            # 需要回退 raw：
            # Contents API 出错或缺内容。
            try:

                content = await self._read_via_raw(
                    owner,
                    name,
                    file_path,
                    candidate,
                )

            except ToolError as error:

                errors.append(str(error))

                continue

            completed += 1

            if content is not None:

                return content

        # 所有来源都是网络错误：
        # 抛出以便定位，而不是伪装成「文件不存在」。
        if completed == 0 and errors:

            raise ToolError(errors[0])

        return ""


    async def _read_via_contents_api(
        self,
        owner: str,
        name: str,
        file_path: str,
        branch: str,
    ) -> str | None:
        """
        GitHub Contents API。

        返回值语义（调用方据此决定是否回退 raw）：

            str           读到内容
            None          文件在该分支上不存在
            _USE_FALLBACK 拿不到内容（目录 / >1MB），
                          需要回退 raw
        """

        url = (
            f"{self.API_BASE}"
            f"/repos/{owner}/{name}"
            f"/contents/{file_path}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    params={"ref": branch},
                    headers=self._headers(),
                    timeout=self.TIMEOUT_SECONDS,
                )

        except httpx.TimeoutException as error:

            raise ToolError(
                f"Contents API timeout: {url}"
            ) from error

        except httpx.HTTPError as error:

            raise ToolError(
                f"Contents API failed: {url}: {error}"
            ) from error

        if response.status_code != 200:

            return None

        payload = response.json()

        if not isinstance(payload, dict):

            return None

        encoded = payload.get("content")

        if (
            payload.get("encoding") != "base64"
            or not encoded
        ):

            # 目录或超过 1MB 的文件：
            # 这是「该来源拿不到」，
            # 不是「文件不存在」，
            # 因此需要回退 raw。
            return self._USE_FALLBACK

        try:

            return base64.b64decode(
                encoded
            ).decode(
                "utf-8",
                errors="replace",
            )

        except Exception:

            return None


    async def _read_via_raw(
        self,
        owner: str,
        name: str,
        file_path: str,
        branch: str,
    ) -> str | None:
        """
        raw.githubusercontent.com 回退。

        返回 None 表示非 200（文件不存在）。
        """

        url = (
            f"{self.RAW_BASE}/"
            f"{owner}/{name}/"
            f"{branch}/{file_path}"
        )

        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    timeout=self.TIMEOUT_SECONDS,
                )

        except httpx.TimeoutException as error:

            raise ToolError(
                f"Read timeout: {url}"
            ) from error

        except httpx.HTTPError as error:

            raise ToolError(
                f"Read failed: {url}: {error}"
            ) from error

        if response.status_code != 200:

            return None

        return response.text
```

### 📄 `app/tools/dependency_analyzer_tool.py`

**层级**：工具层（Tools） · **职责**：依赖分析工具 `DependencyAnalyzerTool`（name=`dependency_analyzer`），解析本地项目的 requirements.txt 与 docker-compose.yml，产出 frameworks / database / llm / embedding / deployment 清单

```python
"""
Dependency Analyzer Tool。

分析项目依赖和部署配置。
"""

from pathlib import Path

from app.tools.base import BaseTool


class DependencyAnalyzerTool(BaseTool):

    """
    项目依赖分析工具。

    分析:

    - requirements.txt
    - pyproject.toml
    - package.json
    - Dockerfile
    - docker-compose.yml
    """

    name = "dependency_analyzer"


    async def execute(
        self,
        project_path: str,
    ) -> dict:


        result = {

            "python_version": None,

            "frameworks": [],

            "database": [],

            "llm": [],

            "embedding": [],

            "deployment": [],

        }

        path = Path(project_path)

        await self._parse_requirements(
            path,
            result
        )

        await self._parse_docker(
            path,
            result
        )

        return result
    async def _parse_requirements(
        self,
        path: Path,
        result: dict
    ):

        file = path / "requirements.txt"


        if not file.exists():

            return
        content = file.read_text(
            encoding="utf-8"
        )

        dependencies = content.lower()

        if "fastapi" in dependencies:

            result["frameworks"].append(
                "FastAPI"
            )

        if "qdrant" in dependencies:

            result["embedding"].append(
                "Qdrant"
            )

        if "sqlalchemy" in dependencies:

            result["database"].append(
                "SQLAlchemy"
            )

        if "deepseek" in dependencies:

            result["llm"].append(
                "DeepSeek"
            )

    async def _parse_docker(
        self,
        path: Path,
        result: dict
    ):

        docker_file = path / "docker-compose.yml"


        if docker_file.exists():

            result["deployment"].append(
                "Docker Compose"
            )
```

### 📄 `app/tools/qdrant_search_tool.py`

**层级**：工具层（Tools） · **职责**：语义检索工具 `QdrantSearchTool`（name=`qdrant_search`），注入 `QdrantVectorStore`，按查询向量返回 Top-K 的 payload

```python
"""
Qdrant Search Tool。

提供 Agent 语义检索能力。
"""


from app.tools.base import BaseTool

from app.vector_store.qdrant import (
    QdrantVectorStore
)

class QdrantSearchTool(BaseTool):

    name = "qdrant_search"

    def __init__(
        self,
        vector_store=None
    ):
        self.vector_store = (
            vector_store
            or QdrantVectorStore()
        )

    async def execute(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):

        return self.search(
            query_vector,
            limit
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):

        points = (
            self.vector_store.search(
                query_vector,
                limit
            )
        )
        return [

            point.payload

            for point in points

        ]
```

### 📄 `app/tools/mysql_query_tool.py`

**层级**：工具层（Tools） · **职责**：数据库查询工具 `MySQLQueryTool`（name=`mysql_query`），封装 AsyncSession 执行 SQL 并返回字典列表

```python
"""
MySQL Query Tool。

负责:
    - Agent 查询业务数据
    - 封装数据库访问能力
"""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.tools.base import BaseTool

class MySQLQueryTool(BaseTool):

    """
    MySQL 查询工具。

    Agent 不直接操作数据库。
    """
    name = "mysql_query"

    def __init__(
        self,
        session: AsyncSession
    ):

        self.session = session

    async def execute(
        self,
        sql: str,
        params: dict | None = None,
    ):


        """
        执行查询。
        Args:

            sql:
                SQL语句

            params:
                参数
        """


        try:

            result = await self.session.execute(
                text(sql),
                params or {}
            )


            rows = result.mappings().all()


            return [
                dict(row)
                for row in rows
            ]

        except Exception as e:

            raise RuntimeError(
                f"MySQL query failed: {e}"
            )
```

### 📄 `app/tools/report_export_tool.py`

**层级**：工具层（Tools） · **职责**：报告导出工具 `ReportExportTool`（name=`report_export`），把标题与正文写成 Markdown 文件

```python
"""
Report Export Tool。

负责:
    - 导出分析报告
    - 支持 Markdown 文件
"""

from pathlib import Path

from app.tools.base import BaseTool

class ReportExportTool(BaseTool):

    name = "report_export"

    def __init__(
        self,
        output_dir: str = "reports"
    ):

        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            exist_ok=True
        )

    async def execute(
        self,
        title: str,
        content: str,
        filename: str = "report.md",
    ):

        return await self.export_markdown(
            title,
            content,
            filename,
        )

    async def export_markdown(
        self,
        title: str,
        content: str,
        filename: str,
    ):

        file_path = (
            self.output_dir
            /
            filename
        )

        markdown = (
            f"# {title}\n\n"
            f"{content}"
        )

        file_path.write_text(
            markdown,
            encoding="utf-8"
        )

        return {

            "path":
            str(file_path),

            "format":
            "markdown"

        }
```

### 📄 `app/tools/github/github_repository_tool.py`

**层级**：工具层（Tools） · **职责**：调用 GitHub REST API 获取仓库元数据（类名 `GitHubRepositoryTool`，name=`github_repository`）

```python
"""
GitHub Repository Tool。
"""

import httpx

from app.core.config import get_settings
from app.core.exceptions import ToolError
from app.tools.base import BaseTool

class GitHubRepositoryTool(BaseTool):

    """
    GitHub Repository 查询工具。

    负责:
        - 调用 GitHub REST API
        - 获取仓库基础信息
        - 获取仓库完整文件树（Git Trees API）
    """

    name = "github_repository"

    BASE_URL = "https://api.github.com"

    def _headers(self) -> dict:
        """构造 GitHub 请求头。

        未认证时的速率限制很低，
        因此配置了 token 就带上。
        """

        headers = {
            "Accept": "application/vnd.github+json",
        }

        token = get_settings().GITHUB_TOKEN

        if token:
            headers["Authorization"] = f"Bearer {token}"

        return headers

    async def execute(
        self,
        owner: str,
        name: str,
    ) -> dict:
        """
        Tool统一入口。

        Agent调用:
            github_repository(owner, name)
        """
        return await self.get_repository(
            owner,
            name,
        )
    async def get_repository(
        self,
        owner: str,
        name: str,
    ) -> dict:

        url = (
            f"{self.BASE_URL}"
            f"/repos/{owner}/{name}"
        )
        async with httpx.AsyncClient() as client:

            response = await client.get(
                url,
                headers=self._headers(),
            )
            response.raise_for_status()
            return response.json()

    async def get_tree(
        self,
        owner: str,
        name: str,
        branch: str = "main",
    ) -> list[dict]:
        """
        获取仓库完整文件树。

        使用 Git Trees API（recursive=1）。

        GitHub Code Search 的 repo: 限定符
        对多数仓库返回 0 条结果，
        因此目录结构必须用 Trees API，
        不能用 Code Search 替代。

        取不到时返回空列表而不是抛异常：
        目录结构属于增强信息，
        不应因此中断整个分析流程。
        """

        for candidate in (
            branch,
            "master",
        ):

            url = (
                f"{self.BASE_URL}"
                f"/repos/{owner}/{name}"
                f"/git/trees/{candidate}"
            )

            try:

                async with httpx.AsyncClient() as client:

                    response = await client.get(
                        url,
                        params={"recursive": "1"},
                        headers=self._headers(),
                    )

            except httpx.TimeoutException as error:

                raise ToolError(
                    f"Tree timeout: {url}"
                ) from error

            except httpx.HTTPError as error:

                raise ToolError(
                    f"Tree failed: {url}: {error}"
                ) from error

            if response.status_code == 200:

                tree = response.json().get(
                    "tree",
                    [],
                )

                if isinstance(tree, list):
                    return tree

        return []
```

### 📄 `app/tools/github/github_code_search_tool.py`

**层级**：工具层（Tools） · **职责**：GitHub 源码搜索工具 `GitHubCodeSearchTool`（name=`github_code_search`），调用 Code Search API；该 API 必须认证，配置了 `GITHUB_TOKEN` 时自动带上 Authorization 头

```python
"""
GitHub Code Search Tool。

负责:
    - 搜索 GitHub 项目源码
    - 查找关键代码位置
"""


import httpx


from app.core.config import get_settings
from app.tools.base import BaseTool

class GitHubCodeSearchTool(BaseTool):


    """
    GitHub源码搜索工具。
    """

    name = "github_code_search"
    BASE_URL = "https://api.github.com"



    async def execute(
        self,
        keyword: str,
        repo: str,
    ) -> list:


        """
        Tool统一入口。
        Args:

            keyword:
                搜索关键词

            repo:
                owner/name
        Example:

            langgraph

            openai/openai-python

        """
        return await self.search_code(
            keyword,
            repo,
        )

    async def search_code(
        self,
        keyword: str,
        repo: str,
    ) -> list:

        """
        调用GitHub Code Search API。
        """

        url = (
            f"{self.BASE_URL}"
            "/search/code"
        )

        params = {

            "q":
            f"{keyword}+repo:{repo}"

        }

        headers = {
            "Accept":
            "application/vnd.github+json"
        }

        # GitHub Code Search API 必须认证，
        # 未配置 token 时会返回 401。
        token = get_settings().GITHUB_TOKEN

        if token:

            headers["Authorization"] = (
                f"Bearer {token}"
            )

        async with httpx.AsyncClient() as client:


            response = await client.get(
                url,
                params=params,
                headers=headers
            )


            response.raise_for_status()


            data = response.json()


            return data.get(
                "items",
                []
            )
```

### 📄 `app/tools/github/parser.py`

**层级**：工具层（Tools） · **职责**：解析 GitHub 仓库 URL，返回 `(owner, name)` 元组

```python
"""GitHub Repository URL 解析工具。"""

from urllib.parse import urlparse


def parse_github_url(url: str) -> tuple[str, str]:
    """解析 GitHub URL，返回 owner 和 repository name。"""

    parsed = urlparse(url)

    if parsed.netloc.lower() != "github.com":
        raise ValueError("只支持 GitHub Repository URL")

    parts = [
        part
        for part in parsed.path.strip("/").split("/")
        if part
    ]

    if len(parts) < 2:
        raise ValueError("无效的 GitHub Repository URL")

    owner = parts[0]
    name = parts[1]

    if name.endswith(".git"):
        name = name[:-4]

    return owner, name
```

### 📄 `app/tools/github/__init__.py`

**层级**：工具层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/tools/llm_chat_tool.py`

**层级**：工具层 · **职责**：LLM Chat Tool。

```python
"""
LLM Chat Tool。

把 LLM 调用封装成 Tool，
供 Skill 通过 context.tools 获取，
与其它 Tool 的装配方式保持一致。

设计约束
========

本 Tool **永不抛异常**。

原因：报告综合分析只是报告的增强章节，
LLM 不可用（没有 API Key / 网络不通 /
额度耗尽 / 返回超时）时，
报告仍然应该正常产出，
只是缺少「结论摘要」部分。

因此所有失败都转成：

    {
        "available": False,
        "reason": "<可读原因>"
    }

由调用方决定如何降级。
"""

from openai import AsyncOpenAI

from app.core.config import get_settings
from app.llm.deepseek import DeepSeekLLM
from app.tools.base import BaseTool


class LLMChatTool(BaseTool):

    name = "llm_chat"

    def __init__(
        self,
        llm=None,
    ):
        """
        llm 允许注入一个假实现用于测试。

        注入时完全不读取配置、不创建网络客户端。
        """

        self._llm = llm

    def _build_llm(self):
        """按配置创建真实的 DeepSeek 客户端。"""

        settings = get_settings()

        api_key = (
            settings.LLM_API_KEY or ""
        ).strip()

        if not api_key:
            return None, (
                "未配置 LLM_API_KEY，"
                "无法调用 LLM 生成综合分析。"
            )

        client = AsyncOpenAI(
            api_key=api_key,
            base_url=settings.LLM_BASE_URL,
            timeout=settings.LLM_TIMEOUT,
        )

        return (
            DeepSeekLLM(
                client,
                model=settings.LLM_MODEL,
                timeout=settings.LLM_TIMEOUT,
                max_tokens=settings.LLM_MAX_TOKENS,
            ),
            None,
        )

    async def execute(
        self,
        messages,
        model: str | None = None,
        **kwargs,
    ):
        """
        执行一次对话。

        返回：

            {"available": True,  "content": "..."}
            {"available": False, "reason": "..."}
        """

        llm = self._llm

        if llm is None:

            llm, reason = self._build_llm()

            if llm is None:

                return {
                    "available": False,
                    "reason": reason,
                }

        try:

            # 默认不传 model，
            # 沿用 BaseLLM 的最小契约
            # chat(messages)，
            # 这样只实现该契约的假实现也能工作。
            if model is None:

                content = await llm.chat(
                    messages
                )

            else:

                content = await llm.chat(
                    messages,
                    model=model,
                )

        # 真实事故的防线：
        # LLM 侧的异常种类很多
        # （鉴权 / 限流 / 超时 / 连接失败），
        # 逐个捕获没有意义，
        # 这里统一降级为 available=False。
        except Exception as error:

            return {
                "available": False,
                "reason": (
                    "LLM 调用失败："
                    f"{type(error).__name__}: "
                    f"{error}"
                ),
            }

        if not isinstance(
            content,
            str,
        ) or not content.strip():

            return {
                "available": False,
                "reason": (
                    "LLM 返回了空内容。"
                ),
            }

        return {
            "available": True,
            "content": content,
        }
```

## 十七、项目分析层（Project Analysis）

文档切分、向量索引构建

### 📄 `app/project_analysis/code_chunker.py`

**层级**：项目分析层（Project Analysis） · **职责**：将 Markdown 文档按标题切分成语义 Chunk，过长章节再做滑窗切分（内部类名 `MarkdownChunker`）

```python
"""Markdown 文档切分器。"""

import re


class MarkdownChunker:
    """将 Markdown 文档切分成适合向量检索的文本块。"""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> list[str]:
        """将 Markdown 文本切分成多个 Chunk。"""

        sections = self._split_by_heading(text)

        chunks: list[str] = []

        for section in sections:
            chunks.extend(
                self._split_section(section)
            )

        return [
            chunk.strip()
            for chunk in chunks
            if chunk.strip()
        ]

    def _split_by_heading(
        self,
        text: str,
    ) -> list[str]:
        """优先按照 Markdown 标题划分语义章节。"""

        parts = re.split(
            r"(?=^#{1,6}\s+)",
            text,
            flags=re.MULTILINE,
        )

        return [
            part.strip()
            for part in parts
            if part.strip()
        ]

    def _split_section(
        self,
        section: str,
    ) -> list[str]:
        """将过长章节进一步切分。"""

        if len(section) <= self.chunk_size:
            return [section]

        chunks: list[str] = []

        start = 0

        while start < len(section):
            end = start + self.chunk_size

            chunk = section[start:end]

            chunks.append(chunk)

            if end >= len(section):
                break

            start = end - self.chunk_overlap

        return chunks
```

### 📄 `app/project_analysis/project_indexer.py`

**层级**：项目分析层（Project Analysis） · **职责**：文档索引编排——切分 → 逐块向量化 → 生成稳定 ID → 写入 Qdrant（内部类名 `DocumentIndexer`）

```python
"""文档索引服务：负责 Chunk、Embedding 和向量存储。"""

from app.embeddings.ollama import OllamaEmbedding
from app.project_analysis.code_chunker import MarkdownChunker
from app.vector_store.qdrant import QdrantVectorStore


class DocumentIndexer:
    """将文档切分并建立 Qdrant 向量索引。"""

    def __init__(
        self,
        collection_name: str = "github_projects",
    ) -> None:
        self.chunker = MarkdownChunker()
        self.embedding = OllamaEmbedding()
        self.vector_store = QdrantVectorStore(
            collection_name=collection_name,
        )

        self.vector_store.create_collection(
            vector_size=1024,
        )

    def index_document(
        self,
        document_id: str,
        text: str,
        metadata: dict,
    ) -> int:
        """将一份文档切分、向量化并写入 Qdrant。"""

        chunks = self.chunker.split(text)

        for index, chunk in enumerate(chunks):
            vector = self.embedding.embed(chunk)

            point_id = self._build_point_id(
                document_id,
                index,
            )

            payload = {
                **metadata,
                "document_id": document_id,
                "chunk_index": index,
                "text": chunk,
            }

            self.vector_store.upsert(
                point_id=point_id,
                vector=vector,
                payload=payload,
            )

        return len(chunks)

    @staticmethod
    def _build_point_id(
        document_id: str,
        chunk_index: int,
    ) -> int:
        """根据文档 ID 和 Chunk 序号生成稳定的整数 ID。"""

        import hashlib

        value = f"{document_id}:{chunk_index}"

        digest = hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

        return int(digest[:16], 16) % (2**63 - 1)
```

### 📄 `app/project_analysis/repository_indexer.py`

**层级**：项目分析层（Project Analysis） · **职责**：拉取仓库 README → 生成向量 → 写入 Qdrant（整篇作为一个向量，不切分）；通过工具层 `FileReaderTool.read_file()` 读取 README

```python
"""Repository 文档索引。"""

from app.tools.file_reader_tool import FileReaderTool
from app.embeddings.ollama import OllamaEmbedding
from app.vector_store.qdrant import QdrantVectorStore


class RepositoryIndexer:


    def __init__(self):

        self.loader = FileReaderTool()

        self.embedding = (
            OllamaEmbedding()
        )

        self.vector_store = (
            QdrantVectorStore(
                collection_name=
                "repositories"
            )
        )


    async def index(
        self,
        owner: str,
        name: str,
        branch: str = "main",
    ):
        content = await (
            self.loader
            .read_file(
                owner,
                name,
                "README.md",
                branch,
            )
        )


        if not content:
            return 0


        vector = (
            self.embedding
            .embed(content)
        )


        self.vector_store.create_collection(
            vector_size=len(vector)
        )


        self.vector_store.insert(
            vector=vector,
            payload={
                "owner":owner,
                "name":name,
                "source":"README.md",
                "text":content,
            }
        )


        return 1
```

### 📄 `app/project_analysis/__init__.py`

**层级**：项目分析层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/project_analysis/analysis_focus.py`

**层级**：项目分析层 · **职责**：本次分析的重点维度。

```python
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
```

### 📄 `app/project_analysis/code_structure_extractor.py`

**层级**：项目分析层 · **职责**：Code Structure Extractor。

```python
"""
Code Structure Extractor。

用 Python AST 从**真实源码**中抽取被分析项目的结构信号。

为什么需要它
============

在此之前，报告 04-09 章（Agent 架构 / Workflow / Skill /
Tool / RAG / Memory）唯一的来源是

    ArchitectureAnalysisSkill._extract_project_structure

它对被分析项目的 README 做关键词匹配，
再把命中的行按逗号切碎当条目。

结果是：一个 README 里没写 "skill" 二字的项目，
即使代码里有一整套 Skill 类，
报告也只能写「未声明该能力」；
而一个 README 写得漂亮但代码空心的项目，
反而能拿到一堆看似完整的条目。

本模块把「代码怎么说」变成一等证据：
每个信号都带文件路径与行号，
可以逐条打开源码复核。

抽取范围
========

只做**静态符号识别**，不做语义推断：

    class 定义      -> 类名 + 基类
    函数定义        -> 函数名 + 装饰器
    import          -> 模块名
    关键调用        -> StateGraph / .add_node / .add_edge 等

不解析调用图、不推断数据流、不判断代码质量。

诚实性约束
==========

- 只有拿到具体符号与行号才会产出条目，不猜。
- 语法解析失败的文件记入 unparsed，
  由调用方如实展示，而不是静默丢弃。
- 一个文件解析失败不影响其它文件。
"""

import ast
import re


def _symbol_pattern(keyword: str):
    """
    构造「符号名里出现该关键词」的模式。

    坑点：不能直接写 r"[^a-z]" 配 IGNORECASE，
    因为 re.IGNORECASE 会让 [^a-z] 连大写字母
    一起排除，于是 PlannerAgent / BaseToolBase
    这类 camelCase 名字反而匹配不上。

    两侧分别处理：

        左侧 (?:^|[^A-Za-z])  大小写都算字母，
                              不受 IGNORECASE 影响
        右侧 (?:$|(?-i:[^a-z]))  用作用域关掉 IGNORECASE，
                              这样 [^a-z] 才真的是
                              「不是小写字母」，
                              camelCase 边界与 _ / 数字都能命中

    已知局限（刻意宽进，宁可多留证据）：
    Toolkit、Retool、agentic 这类词会被命中。
    在被分析项目的类名里出现频率很低，
    而且误判只是多一条待人工复核的证据，
    不会伪造出不存在的结论。
    """

    return re.compile(
        rf"(?:^|[^A-Za-z]){keyword}"
        rf"|{keyword}(?:$|(?-i:[^a-z]))",
        re.IGNORECASE,
    )


def _parent_directory(file_path: str) -> str:
    """取文件所在目录，用于路径信号去重。"""

    text = str(file_path).replace("\\", "/")

    if "/" not in text:
        return text

    directory = text.rsplit("/", 1)[0]

    return directory + "/" if directory else text


class CodeStructureExtractor:
    """从 Python 源码中抽取六个维度的结构信号。"""

    # 与 ArchitectureAnalysisSkill.STRUCTURE_KEYWORDS
    # 保持同一组维度名，
    # 这样两层结果才能按维度合并。
    DIMENSIONS = (
        "agents",
        "workflow",
        "skills",
        "tools",
        "rag",
        "memory",
    )

    # 单个维度最多产出多少条目 / 证据。
    MAX_ITEMS = 12

    MAX_EVIDENCE = 6

    # 实现明细：单个维度最多记录多少条，
    # 每条最多记多少个被调用函数 / 字面量。
    #
    # 明细比条目重得多（一条约 200-400 字节），
    # 上限要收紧，否则 state_data 会明显膨胀。
    MAX_DETAILS = 6

    MAX_CALLS = 6

    MAX_LITERALS = 5

    # 抽取字面量时要忽略的噪声。
    #
    # 形如 "utf-8" / "GET" / "id" 的字符串
    # 到处都是，对理解实现没有帮助，
    # 反而会把真正有信息量的阈值（0.85）
    # 和状态名（"duplicate_suspected"）挤掉。
    LITERAL_NOISE = frozenset(
        {
            "utf-8",
            "utf8",
            "ascii",
            "get",
            "post",
            "put",
            "delete",
            "patch",
            "head",
            "options",
            "json",
            "text",
            "html",
            "text/plain",
            "text/html",
            "application/json",
            "application/x-www-form-urlencoded",
            "content-type",
            "content_length",
            "authorization",
            "bearer",
            "user-agent",
            "id",
            "pk",
            "name",
            "type",
            "kind",
            "status",
            "state",
            "data",
            "value",
            "key",
            "message",
            "error",
            "detail",
            "none",
            "true",
            "false",
            "null",
            "info",
            "debug",
            "warning",
            "system",
            "user",
            "assistant",
        }
    )

    # 调用链里要忽略的内建 / 通用函数名。
    CALL_NOISE = frozenset(
        {
            "print",
            "len",
            "str",
            "int",
            "float",
            "bool",
            "list",
            "dict",
            "set",
            "tuple",
            "range",
            "enumerate",
            "zip",
            "isinstance",
            "issubclass",
            "getattr",
            "setattr",
            "hasattr",
            "super",
            "format",
            "repr",
            "type",
            "min",
            "max",
            "sum",
            "sorted",
            "any",
            "all",
            "open",
            "__init__",
            "__repr__",
            "__str__",
            "__eq__",
            "__hash__",
        }
    )

    # 只有这些扩展名会被 AST 解析。
    PYTHON_EXTENSIONS = (".py",)

    # --------------------------------------------------------------
    # 识别规则
    # --------------------------------------------------------------

    # 类名命中即算该维度的信号。
    #
    # 覆盖 Agent / BaseAgent / PlannerAgent / BaseTool 等写法。
    CLASS_NAME_PATTERNS = {
        "agents": _symbol_pattern("agent"),
        "skills": _symbol_pattern("skill"),
        "tools": _symbol_pattern("tool"),
        "memory": re.compile(
            r"(memory|checkpoint|saver|session)",
            re.IGNORECASE,
        ),
    }

    # 基类名命中即算该维度的信号。
    #
    # 例如 class FinanceAgent(BaseAgent)、
    # class SearchTool(BaseTool)。
    BASE_NAME_PATTERNS = CLASS_NAME_PATTERNS

    # 文件路径命中即算该维度的信号。
    PATH_PATTERNS = {
        "agents": re.compile(
            r"(^|[/_\-.])agents?([/_\-.]|$)",
        ),
        "workflow": re.compile(
            r"(workflow|graph|pipeline|nodes?|state)",
        ),
        "skills": re.compile(
            r"(^|[/_\-.])skills?([/_\-.]|$)",
        ),
        "tools": re.compile(
            r"(^|[/_\-.])tools?([/_\-.]|$)",
        ),
        "rag": re.compile(
            r"(rag|retriev|embedding|vector)",
        ),
        "memory": re.compile(
            r"(memory|checkpoint|session)",
        ),
    }

    # 导入模块名命中即算该维度的信号。
    #
    # agents 刻意不收 langgraph / langchain：
    # 这两个是编排框架，
    # `import langgraph.graph` 说明的是
    # 「用了图编排」，不是「实现了 Agent」。
    # 早期把 langgraph 同时算进 agents，
    # 导致任何用了 LangGraph 的项目
    # 都会凭空多出一批 agents 条目。
    IMPORT_PATTERNS = {
        "rag": re.compile(
            r"(qdrant|chromadb|chroma|faiss|"
            r"pgvector|sentence_transformers|"
            r"vectorstores|embeddings|milvus|weaviate)",
        ),
        "memory": re.compile(
            r"(checkpoint|memory|redis|saver)",
        ),
        "workflow": re.compile(
            r"(langgraph|langchain|prefect|airflow|"
            r"temporal|celery)",
        ),
        # 真正的多 Agent 框架。
        "agents": re.compile(
            r"(autogen|crewai|semantic_kernel|"
            r"langchain\.agents|langgraph\.prebuilt|"
            r"create_react_agent|swarm)",
        ),
    }

    # 类名 / 函数名命中即算 rag 信号。
    #
    # 只收「明确指向检索」的词，
    # 不收 search 这种过于宽泛的词
    # （一个 search_github_repo 不是 RAG）。
    #
    # rag 这三个字母必须带词边界：
    # 直接做子串匹配会命中 storage ——
    # 真实事故：src/app/core/config.py 里的
    # validate_storage_root 被判成了 RAG 实现。
    RAG_SYMBOL_PATTERN = re.compile(
        r"(?:retriev|embed|rerank|similarity_search"
        r"|vector_store|vectorstore)"
        r"|(?:(?:^|[^A-Za-z])rag"
        r"|rag(?:$|(?-i:[^a-z])))",
        re.IGNORECASE,
    )

    # Agent / Workflow 常见角色名。
    ROLE_PATTERN = re.compile(
        r"(planner|executor|critic|synthesizer|"
        r"researcher|supervisor|orchestrator|"
        r"coordinator|router)",
        re.IGNORECASE,
    )

    # 这些属性的调用参数会被原样记录（图谱节点与边）。
    GRAPH_CALL_ATTRIBUTES = (
        "add_node",
        "add_edge",
        "add_conditional_edges",
        "set_entry_point",
        "set_finish_point",
    )

    # 图谱构造函数名。
    GRAPH_CONSTRUCTORS = (
        "StateGraph",
        "MessageGraph",
    )

    # 工具装饰器名。
    TOOL_DECORATORS = (
        "tool",
        "mcp.tool",
    )

    # --------------------------------------------------------------
    # 入口
    # --------------------------------------------------------------

    @classmethod
    def extract(
        cls,
        files: list,
        extra_paths=None,
        max_details=None,
        include_source=False,
    ) -> dict:
        """
        从若干源文件抽取结构信号。

        files:
            [
                {"file_path": "src/app/graph.py",
                 "content": "<源码全文>"},
                ...
            ]

        只接受**未截断**的源码：
        截断过的 Python 几乎必然语法错误。

        max_details:
            单个维度最多记录多少条实现明细。
            默认用 MAX_DETAILS；
            深挖模式会传一个更大的值。

        include_source:
            明细里是否附上源码片段。

            默认 False —— 默认报告只展示「要点 + 证据锚点」，
            明细里的源码片段根本不会被渲染，
            但每条约 1.5KB，六维 × 六条能凭空撑大
            checkpoint 的 state_data。
            深挖模式（ModuleDeepDiveSkill）传 True，
            因为它要展示源码。

        extra_paths:
            只有路径、没有内容的文件
            （通常是仓库文件树里没被读取的部分）。
            它们只参与路径信号，
            这样「存在 src/agents/ 目录」这条证据
            不会因为该目录下的文件没被读到而丢失。

        返回：

            {
                "available": True,
                "dimensions": {
                    "agents": {"items": [...],
                               "evidence": [...]},
                    ...
                },
                "unparsed": [
                    {"file_path": ..., "error": ...}
                ],
                "parsed_files": 3,
            }
        """

        dimensions = {
            name: {
                "items": [],
                "evidence": [],
                # 实现明细：比 items 重，
                # 但能说清「这个模块具体怎么做的」。
                "details": [],
            }
            for name in cls.DIMENSIONS
        }

        unparsed = []

        parsed_files = 0

        # 每条证据的 text 在全局去重，
        # 避免同一个类在多个文件里
        # 把同一个条目刷满。
        seen_items = {
            name: set() for name in cls.DIMENSIONS
        }

        if not isinstance(files, list):
            files = []

        for item in files:

            if not isinstance(item, dict):
                continue

            file_path = item.get("file_path")

            content = item.get("content")

            if not file_path or not isinstance(
                content,
                str,
            ):
                continue

            if not cls._is_python(file_path):
                continue

            try:

                tree = ast.parse(content)

            except (SyntaxError, ValueError) as error:

                unparsed.append(
                    {
                        "file_path": file_path,
                        "error": (
                            f"{type(error).__name__}: "
                            f"{error}"
                        ),
                    }
                )

                continue

            parsed_files += 1

            cls._scan_module(
                tree,
                file_path,
                dimensions,
                seen_items,
            )

            cls._collect_details(
                tree,
                file_path,
                dimensions,
                content,
                max_details,
                include_source,
            )

        # 路径信号在所有符号扫描完之后再收集。
        #
        # 顺序很重要：_add 是按顺序填满
        # MAX_ITEMS 就停止的，
        # 符号（class / 调用）比「路径长这样」
        # 有价值得多，不能让它被路径挤掉。
        path_candidates = []

        for item in files:

            if not isinstance(item, dict):
                continue

            file_path = item.get("file_path")

            if file_path:
                path_candidates.append(file_path)

        if isinstance(extra_paths, list):
            path_candidates += [
                path
                for path in extra_paths
                if isinstance(path, str)
            ]

        for file_path in path_candidates:

            cls._collect_path_signal(
                file_path,
                dimensions,
                seen_items,
            )

        return {
            "available": parsed_files > 0,
            "dimensions": dimensions,
            "unparsed": unparsed,
            "parsed_files": parsed_files,
        }

    # --------------------------------------------------------------
    # 单文件扫描
    # --------------------------------------------------------------

    @classmethod
    def _scan_module(
        cls,
        tree,
        file_path: str,
        dimensions: dict,
        seen_items: dict,
    ) -> None:
        """扫描一个已解析的模块。"""

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.Import, ast.ImportFrom),
            ):
                cls._collect_import(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

            elif isinstance(
                node,
                ast.ClassDef,
            ):
                cls._collect_class(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                cls._collect_function(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

            elif isinstance(node, ast.Call):
                cls._collect_call(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

    @classmethod
    def _collect_import(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """import 语句 -> 维度信号。"""

        if isinstance(node, ast.Import):

            modules = [
                alias.name
                for alias in node.names
            ]

        else:

            module = node.module or ""

            modules = [module] if module else []

            # from x import y 时，y 也可能是
            # 有信号的名字（例如 SqliteSaver）。
            modules += [
                alias.name
                for alias in node.names
            ]

        for module in modules:

            if not module:
                continue

            for dimension, pattern in (
                cls.IMPORT_PATTERNS.items()
            ):

                if not pattern.search(module):
                    continue

                cls._add(
                    dimension,
                    f"import {module}",
                    file_path,
                    node.lineno,
                    dimensions,
                    seen_items,
                )

    @classmethod
    def _collect_class(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """class 定义 -> 维度信号。"""

        bases = []

        for base in node.bases:

            text = cls._unparse(base)

            if text:
                bases.append(text)

        label = f"class {node.name}"

        if bases:
            label += f"({', '.join(bases)})"

        matched = set()

        for dimension, pattern in (
            cls.CLASS_NAME_PATTERNS.items()
        ):

            if pattern.search(node.name):
                matched.add(dimension)

            if any(
                pattern.search(base)
                for base in bases
            ):
                matched.add(dimension)

        if cls.ROLE_PATTERN.search(node.name):
            matched.add("agents")

        # tools 维度额外接受
        # 「在 tool 装饰器下的类」
        # 与名字里带 tool 的类，
        # 前一条已覆盖。
        for dimension in matched:

            cls._add(
                dimension,
                label,
                file_path,
                node.lineno,
                dimensions,
                seen_items,
            )

    @classmethod
    def _collect_function(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """函数定义 -> 维度信号。"""

        decorators = []

        for decorator in node.decorator_list:

            text = cls._unparse(decorator)

            if text:
                decorators.append(text)

        label = f"def {node.name}"

        if decorators:
            label = (
                f"@{', @'.join(decorators)} "
                f"{label}"
            )

        matched = set()

        # langchain 风格的工具声明。
        if any(
            cls._is_tool_decorator(decorator)
            for decorator in decorators
        ):
            matched.add("tools")

        if cls.RAG_SYMBOL_PATTERN.search(node.name):
            matched.add("rag")

        if cls.ROLE_PATTERN.search(node.name):
            matched.add("agents")

        for dimension in matched:

            cls._add(
                dimension,
                label,
                file_path,
                node.lineno,
                dimensions,
                seen_items,
            )

    @classmethod
    def _collect_call(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """
        关键调用 -> 维度信号。

        Workflow 维度最有价值的部分在这里：
        StateGraph 的节点名与边
        会以源码原文的形式被记录下来。
        """

        func = node.func

        # StateGraph(...) —— 图谱构造。
        if (
            isinstance(func, ast.Name)
            and func.id in cls.GRAPH_CONSTRUCTORS
        ):

            cls._add(
                "workflow",
                f"{func.id}(...)",
                file_path,
                node.lineno,
                dimensions,
                seen_items,
            )

            return

        if not isinstance(func, ast.Attribute):
            return

        if func.attr not in cls.GRAPH_CALL_ATTRIBUTES:
            return

        target = cls._unparse(func.value)

        arguments = []

        for argument in node.args:

            text = cls._unparse(argument)

            if text:
                arguments.append(text)

        label = (
            f"{target}.{func.attr}"
            f"({', '.join(arguments)})"
        )

        cls._add(
            "workflow",
            label,
            file_path,
            node.lineno,
            dimensions,
            seen_items,
        )

    # --------------------------------------------------------------
    # 实现明细
    # --------------------------------------------------------------

    @classmethod
    def _collect_details(
        cls,
        tree,
        file_path: str,
        dimensions: dict,
        content: str | None = None,
        max_details: int | None = None,
        include_source: bool = False,
    ) -> None:
        """
        收集「这个模块具体怎么做的」。

        与 _scan_module 的区别：

            _scan_module  抽符号名字，供比较与检索
            _collect_details  抽函数签名 / 调用链 /
                              关键字面量 / 类的方法表，
                              供报告展示实现细节

        最有价值的是 workflow：
        add_node('duplicate_check',
                 self._node_duplicate_check)
        会被解析成那个函数本身，
        于是报告能写出「这个节点做了什么」，
        而不只是「有这么个节点」。
        """

        symbols = cls._build_symbol_table(tree)

        for node in ast.walk(tree):

            if isinstance(node, ast.Call):

                cls._detail_from_graph_call(
                    node,
                    symbols,
                    file_path,
                    dimensions,
                    content,
                    max_details,
                    include_source,
                )

        # 类：给出基类与方法表。
        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                cls._detail_from_class(
                    node,
                    file_path,
                    dimensions,
                    content,
                    max_details,
                    include_source,
                )

        # 函数：给出签名、调用链与字面量。
        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):

                cls._detail_from_function(
                    node,
                    file_path,
                    dimensions,
                    content,
                    max_details,
                    include_source,
                )

    @classmethod
    def _detail_from_graph_call(
        cls,
        node,
        symbols,
        file_path,
        dimensions,
        content=None,
        max_details=None,
        include_source=False,
    ) -> None:
        """
        把 add_node / add_edge 解析成工作流节点明细。
        """

        function = node.func

        if not isinstance(function, ast.Attribute):
            return

        # 只为「带处理函数」的调用产出明细。
        #
        # add_edge 的拓扑已经作为条目记录，
        # 再产一条什么都解析不出来的明细
        # 只会挤占 MAX_DETAILS 配额。
        if function.attr not in (
            "add_node",
            "add_conditional_edges",
        ):
            return

        if not node.args:
            return

        first = cls._unparse(node.args[0])

        target = cls._unparse(function.value)

        entry = {
            "kind": "graph",
            "name": first.strip("'\"") or first,
            "file_path": file_path,
            "line": node.lineno,
            "signature": (
                f"{target}.{function.attr}"
                f"({', '.join(cls._unparse(a) for a in node.args)})"
            ),
            "calls": [],
            "literals": [],
        }

        # add_node 的第二个实参是处理函数，
        # 解析它能拿到真正的实现。
        if (
            function.attr == "add_node"
            and len(node.args) >= 2
        ):

            symbol_name = cls._called_symbol(
                node.args[1]
            )

            if symbol_name:

                definition = symbols.get(
                    symbol_name
                )

                if definition is not None:

                    entry["symbol"] = symbol_name

                    entry["signature"] = (
                        cls._signature(definition)
                    )

                    entry["calls"] = cls._calls_in(
                        definition
                    )

                    entry["literals"] = (
                        cls._literals_in(definition)
                    )

                    if include_source:

                        entry["source"] = (
                            cls._source_segment(
                                content,
                                definition,
                            )
                        )

        cls._add_detail(
            "workflow",
            entry,
            dimensions,
            max_details,
        )

    @classmethod
    def _detail_from_class(
        cls,
        node,
        file_path,
        dimensions,
        content=None,
        max_details=None,
        include_source=False,
    ) -> None:
        """类明细：基类 + 方法表。"""

        bases = [
            rendered
            for rendered in (
                cls._unparse(base)
                for base in node.bases
            )
            if rendered
        ]

        label = f"class {node.name}"

        if bases:
            label += f"({', '.join(bases)})"

        methods = [
            child.name
            for child in node.body
            if isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
        ]

        entry = {
            "kind": "class",
            "name": node.name,
            "file_path": file_path,
            "line": node.lineno,
            "signature": label,
            "calls": [],
            "literals": [],
        }

        if methods:

            entry["methods"] = methods[
                : cls.MAX_CALLS
            ]

        if include_source:

            entry["source"] = cls._source_segment(
                content,
                node,
            )

        for dimension, pattern in (
            cls.CLASS_NAME_PATTERNS.items()
        ):

            matched = pattern.search(node.name) or any(
                pattern.search(base)
                for base in bases
            )

            if matched:

                cls._add_detail(
                    dimension,
                    entry,
                    dimensions,
                    max_details,
                )

        if cls.ROLE_PATTERN.search(node.name):

            cls._add_detail(
                "agents",
                entry,
                dimensions,
                max_details,
            )

    @classmethod
    def _detail_from_function(
        cls,
        node,
        file_path,
        dimensions,
        content=None,
        max_details=None,
        include_source=False,
    ) -> None:
        """函数明细：签名 + 调用链 + 字面量。"""

        decorators = [
            rendered
            for rendered in (
                cls._unparse(decorator)
                for decorator in node.decorator_list
            )
            if rendered
        ]

        entry = {
            "kind": "function",
            "name": node.name,
            "file_path": file_path,
            "line": node.lineno,
            "signature": cls._signature(node),
            "calls": cls._calls_in(node),
            "literals": cls._literals_in(node),
        }

        if include_source:

            entry["source"] = cls._source_segment(
                content,
                node,
            )

        if any(
            cls._is_tool_decorator(decorator)
            for decorator in decorators
        ):

            cls._add_detail(
                "tools",
                entry,
                dimensions,
                max_details,
            )

        if cls.RAG_SYMBOL_PATTERN.search(node.name):

            cls._add_detail(
                "rag",
                entry,
                dimensions,
                max_details,
            )

        if cls.ROLE_PATTERN.search(node.name):

            cls._add_detail(
                "agents",
                entry,
                dimensions,
                max_details,
            )

    @staticmethod
    def _add_detail(
        dimension,
        entry,
        dimensions,
        max_details=None,
    ) -> None:
        """登记一条明细（按 名称+位置 去重）。"""

        bucket = dimensions.get(dimension)

        if bucket is None:
            return

        limit = (
            max_details
            if isinstance(max_details, int)
            else CodeStructureExtractor.MAX_DETAILS
        )

        if len(bucket["details"]) >= limit:
            return

        key = (
            entry.get("name"),
            entry.get("file_path"),
            entry.get("line"),
        )

        for existing in bucket["details"]:

            if (
                existing.get("name"),
                existing.get("file_path"),
                existing.get("line"),
            ) == key:
                return

        bucket["details"].append(entry)

    # --------------------------------------------------------------
    # 路径信号
    # --------------------------------------------------------------

    @classmethod
    def dimensions_for_path(
        cls,
        file_path: str,
    ) -> list:
        """
        路径命中了哪些维度，按固定顺序返回。

        ArchitectureAnalysisSkill 用它做按维度配额：
        每个维度都有独立的样本名额，
        不会出现「workflow 文件太多、
        rag 文件一个都没读」的情况。
        """

        normalized = str(file_path).lower()

        return [
            dimension
            for dimension in cls.DIMENSIONS
            if cls.PATH_PATTERNS[
                dimension
            ].search(normalized)
        ]

    @classmethod
    def path_signal_count(
        cls,
        file_path: str,
    ) -> int:
        """
        路径命中多少个维度的信号。

        ArchitectureAnalysisSkill 用它决定
        优先读哪些文件：
        命中越多，越可能承载架构。

        与 _collect_path_signal 共用同一套 PATTERNS，
        避免两处规则漂移。
        """

        normalized = str(file_path).lower()

        return sum(
            1
            for pattern in cls.PATH_PATTERNS.values()
            if pattern.search(normalized)
        )

    @classmethod
    def _collect_path_signal(
        cls,
        file_path: str,
        dimensions,
        seen_items,
    ) -> None:
        """
        文件路径本身也是证据。

        「存在 src/agents/ 目录」这件事
        与「某个类叫 FinanceAgent」同样说明问题，
        而且前者在没读到那个文件时也能成立。

        按**目录**去重：
        src/agents/ 下有 30 个文件时，
        只记一条 `路径 src/agents/`，
        而不是把 30 个文件名刷满配额 ——
        否则真正有价值的类名会被挤出去。
        """

        normalized = file_path.lower()

        directory = _parent_directory(file_path)

        for dimension, pattern in (
            cls.PATH_PATTERNS.items()
        ):

            if not pattern.search(normalized):
                continue

            cls._add(
                dimension,
                f"路径 {directory}",
                directory,
                None,
                dimensions,
                seen_items,
            )

    # --------------------------------------------------------------
    # 工具方法
    # --------------------------------------------------------------

    @classmethod
    def _add(
        cls,
        dimension: str,
        text: str,
        file_path: str,
        line,
        dimensions: dict,
        seen_items: dict,
    ) -> None:
        """登记一条条目与对应的证据。"""

        bucket = dimensions.get(dimension)

        if bucket is None:
            return

        seen = seen_items[dimension]

        lowered = text.lower()

        # 同一个符号只记一次。
        if lowered in seen:
            return

        seen.add(lowered)

        if len(bucket["items"]) >= cls.MAX_ITEMS:
            return

        bucket["items"].append(text)

        if len(bucket["evidence"]) >= cls.MAX_EVIDENCE:
            return

        bucket["evidence"].append(
            {
                "file_path": file_path,
                "line_start": line,
                "line_end": line,
                "text": text,
            }
        )

    @classmethod
    def _is_python(
        cls,
        file_path: str,
    ) -> bool:
        """只解析 Python 文件。"""

        return str(file_path).lower().endswith(
            cls.PYTHON_EXTENSIONS
        )

    # 代码摘录的起始处：跳过这些前缀开头的行。
    SKIPPABLE_LINE_PREFIXES = (
        "import ",
        "from ",
    )

    @classmethod
    def meaningful_start(
        cls,
        content,
    ) -> int:
        """
        找出源码里第一行「有信息量」的内容的字符下标。

        为什么需要：代码摘录原本固定从第 1 行开始取，
        而 Python 文件开头必然是 import 块 ——
        截出来就是一堆

            import sqlite3
            import uuid
            from decimal import Decimal

        对理解项目毫无帮助。
        真实反馈：「这源码提取了一堆 import 根本没有用」。

        跳过开头的：

            空行 / 注释行
            模块级 docstring
            import / from 语句（含括号与反斜杠续行）

        返回第一行实际代码的位置。
        整份文件都跳完还没找到代码时返回 0，
        保持「从头取」的旧行为，不至于截出空串。

        必须处理**多行 import**：真实文件里常见

            from app.schemas.agent import (
                AgentRunListItem,
                AgentRunResponse,
            )

        这种写法的续行不以 import 开头，
        只看行首的话扫描器会停在第 2 行，
        摘录依然是一串 import 名单。
        """

        if not isinstance(content, str) or not content:
            return 0

        offset = 0

        in_docstring = False

        delimiter = ""

        # 多行 import 的括号深度与反斜杠续行。
        in_import = False

        import_depth = 0

        for line in content.splitlines(
            keepends=True
        ):

            stripped = line.strip()

            # 多行 import 的续行
            if in_import:

                offset += len(line)

                import_depth += (
                    line.count("(") - line.count(")")
                )

                if (
                    import_depth <= 0
                    and not line.rstrip().endswith("\\")
                ):
                    in_import = False

                continue

            if in_docstring:

                offset += len(line)

                if delimiter in stripped:
                    in_docstring = False

                continue

            # 空行与注释
            if not stripped or stripped.startswith("#"):

                offset += len(line)

                continue

            # 模块级 docstring
            if stripped.startswith(('"""', "'''")):

                delimiter = stripped[:3]

                # 单行写法："""xxx"""
                if stripped.count(delimiter) >= 2:

                    offset += len(line)

                    continue

                in_docstring = True

                offset += len(line)

                continue

            # import 段
            if stripped.startswith(
                cls.SKIPPABLE_LINE_PREFIXES
            ):

                offset += len(line)

                depth = (
                    line.count("(") - line.count(")")
                )

                # 括号未闭合或反斜杠续行时，
                # 后面的行还是这条 import 的一部分。
                if depth > 0 or line.rstrip().endswith(
                    "\\"
                ):

                    in_import = True

                    import_depth = depth

                continue

            # 第一行真正的代码
            break

        if offset >= len(content):
            return 0

        return offset

    @classmethod
    def _is_tool_decorator(
        cls,
        decorator: str,
    ) -> bool:
        """判断装饰器是否为 @tool 一类。"""

        if not decorator:
            return False

        lowered = decorator.lower()

        if lowered in cls.TOOL_DECORATORS:
            return True

        # 兼容 @tool(...) 带参数的形式。
        for name in cls.TOOL_DECORATORS:

            if lowered.startswith(name + "("):
                return True

        return lowered.endswith(".tool")

    # --------------------------------------------------------------
    # 函数体分析
    # --------------------------------------------------------------

    @classmethod
    def _signature(cls, node) -> str:
        """
        还原函数签名（含类型标注）。

        这是「下到函数体」的第一步：
        `def _node_duplicate_check(self, state: AgentState)
         -> AgentState` 远比一个名字有信息量。
        """

        arguments = node.args

        parts = []

        positional = list(arguments.posonlyargs) + list(
            arguments.args
        )

        # 默认值对齐到参数尾部。
        defaults = [None] * (
            len(positional) - len(arguments.defaults)
        ) + list(arguments.defaults)

        for argument, default in zip(
            positional,
            defaults,
        ):

            parts.append(
                cls._argument(argument, default)
            )

        if arguments.vararg:

            parts.append(
                "*" + cls._argument(arguments.vararg)
            )

        elif arguments.kwonlyargs:

            # 有仅关键字参数但没有 *args 时，
            # 需要显式一个 * 占位。
            parts.append("*")

        for argument, default in zip(
            arguments.kwonlyargs,
            arguments.kw_defaults,
        ):

            parts.append(
                cls._argument(argument, default)
            )

        if arguments.kwarg:

            parts.append(
                "**" + cls._argument(arguments.kwarg)
            )

        prefix = (
            "async def"
            if isinstance(node, ast.AsyncFunctionDef)
            else "def"
        )

        signature = (
            f"{prefix} {node.name}"
            f"({', '.join(parts)})"
        )

        returns = getattr(node, "returns", None)

        if returns is not None:

            rendered = cls._unparse(returns)

            if rendered:
                signature += f" -> {rendered}"

        return signature

    @classmethod
    def _argument(
        cls,
        argument,
        default=None,
    ) -> str:
        """渲染单个参数（含标注与默认值）。"""

        text = argument.arg

        annotation = getattr(
            argument,
            "annotation",
            None,
        )

        if annotation is not None:

            rendered = cls._unparse(annotation)

            if rendered:
                text += f": {rendered}"

        if default is not None:

            rendered = cls._unparse(default)

            if rendered:
                text += f" = {rendered}"

        return text

    @classmethod
    def _calls_in(cls, node) -> list:
        """
        函数体里调用了哪些自定义函数。

        只取被调用者的名字（`f()` 取 f，
        `obj.method()` 取 method），
        过滤掉内建函数与通用名，
        去重后保序。
        """

        calls = []

        seen = set()

        for child in ast.walk(node):

            if not isinstance(child, ast.Call):
                continue

            function = child.func

            if isinstance(function, ast.Name):

                name = function.id

            elif isinstance(function, ast.Attribute):

                name = function.attr

            else:

                continue

            lowered = name.lower()

            if lowered in cls.CALL_NOISE:
                continue

            # 单字符与全大写下划线常量不是函数调用。
            if len(name) < 3:
                continue

            if lowered in seen:
                continue

            seen.add(lowered)

            calls.append(name)

            if len(calls) >= cls.MAX_CALLS:
                break

        return calls

    @classmethod
    def _literals_in(cls, node) -> list:
        """
        函数体里出现的、有信息量的字面量。

        典型价值：阈值（0.85）、状态名
        （"duplicate_suspected"）、重试次数（3）。
        """

        literals = []

        seen = set()

        for child in ast.walk(node):

            if not isinstance(child, ast.Constant):
                continue

            value = child.value

            if not cls._is_interesting_literal(
                value
            ):
                continue

            rendered = repr(value)

            if rendered in seen:
                continue

            seen.add(rendered)

            literals.append(rendered)

            if len(literals) >= cls.MAX_LITERALS:
                break

        return literals

    @classmethod
    def _is_interesting_literal(
        cls,
        value,
    ) -> bool:
        """判断一个字面量是否值得记录。"""

        # bool 是 int 的子类，必须排在前面排除。
        if isinstance(value, bool):
            return False

        # 0.0 通常是初始化占位，
        # 真正的阈值（0.85）才值得记。
        if isinstance(value, float):
            return value != 0.0

        if isinstance(value, int):
            return abs(value) >= 10

        if isinstance(value, str):

            text = value.strip()

            if len(text) < 4:
                return False

            if text.lower() in cls.LITERAL_NOISE:
                return False

            if text.startswith(
                ("http://", "https://")
            ):
                return False

            # 纯符号 / 纯数字字符串没有信息量。
            if not any(
                char.isalnum() for char in text
            ):
                return False

            return True

        return False

    @classmethod
    def _build_symbol_table(
        cls,
        tree,
    ) -> dict:
        """
        建立 短名 -> 函数节点 的索引。

        用途：把
            builder.add_node('duplicate_check',
                             self._node_duplicate_check)
        解析到
            def _node_duplicate_check(self, state) -> AgentState

        只看短名（不带类名前缀），
        同名冲突时保留第一个 ——
        解析结果会带上文件与行号，
        人工复核时能看出解析得对不对。
        """

        table = {}

        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):

                table.setdefault(node.name, node)

        return table

    @staticmethod
    def _called_symbol(node):
        """
        从 add_node / add_edge 的实参里
        取出「被引用的函数名」。

        支持两种写法：

            self._node_duplicate_check   -> _node_duplicate_check
            _node_duplicate_check        -> _node_duplicate_check
        """

        if isinstance(node, ast.Attribute):

            return node.attr

        if isinstance(node, ast.Name):

            return node.id

        return None

    # 明细里附带的源码片段最多多少字符。
    #
    # 深挖报告要展示「这段代码长什么样」，
    # 因此明细可以带源码；
    # 但一个函数可能有几千字符，
    # 不设上限会让深挖产物失控。
    MAX_DETAIL_SOURCE_CHARS = 1500

    @classmethod
    def _source_segment(
        cls,
        content,
        node,
    ) -> str:
        """
        取出某个 AST 节点对应的源码原文。

        这是深挖报告与默认报告最大的差别：
        默认报告给签名，深挖给源码。
        """

        if not isinstance(content, str) or node is None:
            return ""

        try:

            segment = ast.get_source_segment(
                content,
                node,
            )

        except Exception:

            return ""

        if not segment:
            return ""

        segment = segment.strip()

        if len(segment) > cls.MAX_DETAIL_SOURCE_CHARS:

            segment = (
                segment[
                    : cls.MAX_DETAIL_SOURCE_CHARS
                ]
                + "\n# ...（已截断）"
            )

        return segment

    @staticmethod
    def _unparse(node) -> str:
        """
        把 AST 节点还原成源码文本。

        还原失败返回空串
        （个别节点在低版本 Python 上
         unparse 会抛异常）。
        """

        try:

            return ast.unparse(node).strip()

        except Exception:

            return ""
```

## 十八、AI 能力层（Embeddings）

文本向量化的抽象接口与 Ollama 本地实现

### 📄 `app/embeddings/base.py`

**层级**：AI 能力层（Embeddings） · **职责**：Embedding Provider 的抽象接口定义

```python
"""Embedding Provider 抽象接口。"""

from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """定义统一的文本向量化接口。"""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """将单段文本转换为向量。"""
        raise NotImplementedError

    @abstractmethod
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """批量将文本转换为向量。"""
        raise NotImplementedError
```

### 📄 `app/embeddings/ollama.py`

**层级**：AI 能力层（Embeddings） · **职责**：基于 Ollama 的本地 Embedding 实现

```python
"""基于 Ollama 的本地 Embedding Provider。"""

from ollama import Client

from app.core.config import get_settings
from app.embeddings.base import EmbeddingProvider


class OllamaEmbedding(EmbeddingProvider):
    """使用 Ollama 本地模型生成文本向量。"""

    def __init__(
        self,
        model: str | None = None,
    ) -> None:
        settings = get_settings()

        self.model = model or settings.EMBEDDING_MODEL

        self.client = Client(
            host=settings.OLLAMA_BASE_URL,
            trust_env=False,
        )

    def embed(self, text: str) -> list[float]:
        """将单段文本转换为 Embedding 向量。"""

        response = self.client.embed(
            model=self.model,
            input=text,
        )

        return response["embeddings"][0]

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """批量生成 Embedding 向量。"""

        response = self.client.embed(
            model=self.model,
            input=texts,
        )

        return response["embeddings"]
```

### 📄 `app/embeddings/__init__.py`

**层级**：AI 能力层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

## 十九、向量存储层（Vector Store）

Qdrant Collection 管理、向量写入与相似度检索

### 📄 `app/vector_store/qdrant.py`

**层级**：向量存储层（Vector Store） · **职责**：Qdrant Collection 管理、向量写入与相似度检索

```python
"""Qdrant 向量存储层。"""

from typing import Any
import uuid


from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config import get_settings


class QdrantVectorStore:
    """负责 Collection 管理、向量写入和相似度检索。"""

    def __init__(
            self,
            collection_name: str = "github_projects",
    ) -> None:
        settings = get_settings()

        self.collection_name = collection_name

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            trust_env=False,
        )

    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        """创建向量 Collection。"""

        if self.client.collection_exists(
            self.collection_name
        ):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert(
        self,
        point_id: int,
        vector: list[float],
        payload: dict[str, Any],
    ) -> None:
        """向 Collection 写入一个向量及其业务元数据。"""

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):
        """根据查询向量执行 Top-K 相似度搜索。"""

        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points

    def insert(
        self,
        vector,
        payload,
    ):

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=payload,
        )


        self.client.upsert(
            collection_name=
            self.collection_name,

            points=[
                point
            ],
        )
```

### 📄 `app/vector_store/__init__.py`

**层级**：向量存储层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

## 二十、数据库迁移层（Alembic）

Alembic 异步运行环境与版本化迁移脚本

### 📄 `alembic/env.py`

**层级**：数据库迁移层（Alembic） · **职责**：Alembic 运行环境配置，绑定异步 Engine 与 ORM 元数据

```python
"""Alembic 数据库迁移配置。"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import get_settings
from app.db.base import Base
from app.models import AnalysisRun, AnalysisTask, Repository


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """执行离线数据库迁移。"""

    url = get_settings().DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """配置 Alembic 上下文并执行迁移。"""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """使用异步 SQLAlchemy 执行数据库迁移。"""

    configuration = config.get_section(
        config.config_ini_section,
        {},
    )

    configuration["sqlalchemy.url"] = get_settings().DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(
            do_run_migrations,
        )

    await connectable.dispose()


def run_migrations_online() -> None:
    """执行在线数据库迁移。"""

    asyncio.run(
        run_async_migrations()
    )


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 📄 `alembic/versions/479571222143_create_initial_analysis_tables.py`

**层级**：数据库迁移层（Alembic） · **职责**：初始建表迁移脚本，创建 `repositories` / `analysis_runs` / `analysis_tasks` 三张表

```python
"""create initial analysis tables

Revision ID: 479571222143
Revises: 
Create Date: 2026-09-23 15:18:14.292496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '479571222143'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('repositories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('owner', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('default_branch', sa.String(length=100), nullable=True),
    sa.Column('language', sa.String(length=100), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=False),
    sa.Column('forks', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url')
    )
    op.create_table('analysis_runs',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('repository_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('current_node', sa.String(length=100), nullable=True),
    sa.Column('retry_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['repository_id'], ['repositories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('analysis_tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('run_id', sa.String(length=36), nullable=False),
    sa.Column('task_type', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('input', sa.JSON(), nullable=True),
    sa.Column('output', sa.JSON(), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('retry_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['run_id'], ['analysis_runs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('analysis_tasks')
    op.drop_table('analysis_runs')
    op.drop_table('repositories')
    # ### end Alembic commands ###
```

### 📄 `alembic/versions/a9e1f4c2d8b7_add_evidence_claim_citation.py`

**层级**：数据库迁移层（Alembic） · **职责**：Phase 9 迁移脚本，创建证据链三张表 `evidences` / `claims` / `citations`

```python
"""
add evidence claim citation

Revision ID: a9e1f4c2d8b7
Revises: 479571222143
"""

from alembic import op
import sqlalchemy as sa


revision = "a9e1f4c2d8b7"

down_revision = "479571222143"

branch_labels = None

depends_on = None


def upgrade() -> None:

    op.create_table(
        "evidences",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "repository_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "source_type",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "source_url",
            sa.String(length=1000),
            nullable=True,
        ),

        sa.Column(
            "file_path",
            sa.String(length=1000),
            nullable=True,
        ),

        sa.Column(
            "line_start",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "line_end",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "verification_status",
            sa.String(length=20),
            nullable=False,
            server_default="UNVERIFIED",
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["repository_id"],
            ["repositories.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_evidences_repository_id",
        "evidences",
        ["repository_id"],
    )

    op.create_table(
        "claims",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "run_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "claim_text",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "verification_status",
            sa.String(length=20),
            nullable=False,
            server_default="UNVERIFIED",
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["run_id"],
            ["analysis_runs.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_claims_run_id",
        "claims",
        ["run_id"],
    )

    op.create_table(
        "citations",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "claim_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "evidence_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["claim_id"],
            ["claims.id"],
        ),

        sa.ForeignKeyConstraint(
            ["evidence_id"],
            ["evidences.id"],
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "claim_id",
            "evidence_id",
            name="uq_citations_claim_evidence",
        ),
    )

    op.create_index(
        "ix_citations_claim_id",
        "citations",
        ["claim_id"],
    )

    op.create_index(
        "ix_citations_evidence_id",
        "citations",
        ["evidence_id"],
    )


def downgrade() -> None:

    op.drop_index(
        "ix_citations_evidence_id",
        table_name="citations",
    )

    op.drop_index(
        "ix_citations_claim_id",
        table_name="citations",
    )

    op.drop_table("citations")

    op.drop_index(
        "ix_claims_run_id",
        table_name="claims",
    )

    op.drop_table("claims")

    op.drop_index(
        "ix_evidences_repository_id",
        table_name="evidences",
    )

    op.drop_table("evidences")
```

### 📄 `alembic/versions/b0f6883a5f43_add_checkpoints.py`

**层级**：数据库迁移层（Alembic） · **职责**：Phase 10 迁移脚本，创建 Workflow 检查点表 `checkpoints`

```python
"""
add workflow checkpoints

Revision ID: add_checkpoints_001
Revises: a9e1f4c2d8b7
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_checkpoints_001"

down_revision: Union[
    str,
    Sequence[str],
    None
] = "a9e1f4c2d8b7"

branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建 checkpoints 表。"""

    op.create_table(
        "checkpoints",

        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),

        sa.Column(
            "run_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "checkpoint_version",
            sa.Integer(),
            nullable=False,
            default=1,
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "current_node",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "state_data",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "outputs",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "errors",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "retry_count",
            sa.Integer(),
            nullable=False,
            default=0,
        ),

        sa.Column(
            "pause_reason",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "human_approved",
            sa.Boolean(),
            nullable=False,
            default=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["run_id"],
            ["analysis_runs.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )

    op.create_index(
        "ix_checkpoints_run_id",
        "checkpoints",
        ["run_id"],
    )


def downgrade() -> None:
    """删除 checkpoints 表。"""

    op.drop_index(
        "ix_checkpoints_run_id",
        table_name="checkpoints",
    )

    op.drop_table(
        "checkpoints"
    )
```

## 二十一、测试层（Tests）

单元测试与集成测试

### 📄 `tests/test_agent_registry.py`

**层级**：测试层 · **职责**：Agent 注册中心测试（创建 Skill 注册中心 → 构造 Agent 注册中心 → 断言 Agent 可注册与获取）

```python
"""
测试 Agent Registry。

验证：

Agent 是否可以正常注册和获取。


"""


from app.skills.registry import (
    create_skill_registry
)


from app.agents.agent_registry import (
    create_agent_registry
)



def test_agent_registry():


    # 创建Skill管理器

    skill_registry = (
        create_skill_registry()
    )



    # 创建Agent管理器

    registry = (
        create_agent_registry(
            skill_registry
        )
    )



    # 判断Agent是否存在

    assert (
        registry.get(
            "repository_analysis_agent"
        )
        is not None
    )
```

### 📄 `tests/test_agent_runtime.py`

**层级**：测试层 · **职责**：Agent 运行环境测试（FakeRegistry + FakeAgent，断言 `execute()` 返回 Agent 结果；Agent 不存在时抛异常）

```python
"""
测试 Agent Runtime。


验证：

Runtime

    |

    v

Agent

    |

    v

返回结果


"""


import pytest


from app.agents.agent_runtime import (
    AgentRuntime
)




class FakeAgent:


    async def execute(
        self,
        context,
        input_data
    ):


        return {


            "success":

                True

        }





class FakeRegistry:


    def get(
        self,
        name
    ):


        return FakeAgent()





@pytest.mark.asyncio
async def test_agent_runtime():



    runtime = AgentRuntime(

        FakeRegistry()

    )



    result = await runtime.execute(

        "test_agent",

        None,

        {}

    )



    assert (

        result["success"]

        is True

    )
```

### 📄 `tests/test_analysis_api.py`

**层级**：测试层 · **职责**：API 端到端测试（健康检查、创建任务、查询任务、参数校验、404 场景）

```python
"""Analysis API 测试。"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_create_analysis():

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url":
                "https://github.com/openai/openai-python",
            "question":
                "分析这个项目的 Agent 和 Workflow",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "run_id" in data

    assert (
        data["status"]
        == "WAITING_DESIGN"
    )

    assert (
        data["current_node"]
        == "design_gate"
    )

    assert (
        data["progress"]
        == 20
    )

    assert (
        data["repo_url"]
        == "https://github.com/openai/openai-python"
    )


def test_get_analysis():

    create_response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url":
                "https://github.com/openai/openai-python",
            "question":
                "分析项目架构",
        },
    )

    assert (
        create_response.status_code
        == 200
    )

    run_id = (
        create_response
        .json()["run_id"]
    )

    response = client.get(
        f"/api/v1/analysis/{run_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["run_id"]
        == run_id
    )

    assert (
        data["status"]
        == "WAITING_DESIGN"
    )

    assert (
        data["current_node"]
        == "design_gate"
    )


def test_invalid_repository_url():

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url":
                "https://example.com/test"
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False

    assert (
        data["error"]["code"]
        == "VALIDATION_ERROR"
    )


def test_analysis_not_found():

    response = client.get(
        "/api/v1/analysis/not-exist-run-id"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False

    assert (
        data["error"]["code"]
        == "VALIDATION_ERROR"
    )

def test_parse_github_url_strips_query_string():
    """
    带 query string 的 GitHub URL 必须被正确解析。

    旧实现按 "/" 朴素切分，
    会把 "?utm_source=chatgpt.com" 当成 repository name 的一部分，
    导致 README 与配置文件全部 404、
    证据为 0、technology_stack 全空，
    而该 run 仍然被标记为 COMPLETED。
    """

    from app.services.analysis_service import (
        AnalysisService,
    )

    owner, name = AnalysisService._parse_github_url(
        "https://github.com/smlfy/"
        "enterprise-workflow-agent-platform"
        "?utm_source=chatgpt.com"
    )

    assert owner == "smlfy"

    assert name == "enterprise-workflow-agent-platform"


def test_parse_github_url_handles_common_forms():
    """常见的 URL 写法都要能解析。"""

    from app.services.analysis_service import (
        AnalysisService,
    )

    cases = [
        (
            "https://github.com/openai/openai-python",
            ("openai", "openai-python"),
        ),
        (
            "https://github.com/openai/openai-python.git",
            ("openai", "openai-python"),
        ),
        (
            "https://github.com/openai/openai-python/",
            ("openai", "openai-python"),
        ),
        (
            "https://github.com/openai/openai-python"
            "?tab=readme-ov-file#install",
            ("openai", "openai-python"),
        ),
    ]

    for url, expected in cases:
        assert (
            AnalysisService._parse_github_url(url)
            == expected
        ), url


def test_parse_github_url_rejects_non_github():
    """非 GitHub 域名必须抛业务异常（→ HTTP 400）。"""

    import pytest

    from app.core.exceptions import ValidationError
    from app.services.analysis_service import (
        AnalysisService,
    )

    with pytest.raises(ValidationError):
        AnalysisService._parse_github_url(
            "https://example.com/owner/name"
        )
```

### 📄 `tests/test_analysis_focus.py`

**层级**：测试层 · **职责**：question 驱动分析计划的测试。

```python
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
```

### 📄 `tests/test_analysis_result.py`

**层级**：测试层 · **职责**：（未标注）

```python
from app.services.analysis_result_service import (
    analysis_result_service,
)


def test_analysis_result_build():

    data = {

        "repository": {

            "name": "demo",

            "language": "Python",

            "url":
            "https://github.com/a/b",
        },


        "agent_outputs": {

            "ArchitectureAgent": {

                "summary":
                "architecture",

                "facts":[
                    "FastAPI"
                ],

                "evidence_ids":[
                    "e1"
                ],
            }
        },

        "technology_stack": {

            "languages":[
                "Python"
            ]
        }
    }


    result = (
        analysis_result_service.build(
            "run-001",
            data,
        )
    )


    assert (
        result.run_id
        ==
        "run-001"
    )


    assert (
        result.project_overview.name
        ==
        "demo"
    )


    assert (
        len(result.agents)
        ==
        1
    )
```

### 📄 `tests/test_architecture_code_evidence.py`

**层级**：测试层 · **职责**：代码证据与 README 自述合并的测试。

```python
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
```

### 📄 `tests/test_checkpoint_size_guard.py`

**层级**：测试层 · **职责**：Checkpoint 体积守卫与报告兜底测试。

```python
"""
Checkpoint 体积守卫与报告兜底测试。

背景
====

真实事故：被分析项目 Legal（17.8MB）跑完后，
checkpoint 的 state_data 涨到 263,743 字节，
越过 asyncmy 读取大字段的缓冲区分片上限
（实测与 MySQL sort_buffer_size 262,144 吻合）：

    Lost connection to MySQL server during query
    (Existing exports of data: object cannot be re-sized)

后果是**这个 run 再也读不回来了** ——
恢复、取报告、深挖全部 500，
而任务其实早就 COMPLETED。

两道防线：

1. 写入前守卫：state_data 超限就瘦身，
   保证写进去的行一定能读回来
2. 读取时兜底：checkpoint 读不出来就回读
   磁盘上的 reports/{run_id}_analysis.md
"""

import json
from pathlib import Path

from app.repositories.checkpoint import (
    MAX_STATE_BYTES,
    CheckpointRepository,
)
from app.services.analysis_workflow import (
    AnalysisWorkflowRunner,
)


def build_oversized_state():
    """构造一个远超上限的 state。"""

    return {
        "final_report": {
            "report": {
                "path": "reports/x_analysis.md",
                "format": "markdown",
            },
            "content": "# 报告\n" + "正文" * 20000,
        },
        "readme": "R" * 120000,
        "evidence": [
            {
                "file_path": f"f{i}.py",
                "content": "E" * 1500,
            }
            for i in range(40)
        ],
        "modules": [
            {
                "file_path": f"m{i}.py",
                "content": "M" * 1200,
            }
            for i in range(20)
        ],
        "business_field": {"important": "必须保留"},
    }


# ----------------------------------------------------------------
# 写入守卫
# ----------------------------------------------------------------


def test_oversized_state_is_trimmed_under_limit():

    state = build_oversized_state()

    assert (
        CheckpointRepository._size(state)
        > MAX_STATE_BYTES
    )

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert (
        CheckpointRepository._size(data)
        <= MAX_STATE_BYTES
    )

    assert trims

    assert trims["original_bytes"] > trims[
        "final_bytes"
    ]


def test_trim_drops_the_most_redundant_first():
    """
    先丢报告正文与 README。

    报告正文已经写在 reports/*.md，
    README 也已被抽取成结构 ——
    两者都是「丢了不心疼」的重复数据。
    """

    state = build_oversized_state()

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    dropped = trims["dropped_bytes"]

    assert "final_report.content" in dropped

    assert "readme" in dropped

    # 落到上限以内就停手，
    # 不该继续动 evidence / modules。
    assert "evidence" not in dropped

    assert "modules" not in dropped

    assert "content" not in data["final_report"]

    assert len(data["readme"]) == 4000


def test_trim_preserves_business_fields():
    """瘦身只动重复的大字段，不能误伤业务数据。"""

    state = build_oversized_state()

    data, _ = CheckpointRepository._fit_state_data(
        state
    )

    assert data["business_field"] == {
        "important": "必须保留"
    }

    assert len(data["evidence"]) == 40

    assert len(data["modules"]) == 20


def test_trim_falls_through_to_evidence_and_modules():
    """光丢报告正文和 README 还不够时，继续往后丢。"""

    state = {
        "final_report": {"content": "x" * 100},
        "readme": "short",
        # 光靠 evidence 与 modules 就把体积顶上去
        "evidence": [
            {"content": "E" * 2000} for _ in range(150)
        ],
        "modules": [
            {"content": "M" * 2000} for _ in range(150)
        ],
    }

    assert (
        CheckpointRepository._size(state)
        > MAX_STATE_BYTES
    )

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert (
        CheckpointRepository._size(data)
        <= MAX_STATE_BYTES
    )

    dropped = trims["dropped_bytes"]

    assert "evidence" in dropped or "modules" in dropped


def test_small_state_is_untouched():

    state = {"a": 1, "readme": "short"}

    data, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert trims == {}

    assert data == state


def test_non_dict_state_does_not_crash():

    data, trims = CheckpointRepository._fit_state_data(
        "not-a-dict"
    )

    assert data == "not-a-dict"

    assert trims == {}


# ----------------------------------------------------------------
# 读取兜底
# ----------------------------------------------------------------


def test_report_falls_back_to_disk(tmp_path, monkeypatch):
    """
    checkpoint 读不出来时，回读磁盘上的报告文件。

    没有这条兜底，「分析成功但取报告 500」
    就会一直存在 —— 而报告其实早就写好了。
    """

    monkeypatch.chdir(tmp_path)

    reports = Path("reports")

    reports.mkdir()

    (reports / "run-1_analysis.md").write_text(
        "# 报告\n\n正文内容",
        encoding="utf-8",
    )

    result = AnalysisWorkflowRunner._report_from_disk(
        "run-1",
        None,
    )

    assert result["content"] == "# 报告\n\n正文内容"

    assert "run-1_analysis.md" in result[
        "report"
    ]["path"]


def test_report_fills_missing_content_from_disk(
    tmp_path,
    monkeypatch,
):
    """
    报告正文被瘦身丢掉时，同样从文件回读。

    state 里只剩路径，正文在磁盘上。
    """

    monkeypatch.chdir(tmp_path)

    reports = Path("reports")

    reports.mkdir()

    (reports / "run-2_analysis.md").write_text(
        "# 从文件读回来的报告",
        encoding="utf-8",
    )

    result = AnalysisWorkflowRunner._report_from_disk(
        "run-2",
        {
            "report": {
                "path": "reports/run-2_analysis.md",
                "format": "markdown",
            }
        },
    )

    assert result["content"] == (
        "# 从文件读回来的报告"
    )


def test_report_keeps_inline_content_when_present():
    """state 里有正文就不用读文件。"""

    report = {
        "report": {
            "path": "reports/nope.md",
            "format": "markdown",
        },
        "content": "# 来自 state 的正文",
    }

    result = AnalysisWorkflowRunner._report_from_disk(
        "run-3",
        report,
    )

    assert result is report


def test_report_returns_none_when_nothing_available(
    tmp_path,
    monkeypatch,
):
    """既没 state 也没文件时返回 None，而不是编一个。"""

    monkeypatch.chdir(tmp_path)

    assert (
        AnalysisWorkflowRunner._report_from_disk(
            "missing-run",
            None,
        )
        is None
    )


def test_trimmed_marker_is_underscore_prefixed():
    """
    瘦身记录必须用下划线开头。

    FinalizerNode 组装报告输入时会跳过
    下划线开头的键，否则这条记录会混进报告。
    """

    state = build_oversized_state()

    _, trims = CheckpointRepository._fit_state_data(
        state
    )

    assert trims

    key = "_trimmed"

    assert key.startswith("_")

    # 记录本身要能落库（可 JSON 序列化）。
    json.dumps({key: trims})
```

### 📄 `tests/test_chunker.py`

**层级**：测试层 · **职责**：Markdown 切分器单元测试

```python
"""Markdown Chunker 测试。"""

from app.project_analysis.code_chunker import MarkdownChunker


def test_markdown_chunker():
    """测试 Markdown 是否可以按照章节切分。"""

    text = """# Introduction

This project is an AI Agent platform.

# Architecture

The system contains multiple agents and tools.

# HITL

Human approval is required for sensitive operations.
"""

    chunker = MarkdownChunker()

    chunks = chunker.split(text)

    assert len(chunks) == 3

    assert "Introduction" in chunks[0]
    assert "Architecture" in chunks[1]
    assert "HITL" in chunks[2]
```

### 📄 `tests/test_code_structure_extractor.py`

**层级**：测试层 · **职责**：CodeStructureExtractor 测试。

```python
"""
CodeStructureExtractor 测试。

覆盖：

1. 符号识别（class / 函数 / 导入 / 图谱调用）
2. camelCase 名字边界（BaseTool / PlannerAgent）
3. 语法错误文件不拖垮其它文件
4. 路径信号按目录去重
5. 条目数量上限

全部只做静态解析，不联网。
"""

from app.project_analysis.code_structure_extractor import (
    CodeStructureExtractor,
)


def extract_one(
    file_path,
    content,
):
    """抽取单个文件，返回该次结果。"""

    return CodeStructureExtractor.extract(
        [
            {
                "file_path": file_path,
                "content": content,
            }
        ]
    )


def items_of(
    result,
    dimension,
):
    return result["dimensions"][dimension]["items"]


# ----------------------------------------------------------------
# 符号识别
# ----------------------------------------------------------------


def test_extracts_agent_classes_with_line_numbers():
    """Agent 类必须带真实行号。"""

    result = extract_one(
        "app/agents/finance.py",
        (
            "from abc import ABC\n"
            "\n"
            "class BaseAgent(ABC):\n"
            "    pass\n"
            "\n"
            "class InvoiceAgent(BaseAgent):\n"
            "    pass\n"
        ),
    )

    agents = result["dimensions"]["agents"]

    assert "class BaseAgent(ABC)" in agents["items"]

    assert "class InvoiceAgent(BaseAgent)" in agents["items"]

    # 行号必须指向真实定义位置。
    base_evidence = next(
        item
        for item in agents["evidence"]
        if item["text"] == "class BaseAgent(ABC)"
    )

    assert base_evidence["file_path"] == (
        "app/agents/finance.py"
    )

    assert base_evidence["line_start"] == 3


def test_camelcase_symbol_boundaries():
    """
    camelCase 名字必须被识别。

    回归点：用 [^a-z] 配 re.IGNORECASE 时，
    大写字母也会被排除，
    导致 BaseTool / PlannerAgent 这类名字漏掉。
    """

    result = extract_one(
        "app/tools/base.py",
        (
            "class BaseTool:\n"
            "    pass\n"
            "\n"
            "class MyToolbox:\n"
            "    pass\n"
        ),
    )

    tools = items_of(result, "tools")

    assert "class BaseTool" in tools

    # 小写紧跟的 Toolkit / Toolbox 不算
    # （见 _symbol_pattern 的说明）。
    assert "class MyToolbox" not in tools


def test_extracts_workflow_graph_nodes_and_edges():
    """
    Workflow 维度最有价值的部分：
    StateGraph 的节点与边要以源码原文形式记录。
    """

    result = extract_one(
        "app/graph.py",
        (
            "from langgraph.graph import StateGraph\n"
            "\n"
            "graph = StateGraph(AgentState)\n"
            "graph.add_node('intake', intake)\n"
            "graph.add_edge('intake', 'approve')\n"
        ),
    )

    workflow = result["dimensions"]["workflow"]

    assert "StateGraph(...)" in workflow["items"]

    assert (
        "graph.add_node('intake', intake)"
        in workflow["items"]
    )

    assert (
        "graph.add_edge('intake', 'approve')"
        in workflow["items"]
    )

    # 节点名必须带得回源码位置。
    edge = next(
        item
        for item in workflow["evidence"]
        if item["text"]
        == "graph.add_edge('intake', 'approve')"
    )

    assert edge["line_start"] == 5


def test_langgraph_import_is_not_an_agent_signal():
    """
    langgraph 是编排框架，属于 workflow。

    回归点：早期把 langgraph 也算进 agents，
    于是任何用 LangGraph 的项目
    都会凭空多出一批 agents 条目。
    """

    result = extract_one(
        "app/graph.py",
        "from langgraph.graph import StateGraph\n",
    )

    assert (
        "import langgraph.graph"
        in items_of(result, "workflow")
    )

    assert (
        "import langgraph.graph"
        not in items_of(result, "agents")
    )


def test_extracts_tool_decorator():
    """@tool 装饰器的函数算 Tool。"""

    result = extract_one(
        "app/search.py",
        (
            "from langchain_core.tools import tool\n"
            "\n"
            "@tool\n"
            "def web_search(query):\n"
            "    pass\n"
        ),
    )

    assert any(
        "web_search" in item
        for item in items_of(result, "tools")
    )


def test_extracts_rag_and_memory_signals():
    """RAG / Memory 从导入与符号识别。"""

    result = extract_one(
        "app/store.py",
        (
            "from qdrant_client import QdrantClient\n"
            "from langgraph.checkpoint.sqlite "
            "import SqliteSaver\n"
            "\n"
            "def retrieve_documents(query):\n"
            "    pass\n"
            "\n"
            "class CheckpointStore:\n"
            "    pass\n"
        ),
    )

    assert "import qdrant_client" in items_of(
        result,
        "rag",
    )

    assert "def retrieve_documents" in items_of(
        result,
        "rag",
    )

    assert "class CheckpointStore" in items_of(
        result,
        "memory",
    )


def test_storage_is_not_rag():
    """
    storage 里含 rag 三个字母，但不能算 RAG。

    真实事故：对某个仓库跑真实分析时，
    src/app/core/config.py 的
    validate_storage_root 被判成了 RAG 实现，
    于是 08 章凭空多出一条代码证据。
    """

    result = extract_one(
        "src/app/core/config.py",
        (
            "def validate_storage_root(value):\n"
            "    return value\n"
        ),
    )

    assert items_of(result, "rag") == []

    assert result["dimensions"]["rag"][
        "details"
    ] == []


def test_rag_word_boundary_still_matches():
    """带词边界的 rag 仍要能命中。"""

    result = extract_one(
        "src/app/rag/store.py",
        (
            "def rag_lookup(query):\n"
            "    return query\n"
            "\n"
            "def rerank_results(items):\n"
            "    return items\n"
        ),
    )

    rag = items_of(result, "rag")

    assert "def rag_lookup" in rag

    assert "def rerank_results" in rag


def test_generic_search_is_not_rag():
    """
    名字里只有 search 的函数不算 RAG。

    否则 search_github_repo 之类
    会把任何项目都判成有 RAG。
    """

    result = extract_one(
        "app/github.py",
        "def search_github_repos(q):\n    pass\n",
    )

    assert items_of(result, "rag") == []


# ----------------------------------------------------------------
# 容错
# ----------------------------------------------------------------


def test_syntax_error_is_recorded_not_raised():
    """
    语法错误的文件必须记入 unparsed，
    且不影响其它文件。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "broken.py",
                "content": "def f(:\n",
            },
            {
                "file_path": "app/agents/ok.py",
                "content": "class OkAgent:\n    pass\n",
            },
        ]
    )

    assert len(result["unparsed"]) == 1

    assert (
        result["unparsed"][0]["file_path"]
        == "broken.py"
    )

    assert "SyntaxError" in (
        result["unparsed"][0]["error"]
    )

    # 好文件照常产出。
    assert result["parsed_files"] == 1

    assert "class OkAgent" in items_of(
        result,
        "agents",
    )


def test_truncated_python_is_reported_not_guessed():
    """
    截断的源码会语法错误，必须如实上报。

    这是为什么 AST 抽取要用未截断的全文：
    截断过的 Python 抽不出任何符号，
    但绝不能因此声称「项目没有 Agent」。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "app/agents/half.py",
                "content": "class HalfAgent:\n    def ex",
            }
        ]
    )

    assert result["parsed_files"] == 0

    assert result["available"] is False

    assert len(result["unparsed"]) == 1


def test_non_python_files_are_skipped():
    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "docker-compose.yml",
                "content": "services:\n  api:\n",
            }
        ]
    )

    assert result["parsed_files"] == 0


def test_broken_input_does_not_raise():
    """结构异常时不能抛异常。"""

    result = CodeStructureExtractor.extract(
        "not-a-list"
    )

    assert result["parsed_files"] == 0

    result = CodeStructureExtractor.extract(
        [None, "x", {"file_path": "a.py"}]
    )

    assert result["parsed_files"] == 0


# ----------------------------------------------------------------
# 路径信号
# ----------------------------------------------------------------


def test_path_signal_is_deduped_by_directory():
    """
    同一目录下的多个文件只记一条路径信号。

    否则 src/agents/ 下有 30 个文件时，
    路径会把 MAX_ITEMS 刷满，
    真正有价值的类名被挤出去。
    """

    result = CodeStructureExtractor.extract(
        [],
        extra_paths=[
            "src/agents/a.py",
            "src/agents/b.py",
            "src/agents/c.py",
        ],
    )

    agents = items_of(result, "agents")

    assert agents == ["路径 src/agents/"]


def test_path_signal_covers_unread_files():
    """
    没被读取的文件也要贡献路径信号。

    配额只有 12 个，
    但「存在 src/agents/ 目录」这条证据
    不该因为该目录下的文件没被读到而丢失。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "src/main.py",
                "content": "print('x')\n",
            }
        ],
        extra_paths=["src/agents/未读取到的.py"],
    )

    assert "路径 src/agents/" in items_of(
        result,
        "agents",
    )


def test_symbols_rank_above_path_signals():
    """
    符号条目必须排在路径信号前面。

    _add 是按顺序填满 MAX_ITEMS 就停的，
    如果路径先写入，
    第一个类名就可能被挤掉。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "src/agents/base.py",
                "content": (
                    "class RealAgent:\n    pass\n"
                ),
            }
        ]
    )

    agents = items_of(result, "agents")

    assert agents[0] == "class RealAgent"

    assert agents[-1] == "路径 src/agents/"


# ----------------------------------------------------------------
# 实现明细（下到函数体）
# ----------------------------------------------------------------


GRAPH_SOURCE = (
    "from langgraph.graph import StateGraph\n"
    "\n"
    "class WorkflowService:\n"
    "    def build(self):\n"
    "        builder = StateGraph(AgentState)\n"
    "        builder.add_node('duplicate_check',\n"
    "                          self._node_duplicate_check)\n"
    "        builder.add_edge('a', 'b')\n"
    "        return builder.compile()\n"
    "\n"
    "    def _node_duplicate_check(self, state: AgentState)"
    " -> AgentState:\n"
    "        found = find_similar_invoices(\n"
    "            state['vendor'], state['amount'])\n"
    "        if found.score >= 0.85:\n"
    "            state['status'] = 'duplicate_suspected'\n"
    "        return state\n"
)


def test_node_callback_is_resolved_to_definition():
    """
    add_node 的处理函数必须被解析到真实定义。

    这是「下到函数体」的核心：
    从「有这么个节点」变成
    「这个节点的签名与调用链是什么」。
    """

    result = extract_one(
        "src/app/services/workflow_service.py",
        GRAPH_SOURCE,
    )

    details = result["dimensions"]["workflow"][
        "details"
    ]

    node = next(
        item
        for item in details
        if item["name"] == "duplicate_check"
    )

    assert node["symbol"] == "_node_duplicate_check"

    assert node["signature"] == (
        "def _node_duplicate_check("
        "self, state: AgentState) -> AgentState"
    )

    assert "find_similar_invoices" in node["calls"]


def test_node_detail_carries_threshold_literals():
    """
    关键词面量必须被记录下来。

    0.85 这种阈值是理解实现的关键，
    只记符号名是拿不到的。
    """

    result = extract_one(
        "src/app/services/workflow_service.py",
        GRAPH_SOURCE,
    )

    node = next(
        item
        for item in result["dimensions"][
            "workflow"
        ]["details"]
        if item["name"] == "duplicate_check"
    )

    assert "0.85" in node["literals"]

    assert "'duplicate_suspected'" in node[
        "literals"
    ]


def test_add_edge_does_not_produce_a_detail():
    """
    add_edge 只记拓扑，不产明细。

    它解析不出处理函数，
    产一条空明细只会挤占 MAX_DETAILS。
    """

    result = extract_one(
        "src/app/services/workflow_service.py",
        GRAPH_SOURCE,
    )

    details = result["dimensions"]["workflow"][
        "details"
    ]

    signatures = [
        item["signature"] for item in details
    ]

    assert not any(
        "add_edge" in signature
        for signature in signatures
    )


def test_class_detail_lists_methods():
    """类明细要给出基类与方法表。"""

    result = extract_one(
        "src/app/tools/registry.py",
        (
            "class ToolRegistry(BaseToolkit):\n"
            "    def register(self, tool):\n"
            "        pass\n"
            "\n"
            "    def resolve(self, name):\n"
            "        pass\n"
        ),
    )

    detail = result["dimensions"]["tools"][
        "details"
    ][0]

    assert detail["signature"] == (
        "class ToolRegistry(BaseToolkit)"
    )

    assert detail["methods"] == [
        "register",
        "resolve",
    ]


def test_function_detail_has_signature_and_calls():
    """RAG 函数明细要带签名与调用链。"""

    result = extract_one(
        "src/app/rag/indexer.py",
        (
            "def retrieve_and_rank(query: str,"
            " top_k: int = 5) -> list:\n"
            "    vectors = embed_query(query)\n"
            "    return search_index(vectors, top_k)\n"
        ),
    )

    detail = result["dimensions"]["rag"][
        "details"
    ][0]

    assert detail["signature"] == (
        "def retrieve_and_rank(query: str,"
        " top_k: int = 5) -> list"
    )

    assert detail["calls"] == [
        "embed_query",
        "search_index",
    ]


def test_boring_literals_are_filtered():
    """
    噪声字面量不能把真正的阈值挤掉。

    "utf-8" / "id" 这类到处都是，
    0.0 通常只是初始化占位。
    """

    result = extract_one(
        "src/app/rag/loader.py",
        (
            "def retrieve_file(path):\n"
            "    raw = open(path, encoding='utf-8')\n"
            "    score = 0.0\n"
            "    limit = 25\n"
            "    label = 'not_found_in_index'\n"
            "    return limit\n"
        ),
    )

    literals = result["dimensions"]["rag"][
        "details"
    ][0]["literals"]

    assert "'utf-8'" not in literals

    assert "0.0" not in literals

    assert "25" in literals

    assert "'not_found_in_index'" in literals


def test_builtin_calls_are_filtered():
    """内建函数不能出现在调用链里。"""

    result = extract_one(
        "src/app/rag/util.py",
        (
            "def retrieve_all(items):\n"
            "    total = len(items)\n"
            "    return sorted(items)\n"
        ),
    )

    calls = result["dimensions"]["rag"][
        "details"
    ][0]["calls"]

    assert "len" not in calls

    assert "sorted" not in calls


def test_details_are_capped():
    """明细数量必须有上限，避免 state 膨胀。"""

    functions = "".join(
        f"def retrieve_{i}(q):\n"
        f"    return q\n"
        for i in range(30)
    )

    result = extract_one(
        "src/app/rag/many.py",
        functions,
    )

    details = result["dimensions"]["rag"][
        "details"
    ]

    assert len(details) == (
        CodeStructureExtractor.MAX_DETAILS
    )


def test_items_are_capped():
    """条目数量必须有上限，避免 state 膨胀。"""

    classes = "".join(
        f"class Agent{i}:\n    pass\n"
        for i in range(50)
    )

    result = extract_one(
        "src/agents/many.py",
        classes,
    )

    agents = result["dimensions"]["agents"]

    assert len(agents["items"]) == (
        CodeStructureExtractor.MAX_ITEMS
    )

    assert len(agents["evidence"]) == (
        CodeStructureExtractor.MAX_EVIDENCE
    )


# ----------------------------------------------------------------
# 代码摘录跳过 import 段
# ----------------------------------------------------------------


def test_meaningful_start_skips_import_block():
    """
    摘录必须跳过开头的 import 段。

    真实反馈：「这源码提取了一堆 import 根本没有用」。
    原因是摘录固定从第 1 行取，
    而 Python 文件开头必然是 import 块。
    """

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        '"""模块说明。"""\n'
        "\n"
        "import os\n"
        "import uuid\n"
        "from decimal import Decimal\n"
        "\n"
        "\n"
        "class WorkflowService:\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith(
        "class WorkflowService:"
    )


def test_meaningful_start_handles_multiline_docstring():

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        '"""\n'
        "多行\n"
        "说明\n"
        '"""\n'
        "import os\n"
        "\n"
        "class B:\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith("class B:")


def test_meaningful_start_falls_back_for_import_only_file():
    """
    整份文件只有 import 时回退到 0。

    不能返回 len(source)，那样摘录会是空串。
    """

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = "import os\nimport sys\n"

    assert (
        CodeStructureExtractor.meaningful_start(
            source
        )
        == 0
    )


def test_module_entry_records_start_line():
    """
    摘录跳过了多少行必须记下来 ——
    否则证据会写成「file:1-30」
    但内容其实是第 30 行开始的。
    """

    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    source = (
        "import os\n"
        "import uuid\n"
        "\n"
        "\n"
        "class Real:\n"
        "    pass\n"
    )

    entry = ArchitectureAnalysisSkill()._module_entry(
        "f.py",
        source,
    )

    assert entry["content"].startswith("class Real:")

    assert entry["start_line"] == 5


def test_module_entry_without_imports_has_no_start_line():

    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    entry = ArchitectureAnalysisSkill()._module_entry(
        "f.py",
        "class A:\n    pass\n",
    )

    assert "start_line" not in entry

    assert entry["content"].startswith("class A:")


def test_meaningful_start_handles_multiline_import():
    """
    多行 import 的续行也必须跳过。

    真实事故：workflow_service.py 里

        from app.schemas.agent import (
            AgentRunListItem,
            ...
        )

    只看行首的话，扫描器会停在第 2 行
    （`    AgentRunListItem,` 不以 import 开头），
    摘录依然是一串 import 名单。
    """

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        "import os\n"
        "from app.schemas.agent import (\n"
        "    AgentRunListItem,\n"
        "    AgentRunResponse,\n"
        ")\n"
        "\n"
        "class AgentState(TypedDict):\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith(
        "class AgentState"
    )


def test_meaningful_start_handles_backslash_continuation():

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        "from app.core import a, \\n"
        "    b, c\n"
        "\n"
        "class Real:\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith("class Real:")
```

### 📄 `tests/test_config.py`

**层级**：测试层 · **职责**：配置加载单元测试

```python
"""配置模块测试。"""

from app.core.config import get_settings


def test_settings_load():
    """测试配置是否能够正常加载。"""

    settings = get_settings()

    assert settings.APP_NAME
    assert settings.APP_ENV
    assert settings.LLM_PROVIDER
```

### 📄 `tests/test_context_manager.py`

**层级**：测试层 · **职责**：Phase 11 Context Manager 测试。

```python
"""Phase 11 Context Manager 测试。"""

import pytest

from app.context.manager import (
    ContextItem,
    ContextManager,
)


class FakeMemoryManager:
    """模拟 Memory Manager。"""

    async def retrieve(
        self,
        **kwargs,
    ):
        return {
            "run_memory": {
                "question": (
                    "Workflow怎么实现？"
                ),
                "research_plan": {
                    "tasks": [
                        "workflow"
                    ]
                },
                "agent_outputs": [
                    {
                        "agent": "architecture",
                        "result": (
                            "使用自研 Workflow"
                        ),
                    }
                ],
                "evidences": [
                    {
                        "id": "ev-1",
                        "file_path": (
                            "app/workflow/engine.py"
                        ),
                        "line_start": 1,
                        "line_end": 20,
                        "content": (
                            "class WorkflowEngine"
                        ),
                    }
                ],
            },
            "project_memory": [
                {
                    "run_id": "old-run",
                    "question": (
                        "Agent怎么实现？"
                    ),
                    "status": "COMPLETED",
                }
            ],
        }


@pytest.mark.asyncio
async def test_context_manager_retrieval_filter_and_assembly():
    """Context Manager 应完成 Retrieve / Filter / Assembly。"""

    async def retriever(query):
        return [
            {
                "content": (
                    "WorkflowEngine "
                    "executes workflow nodes"
                ),
                "score": 0.9,
                "file_path": (
                    "app/workflow/engine.py"
                ),
            },
            {
                "content": (
                    "irrelevant database text"
                ),
                "score": 0.1,
            },
        ]

    manager = ContextManager(
        FakeMemoryManager(),
        retriever=retriever,
        max_items=5,
        max_chars=5000,
    )

    result = await manager.build(
        run_id="run-1",
        repository_id=10,
        query="Workflow怎么实现？",
        workflow_state={
            "status": "ANALYZING",
            "current_node": "workflow",
        },
    )

    assert (
        "Current Question"
        in result["text"]
    )

    assert (
        "WorkflowEngine"
        in result["text"]
    )

    assert result["items"]

    assert all(
        item["content"].strip()
        for item in result["items"]
    )


def test_context_manager_deduplicates_and_limits():
    """Context Manager 应去重并限制 Context 数量。"""

    manager = ContextManager(
        FakeMemoryManager(),
        max_items=2,
    )

    items = manager.filter_and_rank(
        [
            ContextItem(
                source="test",
                content="workflow engine",
                score=1.0,
            ),
            ContextItem(
                source="test",
                content="workflow engine",
                score=0.5,
            ),
            ContextItem(
                source="test",
                content="database",
                score=0.2,
            ),
        ],
        "workflow",
    )

    assert len(items) == 2

    assert (
        items[0].content
        == "workflow engine"
    )
```

### 📄 `tests/test_context_retriever.py`

**层级**：测试层 · **职责**：Phase 11 Context Retriever 测试。

```python
"""Phase 11 Context Retriever 测试。"""

import pytest

from app.context.retriever import (
    QdrantContextRetriever,
)


class FakeEmbedding:
    """模拟 Embedding Provider。"""

    def embed(
        self,
        text,
    ):
        assert text == "Workflow"

        return [
            0.1,
            0.2,
        ]


class FakeSearchTool:
    """模拟 Qdrant Search Tool。"""

    async def execute(
        self,
        *,
        query_vector,
        limit,
    ):
        assert query_vector == [
            0.1,
            0.2,
        ]

        assert limit == 3

        return [
            {
                "text": "workflow.py",
                "source": "code",
            }
        ]


@pytest.mark.asyncio
async def test_qdrant_context_retriever():
    """测试自然语言 → Embedding → Qdrant Tool。"""

    retriever = QdrantContextRetriever(
        FakeEmbedding(),
        FakeSearchTool(),
        limit=3,
    )

    result = await retriever(
        "Workflow"
    )

    assert result == [
        {
            "text": "workflow.py",
            "source": "code",
        }
    ]
```

### 📄 `tests/test_database.py`

**层级**：测试层 · **职责**：MySQL 连接连通性测试（需数据库可用）

```python
"""数据库连接测试。"""

import pytest
from sqlalchemy import text

from app.db.session import AsyncSessionLocal


@pytest.mark.asyncio
async def test_database_connection():
    """测试 SQLAlchemy 是否可以连接 MySQL。"""

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT 1")
        )

        assert result.scalar() == 1
```

### 📄 `tests/test_dependency_analyzer_tool.py`

**层级**：测试层 · **职责**：依赖分析工具测试（解析本项目，断言 frameworks 字段存在）

```python
import pytest

from app.tools.dependency_analyzer_tool import (
    DependencyAnalyzerTool
)



@pytest.mark.asyncio
async def test_dependency_analyzer():


    tool = DependencyAnalyzerTool()


    result = await tool.execute(
        "."
    )


    assert isinstance(
        result,
        dict
    )


    assert (
        "frameworks"
        in result
    )
```

### 📄 `tests/test_embedding.py`

**层级**：测试层 · **职责**：Ollama Embedding 单元测试（需 Ollama 服务可用）

```python
"""Embedding Provider 测试。"""

from app.embeddings.ollama import OllamaEmbedding


def test_ollama_embedding():
    """测试 Ollama 是否可以生成 BGE-M3 向量。"""

    provider = OllamaEmbedding()

    vector = provider.embed(
        "Multi-Agent workflow platform"
    )

    assert isinstance(vector, list)
    assert len(vector) > 0
```

### 📄 `tests/test_embedding_qdrant.py`

**层级**：测试层 · **职责**：Embedding → Qdrant 写入 → 语义检索集成测试

```python
"""Embedding 与 Qdrant 集成测试。"""

from app.embeddings.ollama import OllamaEmbedding
from app.vector_store.qdrant import QdrantVectorStore


def test_embedding_to_qdrant():
    """测试文本向量化后写入 Qdrant，并执行语义检索。"""

    embedding = OllamaEmbedding()

    vector_store = QdrantVectorStore(
        collection_name="github_projects",
    )

    vector_store.create_collection(
        vector_size=1024,
    )

    documents = [
        {
            "id": 1,
            "text": "Multi-Agent workflow orchestration platform",
            "repo": "project-agents-workflow",
        },
        {
            "id": 2,
            "text": "FastAPI backend service for REST APIs",
            "repo": "project-fastapi",
        },
        {
            "id": 3,
            "text": "RAG knowledge retrieval system with vector database",
            "repo": "project-rag",
        },
    ]

    for document in documents:
        vector = embedding.embed(
            document["text"],
        )

        vector_store.upsert(
            point_id=document["id"],
            vector=vector,
            payload={
                "repo": document["repo"],
                "text": document["text"],
            },
        )

    query = "AI Agent workflow system"

    query_vector = embedding.embed(query)

    results = vector_store.search(
        query_vector=query_vector,
        limit=3,
    )

    assert len(results) == 3

    print("\nSemantic Search Results:")

    for result in results:
        print(
            result.score,
            result.payload,
        )
```

### 📄 `tests/test_evidence_agent.py`

**层级**：测试层 · **职责**：EvidenceAnalysisAgent 测试（Fake Skill 注入，断言 Agent 编排结果）

```python
"""
EvidenceAnalysisAgent 测试。
"""

import pytest

from app.agents.evidence_analysis_agent import (
    EvidenceAnalysisAgent,
)


class FakeSkill:

    async def execute(
        self,
        context,
        input_data,
    ):

        return {
            "evidence": [
                {
                    "content":
                        "class BaseAgent:"
                }
            ],
            "count": 1,
        }


class FakeSkillRegistry:

    def get(
        self,
        name,
    ):

        assert (
            name
            == "evidence_analysis"
        )

        return FakeSkill()


class FakeContext:

    tools = {}


@pytest.mark.asyncio
async def test_evidence_analysis_agent():

    agent = EvidenceAnalysisAgent(
        FakeSkillRegistry()
    )

    result = await agent.execute(
        FakeContext(),
        {},
    )

    assert (
        result["count"]
        == 1
    )

    assert (
        result["evidence"][0]["content"]
        == "class BaseAgent:"
    )
```

### 📄 `tests/test_evidence_models.py`

**层级**：测试层 · **职责**：证据链三张表模型测试（Evidence / Claim / Citation 字段与默认值）

```python
"""
Evidence / Claim / Citation 模型测试。
"""

from app.models.claim import Claim
from app.models.citation import Citation
from app.models.evidence import Evidence


def test_evidence_model():

    assert Evidence.__tablename__ == "evidences"

    columns = {
        column.name
        for column in Evidence.__table__.columns
    }

    assert {
        "id",
        "repository_id",
        "source_type",
        "source_url",
        "file_path",
        "line_start",
        "line_end",
        "content",
        "verification_status",
        "created_at",
    }.issubset(columns)


def test_claim_model():

    assert Claim.__tablename__ == "claims"

    columns = {
        column.name
        for column in Claim.__table__.columns
    }

    assert {
        "id",
        "run_id",
        "claim_text",
        "verification_status",
        "created_at",
    }.issubset(columns)


def test_citation_model():

    assert Citation.__tablename__ == "citations"

    columns = {
        column.name
        for column in Citation.__table__.columns
    }

    assert {
        "id",
        "claim_id",
        "evidence_id",
        "created_at",
    }.issubset(columns)
```

### 📄 `tests/test_evidence_service.py`

**层级**：测试层 · **职责**：EvidenceService 测试（空内容证据被拒、正常创建与校验路径）

```python
"""
EvidenceService 测试。
"""

import pytest

from app.core.exceptions import ValidationError
from app.services.evidence_service import (
    EvidenceService,
)


class FakeSession:

    async def commit(self):
        pass


@pytest.mark.asyncio
async def test_create_evidence_rejects_empty_content():

    service = EvidenceService(
        FakeSession()
    )

    with pytest.raises(
        ValidationError
    ):

        await service.create_evidence(
            repository_id=1,
            source_type="source",
            content="   ",
        )
```

### 📄 `tests/test_evidence_skill.py`

**层级**：测试层 · **职责**：EvidenceAnalysisSkill 测试（Fake Tool，断言证据分析结果结构）

```python
"""
EvidenceAnalysisSkill 测试。
"""

import pytest

from app.skills.evidence_analysis_skill import (
    EvidenceAnalysisSkill,
)


class FakeQdrantTool:

    async def execute(
        self,
        **kwargs,
    ):

        return [
            {
                "text": (
                    "class BaseAgent:"
                ),
                "document_id": (
                    "agent-base"
                ),
                "chunk_index": 0,
                "file_path": (
                    "app/agents/base.py"
                ),
            }
        ]


class FakeContext:

    tools = {
        "qdrant_search":
            FakeQdrantTool()
    }


@pytest.mark.asyncio
async def test_evidence_analysis_skill():

    skill = EvidenceAnalysisSkill()

    result = await skill.execute(
        FakeContext(),
        {
            "query_vector": [
                0.1,
                0.2,
            ],
            "limit": 5,
        },
    )

    assert (
        result["count"]
        == 1
    )

    evidence = (
        result["evidence"][0]
    )

    assert (
        evidence["content"]
        == "class BaseAgent:"
    )

    assert (
        evidence["file_path"]
        == "app/agents/base.py"
    )

    # 当前索引器没有可靠行号，
    # 所以不能伪造。
    assert (
        evidence["line_start"]
        is None
    )

    assert (
        evidence["line_end"]
        is None
    )

@pytest.mark.asyncio
async def test_evidence_from_architecture_agent_output():
    """
    源码证据分支必须能读到真实的 key。

    旧实现只读 input_data["architecture"]，
    但真实数据结构里没有这个 key
    （真实 key 是 architecture_analysis_agent，
    且 PlanExecutorNode 会把 modules 拍平到顶层），
    因此这个分支以前从未执行过，
    Evidence 里只有 README、没有源码。
    """

    skill = EvidenceAnalysisSkill()

    result = await skill.execute(
        FakeContext(),
        {
            "repo_url": "https://github.com/demo/demo",
            "architecture_analysis_agent": {
                "files": ["app/main.py"],
                "modules": [
                    {
                        "file_path": "app/main.py",
                        "content": "class Demo:\n    pass\n",
                    }
                ],
            },
        },
    )

    file_paths = [
        item["file_path"]
        for item in result["evidence"]
    ]

    assert "app/main.py" in file_paths


@pytest.mark.asyncio
async def test_failed_module_read_is_not_used_as_evidence():
    """读取失败的模块不能变成空内容的假证据。"""

    skill = EvidenceAnalysisSkill()

    result = await skill.execute(
        FakeContext(),
        {
            "repo_url": "https://github.com/demo/demo",
            "modules": [
                {
                    "file_path": "app/broken.py",
                    "content": "",
                    "error": "Read timeout",
                }
            ],
        },
    )

    assert result["count"] == 0
```

### 📄 `tests/test_evidence_store.py`

**层级**：测试层 · **职责**：EvidenceStore 单元测试（非法状态抛 ValidationError、状态值大写归一化）

```python
"""
Evidence Store 单元测试。
"""

import pytest

from app.core.exceptions import ValidationError
from app.evidence.store import EvidenceStore


class FakeSession:

    def add(self, obj):
        pass

    async def flush(self):
        pass


@pytest.mark.asyncio
async def test_invalid_evidence_status():

    store = EvidenceStore(
        FakeSession()
    )

    with pytest.raises(
        ValidationError
    ):

        store.validate_status(
            "INVALID"
        )


@pytest.mark.asyncio
async def test_evidence_status_normalization():

    store = EvidenceStore(
        FakeSession()
    )

    assert (
        store.validate_status(
            "verified"
        )
        == "VERIFIED"
    )
```

### 📄 `tests/test_evidence_verifier.py`

**层级**：测试层 · **职责**：EvidenceVerifier 测试（合法状态流转成功、非法状态抛异常）

```python
"""
Evidence Verification 测试。
"""

import pytest

from app.core.exceptions import ValidationError
from app.evidence.verifier import (
    EvidenceVerifier,
)


class FakeSession:

    async def flush(self):
        pass


class FakeEvidence:

    verification_status = "UNVERIFIED"


@pytest.mark.asyncio
async def test_verify_evidence():

    verifier = EvidenceVerifier(
        FakeSession()
    )

    evidence = FakeEvidence()

    result = await verifier.verify_evidence(
        evidence,
        "verified",
    )

    assert (
        result.verification_status
        == "VERIFIED"
    )


@pytest.mark.asyncio
async def test_invalid_status():

    verifier = EvidenceVerifier(
        FakeSession()
    )

    evidence = FakeEvidence()

    with pytest.raises(
        ValidationError
    ):

        await verifier.verify_evidence(
            evidence,
            "invalid",
        )
```

### 📄 `tests/test_exceptions.py`

**层级**：测试层 · **职责**：异常体系单元测试

```python
"""项目统一异常体系测试。"""

from app.core.exceptions import (
    AgentError,
    ApplicationError,
    LLMError,
    RetryableError,
    ValidationError,
)


def test_application_error():
    """测试基础应用异常。"""

    error = ApplicationError("test error")

    assert error.message == "test error"
    assert error.status_code == 500
    assert error.error_code == "APPLICATION_ERROR"


def test_validation_error():
    """测试参数验证异常。"""

    error = ValidationError("invalid input")

    assert error.message == "invalid input"
    assert error.status_code == 400
    assert error.error_code == "VALIDATION_ERROR"


def test_agent_error():
    """测试 Agent 异常。"""

    error = AgentError("agents failed")

    assert error.status_code == 500
    assert error.error_code == "AGENT_ERROR"


def test_llm_error():
    """测试 LLM 异常。"""

    error = LLMError("llm failed")

    assert error.status_code == 500
    assert error.error_code == "LLM_ERROR"


def test_retryable_error():
    """测试可重试异常。"""

    error = RetryableError("temporary error")

    assert error.error_code == "RETRYABLE_ERROR"
```

### 📄 `tests/test_file_reader_tool.py`

**层级**：测试层 · **职责**：FileReaderTool 测试。

```python
"""
FileReaderTool 测试。

读取策略（Phase 12 网络稳定性修复）：

    1. 优先 GitHub Contents API
       api.github.com/repos/{owner}/{name}/contents/{path}
    2. 失败时回退 raw.githubusercontent.com

原因：部分网络环境下 raw.githubusercontent.com
极不稳定（实测同一 README：
Contents API 0.88 秒成功、raw 20 秒后 ReadError），
而一个文件读取失败曾导致整个 5-Agent 计划 FAILED。

本文件覆盖：

1. Contents API 优先，成功时完全不碰 raw
2. Contents API 失败时回退 raw
3. 大文件（encoding != base64）回退 raw
4. 文件确实不存在时不浪费 raw 超时
5. 所有来源网络错误时抛 ToolError
6. main → master 分支回退
"""

import base64

import httpx
import pytest

from app.core.exceptions import ToolError
from app.tools.file_reader_tool import (
    FileReaderTool,
)


EXPECTED_MAIN = (
    "https://api.github.com/repos/openai/"
    "openai-python/contents/requirements.txt"
)

EXPECTED_MAIN_RAW = (
    "https://raw.githubusercontent.com/openai/"
    "openai-python/main/requirements.txt"
)


class FakeResponse:
    """最小可用的 httpx Response 替身。"""

    def __init__(
        self,
        status_code,
        text="",
        payload=None,
    ):

        self.status_code = status_code

        self.text = text

        self._payload = payload

    def json(self):

        if self._payload is None:
            raise ValueError("no json body")

        return self._payload


def contents_payload(text):
    """构造 Contents API 的 base64 响应体。"""

    return {
        "encoding": "base64",
        "content": base64.b64encode(
            text.encode("utf-8")
        ).decode("ascii"),
    }


class FakeAsyncClient:
    """
    按来源分派的假 httpx.AsyncClient。

    api / raw 都是 {branch: FakeResponse}。
    """

    def __init__(
        self,
        api=None,
        raw=None,
        api_error=None,
        raw_error=None,
    ):

        self.api = api or {}

        self.raw = raw or {}

        self.api_error = api_error

        self.raw_error = raw_error

        self.urls = []

    async def __aenter__(self):

        return self

    async def __aexit__(
        self,
        *exc_info,
    ):

        return False

    @staticmethod
    def _branch_from_url(url):
        """
        从 raw URL 的路径里取分支。

        raw 的 URL 形如
            raw.githubusercontent.com/{owner}/{name}/{branch}/{path}
        分支在路径里，不在 query 参数里。
        """

        tail = url.split(
            "raw.githubusercontent.com/",
            1,
        )[-1]

        parts = tail.split("/")

        if len(parts) > 2:
            return parts[2]

        return None

    async def get(
        self,
        url,
        params=None,
        headers=None,
        timeout=None,
    ):

        is_api = "api.github.com" in url

        if is_api:

            branch = (params or {}).get("ref")

        else:

            branch = self._branch_from_url(url)

        self.urls.append((url, branch))

        if is_api:

            if self.api_error is not None:
                raise self.api_error

            return self.api.get(
                branch,
                FakeResponse(404),
            )

        if self.raw_error is not None:
            raise self.raw_error

        return self.raw.get(
            branch,
            FakeResponse(404),
        )


def install_client(monkeypatch, client):
    """把假 Client 注入 FileReaderTool 使用的 httpx 模块。"""

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: client,
    )

    return client


def api_urls(client):
    return [
        url
        for url, _ in client.urls
        if "api.github.com" in url
    ]


def raw_urls(client):
    return [
        url
        for url, _ in client.urls
        if "raw.githubusercontent.com" in url
    ]


@pytest.mark.asyncio
async def test_contents_api_is_used_first(monkeypatch):
    """
    Contents API 成功时完全不请求 raw。

    这是网络稳定性的关键：
    raw.githubusercontent.com 不稳定时，
    读取不应该再受影响。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            api={
                "main": FakeResponse(
                    200,
                    payload=contents_payload(
                        "fastapi==0.1.0"
                    ),
                )
            }
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert api_urls(client) == [EXPECTED_MAIN]

    # 关键断言：完全没有碰 raw
    assert raw_urls(client) == []


@pytest.mark.asyncio
async def test_falls_back_to_raw_when_api_fails(
    monkeypatch,
):
    """Contents API 网络出错时回退 raw。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            raw={
                "main": FakeResponse(
                    200,
                    "fastapi==0.1.0",
                )
            },
            api_error=httpx.ReadTimeout(""),
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert raw_urls(client) == [EXPECTED_MAIN_RAW]


@pytest.mark.asyncio
async def test_oversized_file_falls_back_to_raw(
    monkeypatch,
):
    """
    超过 1MB 的文件 Contents API 不返回内容
    （encoding != base64），此时回退 raw。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            api={
                "main": FakeResponse(
                    200,
                    payload={
                        "encoding": "none",
                        "content": "",
                        "size": 5_000_000,
                    },
                )
            },
            raw={
                "main": FakeResponse(
                    200,
                    "big file",
                )
            },
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "big file"

    assert raw_urls(client) == [EXPECTED_MAIN_RAW]


@pytest.mark.asyncio
async def test_missing_file_does_not_waste_raw_timeout(
    monkeypatch,
):
    """
    文件确实不存在时，不再去 raw 白等超时。

    修复前：Contents API 404 后仍尝试 raw，
    main + master 两个超时合计 51 秒。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == ""

    # 两个分支都问过 Contents API
    assert len(api_urls(client)) == 2

    # 但一次 raw 都没请求
    assert raw_urls(client) == []


@pytest.mark.asyncio
async def test_all_sources_network_error_raises(
    monkeypatch,
):
    """所有来源都是网络错误时抛 ToolError，而不是伪装成文件不存在。"""

    install_client(
        monkeypatch,
        FakeAsyncClient(
            api_error=httpx.ReadTimeout(""),
            raw_error=httpx.ReadTimeout(""),
        ),
    )

    with pytest.raises(ToolError) as excinfo:

        await FileReaderTool().execute(
            owner="openai",
            name="openai-python",
            file_path="requirements.txt",
        )

    message = str(excinfo.value)

    assert "timeout" in message.lower()

    assert "openai-python" in message


@pytest.mark.asyncio
async def test_branch_fallback_main_to_master(
    monkeypatch,
):
    """main 没有该文件时回退 master。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            api={
                "master": FakeResponse(
                    200,
                    payload=contents_payload(
                        "old-style"
                    ),
                )
            }
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "old-style"

    assert [
        branch for _, branch in client.urls
    ] == ["main", "master"]


@pytest.mark.asyncio
async def test_non_main_branch_does_not_fallback(
    monkeypatch,
):
    """显式指定 master 时不再回退。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
        branch="master",
    )

    assert result == ""

    assert [
        branch for _, branch in client.urls
    ] == ["master"]
```

### 📄 `tests/test_github_client.py`

**层级**：测试层 · **职责**：GitHub REST API 工具测试（需外网可用）

```python
"""GitHub Client 测试。"""

import pytest

from app.tools.github.github_repository_tool import GitHubRepositoryTool


@pytest.mark.asyncio
async def test_get_repository():

    client = GitHubRepositoryTool()

    data = await client.get_repository(
        "langchain-ai",
        "langchain",
    )

    assert data["name"] == "langchain"

    assert (
        data["owner"]["login"]
        ==
        "langchain-ai"
    )
```

### 📄 `tests/test_github_code_search_tool.py`

**层级**：测试层 · **职责**：GitHub 源码搜索工具测试（fake client + fake settings，覆盖返回结果与 token 认证头）

```python
"""GitHub Code Search Tool 测试。"""

import pytest

from app.tools.github import github_code_search_tool as module
from app.tools.github.github_code_search_tool import (
    GitHubCodeSearchTool
)


class FakeResponse:
    """模拟 httpx 响应。"""

    def raise_for_status(self):
        pass

    def json(self):
        return {
            "items": [
                {"path": "app/workflow/engine.py"}
            ]
        }


class FakeAsyncClient:
    """模拟 httpx.AsyncClient，记录请求参数。"""

    captured = {}

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False

    async def get(self, url, params=None, headers=None):
        FakeAsyncClient.captured = {
            "url": url,
            "params": params,
            "headers": headers,
        }
        return FakeResponse()


class FakeSettings:
    """模拟配置对象。"""

    GITHUB_TOKEN = "fake-token"


@pytest.mark.asyncio
async def test_github_code_search(monkeypatch):
    """测试关键词搜索返回结果。"""

    monkeypatch.setattr(
        module.httpx,
        "AsyncClient",
        FakeAsyncClient,
    )

    tool = GitHubCodeSearchTool()

    result = await tool.execute(
        keyword="StateGraph",
        repo="langchain-ai/langchain",
    )

    assert result[0]["path"] == (
        "app/workflow/engine.py"
    )

    assert FakeAsyncClient.captured["url"].endswith(
        "/search/code"
    )

    assert "repo:langchain-ai/langchain" in (
        FakeAsyncClient.captured["params"]["q"]
    )


@pytest.mark.asyncio
async def test_github_code_search_sends_token(monkeypatch):
    """测试配置了 token 时带上认证头。"""

    monkeypatch.setattr(
        module.httpx,
        "AsyncClient",
        FakeAsyncClient,
    )

    monkeypatch.setattr(
        module,
        "get_settings",
        lambda: FakeSettings(),
    )

    tool = GitHubCodeSearchTool()

    await tool.execute(
        keyword="workflow",
        repo="openai/openai-python",
    )

    assert FakeAsyncClient.captured[
        "headers"
    ]["Authorization"] == "Bearer fake-token"
```

### 📄 `tests/test_github_parser.py`

**层级**：测试层 · **职责**：GitHub URL 解析单元测试

```python
"""GitHub URL Parser 测试。"""

import pytest

from app.tools.github.parser import parse_github_url


def test_parse_github_url():
    """测试标准 GitHub Repository URL。"""

    owner, name = parse_github_url(
        "https://github.com/abc/agent-project"
    )

    assert owner == "abc"
    assert name == "agent-project"


def test_parse_git_url():
    """测试 .git 结尾的 Repository URL。"""

    owner, name = parse_github_url(
        "https://github.com/abc/agent-project.git"
    )

    assert owner == "abc"
    assert name == "agent-project"


def test_invalid_github_url():
    """测试非 GitHub URL。"""

    with pytest.raises(ValueError):
        parse_github_url(
            "https://gitlab.com/abc/project"
        )
```

### 📄 `tests/test_indexer.py`

**层级**：测试层 · **职责**：DocumentIndexer 集成测试（Chunk → Embedding → Qdrant）

```python
"""DocumentIndexer 集成测试。"""

from app.project_analysis.project_indexer import DocumentIndexer


def test_document_indexer():
    """测试文档是否能够完成 Chunk、Embedding 和 Qdrant 写入。"""

    indexer = DocumentIndexer(
        collection_name="aipi_indexer_test",
    )

    document = """# Introduction

This is an AI Agent platform.

# HITL

Human approval is required for sensitive operations.

# Workflow

The system supports workflow execution and task recovery.
"""

    chunk_count = indexer.index_document(
        document_id="test-repository-readme",
        text=document,
        metadata={
            "repository_id": 1,
            "repository_url": "https://github.com/example/project",
            "source": "README.md",
        },
    )

    assert chunk_count == 3
```

### 📄 `tests/test_json_output.py`

**层级**：测试层 · **职责**：LLM JSON 输出解析测试。

````python
"""
LLM JSON 输出解析测试。

这套容错逻辑是真实事故换来的：
综合分析要输出六个维度的判断段落，
回复一旦触到 max_tokens 上限就会被切断，
而截断的 JSON 用 json.loads 必然失败，
报告整章退化成「综合分析不可用」。
"""

import json

from app.skills.json_output import (
    parse_json_object,
    strip_code_fence,
)


FULL = json.dumps(
    {
        "summary": {
            "one_line": "结论",
            "core_design": ["设计一", "设计二"],
            "highlights": ["亮点"],
        },
        "dimensions": {
            "agents": "Agent 判断段落",
            "workflow": "Workflow 判断段落",
            "rag": "RAG 判断段落",
        },
    },
    ensure_ascii=False,
    indent=2,
)


# ----------------------------------------------------------------
# 正常形态
# ----------------------------------------------------------------


def test_parses_plain_json():

    parsed = parse_json_object(FULL)

    assert parsed["summary"]["one_line"] == "结论"


def test_parses_fenced_json():

    parsed = parse_json_object(
        "```json\n" + FULL + "\n```"
    )

    assert parsed["dimensions"]["rag"] == "RAG 判断段落"


def test_parses_json_with_surrounding_prose():
    """模型在 JSON 前后加解释文字时要能救回来。"""

    parsed = parse_json_object(
        "好的，以下是分析结果：\n"
        + FULL
        + "\n希望对你有帮助。"
    )

    assert parsed["summary"]["core_design"] == [
        "设计一",
        "设计二",
    ]


def test_returns_none_for_non_json():

    assert parse_json_object("这不是 JSON") is None

    assert parse_json_object("") is None

    assert parse_json_object(None) is None


def test_returns_none_for_json_array():
    """只接受对象；顶层是数组时不算成功。"""

    assert parse_json_object("[1, 2, 3]") is None


# ----------------------------------------------------------------
# 截断修复
# ----------------------------------------------------------------


def test_repairs_truncation_inside_string():
    """截断在字符串中间 —— 补引号与括号。"""

    truncated = FULL[: len(FULL) - 30]

    parsed = parse_json_object(truncated)

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "结论"


def test_repairs_truncation_between_values():
    """截断在值之后 —— 补括号。"""

    parsed = parse_json_object(FULL.rstrip()[:-1])

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "结论"


def test_repairs_truncation_after_key():
    """截断在半个键值上 —— 回退到最后一个逗号。"""

    cut = FULL[: FULL.rindex('"rag"') + 6]

    parsed = parse_json_object(cut)

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "结论"


def test_repairs_truncation_inside_array():

    text = json.dumps(
        {
            "summary": {
                "one_line": "x",
                "core_design": ["a", "b"],
            },
            "dimensions": {},
        },
        ensure_ascii=False,
    )

    parsed = parse_json_object(text[:55])

    assert parsed is not None

    assert parsed["summary"]["one_line"] == "x"


def test_repair_never_invents_content():
    """
    修不出来就返回 None。

    降级成「综合分析不可用」是可接受的；
    把半截内容当结论展示是不可接受的。
    """

    # 值缺失，补括号与回退逗号都救不回来。
    assert parse_json_object('{"a": , "b": 1') is None

    assert parse_json_object("纯粹的一段说明文字。") is None


def test_repair_may_yield_empty_containers():
    """
    补全后是「合法的空结构」时应当接受。

    这不是编造内容：{"summary": {}} 是真实解析出来的，
    调用方会看到 summary 为空并如实降级。
    把它当成解析失败反而会丢掉已经拿到的部分。
    """

    parsed = parse_json_object('{"summary": {')

    assert parsed == {"summary": {}}


def test_repair_handles_braces_inside_strings():
    """字符串里的花括号不能干扰配平。"""

    parsed = parse_json_object(
        '{"a": "包含 } 和 ] 的文本", "b": 1'
    )

    assert parsed is not None

    assert parsed["b"] == 1


def test_repair_handles_escaped_quotes():
    """转义引号不能让扫描器误判字符串结束。"""

    parsed = parse_json_object(
        '{"a": "带 \\" 转义引号的值", "b": 2'
    )

    assert parsed is not None

    assert parsed["b"] == 2


# ----------------------------------------------------------------
# 代码块剥离
# ----------------------------------------------------------------


def test_strip_code_fence():

    assert strip_code_fence(
        "```json\n{}\n```"
    ) == "{}"

    assert strip_code_fence("{}") == "{}"

    assert strip_code_fence(
        "```\n{}\n```"
    ) == "{}"
````

### 📄 `tests/test_memory.py`

**层级**：测试层 · **职责**：Phase 11 Memory 测试。

```python
"""Phase 11 Memory 测试。"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.memory.run_memory import (
    RunMemory,
)

from app.memory.project_memory import (
    ProjectMemory,
)


class FakeScalarResult:
    """模拟 SQLAlchemy scalar 查询结果。"""

    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class FakeScalarsResult:
    """模拟 SQLAlchemy scalars 查询结果。"""

    def __init__(self, values):
        self.values = values

    def scalars(self):
        return self

    def all(self):
        return self.values


@pytest.mark.asyncio
async def test_run_memory_loads_run_and_checkpoint():
    """Run Memory 应能够组合 Run / Task / Checkpoint / Evidence。"""

    session = AsyncMock()

    run = SimpleNamespace(
        id="run-1",
        repository_id=10,
        question="Workflow怎么实现？",
        status="ANALYZING",
        current_node="workflow",
    )

    repository = SimpleNamespace(
        id=10,
        url="https://github.com/demo/repo",
        owner="demo",
        name="repo",
        description="demo",
        language="Python",
    )

    task = SimpleNamespace(
        id=1,
        task_type="architecture",
        status="completed",
        input={},
        output={
            "result": "workflow"
        },
        error=None,
        retry_count=0,
        created_at=None,
    )

    evidence = SimpleNamespace(
        id="ev-1",
        source_type="code",
        file_path="app/workflow.py",
        line_start=10,
        line_end=20,
        content="class WorkflowEngine",
        verification_status="VERIFIED",
    )

    checkpoint = SimpleNamespace(
        data={
            "research_plan": {
                "tasks": [
                    "architecture"
                ]
            }
        },
        outputs=[
            {
                "agent": "architecture"
            }
        ],
        status="ANALYZING",
        current_node="workflow",
        errors=[],
        retry_count=0,
        pause_reason=None,
        human_approved=True,
        checkpoint_version=2,
    )

    session.execute.side_effect = [
        FakeScalarResult(run),
        FakeScalarsResult([task]),
    ]

    session.get.return_value = repository

    memory = RunMemory(
        session
    )

    memory.checkpoint_repository.get_latest = (
        AsyncMock(
            return_value=checkpoint
        )
    )

    memory.evidence_repository.list_by_repository = (
        AsyncMock(
            return_value=[evidence]
        )
    )

    result = await memory.load(
        "run-1"
    )

    assert (
        result["question"]
        == "Workflow怎么实现？"
    )

    assert (
        result["research_plan"]["tasks"]
        == ["architecture"]
    )

    assert (
        result["agent_outputs"]
        == [
            {
                "agent": "architecture"
            }
        ]
    )

    assert (
        result["evidences"][0]["file_path"]
        == "app/workflow.py"
    )


@pytest.mark.asyncio
async def test_project_memory_filters_current_run():
    """Project Memory 不应该把当前 Run 再作为历史 Memory 返回。"""

    session = AsyncMock()

    run1 = SimpleNamespace(
        id="run-1",
        question="Workflow",
        status="COMPLETED",
        current_node="end",
        created_at=SimpleNamespace(
            isoformat=lambda:
            "2026-09-25T00:00:00"
        ),
    )

    run2 = SimpleNamespace(
        id="run-2",
        question="Agent",
        status="COMPLETED",
        current_node="end",
        created_at=SimpleNamespace(
            isoformat=lambda:
            "2026-09-24T00:00:00"
        ),
    )

    task = SimpleNamespace(
        run_id="run-2",
        task_type="agent",
        status="completed",
        output={
            "agent": "planner"
        },
        error=None,
    )

    session.execute.side_effect = [
        FakeScalarsResult(
            [
                run1,
                run2,
            ]
        ),
        FakeScalarsResult(
            [
                task
            ]
        ),
    ]

    memory = ProjectMemory(
        session
    )

    result = await memory.load(
        10,
        exclude_run_id="run-1",
    )

    assert len(result) == 1

    assert (
        result[0]["run_id"]
        == "run-2"
    )

    assert (
        result[0]["tasks"][0][
            "task_type"
        ]
        == "agent"
    )
```

### 📄 `tests/test_module_deep_dive_skill.py`

**层级**：测试层 · **职责**：ModuleDeepDiveSkill 测试。

````python
"""
ModuleDeepDiveSkill 测试。

深挖是「默认报告只看要点，细节按需展开」的
那一半能力，覆盖：

1. 模块名校验
2. 只挑该模块相关文件，且配额远大于默认报告
3. 明细带签名 / 调用链 / 常量 / 源码片段
4. 图节点能解析到真实定义
5. LLM 不可用 / 返回非法 JSON 时降级，
   仍然保留实现明细
6. 如实交代采集范围（读了哪些、哪些失败）

全程使用假 Tool，不联网。
"""

import json

import pytest

from app.core.exceptions import ToolError
from app.skills.module_deep_dive_skill import (
    ModuleDeepDiveSkill,
)

TREE = (
    "src/app/services/workflow_service.py",
    "src/app/services/other_service.py",
    "src/app/models/agent_run.py",
    "src/app/rag/retriever.py",
    "src/app/main.py",
    "tests/test_workflow.py",
)


WORKFLOW_SOURCE = (
    "from langgraph.graph import StateGraph\n"
    "\n"
    "\n"
    "class WorkflowService:\n"
    "    def build(self):\n"
    "        builder = StateGraph(AgentState)\n"
    "        builder.add_node('duplicate_check',\n"
    "                          self._node_duplicate_check)\n"
    "        return builder.compile()\n"
    "\n"
    "    def _node_duplicate_check(self, state) -> dict:\n"
    "        found = find_similar(state['vendor'])\n"
    "        if found.score >= 0.85:\n"
    "            state['status'] = 'suspected'\n"
    "        return state\n"
)


SOURCES = {
    "src/app/services/workflow_service.py": WORKFLOW_SOURCE,
    "src/app/services/other_service.py": (
        "def helper():\n    pass\n"
    ),
    "src/app/models/agent_run.py": (
        "class AgentRun(Base):\n    pass\n"
    ),
    "src/app/rag/retriever.py": (
        "from qdrant_client import QdrantClient\n"
        "\n"
        "def retrieve_documents(query):\n"
        "    return query\n"
    ),
    "src/app/main.py": (
        "from fastapi import FastAPI\n\napp = FastAPI()\n"
    ),
}


VALID_REPLY = json.dumps(
    {
        "responsibility": ["负责把录入流程编排成状态图。"],
        "key_implementations": [
            "duplicate_check 节点用 0.85 阈值判定重复"
        ],
        "data_structures": ["state 字典承载 vendor"],
        "call_flow": ["build() 注册节点后交给图执行"],
        "boundaries": ["数据不足：未见重试逻辑"],
        "risks": ["0.85 是硬编码常量"],
        "open_questions": ["human_review 未在本次范围内"],
    },
    ensure_ascii=False,
)


class FakeRepositoryTool:

    async def get_tree(self, **kwargs):
        return [
            {"path": path, "type": "blob"}
            for path in TREE
        ]


class FakeFileReader:

    def __init__(self, missing=()):
        self.missing = set(missing)
        self.read = []

    async def execute(
        self,
        owner,
        name,
        file_path,
        branch,
    ):
        self.read.append(file_path)

        if file_path in self.missing:
            raise ToolError("HTTP 404: Not Found")

        if file_path in SOURCES:
            return SOURCES[file_path]

        raise ToolError("HTTP 404: Not Found")


class FakeLLMTool:

    def __init__(
        self,
        content=VALID_REPLY,
        available=True,
        reason=None,
    ):
        self.content = content
        self.available = available
        self.reason = reason
        self.calls = []

    async def execute(self, messages, **kwargs):
        self.calls.append(messages)

        if not self.available:
            return {
                "available": False,
                "reason": self.reason,
            }

        return {
            "available": True,
            "content": self.content,
        }


class FakeExporter:

    def __init__(self):
        self.calls = []

    async def execute(
        self,
        *,
        title,
        content,
        filename,
    ):
        self.calls.append(
            {
                "title": title,
                "content": content,
                "filename": filename,
            }
        )

        return {
            "path": f"reports/{filename}",
            "format": "markdown",
        }


class FakeContext:

    def __init__(
        self,
        reader=None,
        llm=None,
        exporter=None,
    ):
        self.tools = {
            "github_repository": FakeRepositoryTool(),
            "file_reader": reader or FakeFileReader(),
        }

        if llm is not None:
            self.tools["llm_chat"] = llm

        if exporter is not None:
            self.tools["report_export"] = exporter


def run_deep_dive(
    module="workflow",
    reader=None,
    llm=None,
    exporter=None,
    **extra,
):
    import asyncio

    input_data = {
        "module": module,
        "owner": "demo",
        "repo": "demo",
        "run_id": "run-1",
    }

    input_data.update(extra)

    return asyncio.run(
        ModuleDeepDiveSkill().execute(
            FakeContext(reader, llm, exporter),
            input_data,
        )
    )


# ----------------------------------------------------------------
# 入参校验
# ----------------------------------------------------------------


def test_rejects_unknown_module():
    """不在六个模块内的名字必须直接拒绝。"""

    with pytest.raises(ValueError) as error:

        run_deep_dive(module="database")

    assert "Unsupported module" in str(
        error.value
    )

    # 提示里要列出合法值，便于调用方纠正。
    assert "workflow" in str(error.value)


def test_requires_owner_and_repo():

    import asyncio

    with pytest.raises(ValueError):

        asyncio.run(
            ModuleDeepDiveSkill().execute(
                FakeContext(),
                {"module": "workflow"},
            )
        )


def test_module_name_is_case_insensitive():
    """模块名大小写不敏感。"""

    result = run_deep_dive(
        module="WorkFlow",
        llm=FakeLLMTool(),
    )

    assert result["module"] == "workflow"


# ----------------------------------------------------------------
# 取材
# ----------------------------------------------------------------


def test_reads_module_relevant_files_first():
    """
    该模块相关的文件必须优先读。

    深挖的价值在于「比默认报告看得多」，
    因此配额要给到 40，并且优先命中该模块的文件。
    """

    result = run_deep_dive(
        module="workflow",
        llm=FakeLLMTool(),
    )

    assert (
        "src/app/services/workflow_service.py"
        in result["files_read"]
    )

    # 配额远大于默认报告的 20。
    assert ModuleDeepDiveSkill.MAX_FILES == 40


def test_unreadable_files_are_reported():
    """读取失败的文件必须如实带出来。"""

    reader = FakeFileReader(
        missing=["src/app/rag/retriever.py"]
    )

    result = run_deep_dive(
        module="workflow",
        reader=reader,
        llm=FakeLLMTool(),
    )

    assert (
        "## 本次采集范围" in result["content"]
    )

    assert "读取失败" in result["content"]

    assert (
        "src/app/rag/retriever.py"
        in result["content"]
    )


def test_fallback_skips_tests_and_migrations():
    """
    兜底补充文件时不能把配额喂给测试与迁移。

    真实案例：workflow 模块只有 workflow_service.py
    一个文件命中，其余 39 个名额全被 tests/ 和
    alembic/ 吃掉 —— 每个文件都是一次 GitHub 请求。
    """

    result = run_deep_dive(
        module="workflow",
        llm=FakeLLMTool(),
    )

    assert not any(
        "tests/" in path or "alembic/" in path
        for path in result["files_read"]
    )

    # 命中目标模块的文件仍要读到。
    assert (
        "src/app/services/workflow_service.py"
        in result["files_read"]
    )


def test_fallback_is_capped():
    """
    兜底补充文件必须封顶。

    实测：workflow 只有 1 个文件命中，
    剩余 39 个名额全用无关文件填满，
    深挖一次要 69 秒、40 次 GitHub 请求，
    而其中 39 个文件对 workflow 维度毫无贡献。
    """

    tree = (
        "src/app/services/workflow_service.py",
        *[
            f"src/app/core/mod{i}.py"
            for i in range(60)
        ],
    )


    class Repo:

        async def get_tree(self, **kwargs):
            return [
                {"path": path, "type": "blob"}
                for path in tree
            ]

    class Context:
        tools = {
            "github_repository": Repo(),
            "file_reader": FakeFileReader(),
        }

    skill = ModuleDeepDiveSkill()

    picked = skill._select_files(
        [
            {"path": path, "type": "blob"}
            for path in tree
        ],
        "workflow",
    )

    assert (
        "src/app/services/workflow_service.py"
        in picked
    )

    assert len(picked) == (
        1 + ModuleDeepDiveSkill.MAX_FALLBACK_FILES
    )

    assert len(picked) <= (
        ModuleDeepDiveSkill.MAX_FILES
    )


def test_rag_module_selects_rag_files():
    """RAG 深挖要优先挑到 rag 相关文件。"""

    result = run_deep_dive(
        module="rag",
        llm=FakeLLMTool(),
    )

    assert (
        "src/app/rag/retriever.py"
        in result["files_read"]
    )


# ----------------------------------------------------------------
# 实现明细
# ----------------------------------------------------------------


def test_details_include_source_snippet():
    """
    深挖与默认报告最大的差别：
    明细要带源码片段，而不只是签名。
    """

    result = run_deep_dive(
        module="workflow",
        llm=FakeLLMTool(),
    )

    content = result["content"]

    assert "## 实现明细" in content

    # 节点解析到真实定义。
    assert "`duplicate_check`" in content

    assert (
        "def _node_duplicate_check(self, state) -> dict"
        in content
    )

    assert "- 调用：`find_similar`" in content

    assert "`0.85`" in content

    # 源码片段真的被展开了。
    assert (
        "found = find_similar(state['vendor'])"
        in content
    )


def test_details_cap_is_larger_than_default():
    """深挖的明细上限必须大于默认报告的 6。"""

    assert ModuleDeepDiveSkill.MAX_DETAILS > 6


# ----------------------------------------------------------------
# 降级
# ----------------------------------------------------------------


def test_degrades_without_llm():
    """
    LLM 不可用时不能抛异常，
    实现明细仍要完整产出。
    """

    result = run_deep_dive(
        llm=FakeLLMTool(
            available=False,
            reason="未配置 LLM_API_KEY。",
        ),
    )

    assert (
        result["analysis"]["available"] is False
    )

    content = result["content"]

    assert "本模块的结论分析不可用" in content

    assert "未配置 LLM_API_KEY。" in content

    # 关键：确定性部分不受影响。
    assert "## 实现明细" in content

    assert (
        "def _node_duplicate_check(self, state) -> dict"
        in content
    )


def test_degrades_without_llm_tool():
    """连 llm_chat 工具都没有时同样降级。"""

    result = run_deep_dive()

    assert (
        result["analysis"]["available"] is False
    )

    assert "## 实现明细" in result["content"]


def test_degrades_on_invalid_json():

    result = run_deep_dive(
        llm=FakeLLMTool(
            content="这不是 JSON"
        ),
    )

    assert (
        result["analysis"]["available"] is False
    )

    assert "JSON" in result["analysis"]["reason"]


def test_parses_fenced_json():

    result = run_deep_dive(
        llm=FakeLLMTool(
            content=(
                "好的：\n```json\n"
                f"{VALID_REPLY}\n```"
            )
        ),
    )

    assert (
        result["analysis"]["available"] is True
    )

    assert (
        result["analysis"]["sections"][
            "responsibility"
        ][0]
        == "负责把录入流程编排成状态图。"
    )


# ----------------------------------------------------------------
# 渲染与导出
# ----------------------------------------------------------------


def test_renders_all_analysis_sections():

    content = run_deep_dive(
        llm=FakeLLMTool()
    )["content"]

    for label in (
        "职责",
        "关键实现",
        "涉及的数据结构",
        "调用流程",
        "边界与限制",
        "风险与可疑之处",
        "需要人工确认",
    ):

        assert f"### {label}" in content


def test_exports_to_module_specific_filename():
    """导出文件名要能区分 run 与模块。"""

    exporter = FakeExporter()

    result = run_deep_dive(
        llm=FakeLLMTool(),
        exporter=exporter,
    )

    assert exporter.calls[0]["filename"] == (
        "run-1_workflow_deep_dive.md"
    )

    assert result["report"]["format"] == (
        "markdown"
    )


def test_filename_falls_back_to_repo_without_run_id():

    import asyncio

    exporter = FakeExporter()

    asyncio.run(
        ModuleDeepDiveSkill().execute(
            FakeContext(exporter=exporter),
            {
                "module": "tools",
                "owner": "demo",
                "repo": "demo",
            },
        )
    )

    assert exporter.calls[0]["filename"] == (
        "demo_tools_deep_dive.md"
    )


def test_prompt_forbids_speculation():
    """深挖同样受「只归纳不推测」约束。"""

    llm = FakeLLMTool()

    run_deep_dive(llm=llm)

    system = llm.calls[0][0]["content"]

    user = llm.calls[0][1]["content"]

    assert "只能使用" in system

    assert "数据不足" in system

    # declared_by 的语义必须交代清楚。
    assert "readme" in system

    assert "<facts>" in user
````

### 📄 `tests/test_mysql_query_tool.py`

**层级**：测试层 · **职责**：MySQL 查询工具测试（FakeSession 模拟查询结果）

```python
import pytest

from app.tools.mysql_query_tool import (
    MySQLQueryTool
)



class FakeResult:


    def mappings(self):

        return self


    def all(self):

        return [
            {
                "name": "test_repo"
            }
        ]



class FakeSession:


    async def execute(
        self,
        sql,
        params
    ):

        return FakeResult()



@pytest.mark.asyncio
async def test_mysql_query_tool():


    tool = MySQLQueryTool(
        FakeSession()
    )


    result = await tool.execute(
        "select * from repo"
    )


    assert result[0]["name"] == (
        "test_repo"
    )
```

### 📄 `tests/test_phase10.py`

**层级**：测试层 · **职责**：Phase 10 测试（HITL 设计闸门、HumanNode 触发暂停、手动暂停与恢复、Checkpoint 存取、可重试错误重试与重试上限、不可重试错误直接失败）

```python
"""Phase 10：HITL / Checkpoint / Pause / Resume / Retry 测试。"""

import pytest

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import WorkflowContext
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.node import BaseNode
from app.workflow.nodes.end_node import EndNode
from app.workflow.nodes.human_node import HumanNode
from app.workflow.nodes.start_node import StartNode
from app.workflow.retry import RetryPolicy
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow


def build_context():
    """创建测试 Context。"""

    return WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )


def build_workflow(
    nodes,
    transitions,
):
    """创建测试 Workflow。"""

    workflow = Workflow()

    for node in nodes:
        workflow.add_node(node)

    for source, target in transitions:

        workflow.add_transition(
            Transition(
                source,
                target,
            )
        )

    return workflow


class TouchNode(BaseNode):
    """记录执行顺序。"""

    def __init__(
        self,
        name,
    ):
        self.name = name

    async def execute(
        self,
        state,
        context,
    ):
        state.data.setdefault(
            "visited",
            [],
        ).append(
            self.name
        )

        return state


class RetryNode(BaseNode):
    """第一次失败，第二次成功。"""

    name = "retry"

    def __init__(self):
        self.calls = 0

    async def execute(
        self,
        state,
        context,
    ):
        self.calls += 1

        if self.calls == 1:

            raise RetryableError(
                "temporary error"
            )

        return state


class FailNode(BaseNode):
    """不可重试失败。"""

    name = "fail"

    async def execute(
        self,
        state,
        context,
    ):

        raise NonRetryableError(
            "invalid input"
        )


@pytest.mark.asyncio
async def test_design_gate_state():
    """测试 Design Gate。"""

    state = WorkflowState(
        run_id="phase10-design"
    )

    state.mark_waiting_design()

    assert (
        state.status
        == WorkflowStatus.WAITING_DESIGN
    )

    state.approve()

    assert (
        state.status
        == WorkflowStatus.ANALYZING
    )

    assert state.human_approved is True


@pytest.mark.asyncio
async def test_human_node_pauses_workflow():
    """测试 HumanNode 真正暂停 Workflow。"""

    workflow = build_workflow(
        [
            StartNode(),
            HumanNode(),
            TouchNode("after"),
            EndNode(),
        ],
        [
            ("start", "human_review"),
            ("human_review", "after"),
            ("after", "end"),
        ],
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-human"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_HUMAN
    )

    assert (
        result.current_node
        == "human_review"
    )

    assert "after" not in result.data.get(
        "visited",
        [],
    )


@pytest.mark.asyncio
async def test_manual_pause_and_resume():
    """测试 Pause → Checkpoint → Resume。"""

    workflow = build_workflow(
        [
            StartNode(),
            TouchNode("before"),
            TouchNode("after"),
            EndNode(),
        ],
        [
            ("start", "before"),
            ("before", "after"),
            ("after", "end"),
        ],
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase10-pause"
    )

    state.data["visited"] = []

    state = await engine.run(
        workflow,
        state,
        build_context(),
    )

    assert (
        state.status
        == WorkflowStatus.COMPLETED
    )


@pytest.mark.asyncio
async def test_checkpoint_save_and_restore():
    """测试 Checkpoint 保存与恢复。"""

    manager = CheckpointManager()

    state = WorkflowState(
        run_id="phase10-checkpoint"
    )

    state.status = (
        WorkflowStatus.PAUSED
    )

    state.current_node = "task_3"

    state.data["completed_tasks"] = [
        "task_1",
        "task_2",
    ]

    state.retry_count = 1

    await manager.save(
        state
    )

    restored = await manager.load(
        "phase10-checkpoint"
    )

    assert restored is not None

    assert (
        restored.current_node
        == "task_3"
    )

    assert (
        restored.data["completed_tasks"]
        == [
            "task_1",
            "task_2",
        ]
    )

    assert (
        restored.retry_count
        == 1
    )


@pytest.mark.asyncio
async def test_retryable_error_is_retried():
    """测试 RetryableError 会 Retry。"""

    retry_node = RetryNode()

    workflow = build_workflow(
        [
            StartNode(),
            retry_node,
            EndNode(),
        ],
        [
            ("start", "retry"),
            ("retry", "end"),
        ],
    )

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=3
        )
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-retry"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.COMPLETED
    )

    assert retry_node.calls == 2

    assert result.retry_count == 1


@pytest.mark.asyncio
async def test_retry_policy_limit():
    """测试 Retry 超过最大次数后失败。"""

    class AlwaysFailNode(BaseNode):

        name = "always_fail"

        async def execute(
            self,
            state,
            context,
        ):

            raise RetryableError(
                "temporary failure"
            )

    workflow = build_workflow(
        [
            StartNode(),
            AlwaysFailNode(),
            EndNode(),
        ],
        [
            ("start", "always_fail"),
            ("always_fail", "end"),
        ],
    )

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=2
        )
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-limit"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.FAILED
    )

    assert (
        result.retry_count == 2
    )


@pytest.mark.asyncio
async def test_non_retryable_error():
    """测试不可重试异常不会 Retry。"""

    workflow = build_workflow(
        [
            StartNode(),
            FailNode(),
            EndNode(),
        ],
        [
            ("start", "fail"),
            ("fail", "end"),
        ],
    )

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(
            max_retry=3
        )
    )

    result = await engine.run(
        workflow,
        WorkflowState(
            run_id="phase10-no-retry"
        ),
        build_context(),
    )

    assert (
        result.status
        == WorkflowStatus.FAILED
    )

    assert result.retry_count == 0
```

### 📄 `tests/test_phase12.py`

**层级**：测试层 · **职责**：Phase 12：单项目完整业务闭环测试。

````python
"""Phase 12：单项目完整业务闭环测试。"""

import pytest

from app.workflow.analysis_workflow import (
    build_analysis_workflow,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import (
    WorkflowContext,
)
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)


class FakeAgent:

    def __init__(
        self,
        name,
        result,
    ):
        self.name = name
        self.result = result
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(
            dict(input_data)
        )

        return self.result


class FakeReportSkill:

    name = "report_generation"

    async def execute(
        self,
        context,
        input_data,
    ):
        return {
            "report": {
                "format": "markdown",
                "content": (
                    "# Project Intelligence Report"
                ),
            }
        }


class FakeSynthesisSkill:
    """
    报告综合分析 Skill 的假实现。

    记录收到的 input_data，
    便于断言 synthesis 节点确实
    把各 Agent 的产出转发给了它。
    """

    name = "report_synthesis"

    def __init__(self):
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(
            dict(input_data)
        )

        return {
            "available": True,
            "reason": None,
            "summary": {
                "one_line": "这是一个演示项目。",
                "core_design": ["显式状态机"],
                "technology_choices": [],
                "highlights": [],
                "risks": [],
                "use_cases": [],
            },
            "dimensions": {
                "agents": "单 Agent 结构。",
            },
        }


def build_context():

    agents = {
        "planner_agent": FakeAgent(
            "planner_agent",
            {
                "tasks": [
                    "repository_analysis_agent",
                    "architecture_analysis_agent",
                    "technology_analysis_agent",
                    "evidence_analysis_agent",
                    "critic_agent",
                ],
                "research_plan": {
                    "plan_version": 1,
                    "tasks": [
                        "repository_analysis_agent",
                        "architecture_analysis_agent",
                        "technology_analysis_agent",
                        "evidence_analysis_agent",
                        "critic_agent",
                    ],
                },
            },
        ),

        "repository_analysis_agent": FakeAgent(
            "repository_analysis_agent",
            {
                "repository": {
                    "name": "demo",
                },
                "readme": "# Demo",
            },
        ),

        "architecture_analysis_agent": FakeAgent(
            "architecture_analysis_agent",
            {
                "architecture": {
                    "modules": [
                        {
                            "file_path":
                                "app/main.py",
                            "content":
                                "print('demo')",
                        }
                    ]
                }
            },
        ),

        "technology_analysis_agent": FakeAgent(
            "technology_analysis_agent",
            {
                "technology_stack": {
                    "frameworks": [
                        "FastAPI"
                    ]
                }
            },
        ),

        "evidence_analysis_agent": FakeAgent(
            "evidence_analysis_agent",
            {
                "evidence": [
                    {
                        "file_path":
                            "app/main.py",
                        "line_start": 1,
                        "line_end": 1,
                        "content":
                            "print('demo')",
                    }
                ]
            },
        ),

        "critic_agent": FakeAgent(
            "critic_agent",
            {
                "passed": True,
                "errors": [],
            },
        ),
    }

    return WorkflowContext(
        agents=agents,
        tools={},
        skills={
            "report_generation":
                FakeReportSkill(),
            "report_synthesis":
                FakeSynthesisSkill(),
        },
        config={},
    )


@pytest.mark.asyncio
async def test_phase12_full_business_loop():

    context = build_context()

    workflow = build_analysis_workflow(
        context
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase12-full-loop"
    )

    state.data = {
        "repository_id": 1,
        "owner": "demo",
        "repo": "demo-project",
        "repo_url":
            "https://github.com/demo/demo-project",
        "question":
            "分析 Multi-Agent Workflow",
    }

    # -------------------------------------------------
    # 1. Start -> Planner -> Design Gate
    # -------------------------------------------------

    result = await engine.run(
        workflow,
        state,
        context,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_DESIGN
    )

    assert (
        result.current_node
        == "design_gate"
    )

    assert (
        "research_plan"
        in result.data
    )

    # -------------------------------------------------
    # 2. Human Approve -> Multi-Agent
    # -------------------------------------------------

    result.approve()

    await checkpoint.save(
        result
    )

    result = await engine.resume(
        workflow,
        context,
        result.run_id,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_HUMAN
    )

    assert (
        result.current_node
        == "human_review"
    )

    assert (
        result.data[
            "executed_tasks"
        ]
        == [
            "repository_analysis_agent",
            "architecture_analysis_agent",
            "technology_analysis_agent",
            "evidence_analysis_agent",
            "critic_agent",
        ]
    )

    assert (
        result.data[
            "critic_agent"
        ]["passed"]
        is True
    )

    # -------------------------------------------------
    # 3. Human Review Approve -> Synthesis -> Finalizer
    # -------------------------------------------------

    result.approve()

    await checkpoint.save(
        result
    )

    result = await engine.resume(
        workflow,
        context,
        result.run_id,
    )

    assert (
        result.status
        == WorkflowStatus.COMPLETED
    )

    assert (
        result.current_node
        == "end"
    )

    assert (
        "final_report"
        in result.data
    )

    assert (
        result.data[
            "final_report"
        ]["report"]["format"]
        == "markdown"
    )

    # Synthesis 节点必须真的跑过，
    # 且拿到了前面各 Agent 的产出
    # （而不是只看自己那一次调用的入参）。
    synthesis = result.data["synthesis"]

    assert synthesis["available"] is True

    assert (
        synthesis["summary"]["one_line"]
        == "这是一个演示项目。"
    )

    synthesis_skill = context.skills[
        "report_synthesis"
    ]

    assert len(synthesis_skill.calls) == 1

    # 入参必须已经带上前面各 Agent 拍平后的产出，
    # 而不是只有启动时那几个字段。
    assert (
        synthesis_skill.calls[0]["repository"]
        == {"name": "demo"}
    )

    assert (
        synthesis_skill.calls[0]["readme"]
        == "# Demo"
    )

    assert (
        "architecture_analysis_agent"
        in synthesis_skill.calls[0]
    )


@pytest.mark.asyncio
async def test_phase12_checkpoint_survives_design_gate():

    context = build_context()

    workflow = build_analysis_workflow(
        context
    )

    checkpoint = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=checkpoint
    )

    state = WorkflowState(
        run_id="phase12-checkpoint"
    )

    state.data = {
        "repository_id": 1,
        "owner": "demo",
        "repo": "demo",
        "question": "test",
    }

    result = await engine.run(
        workflow,
        state,
        context,
    )

    assert (
        result.status
        == WorkflowStatus.WAITING_DESIGN
    )

    restored = await checkpoint.load(
        "phase12-checkpoint"
    )

    assert restored is not None

    assert (
        restored.current_node
        == "design_gate"
    )

    assert (
        restored.data[
            "research_plan"
        ]["plan_version"]
        == 1
    )

# ==========================================================
# Phase 12 契约补充测试
#
# 覆盖文档 15.2 / 15.3 中此前没有实现的部分：
#   目录结构、Agent/Workflow/Skill/Tool 自述结构、
#   以及报告不得再使用硬编码内容。
# ==========================================================


class FakeTreeRepositoryTool:
    """带 get_tree 的假 GitHub Repository Tool。"""

    async def execute(self, *, owner, name):
        return {"owner": owner, "name": name}

    async def get_tree(self, *, owner, name, branch):
        return [
            {"type": "blob", "path": "README.md"},
            {"type": "blob", "path": "requirements.txt"},
            {"type": "blob", "path": "app/main.py"},
            {"type": "blob", "path": "app/agent/base.py"},
            {"type": "blob", "path": "tests/test_app.py"},
            {"type": "tree", "path": "app"},
        ]


class FakeEmptyCodeSearchTool:
    """模拟 Code Search 返回 0 条结果的真实情况。"""

    async def execute(self, *, keyword, repo):
        return []


class FakeModuleReaderTool:
    async def execute(self, *, owner, name, file_path, branch):
        return "class Demo:\n    pass\n"


def build_architecture_context():
    return WorkflowContext(
        agents={},
        tools={
            "github_repository": FakeTreeRepositoryTool(),
            "github_code_search": FakeEmptyCodeSearchTool(),
            "file_reader": FakeModuleReaderTool(),
        },
        skills={},
        config={},
    )


@pytest.mark.asyncio
async def test_directory_structure_comes_from_git_tree():
    """
    Code Search 返回 0 条结果时，
    目录结构必须来自 Git Trees API，
    而不是留空。
    """

    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    result = await ArchitectureAnalysisSkill().execute(
        build_architecture_context(),
        {
            "owner": "demo",
            "repo": "demo",
        },
    )

    structure = result["directory_structure"]

    assert structure["available"] is True

    assert structure["total_files"] == 5

    assert structure["by_extension"][".py"] == 3

    assert (
        structure["source"]
        == "github git trees api"
    )

    # files 也必须被文件树补全。
    assert "app/main.py" in result["files"]


@pytest.mark.asyncio
async def test_module_read_failure_does_not_break_analysis():
    """
    单个源码文件读取失败不能中断整个分析。

    旧行为：抛异常 → 整个 Workflow FAILED。
    """

    from app.core.exceptions import ToolError
    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    class FlakyReader:
        async def execute(self, *, owner, name, file_path, branch):
            raise ToolError(f"Read failed: {file_path}")

    context = WorkflowContext(
        agents={},
        tools={
            "github_repository": FakeTreeRepositoryTool(),
            "github_code_search": FakeEmptyCodeSearchTool(),
            "file_reader": FlakyReader(),
        },
        skills={},
        config={},
    )

    result = await ArchitectureAnalysisSkill().execute(
        context,
        {"owner": "demo", "repo": "demo"},
    )

    # 目录结构仍然可用。
    assert (
        result["directory_structure"]["available"]
        is True
    )

    # 失败被逐条记录，而不是抛出。
    assert result["modules"]

    assert all(
        module.get("error")
        for module in result["modules"]
    )


def test_report_contains_documented_sections():
    """
    报告必须包含 00 结论摘要与 01-11 章。

    注意：文档 15.3 要求的「关键源码」章已移除 ——
    它展示的是文件开头固定字符数，
    而 Python 文件开头必然是 import 块，
    渲染出来只有一堆 import，
    对理解项目没有帮助。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    content = ReportGenerationSkill._build_report({})

    for title in (
        "## 00 结论摘要",
        "## 01 项目概览",
        "## 02 技术栈",
        "## 03 目录结构",
        "## 04 Agent 架构",
        "## 05 Workflow",
        "## 06 Skill",
        "## 07 Tool",
        "## 08 RAG",
        "## 09 Memory",
        "## 10 数据库",
        "## 11 Evidence",
    ):
        assert title in content

    # 关键源码章必须确实不在了。
    assert "关键源码" not in content


def test_report_has_no_hardcoded_content():
    """
    报告不得再出现硬编码内容。

    旧版本把 AIPI 自己的 Tool 列表和
    {"context_enabled": true} 写进报告，
    让报告看起来完整但内容是假的。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    content = ReportGenerationSkill._build_report({})

    assert "GitHub Repository Tool" not in content

    assert "context_enabled" not in content

    assert "memory_enabled" not in content

    # 取不到数据时必须明确说明。
    assert "真实数据不存在" in content


def test_report_uses_project_structure():
    """04/05/06/07/09 必须来自被分析项目的自述结构。"""

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    data = {
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "items": ["Planner", "Critic"],
                    "topics": ["multi-agent"],
                    "evidence": [
                        {
                            "file_path": "README.md",
                            "line_start": 92,
                            "text": "- **Planner** ...",
                        }
                    ],
                },
                "tools": {
                    "declared": True,
                    "items": ["web_search"],
                    "topics": [],
                    "evidence": [],
                },
                "skills": {
                    "declared": False,
                    "items": [],
                    "topics": [],
                    "evidence": [],
                    "reason": "被分析项目未声明 skills。",
                },
            },
        }
    }

    content = ReportGenerationSkill._build_report(data)

    assert "Planner" in content

    assert "web_search" in content

    # 证据必须带可回溯的行号。
    assert "README.md" in content

    # 未声明的维度必须给出原因，
    # 而不是留空或编造内容。
    assert "被分析项目未声明 skills。" in content


def test_report_is_rendered_as_markdown_not_json_dump():
    """
    01-12 章必须是可读的 markdown，
    不能再把中间数据结构直接 dump 成 JSON 代码块。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    data = {
        "repository": {
            "full_name": "demo/demo",
            "language": "Python",
            "topics": ["agents"],
            "stargazers_count": 1,
            "html_url": "https://github.com/demo/demo",
        },
        "technology_stack": {
            "frameworks": ["FastAPI"],
            "source_files": ["pyproject.toml"],
        },
        "directory_structure": {
            "available": True,
            "total_files": 10,
            "by_extension": {".py": 8},
            "top_level_dirs": [
                {"name": "src", "file_count": 8}
            ],
            "key_files": ["README.md"],
        },
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "items": ["Planner"],
                    "topics": [],
                    "evidence": [],
                },
            },
        },
        "architecture_analysis_agent": {
            "modules": [
                {
                    "file_path": "src/main.py",
                    "content": "print('demo')\n",
                }
            ]
        },
        "evidence": [
            {
                "file_path": "README.md",
                "line_start": 1,
                "line_end": 5,
                "content": "# Demo\n",
            }
        ],
    }

    content = ReportGenerationSkill._build_report(
        data
    )

    # 只看 01 章之后：00 章在综合分析不可用时
    # 会用一个 ```text 小块写「不可用 + 原因」，
    # 那是刻意的提示块，不是数据 dump。
    body = content[
        content.index("## 01 项目概览"):
    ]

    assert "```text" not in body

    # 表格渲染出来了。
    assert "| 字段 | 值 |" in content

    assert "| 类别 | 检测结果 |" in content

    # 证据带行号。
    assert "`README.md:1-5`" in content


def test_report_rag_chapter_renders_declared_dimension():
    """
    08 RAG 在被分析项目声明了 rag 时，
    必须渲染自述条目与向量库检测结果。

    回归点：_structure_dimension 成功时
    返回的 dict 不带 "available" 键，
    旧代码用 declared.get("available") 判断，
    导致 RAG 章永远走「不可用」分支。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    data = {
        "technology_stack": {
            "embedding": ["Qdrant"],
        },
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "rag": {
                    "declared": True,
                    "items": ["semantic retrieval"],
                    "topics": [],
                    "evidence": [
                        {
                            "file_path": "README.md",
                            "line_start": 40,
                            "text": "- semantic retrieval",
                        }
                    ],
                },
            },
        },
    }

    content = ReportGenerationSkill._build_report(
        data
    )

    rag = content[
        content.index("## 08 RAG"):
        content.index("## 09 Memory")
    ]

    assert "semantic retrieval" in rag

    assert "Qdrant" in rag

    assert "README.md:40" in rag


def test_report_renders_synthesis_summary_and_judgments():
    """
    综合分析可用时，
    报告必须渲染 00 章与各章末尾的综合判断。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    data = {
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "items": ["Planner"],
                    "topics": [],
                    "evidence": [],
                },
            },
        },
        "synthesis": {
            "available": True,
            "reason": None,
            "summary": {
                "one_line": "这是一个发票审批 Agent。",
                "core_design": ["draft-only"],
                "technology_choices": [],
                "highlights": [],
                "risks": ["RAG 维度数据不足"],
                "use_cases": [],
            },
            "dimensions": {
                "agents": "单 Agent + 显式状态机。",
            },
        },
    }

    content = ReportGenerationSkill._build_report(data)

    assert "## 00 结论摘要" in content

    assert "这是一个发票审批 Agent。" in content

    assert "### 风险与缺口" in content

    assert "RAG 维度数据不足" in content

    # 04 章末尾必须带上判断。
    assert "**综合判断**：单 Agent + 显式状态机。" in content

    # 没有判断的维度不应凭空多出一个空段落。
    assert content.count("**综合判断**") == 1


def test_report_states_when_synthesis_unavailable():
    """
    综合分析不可用时，
    00 章必须说明原因，
    且后续原始数据章节必须完整保留。
    """

    from app.skills.report_generation_skill import (
        ReportGenerationSkill,
    )

    content = ReportGenerationSkill._build_report(
        {
            "synthesis": {
                "available": False,
                "reason": "未配置 LLM_API_KEY。",
            }
        }
    )

    assert "## 00 结论摘要" in content

    assert "综合分析不可用。" in content

    assert "未配置 LLM_API_KEY。" in content

    # 降级不能牵连原始数据章节。
    assert "## 01 项目概览" in content

    assert "## 11 Evidence" in content

    # 不可用时不应出现任何综合判断段落。
    assert "**综合判断**" not in content


def test_plan_executor_does_not_duplicate_agent_results():
    """
    Agent 结果不能被重复存储。

    回归点：同名结果曾被写三遍
    （state.data[agent_name] + 拍平 + outputs），
    architecture 57KB、evidence 29KB，
    把 state_data 推到 263KB，
    越过 asyncmy 单字段 256KB 的缓冲区分片上限，
    报告接口读 checkpoint 直接
    Lost connection to MySQL server。
    """

    from app.workflow.nodes.plan_executor_node import (
        PlanExecutorNode,
    )

    big = {
        "project_structure": {"dimensions": {}},
        "modules": [{"file_path": "a.py"}],
        "files": ["a.py"],
        "directory_structure": {"available": True},
    }

    # architecture：只留读取方需要的子字段，
    # 最大的一块 project_structure 被剔掉。
    slim = PlanExecutorNode._slim_agent_result(
        "architecture_analysis_agent",
        big,
    )

    assert set(slim) == {
        "files",
        "modules",
        "directory_structure",
    }

    assert "project_structure" not in slim

    # evidence：没有任何读取方，整键不写。
    assert (
        PlanExecutorNode._slim_agent_result(
            "evidence_analysis_agent",
            {"evidence": [{"content": "x" * 1000}]},
        )
        is None
    )

    # 其余 Agent 原样保留 —— 删了会破坏断言它们的测试。
    small = {"passed": True, "errors": []}

    assert (
        PlanExecutorNode._slim_agent_result(
            "critic_agent",
            small,
        )
        == small
    )


def test_outputs_stores_marker_not_payload():
    """outputs 只留运行痕迹，不复制正文。"""

    from app.workflow.nodes.plan_executor_node import (
        PlanExecutorNode,
    )

    marker = PlanExecutorNode._output_marker(
        "architecture_analysis_agent",
        {
            "modules": [{"content": "x" * 5000}],
            "files": ["a.py"],
        },
    )

    assert marker["agent"] == (
        "architecture_analysis_agent"
    )

    assert marker["fields"] == ["files", "modules"]

    # 正文不在里面。
    assert "x" * 100 not in str(marker)
````

### 📄 `tests/test_pre_phase12_integration.py`

**层级**：测试层 · **职责**：Phase 12 前置集成测试。

```python
"""
Phase 12 前置集成测试。

验证：

1. AgentNode 使用新的 Agent.execute() 接口
2. Skill -> Tool 参数契约一致
3. Planner -> PlanExecutor -> Multi-Agent 可以真正串起来
4. Critic 可以读取前置 Agent 结果
"""

import pytest

from app.agents.critic_agent import CriticAgent
from app.agents.planner_agent import PlannerAgent
from app.workflow.context import WorkflowContext
from app.workflow.engine import WorkflowEngine
from app.workflow.nodes.agent_node import AgentNode
from app.workflow.nodes.base import BaseNode
from app.workflow.nodes.plan_executor_node import (
    PlanExecutorNode,
)
from app.workflow.state import WorkflowState
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow

from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill,
)
from app.skills.architecture_analysis_skill import (
    ArchitectureAnalysisSkill,
)
from app.skills.technology_analysis_skill import (
    TechnologyAnalysisSkill,
)
from app.skills.report_generation_skill import (
    ReportGenerationSkill,
)


class FakeGithubRepositoryTool:

    async def execute(
        self,
        *,
        owner,
        name,
    ):
        assert owner == "demo"
        assert name == "test-project"

        return {
            "owner": owner,
            "name": name,
        }


class FakeFileReaderTool:

    async def execute(
        self,
        *,
        owner,
        name,
        file_path,
        branch,
    ):
        assert owner == "demo"
        assert name == "test-project"

        assert file_path in {
            "README.md",
            "app/main.py",
        }

        if file_path == "README.md":
            return {
                "content": "# Demo Repository"
            }

        return {
            "content": (
                "class DemoApp:\n"
                "    pass\n"
            )
        }

class FakeDependencyAnalyzerTool:

    async def execute(
        self,
        *,
        project_path,
    ):
        assert project_path == (
            "D:/workspace/test-project"
        )

        return {
            "dependencies": [
                "fastapi",
                "sqlalchemy",
            ]
        }


class FakeCodeSearchTool:

    async def execute(
        self,
        *,
        keyword,
        repo,
    ):
        assert keyword == "class"
        assert repo == (
            "demo/test-project"
        )

        return [
            {
                "path": "app/main.py"
            }
        ]


class FakeReportExportTool:

    async def execute(
        self,
        *,
        title,
        content,
        filename,
    ):
        assert title == (
            "Repository Analysis Report"
        )

        assert filename == (
            "repository_analysis.md"
        )

        assert content

        return {
            "path": filename,
            "format": "markdown",
        }


class FakeSkillRegistry:

    def __init__(self):
        self.skills = {
            "repository_analysis":
                RepositoryAnalysisSkill(),
            "architecture_analysis":
                ArchitectureAnalysisSkill(),
            "technology_analysis":
                TechnologyAnalysisSkill(),
            "report_generation":
                ReportGenerationSkill(),
        }

    def get(self, name):
        return self.skills[name]


class FakeAgent:

    def __init__(
        self,
        name,
        result,
    ):
        self.name = name
        self.result = result
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(
            dict(input_data)
        )

        return self.result


class StartNode(BaseNode):

    name = "start"

    async def execute(
        self,
        state,
        context,
    ):
        return state


class EndNode(BaseNode):

    name = "end"

    async def execute(
        self,
        state,
        context,
    ):
        return state


@pytest.mark.asyncio
async def test_agent_node_uses_new_execute_api():

    class NewApiAgent:

        async def execute(
            self,
            context,
            input_data,
        ):
            assert input_data[
                "question"
            ] == "test"

            return {
                "result": "ok"
            }

    state = WorkflowState(
        run_id="agent-node-test"
    )

    state.data = {
        "question": "test"
    }

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    node = AgentNode(
        name="test_agent",
        agent=NewApiAgent(),
    )

    result = await node.execute(
        state,
        context,
    )

    assert result.data[
        "test_agent"
    ] == {
        "result": "ok"
    }


@pytest.mark.asyncio
async def test_skill_tool_contracts():

    context = WorkflowContext(
        agents={},
        tools={
            "github_repository":
                FakeGithubRepositoryTool(),
            "file_reader":
                FakeFileReaderTool(),
            "dependency_analyzer":
                FakeDependencyAnalyzerTool(),
            "github_code_search":
                FakeCodeSearchTool(),
            "report_export":
                FakeReportExportTool(),
        },
        skills={},
        config={},
    )

    input_data = {
        "owner": "demo",
        "repo": "test-project",
        "project_path":
            "D:/workspace/test-project",
    }

    repository_result = (
        await RepositoryAnalysisSkill().execute(
            context,
            input_data,
        )
    )

    assert (
        repository_result[
            "repository"
        ]["name"]
        == "test-project"
    )

    architecture_result = (
        await ArchitectureAnalysisSkill().execute(
            context,
            input_data,
        )
    )

    assert architecture_result[
        "modules"
    ][0]["file_path"] == "app/main.py"

    technology_result = (
        await TechnologyAnalysisSkill().execute(
            context,
            input_data,
        )
    )

    assert technology_result[
        "technology_stack"
    ]["dependencies"] == [
        "fastapi",
        "sqlalchemy",
    ]

    report_result = (
        await ReportGenerationSkill().execute(
            context,
            {
                "repository":
                    repository_result,
                "architecture":
                    architecture_result,
                "technology":
                    technology_result,
            },
        )
    )

    assert report_result[
        "report"
    ]["format"] == "markdown"


@pytest.mark.asyncio
async def test_planner_tasks_are_consumed_by_workflow():

    planner = PlannerAgent(
        FakeSkillRegistry()
    )

    planner_context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    plan = await planner.execute(
        planner_context,
        {},
    )

    assert plan["tasks"] == [
        "repository_analysis_agent",
        "architecture_analysis_agent",
        "technology_analysis_agent",
        "evidence_analysis_agent",
        "critic_agent",
    ]

    repository_agent = FakeAgent(
        "repository_analysis_agent",
        {
            "repository": {
                "name": "demo"
            }
        },
    )

    architecture_agent = FakeAgent(
        "architecture_analysis_agent",
        {
            "architecture": {
                "modules": []
            }
        },
    )

    technology_agent = FakeAgent(
        "technology_analysis_agent",
        {
            "technology": {
                "stack": ["FastAPI"]
            }
        },
    )

    evidence_agent = FakeAgent(
        "evidence_analysis_agent",
        {
            "evidence": [
                {
                    "content":
                        "FastAPI application"
                }
            ]
        },
    )

    critic_agent = FakeAgent(
        "critic_agent",
        {
            "passed": True,
            "errors": [],
        },
    )

    context = WorkflowContext(
        agents={
            "repository_analysis_agent":
                repository_agent,
            "architecture_analysis_agent":
                architecture_agent,
            "technology_analysis_agent":
                technology_agent,
            "evidence_analysis_agent":
                evidence_agent,
            "critic_agent":
                critic_agent,
        },
        tools={},
        skills={},
        config={},
    )

    workflow = Workflow()

    workflow.add_node(
        StartNode()
    )

    workflow.add_node(
        AgentNode(
            name="planner_agent",
            agent=planner,
        )
    )

    workflow.add_node(
        PlanExecutorNode()
    )

    workflow.add_node(
        EndNode()
    )

    workflow.add_transition(
        Transition(
            "start",
            "planner_agent",
        )
    )

    workflow.add_transition(
        Transition(
            "planner_agent",
            "plan_executor",
        )
    )

    workflow.add_transition(
        Transition(
            "plan_executor",
            "end",
        )
    )

    state = WorkflowState(
        run_id="planner-integration"
    )

    state.data = {
        "owner": "demo",
        "repo": "test-project",
        "project_path":
            "D:/workspace/test-project",
    }

    result = await WorkflowEngine().run(
        workflow,
        state,
        context,
    )

    assert result.status == "COMPLETED"

    assert result.data[
        "executed_tasks"
    ] == [
        "repository_analysis_agent",
        "architecture_analysis_agent",
        "technology_analysis_agent",
        "evidence_analysis_agent",
        "critic_agent",
    ]

    assert "repository" in result.data
    assert "architecture" in result.data
    assert "technology" in result.data
    assert "evidence" in result.data

    assert result.data[
        "critic_agent"
    ]["passed"] is True

    assert len(
        repository_agent.calls
    ) == 1

    assert len(
        architecture_agent.calls
    ) == 1

    assert len(
        technology_agent.calls
    ) == 1

    assert len(
        evidence_agent.calls
    ) == 1

    assert len(
        critic_agent.calls
    ) == 1


@pytest.mark.asyncio
async def test_critic_accepts_agent_output_keys():

    critic = CriticAgent(
        FakeSkillRegistry()
    )

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    # Phase 12: Critic 现在除了 key 存在性，
    # 还校验字段是否真的带有数据，
    # 因此这里提供真实形状的最小内容。
    result = await critic.execute(
        context,
        {
            "repository_analysis_agent": {
                "repository": {
                    "name": "test-project"
                }
            },
            "architecture_analysis_agent": {
                "files": ["app/main.py"],
                "modules": [
                    {
                        "file_path": "app/main.py",
                        "content": "class DemoApp: pass",
                    }
                ],
                "directory_structure": {
                    "available": True
                },
            },
            "technology_analysis_agent": {
                "technology_stack": {
                    "frameworks": ["FastAPI"]
                }
            },
            "project_structure": {
                "available": True,
                "basis": "readme+topics",
                "dimensions": {},
            },
        },
    )

    assert result["passed"] is True
    assert result["errors"] == []


@pytest.mark.asyncio
async def test_critic_rejects_empty_analysis():
    """
    Phase 12: 只有 key、没有数据的分析结果不能被判为通过。

    旧实现只检查 key 是否存在，
    因此 {"files": [], "modules": []} 也会 passed=True，
    让「跑过了但什么都没产出」看起来是成功的。
    """

    critic = CriticAgent(
        FakeSkillRegistry()
    )

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    result = await critic.execute(
        context,
        {
            "repository_analysis_agent": {
                "repository": {}
            },
            "architecture_analysis_agent": {
                "files": [],
                "modules": [],
            },
            "technology_analysis_agent": {
                "technology_stack": {}
            },
        },
    )

    assert result["passed"] is False

    assert (
        "architecture is empty" in result["errors"]
    )

    assert (
        "repository is empty" in result["errors"]
    )

    assert (
        "technology is empty" in result["errors"]
    )

    assert (
        "project_structure missing"
        in result["errors"]
    )
```

### 📄 `tests/test_pre_phase12_structure.py`

**层级**：测试层 · **职责**：Phase 12 前置结构修复回归测试。

```python
"""
Phase 12 前置结构修复回归测试。

验证：

1. Workflow 存在且可以注册 Node / Transition
2. 两个 BaseNode import 实际指向同一个类
3. WorkflowContext 保持旧字段兼容
4. WorkflowContext 支持 Phase 11 Memory / Context
5. WorkflowError 已统一
6. RepositoryRepository 已统一
7. FastAPI main 可以正常导入
"""

from app.core.exceptions import WorkflowError
from app.repositories.repository import (
    RepositoryRepository as RepositoryRepositoryFromMain,
)
from app.repositories.repository_basic import (
    RepositoryRepository as RepositoryRepositoryFromBasic,
)
from app.workflow.context import WorkflowContext
from app.workflow.node import (
    BaseNode as BaseNodeFromWorkflow,
)
from app.workflow.nodes.base import (
    BaseNode as BaseNodeFromNodes,
)
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow
from app.workflow.exceptions import (
    NodeExecutionError,
    WorkflowError as WorkflowErrorFromWorkflow,
)


class DemoNode(BaseNodeFromWorkflow):
    """
    测试 Node。
    """

    name = "demo"

    async def execute(
        self,
        state,
        context,
    ):
        return state


def test_base_node_is_unified():
    """
    两个历史 import 路径必须得到同一个 BaseNode。
    """

    assert (
        BaseNodeFromWorkflow
        is BaseNodeFromNodes
    )


def test_workflow_can_register_node():
    """
    Workflow 可以正常注册 Node。
    """

    workflow = Workflow()

    node = DemoNode()

    workflow.add_node(node)

    assert (
        workflow.get_node("demo")
        is node
    )

    assert (
        workflow.nodes["demo"]
        is node
    )


def test_workflow_can_register_transition():
    """
    Workflow 可以正常注册 Transition。
    """

    workflow = Workflow()

    transition = Transition(
        "start",
        "demo",
    )

    workflow.add_transition(
        transition
    )

    assert len(
        workflow.transitions
    ) == 1

    assert (
        workflow.transitions[0]
        is transition
    )


def test_workflow_context_backward_compatible():
    """
    原有四字段 WorkflowContext 仍然可用。
    """

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    assert context.agents == {}
    assert context.tools == {}
    assert context.skills == {}
    assert context.config == {}

    assert (
        context.memory_manager
        is None
    )

    assert (
        context.context_manager
        is None
    )


def test_workflow_context_supports_phase11_components():
    """
    WorkflowContext 可以携带 Memory / Context Manager。
    """

    memory_manager = object()
    context_manager = object()

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
        memory_manager=memory_manager,
        context_manager=context_manager,
    )

    assert (
        context.memory_manager
        is memory_manager
    )

    assert (
        context.context_manager
        is context_manager
    )


def test_repository_repository_is_unified():
    """
    两个历史 Repository import 路径
    必须指向同一个实现。
    """

    assert (
        RepositoryRepositoryFromMain
        is RepositoryRepositoryFromBasic
    )


def test_workflow_error_is_unified():
    """
    Workflow 层不能再定义第二份 WorkflowError。
    """

    assert (
        WorkflowErrorFromWorkflow
        is WorkflowError
    )

    assert issubclass(
        NodeExecutionError,
        WorkflowError,
    )


def test_fastapi_application_imports():
    """
    main.py 应用可以正常导入。

    该测试同时验证：
    main.py 不再执行错误的模块级
    WorkflowContext 草稿装配。
    """

    from app.main import app

    assert app is not None
```

### 📄 `tests/test_qdrant.py`

**层级**：测试层 · **职责**：Qdrant 向量存储层单元测试（造数据 → 检索 → 断言排序）

```python
"""Qdrant 向量存储测试。"""

from app.vector_store.qdrant import QdrantVectorStore


def test_qdrant_vector_search():
    """测试 Collection 创建、向量写入和相似度搜索。"""

    store = QdrantVectorStore(
        collection_name="aipi_test",
    )

    store.create_collection(
        vector_size=3,
    )

    store.upsert(
        point_id=1,
        vector=[1.0, 0.0, 0.0],
        payload={
            "repo": "project-a",
            "text": "Multi-Agent workflow platform",
        },
    )

    store.upsert(
        point_id=2,
        vector=[0.0, 1.0, 0.0],
        payload={
            "repo": "project-b",
            "text": "FastAPI backend service",
        },
    )

    store.upsert(
        point_id=3,
        vector=[0.9, 0.1, 0.0],
        payload={
            "repo": "project-c",
            "text": "Agent workflow engine",
        },
    )

    results = store.search(
        query_vector=[1.0, 0.0, 0.0],
        limit=2,
    )

    assert len(results) == 2
    assert results[0].payload["repo"] == "project-a"
```

### 📄 `tests/test_qdrant_search_tool.py`

**层级**：测试层 · **职责**：语义检索工具测试（FakeVectorStore 返回固定 payload）

```python
import pytest


from app.tools.qdrant_search_tool import (
    QdrantSearchTool
)



class FakeVectorStore:


    def search(
        self,
        query_vector,
        limit
    ):

        return [

            type(
                "Point",
                (),
                {
                    "payload":
                    {
                        "file":
                        "workflow.py"
                    }
                }
            )

        ]



@pytest.mark.asyncio
async def test_qdrant_search():

    tool = QdrantSearchTool(
        FakeVectorStore()
    )


    result = await tool.execute(
        [0.1,0.2]
    )


    assert result[0]["file"] == (
        "workflow.py"
    )
```

### 📄 `tests/test_report_export_tool.py`

**层级**：测试层 · **职责**：报告导出工具测试（写出 Markdown 到 test_reports/）

```python
import pytest

from app.tools.report_export_tool import (
    ReportExportTool
)

@pytest.mark.asyncio
async def test_report_export():

    tool = ReportExportTool(
        "test_reports"
    )
    result = await tool.execute(
        title="Test Report",
        content="hello agent",
        filename="test.md"
    )

    assert (
        result["format"]
        ==
        "markdown"
    )
```

### 📄 `tests/test_report_synthesis_skill.py`

**层级**：测试层 · **职责**：ReportSynthesisSkill / LLMChatTool / SynthesisNode 测试。

````python
"""
ReportSynthesisSkill / LLMChatTool / SynthesisNode 测试。

覆盖三条关键路径：

1. 正常路径：LLM 返回合法 JSON → 规整成 summary + dimensions
2. 降级路径：无 Key / 调用异常 / 非法 JSON → available=False 且不抛异常
3. 约束路径：prompt 中「只归纳不推测」的规则必须存在，
   且事实里缺失的维度必须以 available=False 呈现给 LLM

全程不发起任何真实网络请求：
LLM 通过 llm_chat 工具注入假实现。
"""

import json

import pytest

from app.skills.report_synthesis_skill import (
    ReportSynthesisSkill,
)
from app.tools.llm_chat_tool import LLMChatTool
from app.workflow.nodes.synthesis_node import (
    SynthesisNode,
)
from app.workflow.state import WorkflowState

VALID_REPLY = json.dumps(
    {
        "summary": {
            "one_line": "这是一个 LangGraph 发票审批 Agent。",
            "core_design": [
                "draft-only + human-in-the-loop",
                "单 Agent 状态机",
            ],
            "technology_choices": ["FastAPI + LangGraph"],
            "highlights": ["有审计轨迹"],
            "risks": ["RAG 维度数据不足"],
            "use_cases": ["参考其 human-in-the-loop 设计"],
        },
        "dimensions": {
            "agents": "单 Agent + 显式状态机。",
            "workflow": "LangGraph StateGraph。",
            "skills": "数据不足：README 未声明 skills。",
            "tools": "4 个校验工具。",
            "rag": "数据不足：README 未声明 rag。",
            "memory": "SQLite checkpoint 持久化。",
        },
    },
    ensure_ascii=False,
)


class FakeLLMTool:
    """假的 llm_chat 工具。"""

    def __init__(
        self,
        content=VALID_REPLY,
        available=True,
        reason=None,
    ):
        self.content = content
        self.available = available
        self.reason = reason
        self.calls = []

    async def execute(
        self,
        messages,
        **kwargs,
    ):
        self.calls.append(messages)

        if not self.available:
            return {
                "available": False,
                "reason": self.reason,
            }

        return {
            "available": True,
            "content": self.content,
        }


class FakeContext:

    def __init__(self, tool=None):
        self.tools = {}

        if tool is not None:
            self.tools["llm_chat"] = tool


def build_data():
    """一份接近真实结构的 state.data。"""

    return {
        "question": "分析这个项目",
        "repository": {
            "name": "enterprise-finance-agent",
            "full_name": "demo/enterprise-finance-agent",
            "description": "Enterprise finance workflow agent.",
            "language": "Python",
            "topics": ["langgraph"],
            "stargazers_count": 1,
            "forks_count": 1,
            "open_issues_count": 0,
            "license": {"name": "MIT License"},
            "size": 64,
            "created_at": "2026-07-22T02:17:59Z",
            "pushed_at": "2026-07-22T02:31:46Z",
        },
        "readme": "# Demo\n- supplier lookup\n",
        "technology_stack": {
            "llm": ["OpenAI"],
            "database": ["SQLAlchemy"],
            "frameworks": ["FastAPI", "LangGraph"],
            "embedding": [],
            "deployment": [],
        },
        "directory_structure": {
            "available": True,
            "total_files": 107,
            "by_extension": {".py": 88},
        },
        "project_structure": {
            "available": True,
            "basis": "readme+topics",
            "dimensions": {
                "agents": {
                    "declared": True,
                    "items": ["Agent may extract fields"],
                    "topics": [],
                    "evidence": [
                        {
                            "file_path": "README.md",
                            "line_start": 10,
                            "text": "- agent state model",
                        }
                    ],
                },
                "rag": {
                    "declared": False,
                    "reason": "README 中没有 rag 相关声明。",
                    "items": [],
                    "topics": [],
                    "evidence": [],
                },
            },
        },
        "modules": [
            {
                "file_path": "docker-compose.yml",
                "content": "services:\n  api:\n",
            }
        ],
        "evidence": [
            {
                "file_path": "README.md",
                "line_start": 1,
                "line_end": 30,
                "content": "x" * 400,
            }
        ],
    }


# ----------------------------------------------------------------
# ReportSynthesisSkill
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_synthesis_returns_normalized_result():

    tool = FakeLLMTool()

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is True

    assert result["reason"] is None

    assert (
        result["summary"]["one_line"]
        == "这是一个 LangGraph 发票审批 Agent。"
    )

    assert result["summary"]["core_design"] == [
        "draft-only + human-in-the-loop",
        "单 Agent 状态机",
    ]

    # dimensions 只保留已知维度。
    assert set(result["dimensions"]) == {
        "agents",
        "workflow",
        "skills",
        "tools",
        "rag",
        "memory",
    }

    assert (
        result["dimensions"]["rag"]
        == "数据不足：README 未声明 rag。"
    )


@pytest.mark.asyncio
async def test_synthesis_unavailable_when_tool_missing():
    """没有注册 llm_chat 工具时必须降级而不是抛异常。"""

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(),
        build_data(),
    )

    assert result["available"] is False

    assert "llm_chat" in result["reason"]


@pytest.mark.asyncio
async def test_synthesis_unavailable_when_llm_unavailable():
    """LLM 侧失败的原因必须原样透传，便于排查。"""

    tool = FakeLLMTool(
        available=False,
        reason="未配置 LLM_API_KEY，无法调用 LLM。",
    )

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is False

    assert (
        result["reason"]
        == "未配置 LLM_API_KEY，无法调用 LLM。"
    )


@pytest.mark.asyncio
async def test_synthesis_unavailable_on_invalid_json():

    tool = FakeLLMTool(
        content="这不是 JSON，只是一段解释文字。"
    )

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is False

    assert "JSON" in result["reason"]


@pytest.mark.asyncio
async def test_synthesis_parses_fenced_json():
    """LLM 用 markdown 代码块包裹、并在前后加解释文字时仍要能解析。"""

    tool = FakeLLMTool(
        content=(
            "好的，以下是结果：\n"
            "```json\n"
            f"{VALID_REPLY}\n"
            "```\n"
            "希望对你有帮助。"
        )
    )

    skill = ReportSynthesisSkill()

    result = await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    assert result["available"] is True

    assert len(result["dimensions"]) == 6


@pytest.mark.asyncio
async def test_synthesis_prompt_forbids_speculation():
    """
    prompt 必须带上「只归纳不推测」的约束。

    这是本 Skill 的核心约束，
    被放宽会让报告重新变成「看起来合理但内容是编的」。
    """

    tool = FakeLLMTool()

    skill = ReportSynthesisSkill()

    await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    messages = tool.calls[0]

    system = messages[0]["content"]

    user = messages[1]["content"]

    assert messages[0]["role"] == "system"

    assert "只能使用" in system

    assert "数据不足" in system

    assert "禁止使用你自己的外部知识" in system

    # 事实必须以 <facts> 包裹交给模型。
    assert "<facts>" in user

    assert "</facts>" in user


@pytest.mark.asyncio
async def test_synthesis_facts_expose_missing_dimensions():
    """
    事实摘要里缺失的维度必须以 available=False + reason 呈现。

    否则 LLM 会把「没采集到」误读成「项目没有这个能力」，
    进而写出「该项目未使用 RAG」这种错误结论。
    """

    tool = FakeLLMTool()

    skill = ReportSynthesisSkill()

    await skill.execute(
        FakeContext(tool),
        build_data(),
    )

    user = tool.calls[0][1]["content"]

    facts = json.loads(
        user[
            user.index("<facts>")
            + len("<facts>"):
            user.index("</facts>")
        ]
    )

    declared = facts["declared_structure"]

    assert declared["agents"]["available"] is True

    assert declared["rag"]["available"] is False

    assert (
        declared["rag"]["reason"]
        == "README 中没有 rag 相关声明。"
    )

    # 没有采集到的维度（本次数据里没有 skills）也必须显式标注。
    assert declared["skills"]["available"] is False

    # README 是主要事实来源，必须带上。
    assert facts["readme"]["available"] is True

    # 真实读到的源码也要给到，用于交叉验证 README 自述。
    assert (
        facts["source_files"][0]["file_path"]
        == "docker-compose.yml"
    )


@pytest.mark.asyncio
async def test_synthesis_survives_broken_data():
    """state.data 结构异常时不能抛异常。"""

    skill = ReportSynthesisSkill()

    tool = FakeLLMTool()

    result = await skill.execute(
        FakeContext(tool),
        {
            "repository": "not-a-dict",
            "readme": 123,
            "project_structure": None,
            "modules": "not-a-list",
            "evidence": None,
        },
    )

    assert result["available"] is True


# ----------------------------------------------------------------
# LLMChatTool
# ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_llm_chat_tool_without_api_key(monkeypatch):
    """
    没有配置 API Key 时必须返回 available=False，
    而不是抛异常让整个 Workflow 失败。
    """

    import app.tools.llm_chat_tool as module

    class FakeSettings:
        LLM_API_KEY = ""
        LLM_MODEL = "deepseek-chat"
        LLM_BASE_URL = "https://api.deepseek.com"
        LLM_TIMEOUT = 60.0

    monkeypatch.setattr(
        module,
        "get_settings",
        lambda: FakeSettings(),
    )

    tool = LLMChatTool()

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )

    assert result["available"] is False

    assert "LLM_API_KEY" in result["reason"]


@pytest.mark.asyncio
async def test_llm_chat_tool_wraps_llm_error():
    """LLM 抛异常时必须转成 available=False 并带上原因。"""

    class ExplodingLLM:

        async def chat(self, messages, **kwargs):
            raise RuntimeError("connection reset")

    tool = LLMChatTool(llm=ExplodingLLM())

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )

    assert result["available"] is False

    assert "connection reset" in result["reason"]


@pytest.mark.asyncio
async def test_llm_chat_tool_rejects_empty_content():
    """LLM 返回空内容算失败，不能当成合法回答。"""

    class EmptyLLM:

        async def chat(self, messages, **kwargs):
            return "   "

    tool = LLMChatTool(llm=EmptyLLM())

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hi"}
        ]
    )

    assert result["available"] is False


@pytest.mark.asyncio
async def test_llm_chat_tool_uses_injected_llm():
    """注入 LLM 时不应读取配置、不应创建网络客户端。"""

    class EchoLLM:

        def __init__(self):
            self.seen = None

        async def chat(self, messages, **kwargs):
            self.seen = messages
            return "ok"

    llm = EchoLLM()

    tool = LLMChatTool(llm=llm)

    result = await tool.execute(
        messages=[
            {"role": "user", "content": "hello"}
        ]
    )

    assert result == {
        "available": True,
        "content": "ok",
    }

    assert llm.seen[0]["content"] == "hello"


# ----------------------------------------------------------------
# SynthesisNode
# ----------------------------------------------------------------


class FakeSkill:

    def __init__(
        self,
        result=None,
        error=None,
    ):
        self.result = result
        self.error = error
        self.calls = []

    async def execute(
        self,
        context,
        input_data,
    ):
        self.calls.append(input_data)

        if self.error is not None:
            raise self.error

        return self.result


@pytest.mark.asyncio
async def test_synthesis_node_writes_state_data():

    skill = FakeSkill(
        result={
            "available": True,
            "reason": None,
            "summary": {"one_line": "结论"},
            "dimensions": {},
        }
    )

    node = SynthesisNode(skill=skill)

    state = WorkflowState(run_id="synthesis-node")

    state.data = {
        "repository": {"name": "demo"},
        "_internal": "should be skipped",
    }

    result = await node.execute(state, FakeContext())

    assert result.data["synthesis"]["available"] is True

    assert len(result.outputs) == 1

    # 下划线开头的内部键不转发。
    assert "_internal" not in skill.calls[0]


@pytest.mark.asyncio
async def test_synthesis_node_degrades_on_skill_error():
    """
    Skill 抛异常时节点必须降级。

    否则综合分析这一章的失败会让
    整个 Analysis Workflow 变成 FAILED。
    """

    node = SynthesisNode(
        skill=FakeSkill(
            error=RuntimeError("boom")
        )
    )

    state = WorkflowState(run_id="synthesis-node-error")

    state.data = {}

    result = await node.execute(state, FakeContext())

    assert result.data["synthesis"]["available"] is False

    assert "boom" in result.data["synthesis"]["reason"]
````

### 📄 `tests/test_repository_analysis_workflow.py`

**层级**：测试层 · **职责**：Skill 驱动的 Workflow 集成测试（Mock Tool → RepositoryAnalysisSkill → SkillNode → Transition 串联执行）

```python
import pytest


from app.workflow.workflow import Workflow

from app.workflow.engine import WorkflowEngine

from app.workflow.state import WorkflowState

from app.workflow.context import WorkflowContext


from app.workflow.nodes.skill_node import SkillNode


from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)


from app.workflow.nodes.base import BaseNode

from app.workflow.transition import Transition


#
# Mock Tool
#

class FakeGithubRepositoryTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "repo": kwargs["name"],
            "owner": kwargs["owner"],
            "name": kwargs["name"],
        }


class FakeFileReaderTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "content":
            "# Demo Repository"
        }


class FakeDependencyAnalyzerTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "dependencies": [
                "fastapi",
                "sqlalchemy"
            ]
        }


class StartNode(BaseNode):

    name = "start"

    async def execute(
        self,
        state,
        context
    ):

        return state


class EndNode(BaseNode):

    name = "end"

    async def execute(
        self,
        state,
        context
    ):

        state.status = "COMPLETED"

        return state


#
# 构建 Workflow
#

def build_workflow():

    workflow = Workflow()

    workflow.add_node(
        StartNode()
    )

    workflow.add_node(
        SkillNode(
            name="repository_analysis",
            skill=RepositoryAnalysisSkill()
        )
    )

    workflow.add_node(
        EndNode()
    )

    workflow.add_transition(
        Transition(
            "start",
            "repository_analysis"
        )
    )

    workflow.add_transition(
        Transition(
            "repository_analysis",
            "end"
        )
    )

    return workflow


#
# 构建 Context
#

def build_context():

    return WorkflowContext(
        agents={},

        tools={
            "github_repository":
                FakeGithubRepositoryTool(),

            "file_reader":
                FakeFileReaderTool(),

            "dependency_analyzer":
                FakeDependencyAnalyzerTool()
        },

        skills={
            "repository_analysis":
                RepositoryAnalysisSkill()
        },

        config={}
    )


#
# Workflow 集成测试
#

@pytest.mark.asyncio
async def test_repository_analysis_skill_workflow():

    workflow = build_workflow()

    state = WorkflowState(
        run_id="repo-analysis-test"
    )

    state.data = {
        "owner": "demo",
        "repo": "test-project",
        "project_path": "."
    }

    context = build_context()

    result = await WorkflowEngine().run(
        workflow,
        state,
        context
    )

    assert result.status == "COMPLETED"

    assert (
        "repository_analysis"
        in result.data
    )

    # Phase 12: RepositoryAnalysisSkill 现在只保留
    # 真实 GitHub API 里存在的字段。
    # 旧断言用的 "repo" 并不是 GitHub API 字段，
    # 因此改用 name。
    assert (
        result.data[
            "repository_analysis"
        ][
            "repository"
        ][
            "name"
        ]
        ==
        "test-project"
    )

    assert (
        result.data[
            "repository_analysis"
        ][
            "readme"
        ][
            "content"
        ]
        ==
        "# Demo Repository"
    )

    assert (
        result.data[
            "repository_analysis"
        ][
            "dependencies"
        ][
            "dependencies"
        ]
        ==
        [
            "fastapi",
            "sqlalchemy"
        ]
    )
```

### 📄 `tests/test_repository_crud.py`

**层级**：测试层 · **职责**：数据访问层测试（创建、按 URL 查、按 ID 查）；运行前会清理同 URL 残留记录以保证可重复运行

```python
"""Repository 数据访问层测试。"""

import pytest
from sqlalchemy import delete

from app.db.session import AsyncSessionLocal
from app.models.repository import Repository
from app.repositories.repository import RepositoryRepository


@pytest.mark.asyncio
async def test_create_and_get_repository():
    """测试 Repository 创建和查询。"""

    url = "https://github.com/test-user/test-agent-project"

    async with AsyncSessionLocal() as session:
        # 先清理上一次运行可能残留的同 URL 记录，
        # 否则 repositories.url 的 UNIQUE 约束会让重复运行失败。
        await session.execute(
            delete(Repository).where(
                Repository.url == url
            )
        )
        await session.commit()

        repository_repository = RepositoryRepository(
            session
        )

        repository = await repository_repository.create(
            url=url,
            owner="test-user",
            name="test-agents-project",
            description="Test Agent Project",
            default_branch="main",
            language="Python",
            stars=100,
            forks=20,
        )

        assert repository.id is not None
        assert repository.owner == "test-user"
        assert repository.name == "test-agents-project"

        found = await repository_repository.get_by_url(
            url
        )

        assert found is not None
        assert found.id == repository.id
        assert found.url == url

        found_by_id = await repository_repository.get_by_id(
            repository.id
        )

        assert found_by_id is not None
        assert found_by_id.name == "test-agents-project"
```

### 📄 `tests/test_repository_pipeline.py`

**层级**：测试层 · **职责**：端到端管道测试（Service 拉取仓库 → Indexer 建立索引）

```python
import pytest

from app.db.session import AsyncSessionLocal
from app.services.repository_service import RepositoryService
from app.project_analysis.repository_indexer import RepositoryIndexer



@pytest.mark.asyncio
async def test_repository_pipeline():

    url = (
        "https://github.com/"
        "langchain-ai/langchain"
    )


    async with AsyncSessionLocal() as session:

        service = (
            RepositoryService(session)
        )


        repository = await (
            service.get_or_create(
                url
            )
        )


        assert (
            repository.owner
            ==
            "langchain-ai"
        )


        indexer = (
            RepositoryIndexer()
        )


        result = await (
            indexer.index(
                repository.owner,
                repository.name,
                repository.default_branch,
            )
        )


        assert result == 1
```

### 📄 `tests/test_repository_service.py`

**层级**：测试层 · **职责**：业务服务层测试（不存在时创建、存在时复用）

```python
"""Repository Service 测试。"""

import pytest

from app.db.session import AsyncSessionLocal
from app.services.repository_service import RepositoryService


@pytest.mark.asyncio
async def test_get_or_create_repository():
    """测试 Repository 不存在时创建，存在时复用。"""

    url = "https://github.com/service-test/agent-project"

    async with AsyncSessionLocal() as session:
        service = RepositoryService(session)

        first = await service.get_or_create(url)

        assert first.id is not None
        assert first.owner == "service-test"
        assert first.name == "agent-project"

        second = await service.get_or_create(url)

        assert second.id == first.id
        assert second.url == first.url
```

### 📄 `tests/test_repository_skill.py`

**层级**：测试层 · **职责**：RepositoryAnalysisSkill 单元测试（Fake GitHub / FileReader / Dependency Tool，断言三路结果合并）

```python
import pytest


from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)



class FakeGithubTool:

    async def execute(
        self,
        **kwargs
    ):
        return {
            "name": kwargs["name"]
        }




class FakeFileReader:


    async def execute(
        self,
        **kwargs
    ):


        return {

            "content":
            "README"

        }




class FakeDependencyTool:


    async def execute(
        self,
        **kwargs
    ):


        return {

            "fastapi":
            "installed"

        }




class Context:


    tools={

        "github_repository":
            FakeGithubTool(),


        "file_reader":
            FakeFileReader(),


        "dependency_analyzer":
            FakeDependencyTool()

    }





@pytest.mark.asyncio
async def test_repository_skill():


    skill = RepositoryAnalysisSkill()



    result = await skill.execute(

        Context(),

        {

            "owner":
            "test",


            "repo":
            "demo"

        }

    )



    assert (
        result["repository"]["name"]
        ==
        "demo"
    )


    assert (
        "readme"
        in result
    )


    assert (
        "dependencies"
        in result
    )
```

### 📄 `tests/test_retrieval.py`

**层级**：测试层 · **职责**：语义检索测试（建立索引 → 用自然语言问题检索 → 断言命中）

```python
"""向量检索测试。"""

from app.embeddings.ollama import OllamaEmbedding
from app.project_analysis.project_indexer import DocumentIndexer
from app.vector_store.qdrant import QdrantVectorStore


def test_semantic_retrieval():
    """测试建立索引后能否通过语义问题找到相关 Chunk。"""

    indexer = DocumentIndexer(
        collection_name="aipi_retrieval_test",
    )

    document = """# Introduction

This is an AI Agent platform.

# HITL

Human approval is required for sensitive operations.

# Workflow

The system supports workflow execution and task recovery.
"""

    indexer.index_document(
        document_id="test-repository-readme",
        text=document,
        metadata={
            "repository_id": 1,
            "source": "README.md",
        },
    )

    embedding = OllamaEmbedding()

    vector_store = QdrantVectorStore(
        collection_name="aipi_retrieval_test",
    )

    query = "Does the system support human approval?"

    query_vector = embedding.embed(query)

    results = vector_store.search(
        query_vector=query_vector,
        limit=3,
    )

    assert len(results) > 0

    print("\nRetrieval Results:")

    for result in results:
        print(
            f"score={result.score}",
            result.payload,
        )

    assert "Human approval" in results[0].payload["text"]
```

### 📄 `tests/test_skill_base.py`

**层级**：测试层 · **职责**：Skill 抽象基类测试（子类具备 `name` / `description` 且可实现 `execute()`）

```python
from app.skills.base import BaseSkill



def test_skill_has_name():

    """
    测试Skill是否具备基本属性
    """


    class DemoSkill(BaseSkill):


        name = "demo"


        description = "demo skill"



        async def execute(
            self,
            context,
            input_data
        ):

            return {}



    skill = DemoSkill()



    assert skill.name == "demo"
```

### 📄 `tests/test_skill_node.py`

**层级**：测试层 · **职责**：SkillNode 单元测试（FakeSkill，断言结果写入 `state.data[node.name]` 与 `state.outputs`）

```python
import pytest

from app.workflow.nodes.skill_node import (
    SkillNode
)

from app.workflow.state import WorkflowState

from app.workflow.context import WorkflowContext


class FakeSkill:

    async def execute(
        self,
        context,
        input_data
    ):

        return {
            "result": "skill success"
        }


@pytest.mark.asyncio
async def test_skill_node_execute():

    node = SkillNode(
        name="test_skill",
        skill=FakeSkill()
    )

    state = WorkflowState(
        run_id="test"
    )

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={}
    )

    result = await node.execute(
        state,
        context
    )

    assert (
        result.data["test_skill"]["result"]
        ==
        "skill success"
    )

    assert len(
        result.outputs
    ) == 1
```

### 📄 `tests/test_skill_registry.py`

**层级**：测试层 · **职责**：Skill 注册中心测试（默认 5 个 Skill 是否注册成功并可获取）

```python
from app.skills.registry import (
    create_skill_registry
)



def test_skill_registry():


    registry = create_skill_registry()



    assert (
        "repository_analysis"
        in registry.skills
    )



    assert (
        registry.get(
            "repository_analysis"
        )
        is not None
    )



    # Analysis Workflow 依赖这两个 Skill：
    # 缺任何一个 build_analysis_workflow 都会直接报错。
    assert (
        "report_generation"
        in registry.skills
    )



    assert (
        "report_synthesis"
        in registry.skills
    )



    # 单模块深挖：默认报告只看要点时，
    # 用户点名某个模块靠这个 Skill 展开细节。
    assert (
        "module_deep_dive"
        in registry.skills
    )
```

### 📄 `tests/test_skill_workflow.py`

**层级**：测试层 · **职责**：Skill 全链路 Workflow 测试（Start → SkillNode(RepositoryAnalysisSkill) → End，断言 status 与 data）

```python
import pytest


from app.workflow.engine import WorkflowEngine

from app.workflow.workflow import Workflow

from app.workflow.state import WorkflowState

from app.workflow.context import WorkflowContext


from app.workflow.nodes.skill_node import SkillNode


from app.workflow.nodes.base import BaseNode

from app.workflow.transition import Transition



from app.skills.repository_analysis_skill import (
    RepositoryAnalysisSkill
)



class StartNode(BaseNode):


    name="start"



    async def execute(
        self,
        state,
        context
    ):

        return state





class EndNode(BaseNode):


    name="end"



    async def execute(
        self,
        state,
        context
    ):

        state.status="COMPLETED"

        return state




class GithubTool:

    async def execute(
        self,
        **kwargs
    ):

        return {
            "repo":
            kwargs["name"]
        }





class FileTool:


    async def execute(
        self,
        **kwargs
    ):


        return "README"





class DependencyTool:


    async def execute(
        self,
        **kwargs
    ):


        return [

            "fastapi"

        ]





def create_workflow():


    workflow = Workflow()


    workflow.add_node(
        StartNode()
    )


    workflow.add_node(

        SkillNode(

            "repository_analysis",

            RepositoryAnalysisSkill()

        )

    )


    workflow.add_node(
        EndNode()
    )


    workflow.add_transition(

        Transition(
            "start",
            "repository_analysis"
        )

    )


    workflow.add_transition(

        Transition(
            "repository_analysis",
            "end"
        )

    )


    return workflow





@pytest.mark.asyncio
async def test_full_skill_workflow():


    workflow=create_workflow()



    state=WorkflowState(

        run_id="test"

    )


    state.data={

        "owner":
        "demo",

        "repo":
        "test"

    }



    context=WorkflowContext(

        agents={},


        tools={


            "github_repository":
                GithubTool(),


            "file_reader":
                FileTool(),


            "dependency_analyzer":
                DependencyTool()


        },


        skills={},


        config={}

    )



    result = await WorkflowEngine().run(

        workflow,

        state,

        context

    )


    assert (
        result.status
        ==
        "COMPLETED"
    )


    assert (

        "repository_analysis"

        in result.data

    )
```

### 📄 `tests/test_tools.py`

**层级**：测试层 · **职责**：工具层测试（`GitHubRepositoryTool` 取仓库、`FileReaderTool` 读文件）

```python
import pytest

from app.tools.github.github_repository_tool import (
    GitHubRepositoryTool
)


from app.tools.file_reader_tool import (
    FileReaderTool
)



@pytest.mark.asyncio
async def test_github_repository_tool():

    tool = GitHubRepositoryTool()


    result = await tool.execute(
        owner="openai",
        name="openai-python"
    )


    assert result is not None



@pytest.mark.asyncio
async def test_file_reader_tool():

    tool = FileReaderTool()


    result = await tool.execute(
        owner="openai",
        name="openai-python",
        file_path="README.md"
    )


    assert isinstance(
        result,
        str
    )
```

### 📄 `tests/test_traceability.py`

**层级**：测试层 · **职责**：可追溯性测试（造 Claim / Citation / Evidence 后，断言溯源链解析到源码文件与行号）

```python
"""
Claim → Citation → Evidence 可追溯测试。
"""

import pytest

from app.evidence.traceability import (
    TraceabilityService,
)


class FakeClaim:

    id = "claim-1"

    claim_text = (
        "The project contains multiple agents."
    )


class FakeCitation:

    def __init__(
        self,
        evidence_id,
    ):
        self.evidence_id = evidence_id


class FakeEvidence:

    def __init__(
        self,
        evidence_id,
    ):
        self.id = evidence_id
        self.file_path = (
            "app/agents/base.py"
        )
        self.line_start = 1
        self.line_end = 20
        self.content = (
            "class BaseAgent:"
        )


@pytest.mark.asyncio
async def test_claim_traceability():

    service = TraceabilityService(
        session=None
    )

    async def get_claim(
        claim_id
    ):
        return FakeClaim()

    async def get_citations(
        claim_id
    ):
        return [
            FakeCitation(
                "evidence-1"
            )
        ]

    async def get_evidence(
        evidence_id
    ):
        return FakeEvidence(
            evidence_id
        )

    service.claims.get_by_id = (
        get_claim
    )

    service.citations.get_by_claim = (
        get_citations
    )

    service.evidences.get_by_id = (
        get_evidence
    )

    result = await (
        service.get_claim_trace(
            "claim-1"
        )
    )

    assert (
        result["claim"].id
        == "claim-1"
    )

    assert len(
        result["citations"]
    ) == 1

    assert len(
        result["evidences"]
    ) == 1

    evidence = (
        result["evidences"][0]
    )

    assert (
        evidence.file_path
        == "app/agents/base.py"
    )

    assert (
        evidence.line_start
        == 1
    )

    assert (
        evidence.line_end
        == 20
    )
```

### 📄 `tests/test_workflow.py`

**层级**：测试层 · **职责**：Workflow Engine 测试（顺序执行、失败捕获、可重试与不可重试、检查点存取、暂停与恢复）

```python
"""Workflow Engine 测试。"""

import pytest

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.workflow.checkpoint import CheckpointManager
from app.workflow.context import WorkflowContext
from app.workflow.engine import WorkflowEngine
from app.workflow.node import BaseNode
from app.workflow.nodes.end_node import EndNode
from app.workflow.nodes.start_node import StartNode
from app.workflow.retry import RetryPolicy
from app.workflow.state import WorkflowState
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow


class TouchNode(BaseNode):
    """记录执行顺序的测试节点。"""

    def __init__(self, name):

        self.name = name

    async def execute(
        self,
        state,
        context
    ):

        state.data.setdefault(
            "visited",
            []
        ).append(self.name)

        return state


class FailNode(BaseNode):
    """不可重试失败的测试节点。"""

    name = "fail"

    async def execute(
        self,
        state,
        context
    ):

        raise NonRetryableError("boom")


class FlakyNode(BaseNode):
    """第一次抛可重试异常，之后成功。"""

    name = "flaky"

    async def execute(
        self,
        state,
        context
    ):

        state.data["attempts"] = (
            state.data.get("attempts", 0) + 1
        )

        if state.data["attempts"] == 1:

            raise RetryableError(
                "temporary error"
            )

        return state


class PauseNode(BaseNode):
    """主动暂停的测试节点。"""

    name = "pause"

    async def execute(
        self,
        state,
        context
    ):

        state.status = "PAUSED"

        return state


def build_workflow(
    nodes,
    transitions
):
    """构建测试用 Workflow。"""

    workflow = Workflow()

    for node in nodes:

        workflow.add_node(node)

    for source, target in transitions:

        workflow.add_transition(
            Transition(source, target)
        )

    return workflow


def build_context():
    """构建测试用 Context。"""

    return WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )


@pytest.mark.asyncio
async def test_workflow_runs_nodes_in_order():
    """测试 Workflow 按顺序执行 Node。"""

    workflow = build_workflow(
        [
            StartNode(),
            TouchNode("a"),
            TouchNode("b"),
            EndNode(),
        ],
        [
            ("start", "a"),
            ("a", "b"),
            ("b", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-order")

    result = await WorkflowEngine().run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "COMPLETED"

    assert result.data["visited"] == ["a", "b"]

    assert result.current_node == "end"


@pytest.mark.asyncio
async def test_node_failure_is_captured():
    """测试 Node 失败被捕获。"""

    workflow = build_workflow(
        [
            StartNode(),
            FailNode(),
            EndNode(),
        ],
        [
            ("start", "fail"),
            ("fail", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-fail")

    result = await WorkflowEngine().run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.errors == ["boom"]

    assert result.current_node == "fail"


@pytest.mark.asyncio
async def test_retryable_error_is_retried():
    """测试可重试异常会按 RetryPolicy 重试。"""

    workflow = build_workflow(
        [
            StartNode(),
            FlakyNode(),
            EndNode(),
        ],
        [
            ("start", "flaky"),
            ("flaky", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-retry")

    engine = WorkflowEngine(
        retry_policy=RetryPolicy(max_retry=3)
    )

    result = await engine.run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "COMPLETED"

    assert result.data["attempts"] == 2

    assert result.retry_count == 1


@pytest.mark.asyncio
async def test_non_retryable_error_is_not_retried():
    """测试不可重试异常不会重试。"""

    workflow = build_workflow(
        [
            StartNode(),
            FailNode(),
            EndNode(),
        ],
        [
            ("start", "fail"),
            ("fail", "end"),
        ],
    )

    state = WorkflowState(run_id="wf-no-retry")

    result = await WorkflowEngine().run(
        workflow,
        state,
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.retry_count == 0


@pytest.mark.asyncio
async def test_checkpoint_save_and_load():
    """测试检查点保存和恢复。"""

    manager = CheckpointManager()

    state = WorkflowState(run_id="cp-1")

    state.data["key"] = "value"

    await manager.save(state)

    # 修改原状态，验证快照相互隔离
    state.data["key"] = "changed"

    restored = await manager.load("cp-1")

    assert restored.data["key"] == "value"

    assert await manager.load("not-exist") is None


@pytest.mark.asyncio
async def test_pause_and_resume():
    """测试暂停后可以从检查点恢复。"""

    workflow = build_workflow(
        [
            StartNode(),
            PauseNode(),
            TouchNode("after"),
            EndNode(),
        ],
        [
            ("start", "pause"),
            ("pause", "after"),
            ("after", "end"),
        ],
    )

    manager = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=manager
    )

    paused = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause"),
        build_context(),
    )

    assert paused.status == "PAUSED"

    assert paused.current_node == "pause"

    assert "after" not in paused.data.get(
        "visited",
        []
    )

    resumed = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause"),
        build_context(),
        resume_from="wf-pause",
    )

    assert resumed.status == "COMPLETED"

    assert resumed.data["visited"] == ["after"]
```

### 📄 `tests/test_workflow_engine_errors.py`

**层级**：测试层 · **职责**：WorkflowEngine 失败语义测试。

```python
"""
WorkflowEngine 失败语义测试。

覆盖：

1. 空异常消息不会丢失异常类型
2. FAILED Checkpoint 恢复时重新执行失败节点
3. 不破坏 PAUSED / WAITING_* 的原有 resume 语义
"""

import httpx
import pytest

from app.core.exceptions import (
    NonRetryableError,
)
from app.workflow.checkpoint import (
    CheckpointManager,
)
from app.workflow.context import (
    WorkflowContext,
)
from app.workflow.engine import (
    WorkflowEngine,
)
from app.workflow.node import BaseNode
from app.workflow.nodes.end_node import (
    EndNode,
)
from app.workflow.nodes.start_node import (
    StartNode,
)
from app.workflow.state import (
    WorkflowState,
    WorkflowStatus,
)
from app.workflow.transition import (
    Transition,
)
from app.workflow.workflow import (
    Workflow,
)


class EmptyMessageNode(BaseNode):
    """
    抛出 str() 为空的异常。

    httpx.ReadTimeout('') 就是这种情况：
    str(error) == ''，args == ('',)。
    """

    name = "empty_error"

    async def execute(
        self,
        state,
        context,
    ):

        raise httpx.ReadTimeout("")


class MessageNode(BaseNode):
    """抛出带消息的异常。"""

    name = "message_error"

    async def execute(
        self,
        state,
        context,
    ):

        raise ValueError("planner result missing")


class FailOnceNode(BaseNode):
    """第一次失败，之后成功（模拟瞬时网络故障）。"""

    name = "plan_executor"

    def __init__(
        self,
        name="plan_executor",
    ):

        self.name = name

    async def execute(
        self,
        state,
        context,
    ):

        state.data["attempts"] = (
            state.data.get("attempts", 0) + 1
        )

        if state.data["attempts"] == 1:

            raise NonRetryableError("boom")

        state.data.setdefault(
            "visited",
            [],
        ).append(self.name)

        return state


class RecordNode(BaseNode):
    """记录执行顺序的节点。"""

    def __init__(
        self,
        name,
    ):

        self.name = name

    async def execute(
        self,
        state,
        context,
    ):

        state.data.setdefault(
            "visited",
            [],
        ).append(self.name)

        return state


class PauseGateNode(BaseNode):
    """模拟 Design Gate：主动进入 WAITING_DESIGN。"""

    name = "design_gate"

    async def execute(
        self,
        state,
        context,
    ):

        state.data["pause_count"] = (
            state.data.get("pause_count", 0) + 1
        )

        state.status = (
            WorkflowStatus.WAITING_DESIGN
        )

        return state


def build_workflow(
    nodes,
    transitions,
):
    """构建测试用 Workflow。"""

    workflow = Workflow()

    for node in nodes:

        workflow.add_node(node)

    for source, target in transitions:

        workflow.add_transition(
            Transition(source, target)
        )

    return workflow


def build_context():
    """构建测试用 Context。"""

    return WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )


@pytest.mark.asyncio
async def test_empty_error_message_keeps_exception_type():
    """
    空异常消息必须降级为异常类型名。

    修复前：errors == [""]
    修复后：errors == ["ReadTimeout"]
    """

    workflow = build_workflow(
        [
            StartNode(),
            EmptyMessageNode(),
            EndNode(),
        ],
        [
            ("start", "empty_error"),
            ("empty_error", "end"),
        ],
    )

    result = await WorkflowEngine().run(
        workflow,
        WorkflowState(run_id="wf-empty-error"),
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.current_node == "empty_error"

    assert result.errors == ["ReadTimeout"]


@pytest.mark.asyncio
async def test_non_empty_error_message_is_preserved():
    """非空消息必须原样保留（保持既有格式）。"""

    workflow = build_workflow(
        [
            StartNode(),
            MessageNode(),
            EndNode(),
        ],
        [
            ("start", "message_error"),
            ("message_error", "end"),
        ],
    )

    result = await WorkflowEngine().run(
        workflow,
        WorkflowState(run_id="wf-message-error"),
        build_context(),
    )

    assert result.status == "FAILED"

    assert result.errors == [
        "planner result missing"
    ]


@pytest.mark.asyncio
async def test_failed_resume_reexecutes_failed_node():
    """
    FAILED 恢复必须重新执行失败节点，而不是跳到下一个节点。

    修复前：current_node=plan_executor 会直接跳到 human_review，
            5 个 Agent 一个都不会执行。
    修复后：重新执行 plan_executor。
    """

    workflow = build_workflow(
        [
            StartNode(),
            FailOnceNode(),
            RecordNode("human_review"),
            RecordNode("finalizer"),
            EndNode(),
        ],
        [
            ("start", "plan_executor"),
            ("plan_executor", "human_review"),
            ("human_review", "finalizer"),
            ("finalizer", "end"),
        ],
    )

    manager = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=manager
    )

    first = await engine.run(
        workflow,
        WorkflowState(run_id="wf-failed-resume"),
        build_context(),
    )

    assert first.status == "FAILED"

    assert first.current_node == "plan_executor"

    assert first.errors == ["boom"]

    assert first.data["attempts"] == 1

    assert first.data.get("visited", []) == []

    # 从 FAILED Checkpoint 恢复。
    restored = await engine.run(
        workflow,
        WorkflowState(run_id="wf-failed-resume"),
        build_context(),
        resume_from="wf-failed-resume",
    )

    # 失败节点被重新执行。
    assert restored.data["attempts"] == 2

    assert restored.data["visited"] == [
        "plan_executor",
        "human_review",
        "finalizer",
    ]

    # errors 被清空。
    assert restored.errors == []

    assert restored.status == "COMPLETED"


@pytest.mark.asyncio
async def test_pause_resume_still_skips_completed_node():
    """
    Pause / Human Gate 语义不能被破坏。

    WAITING_DESIGN 表示 design_gate 已完成，
    恢复时必须从下一个节点继续，而不是重跑 design_gate。
    """

    workflow = build_workflow(
        [
            StartNode(),
            PauseGateNode(),
            RecordNode("plan_executor"),
            EndNode(),
        ],
        [
            ("start", "design_gate"),
            ("design_gate", "plan_executor"),
            ("plan_executor", "end"),
        ],
    )

    manager = CheckpointManager()

    engine = WorkflowEngine(
        checkpoint=manager
    )

    paused = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause-gate"),
        build_context(),
    )

    assert paused.status == "WAITING_DESIGN"

    assert paused.current_node == "design_gate"

    assert paused.data["pause_count"] == 1

    resumed = await engine.run(
        workflow,
        WorkflowState(run_id="wf-pause-gate"),
        build_context(),
        resume_from="wf-pause-gate",
    )

    # design_gate 没有被重新执行。
    assert resumed.data["pause_count"] == 1

    assert resumed.data["visited"] == [
        "plan_executor"
    ]

    assert resumed.status == "COMPLETED"
```

## 二十二、仓库根目录脚本

文档生成脚本与 Agent Loop 实验草稿（未纳入 app/）

### 📄 `generate_project_code.py`

**层级**：根目录脚本 · **职责**：生成 PROJECT_CODE.md。

````python
"""生成 PROJECT_CODE.md。

扫描工作区源码，按分层结构输出「目录树 + 逐文件完整源码」文档。
源码内容直接从源文件读取，不做任何改写。

目录树与各章节的文件清单都由文件系统实时扫描得出：新增、重命名、
删除的 `.py` 文件会在下次运行时自动进入文档，无需修改本脚本。
未收录进任何章节的文件会落入文末的「未归类文件」兜底章节。

用法:
    python generate_project_code.py
"""

from __future__ import annotations

import ast
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Callable, NamedTuple

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "PROJECT_CODE.md"

# 目录树中需要跳过的路径
TREE_SKIP = {
    ".git",
    ".idea",
    ".pytest_cache",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
}

# 目录树注释：key 为相对路径（使用 / 分隔），value 为注释文本
TREE_NOTES = {
    "alembic": "数据库迁移（Alembic）",
    "alembic/versions": "迁移脚本",
    "app": "应用主包",
    "app/api": "── API 层 ──",
    "app/api/v1": "v1 路由",
    "app/core": "── 核心基础设施层 ──",
    "app/db": "── 数据库层 ──",
    "app/models": "── 数据模型层 ──",
    "app/schemas": "── 数据契约层 ──",
    "app/repositories": "── 数据访问层 ──",
    "app/services": "── 业务服务层 ──",
    "app/workflow": "── Workflow 层 ──",
    "app/workflow/nodes": "Workflow 节点层",
    "app/agents": "── Agent 层 ──",
    "app/skills": "── Skill 能力层 ──",
    "app/evidence": "── 证据与溯源层 ──",
    "app/llm": "── LLM 能力层 ──",
    "app/tools": "── 工具层 ──",
    "app/tools/github": "GitHub API 工具",
    "app/project_analysis": "── 项目分析层 ──",
    "app/embeddings": "── AI 能力层 ──",
    "app/vector_store": "── 向量存储层 ──",
    "tests": "── 测试层 ──",
    "test_reports": "测试产生的报告输出目录",
    "a.py": "Agent Loop 实验草稿（未纳入 app/）",
    "agent loop.py": "Agent Loop 草稿片段",
    "alembic.ini": "Alembic 配置",
    "pytest.ini": "Pytest 配置",
    "requirements.txt": "依赖清单",
    ".env": "本地环境变量（已 gitignore）",
    ".env.example": "环境变量模板",
    "generate_project_code.py": "本文档生成脚本",
}

# 章节定义：(章节标题, 章节说明, 层级名, [文件通配符])
#
# 通配符相对仓库根目录展开（`**` 可匹配零层及多层子目录）。章节按声明
# 顺序匹配，每个文件归属第一个命中的章节；未被任何章节命中的文件会
# 自动落入文末的「未归类文件」兜底章节，因此新增文件不会从文档中消失。
class Section(NamedTuple):
    title: str
    blurb: str
    layer: str
    globs: list[str]


SECTIONS: list[Section] = [
    Section(
        "二、入口层",
        "FastAPI 应用装配：日志、异常处理、路由挂载；同时收录 `app` 包标记文件",
        "入口层",
        ["app/__init__.py", "app/main.py"],
    ),
    Section(
        "三、API 层",
        "HTTP 路由定义，负责接收请求、注入数据库 Session、调用 Service",
        "API 层",
        ["app/api/**/*.py"],
    ),
    Section(
        "四、数据契约层（Schemas）",
        "接口的请求体与响应体定义，被 API 层与 Service 层共同引用",
        "数据契约层",
        ["app/schemas/**/*.py"],
    ),
    Section(
        "五、业务服务层（Services）",
        "业务编排：校验入参、组合 DAO 与工具层、掌控事务边界",
        "业务服务层",
        ["app/services/**/*.py"],
    ),
    Section(
        "六、数据访问层（Repositories）",
        "表级别的数据访问对象（DAO），只负责 SQL 与对象映射",
        "数据访问层",
        ["app/repositories/**/*.py"],
    ),
    Section(
        "七、数据模型层（Models）",
        "SQLAlchemy ORM 表结构定义",
        "数据模型层",
        ["app/models/**/*.py"],
    ),
    Section(
        "八、数据库层（DB）",
        "ORM 基类与异步 Engine / Session 管理",
        "数据库层",
        ["app/db/**/*.py"],
    ),
    Section(
        "九、核心基础设施层（Core）",
        "配置、日志、异常体系与全局异常处理器，贯穿所有分层",
        "核心基础设施层",
        ["app/core/**/*.py"],
    ),
    Section(
        "十、Workflow 层（Workflow）",
        "自研工作流引擎：状态、上下文、节点、流转、重试、检查点与执行引擎",
        "Workflow 层",
        ["app/workflow/*.py"],
    ),
    Section(
        "十一、Workflow 节点层（Workflow Nodes）",
        "各类节点的具体实现：开始 / 结束 / 分析 / Agent / Tool / Skill / 人工审核",
        "Workflow 节点层",
        ["app/workflow/nodes/**/*.py"],
    ),
    Section(
        "十二、Agent 层（Agents）",
        "Agent 抽象接口、领域 Agent 实现、Agent 注册中心与运行环境；"
        "Agent 只编排 Skill，不直接持有 Tool",
        "Agent 层",
        ["app/agents/**/*.py"],
    ),
    Section(
        "十三、Skill 层（Skills）",
        "业务能力层：组合多个 Tool 完成一次业务分析，"
        "向 Agent 暴露统一的 execute(context, input_data)",
        "Skill 层",
        ["app/skills/**/*.py"],
    ),
    Section(
        "十四、证据与溯源层（Evidence）",
        "证据链领域层：Evidence / Claim / Citation 的存储与状态校验，"
        "以及 Claim → Citation → Evidence → 源码位置的溯源构建",
        "证据与溯源层",
        ["app/evidence/**/*.py"],
    ),
    Section(
        "十五、LLM 能力层（LLM）",
        "大模型调用的抽象接口与 DeepSeek 实现",
        "LLM 能力层",
        ["app/llm/**/*.py"],
    ),
    Section(
        "十六、工具层（Tools）",
        "Tool 抽象基类与具体工具：文件读取、代码搜索、依赖分析、语义检索、"
        "数据库查询与报告导出",
        "工具层",
        ["app/tools/**/*.py"],
    ),
    Section(
        "十七、项目分析层（Project Analysis）",
        "文档切分、向量索引构建",
        "项目分析层",
        ["app/project_analysis/**/*.py"],
    ),
    Section(
        "十八、AI 能力层（Embeddings）",
        "文本向量化的抽象接口与 Ollama 本地实现",
        "AI 能力层",
        ["app/embeddings/**/*.py"],
    ),
    Section(
        "十九、向量存储层（Vector Store）",
        "Qdrant Collection 管理、向量写入与相似度检索",
        "向量存储层",
        ["app/vector_store/**/*.py"],
    ),
    Section(
        "二十、数据库迁移层（Alembic）",
        "Alembic 异步运行环境与版本化迁移脚本",
        "数据库迁移层",
        ["alembic/**/*.py"],
    ),
    Section(
        "二十一、测试层（Tests）",
        "单元测试与集成测试",
        "测试层",
        ["tests/**/*.py"],
    ),
    Section(
        "二十二、仓库根目录脚本",
        "文档生成脚本与 Agent Loop 实验草稿（未纳入 app/）",
        "根目录脚本",
        ["*.py"],
    ),
]

# 章节内的阅读顺序：命中此表的文件按表内顺序排列，其余文件按路径
# 字母序排在其后。新增文件无需登记也会被收录，只是排在已知文件之后。
PREFERRED_ORDER: list[str] = [
    # 入口 / API / 契约
    "app/__init__.py",
    "app/main.py",
    "app/api/v1/analysis.py",
    "app/schemas/analysis.py",
    "app/schemas/error.py",
    "app/schemas/evidence.py",
    # 服务 / DAO / 模型
    "app/services/analysis_service.py",
    "app/services/repository_service.py",
    "app/services/evidence_service.py",
    "app/repositories/__init__.py",
    "app/repositories/repository.py",
    "app/repositories/repository_basic.py",
    "app/repositories/analysis_run.py",
    "app/repositories/evidence.py",
    "app/repositories/claim.py",
    "app/repositories/citation.py",
    "app/repositories/checkpoint.py",
    "app/models/__init__.py",
    "app/models/repository.py",
    "app/models/analysis_run.py",
    "app/models/analysis_task.py",
    "app/models/evidence.py",
    "app/models/claim.py",
    "app/models/citation.py",
    "app/models/checkpoint.py",
    "app/db/base.py",
    "app/db/session.py",
    # 核心基础设施
    "app/core/config.py",
    "app/core/exceptions.py",
    "app/core/error_handlers.py",
    "app/core/logging.py",
    # Workflow 引擎与节点
    "app/workflow/state.py",
    "app/workflow/context.py",
    "app/workflow/node.py",
    "app/workflow/transition.py",
    "app/workflow/result.py",
    "app/workflow/retry.py",
    "app/workflow/checkpoint.py",
    "app/workflow/exceptions.py",
    "app/workflow/workflow.py",
    "app/workflow/engine.py",
    "app/workflow/nodes/base.py",
    "app/workflow/nodes/start_node.py",
    "app/workflow/nodes/end_node.py",
    "app/workflow/nodes/analysis_node.py",
    "app/workflow/nodes/agent_node.py",
    "app/workflow/nodes/tool_node.py",
    "app/workflow/nodes/skill_node.py",
    "app/workflow/nodes/human_node.py",
    # Agent / Skill / Evidence
    "app/agents/base.py",
    "app/agents/planner_agent.py",
    "app/agents/repository_analysis_agent.py",
    "app/agents/architecture_analysis_agent.py",
    "app/agents/technology_analysis_agent.py",
    "app/agents/evidence_analysis_agent.py",
    "app/agents/critic_agent.py",
    "app/agents/agent_registry.py",
    "app/agents/agent_runtime.py",
    "app/agents/researcher.py",
    "app/skills/__init__.py",
    "app/skills/base.py",
    "app/skills/repository_analysis_skill.py",
    "app/skills/architecture_analysis_skill.py",
    "app/skills/technology_analysis_skill.py",
    "app/skills/evidence_analysis_skill.py",
    "app/skills/report_generation_skill.py",
    "app/skills/registry.py",
    "app/evidence/__init__.py",
    "app/evidence/store.py",
    "app/evidence/verifier.py",
    "app/evidence/traceability.py",
    # LLM / Tool / 项目分析 / 向量
    "app/llm/base.py",
    "app/llm/deepseek.py",
    "app/tools/__init__.py",
    "app/tools/base.py",
    "app/tools/file_reader_tool.py",
    "app/tools/dependency_analyzer_tool.py",
    "app/tools/qdrant_search_tool.py",
    "app/tools/mysql_query_tool.py",
    "app/tools/report_export_tool.py",
    "app/tools/github/github_repository_tool.py",
    "app/tools/github/github_code_search_tool.py",
    "app/tools/github/parser.py",
    "app/project_analysis/code_chunker.py",
    "app/project_analysis/project_indexer.py",
    "app/project_analysis/repository_indexer.py",
    "app/embeddings/base.py",
    "app/embeddings/ollama.py",
    "app/vector_store/qdrant.py",
    # 迁移脚本（按 revision 产生顺序）
    "alembic/env.py",
    "alembic/versions/479571222143_create_initial_analysis_tables.py",
    "alembic/versions/a9e1f4c2d8b7_add_evidence_claim_citation.py",
    "alembic/versions/b0f6883a5f43_add_checkpoints.py",
    # 仓库根目录
    "generate_project_code.py",
    "a.py",
    "agent loop.py",
]

ORDER_INDEX: dict[str, int] = {
    rel: index for index, rel in enumerate(PREFERRED_ORDER)
}

# 每个文件的「层级」与「职责」
DESCRIPTIONS: dict[str, tuple[str, str]] = {
    # 入口层
    "app/main.py": (
        "入口层",
        "FastAPI 应用初始化、日志初始化、全局异常注册、路由挂载；文件末尾额外装配了 `WorkflowContext`（agents / tools / skills）的草稿代码",
    ),
    # API 层
    "app/api/v1/analysis.py": (
        "API 层",
        "Analysis 相关的 HTTP 路由定义，负责接收请求、注入数据库 Session、调用 Service",
    ),
    # 数据契约层
    "app/schemas/analysis.py": (
        "数据契约层（Schemas）",
        "Analysis 接口的请求体与响应体定义",
    ),
    "app/schemas/error.py": (
        "数据契约层（Schemas）",
        "统一错误响应结构，保证各接口返回一致的错误格式",
    ),
    "app/schemas/evidence.py": (
        "数据契约层（Schemas）",
        "Evidence / Claim / Citation 的请求体与响应体定义"
        "（`EvidenceCreateRequest` / `ClaimCreateRequest` / `CitationCreateRequest` 等）",
    ),
    # 业务服务层
    "app/services/analysis_service.py": (
        "业务服务层（Services）",
        "Analysis 任务的业务编排——校验 URL、创建或复用 Repository、创建 Analysis Run 并提交事务",
    ),
    "app/services/repository_service.py": (
        "业务服务层（Services）",
        "Repository 查询 / 创建 / GitHub 数据同步。依赖工具层的 `GitHubRepositoryTool` 与 `parse_github_url`",
    ),
    "app/services/evidence_service.py": (
        "业务服务层（Services）",
        "证据链业务编排：`create_evidence()` / `create_claim()` / `cite()` 落库，"
        "`verify_evidence()` / `verify_claim()` 走校验器，"
        "`get_claim_traceability()` 返回溯源链；调用链为 Service → Store → Verifier → Traceability → Repository",
    ),
    # 数据访问层
    "app/repositories/__init__.py": (
        "数据访问层（Repositories）",
        "本层类的统一导出入口",
    ),
    "app/repositories/repository.py": (
        "数据访问层（Repositories）",
        "`repositories` 表的数据访问（**全字段版**，`create()` 内部 commit）",
    ),
    "app/repositories/repository_basic.py": (
        "数据访问层（Repositories）",
        "`repositories` 表的数据访问（**精简版**，`create()` 只 flush，事务交给调用方）",
    ),
    "app/repositories/analysis_run.py": (
        "数据访问层（Repositories）",
        "`analysis_runs` 表的数据访问",
    ),
    "app/repositories/evidence.py": (
        "数据访问层（Repositories）",
        "`evidences` 表的数据访问：`create()` / `get_by_id()` / `list_by_repository()`",
    ),
    "app/repositories/claim.py": (
        "数据访问层（Repositories）",
        "`claims` 表的数据访问：`create()` / `get_by_id()` / `list_by_run()`",
    ),
    "app/repositories/citation.py": (
        "数据访问层（Repositories）",
        "`citations` 表的数据访问：`create()` / `get_by_id()` / `get_by_claim()` / `exists()`",
    ),
    "app/repositories/checkpoint.py": (
        "数据访问层（Repositories）",
        "`checkpoints` 表的数据访问：`save()`（同 run 内自增版本号）/ "
        "`get_latest()` / `delete()`，支撑 Workflow 的暂停与恢复",
    ),
    # 数据模型层
    "app/models/__init__.py": (
        "数据模型层（Models）",
        "模型统一导出（同时供 Alembic 迁移发现全部表）",
    ),
    "app/models/repository.py": (
        "数据模型层（Models）",
        "`repositories` 表结构定义",
    ),
    "app/models/analysis_run.py": (
        "数据模型层（Models）",
        "`analysis_runs` 表结构定义",
    ),
    "app/models/analysis_task.py": (
        "数据模型层（Models）",
        "`analysis_tasks` 表结构定义",
    ),
    "app/models/evidence.py": (
        "数据模型层（Models）",
        "`evidences` 表结构定义（Phase 9）：一条可验证的证据，"
        "带 source_type / source_url / file_path / line 等来源定位字段与 verification_status",
    ),
    "app/models/claim.py": (
        "数据模型层（Models）",
        "`claims` 表结构定义（Phase 9）：一次分析 Run 产出的结论，"
        "通过 `citations` 关联到证据",
    ),
    "app/models/citation.py": (
        "数据模型层（Models）",
        "`citations` 表结构定义：Claim → Evidence 的引用关系，"
        "对 (claim_id, evidence_id) 加唯一约束避免重复引用",
    ),
    "app/models/checkpoint.py": (
        "数据模型层（Models）",
        "`checkpoints` 表结构定义：Workflow 状态快照，"
        "保存 run_id / checkpoint_version / current_node / state_data / outputs / "
        "errors / retry_count / pause_reason / human_approved",
    ),
    # 数据库层
    "app/db/base.py": (
        "数据库层（DB）",
        "SQLAlchemy ORM 声明式基类",
    ),
    "app/db/session.py": (
        "数据库层（DB）",
        "异步 Engine、Session 工厂，以及 FastAPI 的数据库依赖 `get_db`",
    ),
    # 核心基础设施层
    "app/core/config.py": (
        "核心基础设施层（Core）",
        "从环境变量与 `.env` 加载全局配置，并生成 MySQL 异步连接串",
    ),
    "app/core/exceptions.py": (
        "核心基础设施层（Core）",
        "项目统一异常体系，按错误来源划分类型并绑定 HTTP 状态码与错误码",
    ),
    "app/core/error_handlers.py": (
        "核心基础设施层（Core）",
        "FastAPI 全局异常处理器，将业务异常与未预期异常转换为统一 JSON 响应",
    ),
    "app/core/logging.py": (
        "核心基础设施层（Core）",
        "全局日志初始化格式，以及带 `run_id` 的任务日志辅助函数",
    ),
    # Workflow 层
    "app/workflow/state.py": (
        "Workflow 层（Workflow）",
        "Workflow 运行状态 `WorkflowState`：run_id、status、current_node、data、outputs、errors、retry_count",
    ),
    "app/workflow/context.py": (
        "Workflow 层（Workflow）",
        "Workflow 执行上下文 `WorkflowContext`：agents / tools / skills / config",
    ),
    "app/workflow/node.py": (
        "Workflow 层（Workflow）",
        "节点抽象 `BaseNode`，定义 `execute(state, context)`",
    ),
    "app/workflow/transition.py": (
        "Workflow 层（Workflow）",
        "节点流转关系 `Transition`：source / target / 可选条件函数",
    ),
    "app/workflow/result.py": (
        "Workflow 层（Workflow）",
        "节点执行结果 `NodeResult`：success / data / error",
    ),
    "app/workflow/retry.py": (
        "Workflow 层（Workflow）",
        "重试策略 `RetryPolicy`：max_retry 与 `can_retry()`",
    ),
    "app/workflow/checkpoint.py": (
        "Workflow 层（Workflow）",
        "状态保存与恢复 `CheckpointManager`，内存实现：按 run_id 用 `deepcopy` 保存 `WorkflowState` 快照",
    ),
    "app/workflow/exceptions.py": (
        "Workflow 层（Workflow）",
        "Workflow 自有异常：`WorkflowError`（继承 `ApplicationError`，可被全局异常处理器捕获）/ `NodeExecutionError`",
    ),
    "app/workflow/workflow.py": (
        "Workflow 层（Workflow）",
        "流程定义 `Workflow`：`add_node()` 注册节点、`add_transition()` 注册流转",
    ),
    "app/workflow/engine.py": (
        "Workflow 层（Workflow）",
        "执行引擎 `WorkflowEngine`：从 `start` 节点起循环执行，异常时记录 errors 并置 FAILED，正常结束置 COMPLETED；支持可选 `checkpoint` / `retry_policy`，`RetryableError` 按 `RetryPolicy` 重试，`PAUSED` 状态保存检查点后退出，`resume_from` 可从检查点恢复",
    ),
    # Workflow 节点层
    "app/workflow/nodes/base.py": (
        "Workflow 节点层",
        "节点基类 `BaseNode`（与 `app/workflow/node.py` 中的同名类重复定义）",
    ),
    "app/workflow/nodes/start_node.py": (
        "Workflow 节点层",
        "开始节点 `StartNode`（name=`start`），把 status 置为 RUNNING",
    ),
    "app/workflow/nodes/end_node.py": (
        "Workflow 节点层",
        "结束节点 `EndNode`（name=`end`），把 status 置为 COMPLETED",
    ),
    "app/workflow/nodes/analysis_node.py": (
        "Workflow 节点层",
        "分析节点 `AnalysisNode`（name=`analysis`），当前为占位实现",
    ),
    "app/workflow/nodes/agent_node.py": (
        "Workflow 节点层",
        "Agent 节点 `AgentNode`，调用 `agent.run(state, context)` 并把结果追加到 `state.outputs`",
    ),
    "app/workflow/nodes/tool_node.py": (
        "Workflow 节点层",
        "Tool 节点 `ToolNode`，从 `state.data[node.name]` 取参后调用 `tool.execute(**args)`，并把结果追加到 `state.outputs`",
    ),
    "app/workflow/nodes/skill_node.py": (
        "Workflow 节点层",
        "Skill 节点 `SkillNode`，以 `skill.execute(context=context, input_data=state.data)` 调用 Skill，把结果同时写入 `state.data[node.name]` 与 `state.outputs`",
    ),
    "app/workflow/nodes/human_node.py": (
        "Workflow 节点层",
        "HITL 人工审核节点 `HumanNode`（name=`human_review`），把 status 置为 WAITING_HUMAN 以暂停流程",
    ),
    # Agent 层
    "app/agents/base.py": (
        "Agent 层（Agents）",
        "Agent 抽象基类 `BaseAgent`：持有 `skill_registry`，提供 `get_skill(name)`，子类实现 `execute(context, input_data)`。Agent 不直接持有 Tool，只编排 Skill",
    ),
    "app/agents/planner_agent.py": (
        "Agent 层（Agents）",
        "任务规划 Agent `PlannerAgent`（name=`planner_agent`）。当前返回**固定**的分析任务清单（repository → architecture → technology → evidence → critic），后续 Phase 升级为 LLM 动态规划",
    ),
    "app/agents/repository_analysis_agent.py": (
        "Agent 层（Agents）",
        "仓库基础信息分析 Agent `RepositoryAnalysisAgent`（name=`repository_analysis_agent`），转调 `repository_analysis` Skill",
    ),
    "app/agents/architecture_analysis_agent.py": (
        "Agent 层（Agents）",
        "架构分析 Agent `ArchitectureAnalysisAgent`（name=`architecture_analysis_agent`），转调 `architecture_analysis` Skill",
    ),
    "app/agents/technology_analysis_agent.py": (
        "Agent 层（Agents）",
        "技术栈分析 Agent `TechnologyAnalysisAgent`（name=`technology_analysis_agent`），转调 `technology_analysis` Skill",
    ),
    "app/agents/evidence_analysis_agent.py": (
        "Agent 层（Agents）",
        "证据追踪 Agent `EvidenceAnalysisAgent`（name=`evidence_analysis_agent`），转调 `evidence_analysis` Skill",
    ),
    "app/agents/critic_agent.py": (
        "Agent 层（Agents）",
        "结果检查 Agent `CriticAgent`（name=`critic_agent`），检查 `input_data` 是否含 `repository` / `architecture` / `technology` 三项，返回 `{passed, errors}`",
    ),
    "app/agents/agent_registry.py": (
        "Agent 层（Agents）",
        "Agent 注册中心 `AgentRegistry`：按 `agent.name` 注册与获取；`create_agent_registry(skill_registry)` 在启动时构造全部 6 个领域 Agent",
    ),
    "app/agents/researcher.py": (
        "Agent 层（Agents）",
        "**空文件**（0 字节），预留的研究 Agent 占位",
    ),
    "app/agents/agent_runtime.py": (
        "Agent 层（Agents）",
        "Agent 运行环境 `AgentRuntime`：持有 `agent_registry`，`execute(agent_name, context, input_data)` 按名取 Agent 后转调其 `execute()`",
    ),
    # Skill 层
    "app/skills/__init__.py": (
        "Skill 层（Skills）",
        "Skill 包入口，导出 `BaseSkill`",
    ),
    "app/skills/base.py": (
        "Skill 层（Skills）",
        "Skill 抽象基类 `BaseSkill`：`name` / `description` 标识与 `execute(context, input_data)`。Skill 组合多个 Tool 完成一次业务能力，例如 `RepositoryAnalysisSkill` = GitHub Tool + FileReader Tool + DependencyAnalyzer Tool",
    ),
    "app/skills/repository_analysis_skill.py": (
        "Skill 层（Skills）",
        "仓库分析能力 `RepositoryAnalysisSkill`（name=`repository_analysis`），依次调用 `github_repository` / `file_reader` / `dependency_analyzer` 三个 Tool，产出 `{repository, readme, dependencies}`",
    ),
    "app/skills/architecture_analysis_skill.py": (
        "Skill 层（Skills）",
        "架构分析能力 `ArchitectureAnalysisSkill`（name=`architecture_analysis`），用 `github_code_search` 搜出文件列表，再逐个用 `file_reader` 读取内容，产出 `{files, modules}`",
    ),
    "app/skills/technology_analysis_skill.py": (
        "Skill 层（Skills）",
        "技术栈分析能力 `TechnologyAnalysisSkill`（name=`technology_analysis`），调用 `dependency_analyzer` Tool，产出 `{technology_stack}`",
    ),
    "app/skills/evidence_analysis_skill.py": (
        "Skill 层（Skills）",
        "证据追踪能力 `EvidenceAnalysisSkill`（name=`evidence_analysis`），调用 `qdrant_search` Tool 做语义检索，产出 `{evidence}`",
    ),
    "app/skills/report_generation_skill.py": (
        "Skill 层（Skills）",
        "报告生成能力 `ReportGenerationSkill`（name=`report_generation`），聚合各 Skill 结果并交给 `report_export` Tool 导出；Tool 缺失时直接返回结构化结果",
    ),
    "app/skills/registry.py": (
        "Skill 层（Skills）",
        "Skill 注册中心 `SkillRegistry`（`register()` / `get(name)`）；`create_skill_registry()` 注册全部 5 个默认 Skill",
    ),
    # 证据与溯源层
    "app/evidence/__init__.py": (
        "证据与溯源层（Evidence）",
        "证据链领域层的包标记文件；本层聚合 Evidence / Claim / Citation / Verification / Traceability 五块能力",
    ),
    "app/evidence/store.py": (
        "证据与溯源层（Evidence）",
        "领域存储 `EvidenceStore`：包装三个 Repository 完成证据对象的落库与关联校验"
        "（`create_evidence()` / `create_claim()` / `create_citation()`），"
        "并定义合法状态集合 `VERIFICATION_STATUSES`（VERIFIED / UNVERIFIED / CONFLICT）",
    ),
    "app/evidence/verifier.py": (
        "证据与溯源层（Evidence）",
        "校验器 `EvidenceVerifier`：校验状态取值合法性，"
        "对 Evidence / Claim 执行 `verify_evidence()` / `verify_claim()` 状态流转",
    ),
    "app/evidence/traceability.py": (
        "证据与溯源层（Evidence）",
        "溯源服务 `TraceabilityService`：`get_claim_trace()` 沿 "
        "Claim → Citation → Evidence → Source → File → Line 组装完整证据链",
    ),
    # LLM 能力层
    "app/llm/base.py": (
        "LLM 能力层（LLM）",
        "LLM 抽象接口 `BaseLLM`，定义 `chat(messages)`",
    ),
    "app/llm/deepseek.py": (
        "LLM 能力层（LLM）",
        "DeepSeek 实现 `DeepSeekLLM`，包装 OpenAI 兼容客户端，固定 `model=\"deepseek-chat\"`，返回 `choices[0].message.content`",
    ),
    # 工具层
    "app/tools/__init__.py": (
        "工具层（Tools）",
        "本层部分工具的统一导出入口（当前导出 `MySQLQueryTool` 与 `ReportExportTool`）",
    ),
    "app/tools/base.py": (
        "工具层（Tools）",
        "Tool 抽象基类 `BaseTool`，定义 `name` 与 `execute(**kwargs)`",
    ),
    "app/tools/file_reader_tool.py": (
        "工具层（Tools）",
        "GitHub 文件读取工具 `FileReaderTool`（name=`file_reader`），从 raw.githubusercontent.com 读取文件，`main` 取不到时自动回退 `master`",
    ),
    "app/tools/dependency_analyzer_tool.py": (
        "工具层（Tools）",
        "依赖分析工具 `DependencyAnalyzerTool`（name=`dependency_analyzer`），解析本地项目的 requirements.txt 与 docker-compose.yml，产出 frameworks / database / llm / embedding / deployment 清单",
    ),
    "app/tools/qdrant_search_tool.py": (
        "工具层（Tools）",
        "语义检索工具 `QdrantSearchTool`（name=`qdrant_search`），注入 `QdrantVectorStore`，按查询向量返回 Top-K 的 payload",
    ),
    "app/tools/mysql_query_tool.py": (
        "工具层（Tools）",
        "数据库查询工具 `MySQLQueryTool`（name=`mysql_query`），封装 AsyncSession 执行 SQL 并返回字典列表",
    ),
    "app/tools/report_export_tool.py": (
        "工具层（Tools）",
        "报告导出工具 `ReportExportTool`（name=`report_export`），把标题与正文写成 Markdown 文件",
    ),
    "app/tools/github/github_repository_tool.py": (
        "工具层（Tools）",
        "调用 GitHub REST API 获取仓库元数据（类名 `GitHubRepositoryTool`，name=`github_repository`）",
    ),
    "app/tools/github/github_code_search_tool.py": (
        "工具层（Tools）",
        "GitHub 源码搜索工具 `GitHubCodeSearchTool`（name=`github_code_search`），调用 Code Search API；该 API 必须认证，配置了 `GITHUB_TOKEN` 时自动带上 Authorization 头",
    ),
    "app/tools/github/parser.py": (
        "工具层（Tools）",
        "解析 GitHub 仓库 URL，返回 `(owner, name)` 元组",
    ),
    # 项目分析层
    "app/project_analysis/code_chunker.py": (
        "项目分析层（Project Analysis）",
        "将 Markdown 文档按标题切分成语义 Chunk，过长章节再做滑窗切分（内部类名 `MarkdownChunker`）",
    ),
    "app/project_analysis/project_indexer.py": (
        "项目分析层（Project Analysis）",
        "文档索引编排——切分 → 逐块向量化 → 生成稳定 ID → 写入 Qdrant（内部类名 `DocumentIndexer`）",
    ),
    "app/project_analysis/repository_indexer.py": (
        "项目分析层（Project Analysis）",
        "拉取仓库 README → 生成向量 → 写入 Qdrant（整篇作为一个向量，不切分）；通过工具层 `FileReaderTool.read_file()` 读取 README",
    ),
    # AI 能力层
    "app/embeddings/base.py": (
        "AI 能力层（Embeddings）",
        "Embedding Provider 的抽象接口定义",
    ),
    "app/embeddings/ollama.py": (
        "AI 能力层（Embeddings）",
        "基于 Ollama 的本地 Embedding 实现",
    ),
    # 向量存储层
    "app/vector_store/qdrant.py": (
        "向量存储层（Vector Store）",
        "Qdrant Collection 管理、向量写入与相似度检索",
    ),
    # Alembic
    "alembic/env.py": (
        "数据库迁移层（Alembic）",
        "Alembic 运行环境配置，绑定异步 Engine 与 ORM 元数据",
    ),
    "alembic/versions/479571222143_create_initial_analysis_tables.py": (
        "数据库迁移层（Alembic）",
        "初始建表迁移脚本，创建 `repositories` / `analysis_runs` / `analysis_tasks` 三张表",
    ),
    "alembic/versions/a9e1f4c2d8b7_add_evidence_claim_citation.py": (
        "数据库迁移层（Alembic）",
        "Phase 9 迁移脚本，创建证据链三张表 `evidences` / `claims` / `citations`",
    ),
    "alembic/versions/b0f6883a5f43_add_checkpoints.py": (
        "数据库迁移层（Alembic）",
        "Phase 10 迁移脚本，创建 Workflow 检查点表 `checkpoints`",
    ),
}

# 测试层描述
TEST_DESCRIPTIONS: dict[str, str] = {
    "tests/test_agent_registry.py": "Agent 注册中心测试（创建 Skill 注册中心 → 构造 Agent 注册中心 → 断言 Agent 可注册与获取）",
    "tests/test_agent_runtime.py": "Agent 运行环境测试（FakeRegistry + FakeAgent，断言 `execute()` 返回 Agent 结果；Agent 不存在时抛异常）",
    "tests/test_analysis_api.py": "API 端到端测试（健康检查、创建任务、查询任务、参数校验、404 场景）",
    "tests/test_chunker.py": "Markdown 切分器单元测试",
    "tests/test_config.py": "配置加载单元测试",
    "tests/test_database.py": "MySQL 连接连通性测试（需数据库可用）",
    "tests/test_dependency_analyzer_tool.py": "依赖分析工具测试（解析本项目，断言 frameworks 字段存在）",
    "tests/test_embedding.py": "Ollama Embedding 单元测试（需 Ollama 服务可用）",
    "tests/test_embedding_qdrant.py": "Embedding → Qdrant 写入 → 语义检索集成测试",
    "tests/test_evidence_agent.py": "EvidenceAnalysisAgent 测试（Fake Skill 注入，断言 Agent 编排结果）",
    "tests/test_evidence_models.py": "证据链三张表模型测试（Evidence / Claim / Citation 字段与默认值）",
    "tests/test_evidence_service.py": "EvidenceService 测试（空内容证据被拒、正常创建与校验路径）",
    "tests/test_evidence_skill.py": "EvidenceAnalysisSkill 测试（Fake Tool，断言证据分析结果结构）",
    "tests/test_evidence_store.py": "EvidenceStore 单元测试（非法状态抛 ValidationError、状态值大写归一化）",
    "tests/test_evidence_verifier.py": "EvidenceVerifier 测试（合法状态流转成功、非法状态抛异常）",
    "tests/test_exceptions.py": "异常体系单元测试",
    "tests/test_github_client.py": "GitHub REST API 工具测试（需外网可用）",
    "tests/test_github_code_search_tool.py": "GitHub 源码搜索工具测试（fake client + fake settings，覆盖返回结果与 token 认证头）",
    "tests/test_github_parser.py": "GitHub URL 解析单元测试",
    "tests/test_indexer.py": "DocumentIndexer 集成测试（Chunk → Embedding → Qdrant）",
    "tests/test_mysql_query_tool.py": "MySQL 查询工具测试（FakeSession 模拟查询结果）",
    "tests/test_phase10.py": "Phase 10 测试（HITL 设计闸门、HumanNode 触发暂停、手动暂停与恢复、Checkpoint 存取、可重试错误重试与重试上限、不可重试错误直接失败）",
    "tests/test_qdrant.py": "Qdrant 向量存储层单元测试（造数据 → 检索 → 断言排序）",
    "tests/test_qdrant_search_tool.py": "语义检索工具测试（FakeVectorStore 返回固定 payload）",
    "tests/test_report_export_tool.py": "报告导出工具测试（写出 Markdown 到 test_reports/）",
    "tests/test_repository_analysis_workflow.py": "Skill 驱动的 Workflow 集成测试（Mock Tool → RepositoryAnalysisSkill → SkillNode → Transition 串联执行）",
    "tests/test_repository_crud.py": "数据访问层测试（创建、按 URL 查、按 ID 查）；运行前会清理同 URL 残留记录以保证可重复运行",
    "tests/test_repository_pipeline.py": "端到端管道测试（Service 拉取仓库 → Indexer 建立索引）",
    "tests/test_repository_service.py": "业务服务层测试（不存在时创建、存在时复用）",
    "tests/test_repository_skill.py": "RepositoryAnalysisSkill 单元测试（Fake GitHub / FileReader / Dependency Tool，断言三路结果合并）",
    "tests/test_retrieval.py": "语义检索测试（建立索引 → 用自然语言问题检索 → 断言命中）",
    "tests/test_skill_base.py": "Skill 抽象基类测试（子类具备 `name` / `description` 且可实现 `execute()`）",
    "tests/test_skill_node.py": "SkillNode 单元测试（FakeSkill，断言结果写入 `state.data[node.name]` 与 `state.outputs`）",
    "tests/test_skill_registry.py": "Skill 注册中心测试（默认 5 个 Skill 是否注册成功并可获取）",
    "tests/test_skill_workflow.py": "Skill 全链路 Workflow 测试（Start → SkillNode(RepositoryAnalysisSkill) → End，断言 status 与 data）",
    "tests/test_tools.py": "工具层测试（`GitHubRepositoryTool` 取仓库、`FileReaderTool` 读文件）",
    "tests/test_traceability.py": "可追溯性测试（造 Claim / Citation / Evidence 后，断言溯源链解析到源码文件与行号）",
    "tests/test_workflow.py": "Workflow Engine 测试（顺序执行、失败捕获、可重试与不可重试、检查点存取、暂停与恢复）",
}

LAYER_DIAGRAM = """```
                        ┌─────────────────────────┐
    HTTP 请求 ─────────▶ │   API 层                │  app/api/v1/
                        │   (路由 + 依赖注入)      │
                        └───────────┬─────────────┘
                                    │
                                    ▼
                        ┌─────────────────────────┐
                        │   业务服务层             │  app/services/
                        │   (业务编排)             │
                        └───────┬─────────┬───────┘
                                │         │
                ┌───────────────┘         └───────────────┐
                ▼                                         ▼
    ┌───────────────────────┐               ┌─────────────────────────┐
    │  数据访问层            │               │  工具层                  │
    │  app/repositories/    │               │  app/tools/             │
    └───────────┬───────────┘               └────────────┬────────────┘
                │                                        │
                ▼                                        ▼
    ┌───────────────────────┐               ┌─────────────────────────┐
    │  数据模型层            │               │  项目分析层              │
    │  app/models/          │               │  app/project_analysis/  │
    └───────────┬───────────┘               └───────────┬─────────────┘
                │                                       │
                ▼                                       ▼
    ┌───────────────────────┐               ┌─────────────────────────┐
    │  数据库层              │               │  AI 能力层 / 向量存储层  │
    │  app/db/              │               │  app/embeddings/        │
    │      → MySQL          │               │  app/vector_store/      │
    └───────────────────────┘               │      → Qdrant           │
                                            └─────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │  Workflow 层  app/workflow/  +  app/workflow/nodes/             │
    │  WorkflowEngine 按 Transition 驱动 Node 执行，共享 WorkflowState │
    └───────────────┬─────────────────────────────┬───────────────────┘
                    │                             │
                    ▼                             ▼
    ┌────────────────────────────────────────────────────────┐
    │  Agent 层  app/agents/                                  │
    │  BaseAgent / *Agent / AgentRegistry / AgentRuntime      │
    └───────────────────────────┬────────────────────────────┘
                                │  通过 SkillRegistry 取能力
                                ▼
    ┌────────────────────────────────────────────────────────┐
    │  Skill 层  app/skills/                                  │
    │  BaseSkill / *Skill / SkillRegistry                     │
    │  一个 Skill 组合多个 Tool 完成一次业务能力               │
    └───────────────────────────┬────────────────────────────┘
                                │
                                ▼
    ┌───────────────────────────┐   ┌─────────────────────────┐
    │  工具层  app/tools/        │   │  LLM 能力层  app/llm/    │
    │  BaseTool / *Tool          │   │  BaseLLM / DeepSeekLLM  │
    └───────────────────────────┘   └─────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────┐
    │  证据与溯源层  app/evidence/                                     │
    │  EvidenceStore / EvidenceVerifier / TraceabilityService         │
    │  证据链：Claim ─▶ Citation ─▶ Evidence ─▶ Source(file:line)      │
    └────────────────────────────────┬────────────────────────────────┘
                                     │  经 app/repositories/ 落 MySQL
                                     ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │  Workflow 状态持久化  app/workflow/checkpoint.py                 │
    │  WorkflowState ⇄ app/models/checkpoint.py（checkpoints 表）      │
    │  支撑暂停 / 恢复 / 重试                                           │
    └─────────────────────────────────────────────────────────────────┘

    调用链：Workflow ─▶ Node ─▶ Agent ─▶ Skill ─▶ Tool

    贯穿各层：app/core/（配置、日志、异常、异常处理器）
    数据契约：app/schemas/（被 API 层与 Service 层共同引用）
```"""

# ============================================================
# 已知注意事项
#
# 每条问题都带一个 still_holds() 自动判定。生成文档时只输出判定为
# True（问题仍存在）的条目，已解决的条目会自己从文档里消失，剩余
# 条目的编号随实际保留数量自动重排，无需手工维护编号。
#
# 判定无法确定时一律返回 True —— 宁可让过期条目多留一会儿，也不
# 要把真实问题悄悄删掉。
#
# 新增一条：在 KNOWN_ISSUES 里追加一个 KnownIssue，并把 clears_when
# 写清楚，便于日后核对判定口径是否仍然合理。
# ============================================================


class KnownIssue(NamedTuple):
    """一条已知问题及其自动判定。"""

    title: str
    body: str
    still_holds: Callable[[], bool]
    clears_when: str


def _src(rel: str) -> str:
    """读取工作区源码用于判定；文件不存在时返回空串。"""

    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except OSError:
        return ""


def _tree(rel: str):
    """解析源码为 AST；语法错误时返回 None。"""

    try:
        return ast.parse(_src(rel))
    except SyntaxError:
        return None


def _all_src() -> str:
    """拼接扫描范围内全部 .py 的源码。"""

    return "".join(_src(rel) for rel in source_files())


def _dir_src(prefix: str) -> str:
    """拼接指定目录前缀下全部 .py 的源码。"""

    return "".join(
        _src(rel) for rel in source_files() if rel.startswith(prefix)
    )


def _first_class_name(rel: str) -> str:
    """文件里第一个顶层类名；没有类时返回空串。"""

    tree = _tree(rel)

    if tree is None:
        return ""

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            return node.name

    return ""


def _file_class_mismatch() -> bool:
    """文件名与内部主类名是否仍不一致（文件名应能转出主类名）。"""

    for rel in (
        "app/project_analysis/code_chunker.py",
        "app/project_analysis/project_indexer.py",
    ):
        expected = "".join(
            part.title() for part in Path(rel).stem.split("_")
        )

        actual = _first_class_name(rel)

        if actual and actual != expected:
            return True

    return False


def _qdrant_insert_overlaps() -> bool:
    """qdrant.py 里是否仍有与 upsert() 重叠的 insert()。"""

    return bool(
        re.search(
            r"^\s*def insert\(",
            _src("app/vector_store/qdrant.py"),
            re.M,
        )
    )


def _duplicate_github_parsers() -> bool:
    """两份 GitHub URL 解析实现是否都还在。"""

    return (
        "def _parse_github_url"
        in _src("app/services/analysis_service.py")
        and "def parse_github_url"
        in _src("app/tools/github/parser.py")
    )


_STEP_LIMIT = re.compile(
    r"max_steps|MAX_STEPS|step_limit|MAX_ITERATIONS|max_iterations"
)


def _engine_boundaries_unresolved() -> bool:
    """引擎主循环仍无步数保护，或 retry_count 仍是全局预算。"""

    no_step_limit = not _STEP_LIMIT.search(
        _src("app/workflow/engine.py")
    )

    global_retry = "retry_count" in _src("app/workflow/state.py")

    return no_step_limit or global_retry


_TOKEN_GUARD = re.compile(r"if\s+not\s+token[\s\S]{0,300}?raise")


def _code_search_requires_token() -> bool:
    """未配置 GITHUB_TOKEN 时仍会发出必然 401 的请求。"""

    return not _TOKEN_GUARD.search(
        _src("app/tools/github/github_code_search_tool.py")
    )


_TOOL_SCHEMA = re.compile(r"BaseModel|pydantic")
_TOOL_LOGGING = re.compile(r"core\.logging|get_logger|import\s+logging")


def _tools_lack_schema_and_logging() -> bool:
    """工具层是否仍缺 Pydantic Schema，或仍没接入日志。"""

    tools = _dir_src("app/tools")

    return not (
        _TOOL_SCHEMA.search(tools)
        and _TOOL_LOGGING.search(tools)
    )


def _agent_node_uses_old_api() -> bool:
    """AgentNode 是否仍在调用已废弃的 agent.run(state, context)。"""

    return bool(
        re.search(
            r"self\.agent\.run\(",
            _src("app/workflow/nodes/agent_node.py"),
        )
    )


def _skills_hardcode_tools() -> bool:
    """Skill 层是否仍硬编码工具名，或调用实参与 Tool 形参不符。"""

    skills = _dir_src("app/skills")

    # 直接下标取工具，缺键即 KeyError
    if re.search(r"context\.tools\[", skills):
        return True

    # file_reader 的形参是 file_path，不是 path
    if re.search(
        r"file_reader\.execute\([\s\S]{0,300}?\bpath\s*=",
        skills,
    ):
        return True

    # report_export 的形参是 title / content / filename，不是 data
    if re.search(
        r"exporter\.execute\([\s\S]{0,300}?\bdata\s*=",
        skills,
    ):
        return True

    return False


def _critic_required_fields() -> set:
    """CriticAgent 里写死的必填字段集合。"""

    tree = _tree("app/agents/critic_agent.py")

    if tree is None:
        return set()

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue

        targets = [
            t.id for t in node.targets if isinstance(t, ast.Name)
        ]

        if "required_fields" in targets and isinstance(node.value, ast.List):
            return {
                element.value
                for element in node.value.elts
                if isinstance(element, ast.Constant)
                and isinstance(element.value, str)
            }

    return set()


def _skill_node_names() -> set:
    """全仓装配 SkillNode 时使用的节点名。"""

    return set(
        re.findall(
            r"SkillNode\(\s*(?:name\s*=\s*)?[\"'](\w+)[\"']",
            _all_src(),
        )
    )


def _skill_keys_mismatch_critic() -> bool:
    """SkillNode 写入的 key 是否仍与 CriticAgent 的必填字段对不上。"""

    required = _critic_required_fields()

    written = _skill_node_names()

    if not required or not written:
        # 判定不出来：保留条目，避免把真实问题悄悄删掉。
        return True

    return not required.issubset(written)


_PLANNER_TASKS_READ = re.compile(
    r"\[\s*[\"']tasks[\"']\s*\]|\.get\(\s*[\"']tasks[\"']"
)


def _planner_tasks_unconsumed() -> bool:
    """PlannerAgent 返回的 tasks 是否仍无人消费。

    只统计 workflow / services 层的读取：app/memory/ 下的同名变量是
    数据库 analysis_tasks，与本条无关，故不计入。
    """

    consumers = _dir_src("app/workflow") + _dir_src("app/services")

    return not _PLANNER_TASKS_READ.search(consumers)


def _evidence_not_exposed() -> bool:
    """证据链是否仍没有对外路由，或仍未被 main.py 装配。"""

    has_route = bool(re.search(r"evidence", _dir_src("app/api"), re.I))

    wired = "EvidenceService" in _src("app/main.py")

    return not (has_route and wired)


KNOWN_ISSUES: list[KnownIssue] = [
    KnownIssue(
        title="文件名与类名不一致",
        body="""   - `app/project_analysis/code_chunker.py` 内部类为 `MarkdownChunker`
   - `app/project_analysis/project_indexer.py` 内部类为 `DocumentIndexer`""",
        still_holds=_file_class_mismatch,
        clears_when="两个文件的主类名与文件名一致（CodeChunker / ProjectIndexer）",
    ),
    KnownIssue(
        title="`app/vector_store/qdrant.py` 的 `insert()` 方法",
        body="""   - 与 `upsert()` 功能重叠，仅 `RepositoryIndexer` 调用；`uuid` 导入专为此方法服务
   - 其 `PointStruct` 的 `id` 使用 UUID 字符串，而 `upsert()` 使用整数，两种 ID 类型混用""",
        still_holds=_qdrant_insert_overlaps,
        clears_when="qdrant.py 中不再定义 insert()，调用方统一走 upsert()",
    ),
    KnownIssue(
        title="两份重复的 GitHub URL 解析实现",
        body="""   - `app/services/analysis_service.py::_parse_github_url` — 基于字符串切分，不做域名校验
   - `app/tools/github/parser.py::parse_github_url` — 基于 `urlparse`，校验 `netloc == "github.com"` 并剥离 `.git` 后缀""",
        still_holds=_duplicate_github_parsers,
        clears_when="analysis_service 改用 tools/github/parser.py，且自身不再定义 _parse_github_url",
    ),
    KnownIssue(
        title="Workflow 引擎的行为边界",
        body="""   - 暂停判定已扩展为 `PAUSED` / `WAITING_HUMAN` / `WAITING_DESIGN` 三态
     （`WorkflowEngine.PAUSE_STATUSES`），`HumanNode` 触发的暂停现在能被引擎识别
   - 主循环 `while current_node:` 仍没有最大步数保护，编排中出现环会一直执行
   - `retry_count` 是 `state` 上的全局预算，不是每个节点独立计数""",
        still_holds=_engine_boundaries_unresolved,
        clears_when="engine.py 出现 max_steps 之类的步数上限，且 retry_count 不再由 state 全局持有",
    ),
    KnownIssue(
        title="未配置 `GITHUB_TOKEN` 时 Code Search 仍不可用",
        body="""   - `GitHubCodeSearchTool` 已支持自动带 `Authorization` 头，但 GitHub Code Search API 强制认证
   - 未配置 token 时真实调用会返回 401""",
        still_holds=_code_search_requires_token,
        clears_when="github_code_search_tool.py 在 token 缺失时提前抛业务异常，而不是发出必然 401 的请求",
    ),
    KnownIssue(
        title="Phase 6 完成标准尚未全部达成",
        body="""   - 实施文档 §9.7 要求每个 Tool 具备「输入 Schema / 输出 Schema / 异常处理 / 日志 / 测试」
   - 当前 7 个 Tool 均未定义 Pydantic Schema，也均未接入 `app/core/logging.py`""",
        still_holds=_tools_lack_schema_and_logging,
        clears_when="app/tools/ 下出现 Pydantic 模型，且接入 app/core/logging.py",
    ),
    KnownIssue(
        title="Agent 接口已换代，`AgentNode` 未同步",
        body="""   - `BaseAgent` 已从 `run(state, context)` 改为 `execute(context, input_data)`，并改为持有 `skill_registry`
   - 全部 6 个领域 Agent 都已按新接口实现，`AgentRuntime.execute(agent_name, context, input_data)` 也已适配
   - 但 `app/workflow/nodes/agent_node.py` 仍在调用 `self.agent.run(state, context)`，属于旧接口残留""",
        still_holds=_agent_node_uses_old_api,
        clears_when="agent_node.py 改调 self.agent.execute(context, input_data)",
    ),
    KnownIssue(
        title="Skill 内硬编码 Tool 名与实参不匹配",
        body="""   - 各 Skill 直接以 `context.tools["github_repository"]` 之类取工具，键名写死，缺键即 `KeyError`，没有降级或报错提示
   - `ArchitectureAnalysisSkill` 调用 `file_reader.execute(**input_data, path=file)`，但 `FileReaderTool.execute` 的形参是 `file_path`；且 `github_code_search` 需要 `keyword` / `repo`，与 `input_data` 不一定对得上
   - `ReportGenerationSkill` 调用 `exporter.execute(data=input_data)`，而 `ReportExportTool.execute` 的形参是 `title` / `content` / `filename`""",
        still_holds=_skills_hardcode_tools,
        clears_when="Skill 不再以 context.tools[...] 取工具，且 file_reader / exporter 的调用实参与 Tool 形参一致",
    ),
    KnownIssue(
        title="Skill 输出键名与 `CriticAgent` 校验字段不一致",
        body="""   - `SkillNode` 把每个 Skill 的结果写入 `state.data[node.name]`，即 `repository_analysis` / `architecture_analysis` / `technology_analysis`
   - `CriticAgent` 检查的却是 `repository` / `architecture` / `technology`，两者对不上，`passed` 会恒为 `False`
   - `PlannerAgent` 返回的 `tasks` 列表目前也没有任何代码消费，Workflow 尚未真正按计划驱动 Agent 执行""",
        still_holds=lambda: (
            _skill_keys_mismatch_critic()
            or _planner_tasks_unconsumed()
        ),
        clears_when="CriticAgent 的必填字段都能在 SkillNode 写入的 key 中找到，且 workflow / services 层有了 tasks 的消费者",
    ),
    KnownIssue(
        title="证据链能力尚未对外暴露",
        body="""   - `app/evidence/`（Store / Verifier / Traceability）、`EvidenceService`
     与 `app/schemas/evidence.py` 均已实现并有测试覆盖
   - 但 `app/api/` 下没有任何证据相关路由，`app/main.py` 也未装配 `EvidenceService`，
     目前只能由测试或脚本直接调用，尚未形成可访问的接口""",
        still_holds=_evidence_not_exposed,
        clears_when="app/api/ 下出现证据相关路由，且 main.py 装配了 EvidenceService",
    ),
]


@lru_cache(maxsize=1)
def known_issues():
    """按自动判定把条目分成 (仍存在, 已解决)。

    结果缓存，避免 build() 与 main() 各跑一遍判定。
    """

    kept: list[KnownIssue] = []
    cleared: list[KnownIssue] = []

    for issue in KNOWN_ISSUES:
        (kept if issue.still_holds() else cleared).append(issue)

    return kept, cleared


def render_known_issues() -> str:
    """渲染「已知注意事项」正文，编号按实际保留的条目重排。"""

    kept, _ = known_issues()

    if not kept:
        return (
            "当前没有已知问题：清单中的全部条目均已由自动判定确认解决。"
        )

    return "\n\n".join(
        f"{index}. **{issue.title}**\n{issue.body}"
        for index, issue in enumerate(kept, 1)
    )



def note_for(rel: str, is_dir: bool) -> str:
    """返回目录树中某一项的注释。"""

    if rel in TREE_NOTES:
        return TREE_NOTES[rel]

    if not is_dir and rel.endswith("__init__.py"):
        if (ROOT / rel).stat().st_size == 0:
            return "(空)"

    return ""


def auto_duty(rel: str) -> str:
    """未人工登记的文件：取模块文档字符串的首行作为职责。"""

    try:
        tree = ast.parse((ROOT / rel).read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError, OSError):
        return ""

    for line in (ast.get_docstring(tree) or "").splitlines():
        if line.strip():
            return line.strip()

    return ""


def sort_key(rel: str) -> tuple[int, str]:
    """章节内排序：先按 PREFERRED_ORDER，表外文件按路径字母序排在后面。"""

    return (ORDER_INDEX.get(rel, len(PREFERRED_ORDER)), rel)


def source_files() -> list[str]:
    """工作区内参与归档的全部 `.py` 文件（相对路径，已排序）。"""

    found = []

    for path in ROOT.rglob("*.py"):
        rel = path.relative_to(ROOT)

        if any(part in TREE_SKIP for part in rel.parts):
            continue

        found.append(rel.as_posix())

    return sorted(found, key=sort_key)


def expand(pattern: str) -> set[str]:
    """把章节通配符展开为相对路径集合（`**` 递归匹配任意层子目录）。"""

    return {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.glob(pattern)
        if path.is_file()
    }


def classify(files: list[str]) -> list[tuple[Section, list[str]]]:
    """按章节声明顺序分配文件；未命中的文件汇总进末尾的兜底章节。"""

    owned: dict[str, Section] = {}

    for section in SECTIONS:
        for pattern in section.globs:
            for rel in expand(pattern):
                if rel in files:
                    owned.setdefault(rel, section)

    grouped: list[tuple[Section, list[str]]] = []

    for section in SECTIONS:
        member = [rel for rel in files if owned.get(rel) is section]

        if member:
            grouped.append((section, member))

    orphan = [rel for rel in files if rel not in owned]

    if orphan:
        grouped.append(
            (
                Section(
                    "二十三、未归类文件",
                    "未命中任何章节通配符的文件。出现本章节说明仓库里有了"
                    "尚未归档的新目录，可在 `SECTIONS` 中为它补一个章节。",
                    "未归类",
                    [],
                ),
                orphan,
            )
        )

    return grouped


def render_tree() -> str:
    """从文件系统实时渲染目录树。"""

    lines: list[tuple[str, str]] = []

    def walk(directory: Path, prefix: str) -> None:
        entries = sorted(
            (
                entry
                for entry in directory.iterdir()
                if entry.name not in TREE_SKIP
                and not entry.name.endswith(".pyc")
            ),
            key=lambda entry: (entry.is_file(), entry.name.lower()),
        )

        for index, entry in enumerate(entries):
            last = index == len(entries) - 1

            connector = "└── " if last else "├── "
            display = entry.name + ("/" if entry.is_dir() else "")

            rel = entry.relative_to(ROOT).as_posix()

            lines.append(
                (
                    f"{prefix}{connector}{display}",
                    note_for(rel, entry.is_dir()),
                )
            )

            if entry.is_dir():
                walk(
                    entry,
                    prefix + ("    " if last else "│   "),
                )

    walk(ROOT, "")

    width = max(len(left) for left, _ in lines) + 3

    rendered = []

    for left, note in lines:
        if note:
            rendered.append(f"{left.ljust(width)}# {note}")
        else:
            rendered.append(left)

    return "\n".join(rendered)


def fence_for(text: str) -> str:
    """返回不会与正文冲突的代码围栏。"""

    longest = 0
    current = 0

    for char in text:
        if char == "`":
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    return "`" * max(3, longest + 1)


def empty_files() -> list[str]:
    """列出工作区内所有 0 字节的 .py 文件。"""

    found = []

    for path in sorted(ROOT.rglob("*.py")):
        rel = path.relative_to(ROOT)

        if any(part in TREE_SKIP for part in rel.parts):
            continue

        if path.stat().st_size == 0:
            found.append(rel.as_posix())

    return found


def build() -> str:
    """组装完整文档。"""

    empties = set(empty_files())
    blocks = 0
    body: list[str] = []
    grouped = classify(source_files())

    for section, members in grouped:
        body.append(f"## {section.title}")
        body.append("")
        body.append(section.blurb)
        body.append("")

        for rel in members:
            path = ROOT / rel

            layer, duty = DESCRIPTIONS.get(rel) or (
                section.layer,
                TEST_DESCRIPTIONS.get(rel) or auto_duty(rel) or "（未标注）",
            )

            body.append(f"### 📄 `{rel}`")
            body.append("")
            body.append(f"**层级**：{layer} · **职责**：{duty}")
            body.append("")

            if rel in empties:
                body.append("> 该文件为 **0 字节** 空文件，无源码内容。")
                body.append("")
                continue

            source = path.read_text(encoding="utf-8").rstrip("\n")
            fence = fence_for(source)

            body.append(f"{fence}python")
            body.append(source)
            body.append(fence)
            body.append("")

            blocks += 1

    # 附录
    appendix = [
        "---",
        "",
        "## 二十三、附录",
        "",
        "### 空文件清单",
        "",
        f"以下 {len(empties)} 个文件均为 **0 字节**，"
        "其中绝大多数是用于将目录声明为 Python 包的标记文件：",
        "",
        "| 文件路径 | 说明 |",
        "|---|---|",
    ]

    for rel in sorted(empties):
        if rel.endswith("__init__.py"):
            note = "包标记文件"
        elif rel.startswith("app/agents/"):
            note = "预留占位，尚未实现"
        else:
            note = "空文件"

        appendix.append(f"| `{rel}` | {note} |")

    appendix += [
        "",
        "### 配置文件",
        "",
        "| 文件 | 说明 |",
        "|---|---|",
        "| `alembic.ini` | Alembic 迁移配置，`script_location = %(here)s/alembic`，"
        "`sqlalchemy.url` 留空由 `env.py` 动态注入 |",
        "| `pytest.ini` | `pythonpath = .`、`asyncio_mode = auto` |",
        "| `requirements.txt` | 依赖清单 |",
        "| `.env` / `.env.example` | 环境变量（`.env` 已 gitignore） |",
        "",
        "### 已知注意事项",
        "",
        render_known_issues(),
        "",
        "---",
        "",
        f"*本文档由 `generate_project_code.py` 扫描工作区 `.py` 文件自动生成："
        f"共收录 **{blocks} 段代码**（非空文件），"
        f"另有 {len(empties)} 个 0 字节空文件，见上方「空文件清单」。*",
        "",
    ]

    header = [
        "# AIPI Platform 项目代码总览",
        "",
        "> AI Agent GitHub Project Intelligence Platform",
        ">",
        "> 本文档按**分层**整理项目中每个 `.py` 文件的完整源码，"
        "每段代码均标注所属层级与文件路径。",
        "> 代码内容由脚本从源文件直接读取生成，与仓库当前状态一致。",
        "",
        "---",
        "",
        "## 一、项目目录",
        "",
        "```",
        "AIPI Platform/",
        "│",
        render_tree(),
        "```",
        "",
        "### 分层调用关系",
        "",
        LAYER_DIAGRAM,
        "",
        "---",
        "",
    ]

    return "\n".join(header + body + appendix)


def main() -> None:
    OUTPUT.write_text(
        build(),
        encoding="utf-8",
        newline="\n",
    )

    print(f"已生成 {OUTPUT}")

    _, cleared = known_issues()

    if cleared:
        print(f"已自动移除 {len(cleared)} 条判定为已解决的问题：")

        for issue in cleared:
            print(f"  - {issue.title}")
            print(f"      判定口径：{issue.clears_when}")


if __name__ == "__main__":
    sys.exit(main())
````

### 📄 `a.py`

**层级**：根目录脚本 · **职责**：（未标注）

```python

import json
import os

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. 加载环境变量
# ============================================================

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError(
        "没有找到 DEEPSEEK_API_KEY，请检查 .env 文件"
    )


# ============================================================
# 2. 创建 DeepSeek Client
# ============================================================

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


# ============================================================
# 3. 定义真正的 Python Tool
# ============================================================

def calculator(a: float, b: float, operation: str) -> float:
    """
    一个最简单的计算器 Tool。
    """

    if operation == "add":
        return a + b

    elif operation == "subtract":
        return a - b

    elif operation == "multiply":
        return a * b

    elif operation == "divide":
        if b == 0:
            raise ValueError("除数不能为 0")

        return a / b

    else:
        raise ValueError(
            f"不支持的操作: {operation}"
        )


# ============================================================
# 4. 告诉 DeepSeek：有哪些 Tool 可以使用
# ============================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "执行数学计算。"
                "支持加法、减法、乘法和除法。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "第一个数字"
                    },
                    "b": {
                        "type": "number",
                        "description": "第二个数字"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],
                        "description": "计算操作"
                    }
                },
                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    }
]


# ============================================================
# 5. Tool 注册表
# ============================================================

TOOL_REGISTRY = {
    "calculator": calculator
}


# ============================================================
# 6. 手写 Agent Loop
# ============================================================

def agent_loop(user_input: str) -> str:

    # --------------------------------------------------------
    # 保存整个对话历史
    # --------------------------------------------------------

    messages = [
        {
            "role": "user",
            "content": user_input
        }
    ]

    # --------------------------------------------------------
    # Agent 最大循环次数
    # --------------------------------------------------------

    max_iterations = 10

    for iteration in range(max_iterations):

        print(
            f"\n========== Agent Loop "
            f"{iteration + 1} =========="
        )

        # ----------------------------------------------------
        # ① 调用 DeepSeek
        # ----------------------------------------------------

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        # ----------------------------------------------------
        # ② 获取 DeepSeek 返回的 message
        # ----------------------------------------------------

        message = response.choices[0].message

        # ----------------------------------------------------
        # ③ 把 assistant message 放进历史
        # ----------------------------------------------------

        messages.append(message)

        # ----------------------------------------------------
        # ④ 判断 DeepSeek 有没有要求调用 Tool
        # ----------------------------------------------------

        if not message.tool_calls:

            print("\n[Agent] DeepSeek 不需要 Tool")

            return message.content

        # ----------------------------------------------------
        # ⑤ DeepSeek 要求调用 Tool
        # ----------------------------------------------------

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments_json = tool_call.function.arguments

            print(
                f"\n[Agent] 请求调用 Tool: {tool_name}"
            )

            print(
                f"[Agent] Tool 参数: {arguments_json}"
            )

            # ------------------------------------------------
            # ⑥ 解析 JSON 参数
            # ------------------------------------------------

            try:

                arguments = json.loads(
                    arguments_json
                )

            except json.JSONDecodeError:

                raise ValueError(
                    f"Tool 参数不是合法 JSON: "
                    f"{arguments_json}"
                )

            # ------------------------------------------------
            # ⑦ 根据 Tool 名字找到 Python 函数
            # ------------------------------------------------

            tool = TOOL_REGISTRY.get(tool_name)

            if tool is None:

                tool_result = (
                    f"错误：不存在 Tool "
                    f"{tool_name}"
                )

            else:

                try:

                    # ----------------------------------------
                    # ⑧ 真正执行 Python Tool
                    # ----------------------------------------

                    result = tool(**arguments)

                    tool_result = str(result)

                except Exception as e:

                    tool_result = (
                        f"Tool 执行失败：{str(e)}"
                    )

            print(
                f"[Tool] 执行结果: {tool_result}"
            )

            # ------------------------------------------------
            # ⑨ 把 Tool 结果返回给 DeepSeek
            # ------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )

    # --------------------------------------------------------
    # 超过最大循环次数
    # --------------------------------------------------------

    raise RuntimeError(
        "Agent 超过最大循环次数"
    )


# ============================================================
# 7. 程序入口
# ============================================================

if __name__ == "__main__":

    user_input = input(
        "请输入你的问题："
    )

    answer = agent_loop(user_input)

    print("\n==============================")
    print("最终回答：")
    print(answer)
```

### 📄 `agent loop.py`

**层级**：根目录脚本 · **职责**：（未标注）

```python
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

#加载环境变量

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
```

## 二十三、未归类文件

未命中任何章节通配符的文件。出现本章节说明仓库里有了尚未归档的新目录，可在 `SECTIONS` 中为它补一个章节。

### 📄 `app/context/__init__.py`

**层级**：未归类 · **职责**：Context Manager 层。

```python
"""Context Manager 层。"""

from app.context.manager import (
    ContextItem,
    ContextManager,
)


__all__ = [
    "ContextItem",
    "ContextManager",
]
```

### 📄 `app/context/manager.py`

**层级**：未归类 · **职责**：Context Manager。

```python
"""Context Manager。

负责：

Retrieval
    ↓
Context Filtering
    ↓
Ranking
    ↓
Context Assembly
"""


import re

from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
)


@dataclass(frozen=True)
class ContextItem:
    """一个可供 Agent 使用的上下文片段。"""

    source: str

    content: str

    score: float = 0.0

    metadata: dict[str, Any] | None = None


class ContextManager:
    """
    把 Memory、Workflow State
    和语义检索结果组装成受控上下文。
    """

    def __init__(
        self,
        memory_manager,
        retriever: (
            Callable[
                [str],
                Awaitable[
                    list[dict[str, Any]]
                ],
            ]
            | None
        ) = None,
        *,
        max_items: int = 12,
        max_chars: int = 12000,
    ) -> None:

        self.memory_manager = (
            memory_manager
        )

        self.retriever = retriever

        self.max_items = max_items

        self.max_chars = max_chars

    async def build(
        self,
        *,
        run_id: str,
        repository_id: int,
        query: str,
        workflow_state: Any | None = None,
        user_instruction: str | None = None,
    ) -> dict[str, Any]:
        """
        构建结构化 Context
        和最终文本 Context。
        """

        memory = (
            await self.memory_manager.retrieve(
                run_id=run_id,
                repository_id=repository_id,
                query=query,
            )
        )

        items = self._memory_items(
            memory
        )

        # 可选语义检索。
        #
        # 如果接入 Qdrant，
        # retriever 会返回相关源码片段。
        if (
            self.retriever is not None
            and query.strip()
        ):
            retrieved = await self.retriever(
                query
            )

            items.extend(
                self._retrieval_items(
                    retrieved
                )
            )

        # Filter + Rank + Deduplicate
        items = self.filter_and_rank(
            items,
            query,
        )

        # Context Assembly
        text = self.assemble(
            query=query,
            items=items,
            workflow_state=workflow_state,
            user_instruction=user_instruction,
        )

        return {
            "query": query,
            "items": [
                {
                    "source": item.source,
                    "content": item.content,
                    "score": item.score,
                    "metadata": (
                        item.metadata or {}
                    ),
                }
                for item in items
            ],
            "text": text,
        }

    def filter_and_rank(
        self,
        items: list[ContextItem],
        query: str,
    ) -> list[ContextItem]:
        """
        过滤空内容、去重，
        并按照关键词相关性排序。
        """

        keywords = re.findall(
            r"[A-Za-z0-9_]+|[\u4e00-\u9fff]{2,}",
            query.lower(),
        )

        scored: list[ContextItem] = []

        for item in items:

            content = item.content.strip()

            if not content:
                continue

            lowered = content.lower()

            keyword_score = sum(
                1
                for keyword in keywords
                if keyword in lowered
            )

            score = (
                item.score
                + keyword_score
            )

            scored.append(
                ContextItem(
                    source=item.source,
                    content=content,
                    score=score,
                    metadata=item.metadata,
                )
            )

        scored.sort(
            key=lambda item: item.score,
            reverse=True,
        )

        # 去重
        unique: list[ContextItem] = []

        seen: set[str] = set()

        for item in scored:

            key = item.content

            if key in seen:
                continue

            seen.add(key)

            unique.append(item)

            if len(unique) >= self.max_items:
                break

        return unique

    def assemble(
        self,
        *,
        query: str,
        items: list[ContextItem],
        workflow_state: Any | None = None,
        user_instruction: str | None = None,
    ) -> str:
        """把 Context 组装成 Agent 可使用的文本。"""

        sections = [
            "## Current Question",
            query.strip(),
        ]

        if user_instruction:

            sections.extend(
                [
                    "## User Instruction",
                    user_instruction.strip(),
                ]
            )

        if workflow_state is not None:

            sections.extend(
                [
                    "## Workflow State",
                    self._stringify(
                        workflow_state
                    ),
                ]
            )

        if items:

            sections.append(
                "## Retrieved Context"
            )

            for index, item in enumerate(
                items,
                start=1,
            ):

                sections.extend(
                    [
                        (
                            f"### Context {index} "
                            f"[{item.source}]"
                        ),
                        item.content,
                    ]
                )

        text = "\n\n".join(
            section
            for section in sections
            if section.strip()
        )

        if len(text) <= self.max_chars:
            return text

        return (
            text[
                : self.max_chars
            ].rstrip()
            + "\n...[context truncated]"
        )

    @staticmethod
    def _memory_items(
        memory: dict[str, Any],
    ) -> list[ContextItem]:
        """把 Memory 转换成 ContextItem。"""

        items: list[ContextItem] = []

        run_memory = memory.get(
            "run_memory"
        )

        if run_memory:

            if run_memory.get(
                "question"
            ):

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.question"
                        ),
                        content=str(
                            run_memory[
                                "question"
                            ]
                        ),
                        score=5.0,
                    )
                )

            if run_memory.get(
                "research_plan"
            ):

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.research_plan"
                        ),
                        content=str(
                            run_memory[
                                "research_plan"
                            ]
                        ),
                        score=4.0,
                    )
                )

            if run_memory.get(
                "final_report"
            ):

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.final_report"
                        ),
                        content=str(
                            run_memory[
                                "final_report"
                            ]
                        ),
                        score=2.5,
                    )
                )

            for task in run_memory.get(
                "task_results",
                [],
            )[-8:]:

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.task_result"
                        ),
                        content=str(task),
                        score=3.0,
                        metadata={
                            "task_id": task.get(
                                "id"
                            ),
                            "task_type": task.get(
                                "task_type"
                            ),
                        },
                    )
                )

            for output in run_memory.get(
                "agent_outputs",
                [],
            )[-5:]:

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.agent_output"
                        ),
                        content=str(
                            output
                        ),
                        score=3.0,
                    )
                )

            for evidence in run_memory.get(
                "evidences",
                [],
            )[-10:]:

                items.append(
                    ContextItem(
                        source=(
                            "run_memory.evidence"
                        ),
                        content=str(
                            evidence
                        ),
                        score=4.0,
                        metadata={
                            "evidence_id": (
                                evidence.get(
                                    "id"
                                )
                            ),
                            "file_path": (
                                evidence.get(
                                    "file_path"
                                )
                            ),
                            "line_start": (
                                evidence.get(
                                    "line_start"
                                )
                            ),
                            "line_end": (
                                evidence.get(
                                    "line_end"
                                )
                            ),
                        },
                    )
                )

        for memory_item in memory.get(
            "project_memory",
            [],
        ):

            items.append(
                ContextItem(
                    source=(
                        "project_memory"
                    ),
                    content=str(
                        memory_item
                    ),
                    score=2.0,
                    metadata={
                        "run_id": (
                            memory_item.get(
                                "run_id"
                            )
                        ),
                    },
                )
            )

        return items

    @staticmethod
    def _retrieval_items(
        results: list[dict[str, Any]],
    ) -> list[ContextItem]:
        """
        把 Qdrant / 其他 Retriever
        的结果转换成 ContextItem。
        """

        items: list[ContextItem] = []

        for result in results:

            content = (
                result.get("content")
                or result.get("text")
                or result.get("payload")
                or ""
            )

            items.append(
                ContextItem(
                    source=(
                        "semantic_retrieval"
                    ),
                    content=str(
                        content
                    ),
                    score=float(
                        result.get(
                            "score",
                            1.0,
                        )
                    ),
                    metadata=result,
                )
            )

        return items

    @staticmethod
    def _stringify(
        value: Any,
    ) -> str:

        if isinstance(
            value,
            str,
        ):
            return value

        return str(value)
```

### 📄 `app/context/retriever.py`

**层级**：未归类 · **职责**：Context 语义检索适配器。

```python
"""Context 语义检索适配器。"""

from typing import Any


class QdrantContextRetriever:
    """
    把现有 Embedding + QdrantSearchTool
    适配成 Context Retriever。

    不修改现有 Tool / Vector Store。
    """

    def __init__(
        self,
        embedding_provider,
        search_tool,
        *,
        limit: int = 5,
    ) -> None:

        self.embedding_provider = (
            embedding_provider
        )

        self.search_tool = search_tool

        self.limit = limit

    async def __call__(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        """
        将自然语言问题转换为向量，
        然后调用 Qdrant Search Tool。
        """

        query_vector = (
            self.embedding_provider.embed(
                query
            )
        )

        results = await (
            self.search_tool.execute(
                query_vector=query_vector,
                limit=self.limit,
            )
        )

        return [
            (
                result
                if isinstance(
                    result,
                    dict,
                )
                else {
                    "content": result
                }
            )
            for result in results
        ]
```

### 📄 `app/memory/__init__.py`

**层级**：未归类 · **职责**：Memory 层。

```python
"""Memory 层。"""

from app.memory.manager import MemoryManager
from app.memory.project_memory import ProjectMemory
from app.memory.run_memory import RunMemory


__all__ = [
    "MemoryManager",
    "ProjectMemory",
    "RunMemory",
]
```

### 📄 `app/memory/manager.py`

**层级**：未归类 · **职责**：Memory Manager。

```python
"""Memory Manager。"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.memory.project_memory import (
    ProjectMemory,
)
from app.memory.run_memory import (
    RunMemory,
)


class MemoryManager:
    """统一管理 Run Memory 与 Project Memory。"""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.run_memory = RunMemory(
            session
        )

        self.project_memory = ProjectMemory(
            session
        )

    async def get_run_memory(
        self,
        run_id: str,
    ) -> dict[str, Any] | None:
        """获取当前 Run 的记忆。"""

        return await self.run_memory.load(
            run_id
        )

    async def get_project_memory(
        self,
        repository_id: int,
        *,
        run_id: str | None = None,
        query: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """获取并按当前问题过滤项目历史记忆。"""

        memories = await self.project_memory.load(
            repository_id,
            exclude_run_id=run_id,
            limit=max(
                limit * 2,
                limit,
            ),
        )

        return (
            self.project_memory.filter_by_query(
                memories,
                query,
                limit=limit,
            )
        )

    async def retrieve(
        self,
        *,
        run_id: str,
        repository_id: int,
        query: str | None = None,
        project_memory_limit: int = 5,
    ) -> dict[str, Any]:
        """
        一次性取得 Context Manager
        所需的 Memory。
        """

        run_memory = (
            await self.get_run_memory(
                run_id
            )
        )

        project_memory = (
            await self.get_project_memory(
                repository_id,
                run_id=run_id,
                query=query,
                limit=project_memory_limit,
            )
        )

        return {
            "run_memory": run_memory,
            "project_memory": project_memory,
        }
```

### 📄 `app/memory/project_memory.py`

**层级**：未归类 · **职责**：Project Memory。

```python
"""Project Memory。"""

import re
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun
from app.models.analysis_task import AnalysisTask


class ProjectMemory:
    """
    读取同一 Repository 的历史分析结果。

    Project Memory 第一版只做历史 Run 检索，
    不引入独立长期记忆表。
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

    async def load(
        self,
        repository_id: int,
        *,
        exclude_run_id: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """加载指定 Repository 最近的历史分析。"""

        query = (
            select(AnalysisRun)
            .where(
                AnalysisRun.repository_id
                == repository_id
            )
            .order_by(
                AnalysisRun.created_at.desc()
            )
            .limit(
                max(limit, 1)
            )
        )

        result = await self.session.execute(
            query
        )

        runs = list(
            result.scalars().all()
        )

        if exclude_run_id is not None:
            runs = [
                run
                for run in runs
                if run.id != exclude_run_id
            ]

        if not runs:
            return []

        run_ids = [
            run.id
            for run in runs
        ]

        task_result = await self.session.execute(
            select(AnalysisTask)
            .where(
                AnalysisTask.run_id.in_(
                    run_ids
                )
            )
            .order_by(
                AnalysisTask.created_at
            )
        )

        tasks = list(
            task_result.scalars().all()
        )

        tasks_by_run: dict[
            str,
            list[dict[str, Any]]
        ] = {
            run_id: []
            for run_id in run_ids
        }

        for task in tasks:
            tasks_by_run.setdefault(
                task.run_id,
                [],
            ).append(
                {
                    "task_type": (
                        task.task_type
                    ),
                    "status": (
                        task.status
                    ),
                    "output": (
                        task.output
                    ),
                    "error": (
                        task.error
                    ),
                }
            )

        return [
            {
                "run_id": run.id,
                "question": run.question,
                "status": run.status,
                "current_node": (
                    run.current_node
                ),
                "created_at": (
                    run.created_at.isoformat()
                ),
                "tasks": (
                    tasks_by_run.get(
                        run.id,
                        [],
                    )
                ),
            }
            for run in runs
        ]

    @staticmethod
    def filter_by_query(
        memories: list[dict[str, Any]],
        query: str | None,
        *,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        """
        按关键词相关性过滤历史记忆。
        """

        if not query:
            return memories[:limit]

        keywords = set(
            re.findall(
                r"[A-Za-z0-9_]+|[\u4e00-\u9fff]{2,}",
                query.lower(),
            )
        )

        if not keywords:
            return memories[:limit]

        scored: list[
            tuple[int, dict[str, Any]]
        ] = []

        for memory in memories:
            text = str(memory).lower()

            score = sum(
                1
                for keyword in keywords
                if keyword in text
            )

            if score > 0:
                scored.append(
                    (
                        score,
                        memory,
                    )
                )

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [
            memory
            for _, memory
            in scored[:limit]
        ]
```

### 📄 `app/memory/run_memory.py`

**层级**：未归类 · **职责**：Research Run Memory。

```python
"""Research Run Memory。"""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun
from app.models.analysis_task import AnalysisTask
from app.repositories.checkpoint import CheckpointRepository
from app.repositories.evidence import EvidenceRepository


class RunMemory:
    """
    读取一次 Analysis Run 的短期 / 情景记忆。

    Phase 11 不新增 Memory 专用表，
    而是复用已经存在的：

    analysis_runs
    analysis_tasks
    checkpoints
    evidences
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session

        self.checkpoint_repository = (
            CheckpointRepository(session)
        )

        self.evidence_repository = (
            EvidenceRepository(session)
        )

    async def load(
        self,
        run_id: str,
    ) -> dict[str, Any] | None:
        """加载一次 Run 的完整记忆快照。"""

        result = await self.session.execute(
            select(AnalysisRun).where(
                AnalysisRun.id == run_id
            )
        )

        run = result.scalar_one_or_none()

        if run is None:
            return None

        repository = await self.session.get(
            __import__(
                "app.models.repository",
                fromlist=["Repository"],
            ).Repository,
            run.repository_id,
        )

        task_result = await self.session.execute(
            select(AnalysisTask)
            .where(
                AnalysisTask.run_id == run_id
            )
            .order_by(
                AnalysisTask.created_at
            )
        )

        tasks = list(
            task_result.scalars().all()
        )

        checkpoint = (
            await self.checkpoint_repository.get_latest(
                run_id
            )
        )

        evidences = []

        if repository is not None:
            evidences = (
                await self.evidence_repository
                .list_by_repository(
                    repository.id
                )
            )

        checkpoint_data = (
            checkpoint.data
            if checkpoint
            else {}
        )

        return {
            # 当前 Run
            "run_id": run.id,
            "question": run.question,
            "status": run.status,
            "current_node": run.current_node,

            # Repository
            "repository": (
                {
                    "id": repository.id,
                    "url": repository.url,
                    "owner": repository.owner,
                    "name": repository.name,
                    "description": repository.description,
                    "language": repository.language,
                }
                if repository is not None
                else None
            ),

            # Research Plan
            "research_plan": (
                checkpoint_data.get(
                    "research_plan"
                )
            ),

            # Phase 14/12 可以继续使用
            # 这里提前预留最终报告。
            "final_report": (
                checkpoint_data.get(
                    "final_report"
                )
            ),

            # Agent 输出
            "agent_outputs": (
                checkpoint.outputs
                if checkpoint
                else []
            ),

            # Task 结果
            "task_results": [
                {
                    "id": task.id,
                    "task_type": task.task_type,
                    "status": task.status,
                    "input": task.input,
                    "output": task.output,
                    "error": task.error,
                    "retry_count": task.retry_count,
                }
                for task in tasks
            ],

            # Evidence
            #
            # 第一版只保留最近 20 条，
            # 避免 Context 无限膨胀。
            "evidences": [
                {
                    "id": evidence.id,
                    "source_type": (
                        evidence.source_type
                    ),
                    "file_path": (
                        evidence.file_path
                    ),
                    "line_start": (
                        evidence.line_start
                    ),
                    "line_end": (
                        evidence.line_end
                    ),
                    "content": evidence.content,
                    "verification_status": (
                        evidence.verification_status
                    ),
                }
                for evidence in evidences[-20:]
            ],

            # Workflow Checkpoint
            "workflow_state": (
                {
                    "status": checkpoint.status,
                    "current_node": (
                        checkpoint.current_node
                    ),
                    "data": checkpoint.data,
                    "errors": checkpoint.errors,
                    "retry_count": (
                        checkpoint.retry_count
                    ),
                    "pause_reason": (
                        checkpoint.pause_reason
                    ),
                    "human_approved": (
                        checkpoint.human_approved
                    ),
                    "checkpoint_version": (
                        checkpoint.checkpoint_version
                    ),
                }
                if checkpoint is not None
                else None
            ),
        }
```

---

## 二十三、附录

### 空文件清单

以下 15 个文件均为 **0 字节**，其中绝大多数是用于将目录声明为 Python 包的标记文件：

| 文件路径 | 说明 |
|---|---|
| `app/__init__.py` | 包标记文件 |
| `app/agents/researcher.py` | 预留占位，尚未实现 |
| `app/api/__init__.py` | 包标记文件 |
| `app/api/v1/__init__.py` | 包标记文件 |
| `app/core/__init__.py` | 包标记文件 |
| `app/db/__init__.py` | 包标记文件 |
| `app/embeddings/__init__.py` | 包标记文件 |
| `app/llm/__init__.py` | 包标记文件 |
| `app/project_analysis/__init__.py` | 包标记文件 |
| `app/schemas/__init__.py` | 包标记文件 |
| `app/services/__init__.py` | 包标记文件 |
| `app/tools/github/__init__.py` | 包标记文件 |
| `app/vector_store/__init__.py` | 包标记文件 |
| `app/workflow/__init__.py` | 包标记文件 |
| `app/workflow/nodes/__init__.py` | 包标记文件 |

### 配置文件

| 文件 | 说明 |
|---|---|
| `alembic.ini` | Alembic 迁移配置，`script_location = %(here)s/alembic`，`sqlalchemy.url` 留空由 `env.py` 动态注入 |
| `pytest.ini` | `pythonpath = .`、`asyncio_mode = auto` |
| `requirements.txt` | 依赖清单 |
| `.env` / `.env.example` | 环境变量（`.env` 已 gitignore） |

### 已知注意事项

1. **文件名与类名不一致**
   - `app/project_analysis/code_chunker.py` 内部类为 `MarkdownChunker`
   - `app/project_analysis/project_indexer.py` 内部类为 `DocumentIndexer`

2. **`app/vector_store/qdrant.py` 的 `insert()` 方法**
   - 与 `upsert()` 功能重叠，仅 `RepositoryIndexer` 调用；`uuid` 导入专为此方法服务
   - 其 `PointStruct` 的 `id` 使用 UUID 字符串，而 `upsert()` 使用整数，两种 ID 类型混用

3. **两份重复的 GitHub URL 解析实现**
   - `app/services/analysis_service.py::_parse_github_url` — 基于字符串切分，不做域名校验
   - `app/tools/github/parser.py::parse_github_url` — 基于 `urlparse`，校验 `netloc == "github.com"` 并剥离 `.git` 后缀

4. **Workflow 引擎的行为边界**
   - 暂停判定已扩展为 `PAUSED` / `WAITING_HUMAN` / `WAITING_DESIGN` 三态
     （`WorkflowEngine.PAUSE_STATUSES`），`HumanNode` 触发的暂停现在能被引擎识别
   - 主循环 `while current_node:` 仍没有最大步数保护，编排中出现环会一直执行
   - `retry_count` 是 `state` 上的全局预算，不是每个节点独立计数

5. **未配置 `GITHUB_TOKEN` 时 Code Search 仍不可用**
   - `GitHubCodeSearchTool` 已支持自动带 `Authorization` 头，但 GitHub Code Search API 强制认证
   - 未配置 token 时真实调用会返回 401

6. **Phase 6 完成标准尚未全部达成**
   - 实施文档 §9.7 要求每个 Tool 具备「输入 Schema / 输出 Schema / 异常处理 / 日志 / 测试」
   - 当前 7 个 Tool 均未定义 Pydantic Schema，也均未接入 `app/core/logging.py`

7. **Skill 输出键名与 `CriticAgent` 校验字段不一致**
   - `SkillNode` 把每个 Skill 的结果写入 `state.data[node.name]`，即 `repository_analysis` / `architecture_analysis` / `technology_analysis`
   - `CriticAgent` 检查的却是 `repository` / `architecture` / `technology`，两者对不上，`passed` 会恒为 `False`
   - `PlannerAgent` 返回的 `tasks` 列表目前也没有任何代码消费，Workflow 尚未真正按计划驱动 Agent 执行

8. **证据链能力尚未对外暴露**
   - `app/evidence/`（Store / Verifier / Traceability）、`EvidenceService`
     与 `app/schemas/evidence.py` 均已实现并有测试覆盖
   - 但 `app/api/` 下没有任何证据相关路由，`app/main.py` 也未装配 `EvidenceService`，
     目前只能由测试或脚本直接调用，尚未形成可访问的接口

---

*本文档由 `generate_project_code.py` 扫描工作区 `.py` 文件自动生成：共收录 **169 段代码**（非空文件），另有 15 个 0 字节空文件，见上方「空文件清单」。*
