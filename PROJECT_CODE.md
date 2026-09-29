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
│   │   ├── comparison_agent.py
│   │   ├── critic_agent.py
│   │   ├── evidence_analysis_agent.py
│   │   ├── planner_agent.py
│   │   ├── repository_analysis_agent.py
│   │   ├── researcher.py
│   │   └── technology_analysis_agent.py
│   ├── api/                                                         # ── API 层 ──
│   │   ├── v1/                                                      # v1 路由
│   │   │   ├── __init__.py                                          # (空)
│   │   │   ├── analysis.py
│   │   │   └── comparison.py
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
│   │   ├── code_chunker.py
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
│   │   ├── comparison.py
│   │   ├── error.py
│   │   └── evidence.py
│   ├── services/                                                    # ── 业务服务层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis_result_service.py
│   │   ├── analysis_service.py
│   │   ├── analysis_workflow.py
│   │   ├── comparison_service.py
│   │   ├── evidence_service.py
│   │   └── repository_service.py
│   ├── skills/                                                      # ── Skill 能力层 ──
│   │   ├── __init__.py
│   │   ├── architecture_analysis_skill.py
│   │   ├── base.py
│   │   ├── evidence_analysis_skill.py
│   │   ├── registry.py
│   │   ├── report_generation_skill.py
│   │   ├── repository_analysis_skill.py
│   │   └── technology_analysis_skill.py
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
│   ├── 799049b1-3d51-4c2f-bbe5-81930ce59a23_analysis.md
│   ├── a57edd4e-59b1-4aa9-a889-d4d10dfbc0d5_analysis.md
│   ├── caaaf822-e1ee-42f8-a52a-3b1eac1434bb_analysis.md
│   └── d1d71c3e-a9b6-4073-8d3d-bbbfe0b11005_analysis.md
├── test_reports/                                                    # 测试产生的报告输出目录
│   └── test.md
├── tests/                                                           # ── 测试层 ──
│   ├── test_agent_registry.py
│   ├── test_agent_runtime.py
│   ├── test_analysis_api.py
│   ├── test_analysis_result.py
│   ├── test_chunker.py
│   ├── test_comparison_agent.py
│   ├── test_comparison_api.py
│   ├── test_comparison_real_runmemory_schema.py
│   ├── test_comparison_service.py
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
│   ├── test_memory.py
│   ├── test_mysql_query_tool.py
│   ├── test_phase10.py
│   ├── test_phase12.py
│   ├── test_pre_phase12_integration.py
│   ├── test_pre_phase12_structure.py
│   ├── test_qdrant.py
│   ├── test_qdrant_search_tool.py
│   ├── test_report_export_tool.py
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

from fastapi import FastAPI

from app.api.v1.analysis import (
    router as analysis_router,
)
from app.api.v1.comparison import (
    router as comparison_router,
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


# 注册 Comparison API。
app.include_router(
    comparison_router,
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
    项目根路径。
    """

    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
    }
```

## 三、API 层

HTTP 路由定义，负责接收请求、注入数据库 Session、调用 Service

### 📄 `app/api/v1/analysis.py`

**层级**：API 层 · **职责**：Analysis 相关的 HTTP 路由定义，负责接收请求、注入数据库 Session、调用 Service

```python
"""Analysis API 路由。"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.analysis import (
    AnalysisCreateRequest,
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
```

### 📄 `app/api/__init__.py`

**层级**：API 层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/api/v1/__init__.py`

**层级**：API 层 · **职责**：（未标注）

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/api/v1/comparison.py`

**层级**：API 层 · **职责**：Comparison API 路由。

```python
"""Comparison API 路由。"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.comparison import (
    ComparisonCreateRequest,
    ComparisonResponse,
)
from app.services.comparison_service import (
    comparison_service,
)


router = APIRouter(
    prefix="/comparison",
    tags=["Comparison"],
)


@router.post(
    "",
    response_model=ComparisonResponse,
)
async def create_comparison(
    request: ComparisonCreateRequest,
    session: AsyncSession = Depends(
        get_db
    ),
) -> ComparisonResponse:
    """
    比较两个已经完成的项目分析结果。
    """

    return await (
        comparison_service.create_comparison(
            session,
            request,
        )
    )
```

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
Workflow执行结果标准化。

用于:
    Workflow
        ↓
    Report
        ↓
    Comparison
"""

from typing import Any

from pydantic import BaseModel, Field


class ProjectOverview(BaseModel):
    """
    项目概览。
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



class AgentResult(BaseModel):
    """
    Agent分析结果。
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
    Phase12标准分析结果。
    """

    run_id: str


    project_overview: ProjectOverview = Field(
        default_factory=ProjectOverview
    )


    technology_stack: TechnologyStack = Field(
        default_factory=TechnologyStack
    )


    agents: list[AgentResult] = Field(
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

### 📄 `app/schemas/comparison.py`

**层级**：数据契约层 · **职责**：Comparison API 数据契约。

```python
"""
Comparison API 数据契约。
"""

from typing import Any

from pydantic import BaseModel, Field


class ComparisonCreateRequest(BaseModel):
    """创建多项目比较请求。"""

    run_ids: list[str] = Field(
        ...,
        min_length=2,
        max_length=2,
        description=(
            "两个已经完成的 Analysis Run ID"
        ),
    )


class ComparisonProjectResponse(BaseModel):
    """比较项目摘要。"""

    run_id: str
    repository_id: int | None = None
    repository_url: str | None = None
    repository_name: str | None = None
    status: str


class ComparisonResponse(BaseModel):
    """多项目比较结果。"""

    comparison_id: str

    status: str

    evidence_based: bool

    projects: list[
        ComparisonProjectResponse
    ]

    comparison: dict[str, Any]
```

## 五、业务服务层（Services）

业务编排：校验入参、组合 DAO 与工具层、掌控事务边界

### 📄 `app/services/analysis_service.py`

**层级**：业务服务层（Services） · **职责**：Analysis 任务的业务编排——校验 URL、创建或复用 Repository、创建 Analysis Run 并提交事务

```python
"""Analysis 任务业务逻辑。"""

from uuid import uuid4

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
    AnalysisReportResponse,
    AnalysisResponse,
)
from app.services.analysis_workflow import (
    AnalysisWorkflowRunner,
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
        """解析 GitHub owner/repository。"""

        path = (
            repo_url
            .rstrip("/")
            .split("/")
        )

        if len(path) < 2:
            raise ValidationError(
                "Invalid GitHub repository URL."
            )

        owner = path[-2]
        name = path[-1]

        if name.endswith(".git"):
            name = name[:-4]

        if not owner or not name:
            raise ValidationError(
                "Invalid GitHub repository URL."
            )

        return owner, name


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

负责将 Workflow State
转换成标准 AnalysisResult。
"""

from typing import Any


from app.schemas.analysis_result import (
    AnalysisResult,
    AgentResult,
    ProjectOverview,
    TechnologyStack,
)



class AnalysisResultService:
    """
    构建标准分析结果。
    """


    def build(
        self,
        run_id: str,
        data: dict[str, Any],
    ) -> AnalysisResult:
        """
        Workflow State
        ->
        AnalysisResult
        """


        repository = (
            data.get(
                "repository",
                {}
            )
        )


        agents = []


        agent_outputs = (
            data.get(
                "agent_outputs",
                {}
            )
        )


        for name, output in (
            agent_outputs.items()
        ):

            if not isinstance(
                output,
                dict,
            ):
                continue


            agents.append(
                AgentResult(
                    agent_name=name,

                    summary=(
                        output.get(
                            "summary"
                        )
                    ),

                    facts=(
                        output.get(
                            "facts",
                            []
                        )
                    ),

                    evidence_ids=(
                        output.get(
                            "evidence_ids",
                            []
                        )
                    ),
                )
            )


        technology = (
            data.get(
                "technology_stack",
                {}
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
                technology.get(
                    "languages",
                    []
                ),

                frameworks=
                technology.get(
                    "frameworks",
                    []
                ),

                databases=
                technology.get(
                    "databases",
                    []
                ),

                tools=
                technology.get(
                    "tools",
                    []
                ),
            ),


            agents=agents,


            workflow={
                "state":
                    data.get(
                        "workflow_state"
                    )
            },


            skills=data.get(
                "skills",
                []
            ),


            tools=data.get(
                "tools",
                []
            ),


            rag=data.get(
                "rag",
                {}
            ),


            memory=data.get(
                "memory",
                {}
            ),


            database=data.get(
                "database",
                {}
            ),


            evidence=data.get(
                "evidences",
                []
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

from app.agents.agent_registry import (
    create_agent_registry,
)
from app.context.manager import (
    ContextManager,
)
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
from app.tools.mysql_query_tool import (
    MySQLQueryTool,
)
from app.tools.qdrant_search_tool import (
    QdrantSearchTool,
)
from app.tools.report_export_tool import (
    ReportExportTool,
)
from app.skills.registry import (
    create_skill_registry,
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
        """获取最终报告。"""

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:
            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        return state.data.get(
            "final_report"
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

### 📄 `app/services/comparison_service.py`

**层级**：业务服务层 · **职责**：多项目比较业务服务。

```python
"""
多项目比较业务服务。

职责：

API
 ↓
ComparisonService
 ↓
AnalysisRun / RunMemory
 ↓
ComparisonAgent
"""
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.comparison_agent import (
    ComparisonAgent,
)
from app.core.exceptions import ValidationError
from app.memory.run_memory import RunMemory
from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.schemas.comparison import (
    ComparisonCreateRequest,
    ComparisonProjectResponse,
    ComparisonResponse,
)


class ComparisonService:
    """负责多项目分析结果比较。"""

    comparison_agent_factory = (
        ComparisonAgent
    )

    async def create_comparison(
        self,
        session: AsyncSession,
        request: ComparisonCreateRequest,
    ) -> ComparisonResponse:
        """比较两个已经完成的 Analysis Run。"""

        run_ids = [
            run_id.strip()
            for run_id in request.run_ids
        ]

        if len(run_ids) != 2:
            raise ValidationError(
                "Exactly two analysis run IDs "
                "are required."
            )

        if run_ids[0] == run_ids[1]:
            raise ValidationError(
                "The two analysis runs "
                "must be different."
            )

        run_repository = (
            AnalysisRunRepository(
                session
            )
        )

        runs = []

        for run_id in run_ids:
            run = await (
                run_repository.get_by_id(
                    run_id
                )
            )

            if run is None:
                raise ValidationError(
                    f"Analysis run not found: "
                    f"{run_id}"
                )

            if run.status != "COMPLETED":
                raise ValidationError(
                    "Only completed analysis runs "
                    "can be compared: "
                    f"{run_id} "
                    f"has status {run.status}."
                )

            runs.append(run)

        if (
            runs[0].repository_id
            == runs[1].repository_id
        ):
            raise ValidationError(
                "The two analysis runs "
                "must belong to different repositories."
            )

        memory = RunMemory(
            session
        )

        project_a = await memory.load(
            runs[0].id
        )

        project_b = await memory.load(
            runs[1].id
        )

        if project_a is None:
            raise ValidationError(
                f"Analysis memory not found: "
                f"{runs[0].id}"
            )

        if project_b is None:
            raise ValidationError(
                f"Analysis memory not found: "
                f"{runs[1].id}"
            )

        agent = (
            self.comparison_agent_factory(
                skill_registry=None
            )
        )

        result = await agent.execute(
            context=None,
            input_data={
                "project_a": project_a,
                "project_b": project_b,
            },
        )

        projects = [
            ComparisonProjectResponse(
                run_id=project.get(
                    "run_id"
                ),
                repository_id=project.get(
                    "repository_id"
                ),
                repository_url=project.get(
                    "repository_url"
                ),
                repository_name=project.get(
                    "repository_name"
                ),
                status=project.get(
                    "status"
                ),
            )
            for project in result.get(
                "projects",
                [],
            )
        ]

        return ComparisonResponse(
            comparison_id=str(
                uuid4()
            ),
            status="COMPLETED",
            evidence_based=bool(
                result.get(
                    "evidence_based",
                    False,
                )
            ),
            projects=projects,
            comparison=result.get(
                "comparison",
                {},
            ),
        )


comparison_service = ComparisonService()
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

from sqlalchemy import (
    delete,
    desc,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.checkpoint import Checkpoint
from app.workflow.state import WorkflowState


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
        """保存 WorkflowState 快照。"""

        checkpoint = Checkpoint(
            run_id=state.run_id,
            checkpoint_version=(
                state.checkpoint_version
            ),
            status=state.status,
            current_node=state.current_node,
            state_data=state.data,
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

    async def get_latest(
        self,
        run_id: str,
    ) -> WorkflowState | None:
        """获取指定 run 的最新 Checkpoint。"""

        result = await self.session.execute(
            select(Checkpoint)
            .where(
                Checkpoint.run_id == run_id
            )
            .order_by(
                desc(
                    Checkpoint.checkpoint_version
                )
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
    LLM_PROVIDER: str = "deepseek"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "deepseek-chat"

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

**层级**：Workflow 节点层 · **职责**：最终报告生成节点。

```python
"""
最终报告生成节点。

Phase12:
    Workflow State
        ↓
    AnalysisResult
        ↓
    ReportGenerationSkill
        ↓
    final_report
"""


from .base import BaseNode

from app.services.analysis_result_service import (
    analysis_result_service,
)


class FinalizerNode(BaseNode):
    """
    最终报告生成节点。
    """

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
        """
        生成最终项目分析报告。

        Phase12新增:

        state.data
            ↓
        AnalysisResult
            ↓
        Report
        """


        # ==========================
        # 1. 构建标准 AnalysisResult
        # ==========================

        analysis_result = (
            analysis_result_service.build(
                run_id=state.run_id,
                data=state.data,
            )
        )


        # 保存结构化分析结果

        state.data[
            "analysis_result"
        ] = analysis_result.model_dump()



        # ==========================
        # 2. 构造报告输入
        # ==========================

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


        # ==========================
        # 3. 生成 Markdown 报告
        # ==========================

        result = await self.skill.execute(
            context=context,
            input_data=report_input,
        )


        # ==========================
        # 4. 保留旧字段兼容
        # ==========================

        state.data[
            "final_report"
        ] = result


        state.outputs.append(
            result
        )


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

            # 保存 Agent 级别输出。
            state.data[
                agent_name
            ] = result

            # 合并结构化输出。
            if isinstance(
                result,
                dict,
            ):
                state.data.update(
                    result
                )

            state.outputs.append(
                result
            )

            executed_tasks.append(
                agent_name
            )

        state.data[
            "executed_tasks"
        ] = executed_tasks

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
"""

from app.agents.base import BaseAgent


class PlannerAgent(
    BaseAgent
):
    """项目分析规划 Agent。"""

    name = "planner_agent"

    description = (
        "Create a research plan for GitHub "
        "project analysis."
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        """生成第一版项目分析计划。"""

        tasks = [
            "repository_analysis_agent",
            "architecture_analysis_agent",
            "technology_analysis_agent",
            "evidence_analysis_agent",
            "critic_agent",
        ]

        research_plan = {
            "plan_version": 1,
            "analysis_type": (
                "github_agent_project"
            ),
            "question": input_data.get(
                "question"
            ),
            "tasks": tasks,
            "evidence_required": True,
        }

        return {
            "tasks": tasks,
            "research_plan": research_plan,
        }
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

    async def execute(
        self,
        context,
        input_data,
    ):
        errors = []

        required_fields = {
            "repository": [
                "repository",
                "repository_analysis",
                "repository_analysis_agent",
            ],
            "architecture": [
                "architecture",
                "architecture_analysis",
                "architecture_analysis_agent",
            ],
            "technology": [
                "technology",
                "technology_analysis",
                "technology_analysis_agent",
                "technology_stack",
            ],
        }

        for logical_name, aliases in (
            required_fields.items()
        ):
            if not any(
                alias in input_data
                for alias in aliases
            ):
                errors.append(
                    f"{logical_name} missing"
                )

        return {
            "passed": not errors,
            "errors": errors,
        }
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
from app.agents.comparison_agent import (
    ComparisonAgent,
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
        ComparisonAgent(
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

### 📄 `app/agents/comparison_agent.py`

**层级**：Agent 层 · **职责**：Comparison Agent。

```python
"""
Comparison Agent。

负责基于两个已经完成的 Analysis Run
以及对应 Evidence，生成多项目比较结果。

Phase 13 不让 LLM 凭空生成结论，
只比较 Analysis Result 中已经存在的结构化事实。

真实数据来源（RunMemory.load() 的顶层结构）：

    run_id / status / current_node / question
    repository / research_plan / final_report
    agent_outputs / task_results / evidences / workflow_state

注意：

    project["analysis"] 这个结构在真实数据中并不存在，
    因此所有维度都必须从上面这些真实字段读取。

各维度真实数据来源：

    agent            workflow_state.data.executed_tasks
    workflow         workflow_state.data.research_plan
    rag              workflow_state.data.technology_stack.embedding
    database         workflow_state.data.technology_stack.database
    deployment       workflow_state.data.technology_stack.deployment
    code_complexity  workflow_state.data.repository（language / size）
                     + architecture_analysis_agent（files / modules）
                     + technology_stack.source_files

    skill / tool / memory / extension：

        当前 Analysis Workflow 并未提取被分析项目的
        对应结构，真实数据不存在，
        因此返回 NOT_AVAILABLE 并给出明确原因，
        而不是因为字段名写错而“看起来没有数据”。

Evidence：

    引用必须来自 project["evidences"][*]["id"]（真实 Evidence ID）。
    归因规则是确定性的：

        维度值中的字符串叶子值会被拆成 token，
        若某个 token 出现在某条 Evidence 的 content 中，
        则该 Evidence 被引用。

    只取字符串叶子值、不取 dict key，
    是为了避免 JSON 结构名（tasks / question 等）
    与 Evidence 内容产生巧合匹配。

    该规则不会生成、不会猜测、不会以下标冒充 Evidence ID。
"""

import re

from dataclasses import dataclass
from typing import Any

from app.agents.base import BaseAgent


@dataclass(frozen=True)
class DimensionExtraction:
    """单个项目在某个维度上的真实数据提取结果。"""

    # 维度值
    value: Any = None

    # 真实来源字段路径，便于审计
    source: str | None = None

    # 真实数据是否存在
    available: bool = False

    # 不可用原因（available 为 False 时说明是数据缺失）
    reason: str | None = None


class ComparisonAgent(BaseAgent):
    """多项目比较 Agent。"""

    name = "comparison_agent"

    description = (
        "Compare multiple GitHub project "
        "analysis results using evidence."
    )

    DIMENSIONS = (
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
    )

    # 维度值中可参与 Evidence 归因的 token。
    #
    # 至少 4 个字符，避免过短的通用词造成巧合匹配。
    _TOKEN_PATTERN = re.compile(
        r"[A-Za-z][A-Za-z0-9_.\-]{3,}"
    )

    async def execute(
        self,
        context,
        input_data,
    ) -> dict[str, Any]:
        """
        比较两个项目。

        input_data:
            {
                "project_a": {...},
                "project_b": {...}
            }

        其中 project 必须是 RunMemory.load() 的真实返回结构。
        """

        project_a = input_data.get(
            "project_a"
        )

        project_b = input_data.get(
            "project_b"
        )

        if not isinstance(project_a, dict):
            raise ValueError(
                "project_a must be a dictionary."
            )

        if not isinstance(project_b, dict):
            raise ValueError(
                "project_b must be a dictionary."
            )

        comparison = {}

        for dimension in self.DIMENSIONS:
            comparison[dimension] = (
                self._compare_dimension(
                    project_a,
                    project_b,
                    dimension,
                )
            )

        return {
            "comparison": comparison,
            "projects": [
                self._project_summary(
                    project_a
                ),
                self._project_summary(
                    project_b
                ),
            ],
            # 只有比较结果确实引用了真实 Evidence 时
            # evidence_based 才为 True。
            "evidence_based": (
                self._is_evidence_based(
                    comparison
                )
            ),
        }

    @staticmethod
    def _is_evidence_based(
        comparison: dict[str, Any],
    ) -> bool:
        """
        根据实际 Evidence 引用情况计算 evidence_based。

        不能因为 API 成功返回而置 True，
        也不能因为有 dimensions 而置 True。
        """

        for result in comparison.values():

            if not isinstance(result, dict):
                continue

            for side in (
                "project_a",
                "project_b",
            ):

                value = result.get(side)

                if not isinstance(value, dict):
                    continue

                if value.get("evidence_ids"):
                    return True

        return False

    @classmethod
    def _compare_dimension(
        cls,
        project_a: dict[str, Any],
        project_b: dict[str, Any],
        dimension: str,
    ) -> dict[str, Any]:
        """比较单个维度。"""

        extraction_a = cls._extract_dimension(
            project_a,
            dimension,
        )

        extraction_b = cls._extract_dimension(
            project_b,
            dimension,
        )

        if (
            not extraction_a.available
            and not extraction_b.available
        ):
            relation = "NOT_AVAILABLE"

        elif (
            not extraction_a.available
            or not extraction_b.available
        ):
            relation = "ONE_SIDE_UNAVAILABLE"

        elif extraction_a.value == extraction_b.value:
            relation = "SAME"

        else:
            relation = "DIFFERENT"

        return {
            "relation": relation,

            # 真实来源字段，便于确认数据不是凭空产生的。
            "source": (
                extraction_a.source
                or extraction_b.source
            ),

            "project_a": cls._build_side(
                project_a,
                extraction_a,
            ),

            "project_b": cls._build_side(
                project_b,
                extraction_b,
            ),
        }

    @classmethod
    def _build_side(
        cls,
        project: dict[str, Any],
        extraction: DimensionExtraction,
    ) -> dict[str, Any]:
        """构建单侧比较结果。"""

        evidence_ids: list[str] = []

        if extraction.available:
            evidence_ids = (
                cls._attribute_evidence_ids(
                    project,
                    extraction.value,
                )
            )

        return {
            "value": extraction.value,
            "evidence_ids": evidence_ids,
            "available": extraction.available,
            "unavailable_reason": (
                extraction.reason
            ),
        }

    @classmethod
    def _extract_dimension(
        cls,
        project: dict[str, Any],
        dimension: str,
    ) -> DimensionExtraction:
        """
        从真实 Analysis Result 中提取某个维度。

        不进行主观推断：
        只读取真实存在的字段，
        读不到就返回 available=False 并说明原因。
        """

        data = cls._workflow_data(
            project
        )

        technology = data.get(
            "technology_stack"
        )

        if not isinstance(
            technology,
            dict,
        ):
            technology = None

        if dimension == "agent":
            return cls._extract_agent(data)

        if dimension == "workflow":
            return cls._extract_workflow(data)

        if dimension in {
            "rag",
            "database",
            "deployment",
        }:
            return cls._extract_technology(
                technology,
                dimension,
            )

        if dimension == "code_complexity":
            return cls._extract_code_complexity(
                data,
                technology,
            )

        return cls._unavailable_dimension(
            dimension
        )

    @staticmethod
    def _workflow_data(
        project: dict[str, Any],
    ) -> dict[str, Any]:
        """读取 workflow_state.data（真实业务数据所在位置）。"""

        workflow_state = project.get(
            "workflow_state"
        )

        if not isinstance(
            workflow_state,
            dict,
        ):
            return {}

        data = workflow_state.get(
            "data"
        )

        if not isinstance(
            data,
            dict,
        ):
            return {}

        return data

    @staticmethod
    def _extract_agent(
        data: dict[str, Any],
    ) -> DimensionExtraction:
        """Agent 维度：真实 Agent 执行列表。"""

        executed_tasks = data.get(
            "executed_tasks"
        )

        if (
            not isinstance(
                executed_tasks,
                list,
            )
            or not executed_tasks
        ):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    "executed_tasks。"
                ),
            )

        return DimensionExtraction(
            value={
                "count": len(executed_tasks),
                "agents": list(executed_tasks),
            },
            source=(
                "workflow_state.data."
                "executed_tasks"
            ),
            available=True,
        )

    @staticmethod
    def _extract_workflow(
        data: dict[str, Any],
    ) -> DimensionExtraction:
        """Workflow 维度：真实 Research Plan。"""

        research_plan = data.get(
            "research_plan"
        )

        if research_plan is None:
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    "research_plan。"
                ),
            )

        # research_plan["question"] 是本次分析请求，
        # 属于 Run 元数据，不是被分析项目的属性。
        # 若不剔除，两个项目只要提问不同
        # 就会让 workflow 维度被判为 DIFFERENT。
        plan = research_plan

        if isinstance(
            research_plan,
            dict,
        ):
            plan = {
                key: value
                for key, value in (
                    research_plan.items()
                )
                if key != "question"
            }

        # 只使用 research_plan 本身。
        #
        # 不把 workflow_state.status / current_node
        # 放进维度值：它们是本次 Run 的执行状态，
        # 不是被分析项目的属性。
        # 例如 status="COMPLETED" 会让 token "completed"
        # 与 README Evidence 巧合匹配，
        # 从而产生看起来合理、实际无意义的 Evidence 引用。
        return DimensionExtraction(
            value=plan,
            source=(
                "workflow_state.data."
                "research_plan"
            ),
            available=True,
        )

    @staticmethod
    def _extract_technology(
        technology: dict[str, Any] | None,
        dimension: str,
    ) -> DimensionExtraction:
        """
        技术栈相关维度。

        rag 使用 technology_stack.embedding：
        该字段是 TechnologyAnalysisSkill 对
        向量库 / Embedding（qdrant / chromadb）
        的真实检测结果，是当前真实数据中
        与 RAG 最直接对应的字段。
        """

        key = {
            "rag": "embedding",
            "database": "database",
            "deployment": "deployment",
        }[dimension]

        if (
            technology is None
            or key not in technology
        ):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    f"technology_stack.{key}。"
                ),
            )

        return DimensionExtraction(
            value=technology.get(key),
            source=(
                "workflow_state.data."
                f"technology_stack.{key}"
            ),
            available=True,
        )

    @staticmethod
    def _extract_code_complexity(
        data: dict[str, Any],
        technology: dict[str, Any] | None,
    ) -> DimensionExtraction:
        """代码复杂度维度：仓库规模与架构分析结果。"""

        repository = data.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            repository = None

        architecture = data.get(
            "architecture_analysis_agent"
        )

        if not isinstance(
            architecture,
            dict,
        ):
            architecture = {}

        if (
            repository is None
            and not architecture
        ):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    "repository 与 "
                    "architecture_analysis_agent 数据。"
                ),
            )

        files = architecture.get(
            "files"
        )

        modules = architecture.get(
            "modules"
        )

        source_files = None

        if technology is not None:
            source_files = technology.get(
                "source_files"
            )

        return DimensionExtraction(
            value={
                "language": (
                    repository or {}
                ).get("language"),
                "size_kb": (
                    repository or {}
                ).get("size"),
                "file_count": (
                    len(files)
                    if isinstance(
                        files,
                        list,
                    )
                    else None
                ),
                "module_count": (
                    len(modules)
                    if isinstance(
                        modules,
                        list,
                    )
                    else None
                ),
                "source_files": source_files,
            },
            source=(
                "workflow_state.data.repository + "
                "architecture_analysis_agent + "
                "technology_stack.source_files"
            ),
            available=True,
        )

    @staticmethod
    def _unavailable_dimension(
        dimension: str,
    ) -> DimensionExtraction:
        """
        真实数据不存在时的显式结果。

        与“字段名写错导致读不到”区分开：
        这里是当前 Analysis Workflow
        确实没有提取被分析项目的该结构。
        """

        return DimensionExtraction(
            available=False,
            reason=(
                "当前 Analysis Workflow 未提取"
                "被分析项目的 "
                f"{dimension} 结构，"
                "真实数据不存在。"
            ),
        )

    @classmethod
    def _attribute_evidence_ids(
        cls,
        project: dict[str, Any],
        value: Any,
    ) -> list[str]:
        """
        把真实 Evidence 归因到维度值。

        Evidence ID 只能来自 project["evidences"][*]["id"]。
        """

        evidences = project.get(
            "evidences"
        )

        if not isinstance(
            evidences,
            list,
        ):
            return []

        tokens = cls._specific_tokens(
            value
        )

        if not tokens:
            return []

        evidence_ids: list[str] = []

        for evidence in evidences:

            if not isinstance(
                evidence,
                dict,
            ):
                continue

            evidence_id = evidence.get("id")

            content = evidence.get("content")

            if (
                not isinstance(
                    evidence_id,
                    str,
                )
                or not evidence_id
            ):
                continue

            if not isinstance(content, str):
                continue

            if evidence_id in evidence_ids:
                continue

            lowered = content.lower()

            if any(
                token in lowered
                for token in tokens
            ):
                evidence_ids.append(
                    evidence_id
                )

        return evidence_ids

    @classmethod
    def _specific_tokens(
        cls,
        value: Any,
    ) -> set[str]:
        """
        提取维度值中的字面量 token。

        只取字符串叶子值，不取 dict key，
        避免 JSON 结构名（tasks / question 等）
        与 Evidence 内容产生巧合匹配。
        """

        tokens: set[str] = set()

        def visit(item: Any) -> None:

            if isinstance(item, dict):

                for child in item.values():
                    visit(child)

            elif isinstance(
                item,
                (list, tuple),
            ):

                for child in item:
                    visit(child)

            elif isinstance(item, str):

                for token in (
                    cls._TOKEN_PATTERN
                    .findall(item)
                ):
                    tokens.add(
                        token.lower()
                    )

        visit(value)

        return tokens

    @staticmethod
    def _project_summary(
        project: dict[str, Any],
    ) -> dict[str, Any]:
        """生成项目基本信息摘要。"""

        repository = project.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            repository = {}

        return {
            "run_id": project.get(
                "run_id"
            ),
            "repository_id": repository.get(
                "id"
            ),
            "repository_url": repository.get(
                "url"
            ),
            "repository_name": repository.get(
                "name"
            ),
            "status": project.get(
                "status"
            ),
        }
```

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

from app.skills.base import BaseSkill


class RepositoryAnalysisSkill(
    BaseSkill
):
    """GitHub Repository 分析 Skill。"""

    name = "repository_analysis"

    description = (
        "Analyze github repository information"
    )

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

        # 获取仓库基本信息
        result["repository"] = (
            await github_tool.execute(
                owner=owner,
                name=repo,
            )
        )

        # 获取 README
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
"""

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

        files = await code_search.execute(
            keyword=keyword,
            repo=repository,
        )

        architecture = {
            "files": files,
            "modules": [],
        }

        branch = input_data.get(
            "branch",
            "main",
        )

        for item in files:

            if isinstance(
                item,
                dict,
            ):
                file_path = item.get(
                    "path"
                )
            else:
                file_path = str(item)

            if not file_path:
                continue

            content = await file_reader.execute(
                owner=owner,
                name=repo,
                file_path=file_path,
                branch=branch,
            )

            architecture[
                "modules"
            ].append(
                {
                    "file_path": file_path,
                    "content": content,
                }
            )

        return architecture
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

        for file_path in target_files:

            content = await file_reader.execute(
                owner=owner,
                name=repo,
                file_path=file_path,
                branch=branch,
            )

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

        return {
            "technology_stack": {
                "frameworks": frameworks,
                "database": databases,
                "llm": llms,
                "embedding": embeddings,
                "deployment": deployment,
                "source_files": list(
                    contents.keys()
                ),
            }
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

from app.skills.base import BaseSkill
from app.services.evidence_service import (
    EvidenceService,
)


class EvidenceAnalysisSkill(
    BaseSkill
):
    """生成可追溯 Evidence。"""

    name = "evidence_analysis"

    description = (
        "Extract traceable evidence from "
        "repository analysis results."
    )

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

        if (
            session is not None
            and repository_id is not None
        ):
            service = EvidenceService(
                session
            )

            persisted = []

            for item in unique:

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

                item = dict(item)

                item["evidence_id"] = (
                    record.id
                )

                persisted.append(item)

            unique = persisted

        return {
            "evidence": unique,
            "count": len(unique),
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

        architecture = input_data.get(
            "architecture"
        )

        if isinstance(
            architecture,
            dict,
        ):

            modules = architecture.get(
                "modules",
                [],
            )

            for module in modules:

                if not isinstance(
                    module,
                    dict,
                ):
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

                if not content:
                    continue

                evidence.append(
                    {
                        "source_type": "github",
                        "source_url": repo_url,
                        "file_path": file_path,
                        "line_start": 1,
                        "line_end": len(
                            str(content).splitlines()
                        ),
                        "content": str(content),
                        "metadata": {},
                    }
                )

        return evidence
```

### 📄 `app/skills/report_generation_skill.py`

**层级**：Skill 层（Skills） · **职责**：报告生成能力 `ReportGenerationSkill`（name=`report_generation`），聚合各 Skill 结果并交给 `report_export` Tool 导出；Tool 缺失时直接返回结构化结果

````python
"""
报告生成 Skill。

负责：

AnalysisResult
    ↓
Markdown Report
"""


import json


from app.skills.base import BaseSkill



class ReportGenerationSkill(
    BaseSkill
):
    """
    生成项目分析报告。
    """


    name = "report_generation"


    description = (
        "Generate final GitHub "
        "project intelligence report."
    )



    async def execute(
        self,
        context,
        input_data: dict,
    ):
        """
        生成 Markdown 报告。
        """


        exporter = context.tools.get(
            "report_export"
        )


        title = input_data.get(
            "title",
            "GitHub Project Intelligence Report",
        )


        filename = input_data.get(
            "filename",
            "repository_analysis.md",
        )


        # =========================
        # Phase12:
        # 使用标准 AnalysisResult
        # =========================

        report_data = (
            input_data.get(
                "analysis_result"
            )
            or input_data
        )


        content = (
            self._build_markdown(
                report_data
            )
        )



        # =========================
        # 优先使用 ReportExportTool
        # =========================

        if exporter is not None:

            report = await exporter.execute(
                title=title,
                content=content,
                filename=filename,
            )


            return {

                "report":
                    report,

                "content":
                    content,
            }



        # fallback

        return {

            "report": {

                "format":
                    "markdown",

                "content":
                    content,
            },

            "content":
                content,
        }



    @staticmethod
    def _build_markdown(
        data: dict,
    ):
        """
        构造 Markdown。
        """


        sections = []



        # =====================
        # 01 项目概览
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "01 项目概览",

                data.get(
                    "project_overview",
                    {},
                ),
            )
        )



        # =====================
        # 02 技术栈
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "02 技术栈",

                data.get(
                    "technology_stack",
                    {},
                ),
            )
        )



        # =====================
        # 03 Agent 架构
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "03 Agent 架构",

                data.get(
                    "agents",
                    [],
                ),
            )
        )



        # =====================
        # 04 Workflow
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "04 Workflow",

                data.get(
                    "workflow",
                    {},
                ),
            )
        )



        # =====================
        # 05 Skill
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "05 Skill",

                data.get(
                    "skills",
                    [],
                ),
            )
        )



        # =====================
        # 06 Tool
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "06 Tool",

                data.get(
                    "tools",
                    [],
                ),
            )
        )



        # =====================
        # 07 RAG / Evidence
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "07 RAG / Evidence",

                {

                    "rag":
                        data.get(
                            "rag",
                            {},
                        ),

                    "evidence":
                        data.get(
                            "evidence",
                            [],
                        ),
                },
            )
        )



        # =====================
        # 08 Memory
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "08 Memory / Context",

                {

                    "memory":
                        data.get(
                            "memory",
                            {},
                        ),
                },
            )
        )



        # =====================
        # 09 Database
        # =====================

        sections.append(

            ReportGenerationSkill._section(

                "09 Database",

                data.get(
                    "database",
                    {},
                ),
            )
        )



        return "\n\n".join(
            sections
        )



    @staticmethod
    def _section(
        title: str,
        value,
    ):

        if value is None:

            value = "暂无数据"


        if isinstance(
            value,
            str,
        ):

            content = value

        else:

            content = json.dumps(

                value,

                ensure_ascii=False,

                indent=2,

                default=str,
            )



        return (

            f"## {title}\n\n"

            f"```text\n"

            f"{content}\n"

            f"```"
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



    return registry
```

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
"""

from .base import BaseLLM
class DeepSeekLLM(BaseLLM):

    def __init__(
        self,
        client
    ):

        self.client = client
    async def chat(
        self,
        messages
    ):

        response = await self.client.chat.completions.create(

            model="deepseek-chat",
            messages=messages
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
    - 从 GitHub raw 地址读取项目文件
"""


import httpx

from app.core.exceptions import ToolError
from app.tools.base import BaseTool



class FileReaderTool(BaseTool):


    """
    GitHub 文件读取工具。
    当前支持:
        - README.md
    后续可以扩展:
        - .py
        - requirements.txt
        - pyproject.toml
    """


    name = "file_reader"


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


        url = (
            "https://raw.githubusercontent.com/"
            f"{owner}/{name}/"
            f"{branch}/{file_path}"
        )

        # httpx 的超时异常（例如 ReadTimeout）
        # 其 str() 可能是空字符串，
        # 直接向上抛出会丢失 URL 和异常语义，
        # 因此统一转换成带上下文的 ToolError。
        try:

            async with httpx.AsyncClient() as client:

                response = await client.get(
                    url,
                    timeout=10,
                )

        except httpx.TimeoutException as error:

            raise ToolError(
                f"Read timeout: {url}"
            ) from error

        except httpx.HTTPError as error:

            raise ToolError(
                f"Read failed: {url}: {error}"
            ) from error

        # 非 200 视为“文件不存在”，
        # 保持原有语义：不抛异常。
        if response.status_code != 200:

            # main不存在时尝试master

            if branch == "main":

                return await self.read_file(
                    owner,
                    name,
                    file_path,
                    "master",
                )

            return ""

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
from app.tools.base import BaseTool

class GitHubRepositoryTool(BaseTool):

    """
    GitHub Repository 查询工具。

    负责:
        - 调用 GitHub REST API
        - 获取仓库基础信息
    """

    name = "github_repository"

    BASE_URL = "https://api.github.com"

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
                url
            )
            response.raise_for_status()
            return response.json()
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

### 📄 `tests/test_comparison_agent.py`

**层级**：测试层 · **职责**：Comparison Agent 测试。

```python
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
```

### 📄 `tests/test_comparison_api.py`

**层级**：测试层 · **职责**：Comparison API 测试。

```python
"""Comparison API 测试。"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(
    app
)


def test_comparison_route_exists():
    """
    验证 Comparison API 已经挂载。

    这里使用非法 Run ID，
    重点检查路由是否存在，而不是执行真实比较。
    """

    response = client.post(
        "/api/v1/comparison",
        json={
            "run_ids": [
                "run-a",
                "run-b",
            ]
        },
    )

    # 由于 run 不存在，
    # 应该进入统一业务异常处理，
    # 而不是 404 路由不存在。
    assert response.status_code != 404


def test_comparison_request_requires_two_runs():
    """必须提供两个 Run ID。"""

    response = client.post(
        "/api/v1/comparison",
        json={
            "run_ids": [
                "only-one-run"
            ]
        },
    )

    assert (
        response.status_code
        == 422
    )
```

### 📄 `tests/test_comparison_real_runmemory_schema.py`

**层级**：测试层 · **职责**：Phase 13 真实结构回归测试。

```python
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


def build_real_run(
    run_id,
    repository_id,
    repository_name,
    technology_stack,
    evidences=None,
    language="Python",
    size_kb=8586,
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
                "executed_tasks": list(executed_tasks),
                "research_plan": research_plan,
                "technology_stack": technology_stack,
                "architecture_analysis_agent": {
                    "files": [],
                    "modules": [],
                },
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
            "project_a": build_real_run(
                "d1d71c3e-a9b6-4073-8d3d-bbbfe0b11005",
                26,
                "Multi-Agent-Research-Assistant",
                TECH_A,
                evidences=EVIDENCES_A,
            ),
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
async def test_requirement_2_executed_tasks_is_read():
    """
    要求 2：
    executed_tasks 可以被正确读取。
    """

    result = await compare_two_real_runs()

    value = result["comparison"]["agent"][
        "project_a"
    ]["value"]

    assert value["count"] == 5

    assert value["agents"] == [
        "repository_analysis_agent",
        "architecture_analysis_agent",
        "technology_analysis_agent",
        "evidence_analysis_agent",
        "critic_agent",
    ]


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
async def test_real_runs_produce_more_than_one_usable_dimension():
    """
    修复前只有 workflow 一个维度可用。

    现在 database / deployment / code_complexity /
    agent / workflow / rag 都应给出真实结果。
    """

    result = await compare_two_real_runs()

    usable = [
        dimension
        for dimension, entry in (
            result["comparison"].items()
        )
        if entry["project_a"]["available"]
    ]

    for expected in (
        "agent",
        "workflow",
        "rag",
        "database",
        "deployment",
        "code_complexity",
    ):
        assert expected in usable

    # 真实数据中确实不存在的维度仍然如实返回不可用。
    for missing in (
        "skill",
        "tool",
        "memory",
        "extension",
    ):
        assert (
            result["comparison"][missing][
                "relation"
            ]
            == "NOT_AVAILABLE"
        )


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
```

### 📄 `tests/test_comparison_service.py`

**层级**：测试层 · **职责**：Comparison Service 测试。

```python
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


def run_memory_payload(
    run_id,
    repository_id,
    repository_name,
    technology_stack,
    evidences=None,
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

    assert result.status == "COMPLETED"

    assert len(result.projects) == 2

    assert (
        result.projects[0].repository_name
        == "project-a"
    )

    # Agent 维度来自真实 executed_tasks。
    agent_dimension = result.comparison["agent"]

    assert agent_dimension["relation"] == "SAME"

    assert (
        agent_dimension["project_a"]["value"][
            "count"
        ]
        == 5
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

覆盖：

1. httpx 超时转换为带 URL 的 ToolError
2. 其他 httpx 错误同样转换为 ToolError
3. 保持 404 → master fallback 的既有行为
4. 保持正常读取行为
"""

import httpx
import pytest

from app.core.exceptions import ToolError
from app.tools.file_reader_tool import (
    FileReaderTool,
)


BASE = "https://raw.githubusercontent.com"

EXPECTED_MAIN = (
    f"{BASE}/openai/openai-python/"
    "main/requirements.txt"
)

EXPECTED_MASTER = (
    f"{BASE}/openai/openai-python/"
    "master/requirements.txt"
)


class FakeResponse:
    """最小可用的 httpx Response 替身。"""

    def __init__(
        self,
        status_code,
        text="",
    ):

        self.status_code = status_code

        self.text = text


class FakeAsyncClient:
    """
    假 httpx.AsyncClient。

    支持两种模式：

    - error 不为 None：get() 直接抛异常
    - 否则按 responses 顺序返回
    """

    def __init__(
        self,
        responses=None,
        error=None,
    ):

        self.responses = list(
            responses or []
        )

        self.error = error

        self.urls = []

    async def __aenter__(self):

        return self

    async def __aexit__(
        self,
        *exc_info,
    ):

        return False

    async def get(
        self,
        url,
        timeout=None,
    ):

        self.urls.append(url)

        if self.error is not None:

            raise self.error

        if not self.responses:

            return FakeResponse(404)

        return self.responses.pop(0)


def install_client(
    monkeypatch,
    client,
):
    """把假 Client 注入 FileReaderTool 使用的 httpx 模块。"""

    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda *args, **kwargs: client,
    )

    return client


@pytest.mark.asyncio
async def test_timeout_is_converted_to_tool_error(
    monkeypatch,
):
    """
    httpx.ReadTimeout 必须转换成 ToolError，
    并且错误信息包含 URL。

    httpx.ReadTimeout('') 的 str() 为空字符串，
    直接向上抛出会产生 errors == [""]。
    """

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            error=httpx.ReadTimeout("")
        ),
    )

    with pytest.raises(ToolError) as excinfo:

        await FileReaderTool().execute(
            owner="openai",
            name="openai-python",
            file_path="requirements.txt",
        )

    message = str(excinfo.value)

    assert "Read timeout" in message

    assert EXPECTED_MAIN in message

    assert message.strip() != ""

    assert client.urls == [EXPECTED_MAIN]


@pytest.mark.asyncio
async def test_connect_error_is_converted_to_tool_error(
    monkeypatch,
):
    """非超时的 httpx 错误同样转换成 ToolError。"""

    install_client(
        monkeypatch,
        FakeAsyncClient(
            error=httpx.ConnectError(
                "connection refused"
            )
        ),
    )

    with pytest.raises(ToolError) as excinfo:

        await FileReaderTool().execute(
            owner="openai",
            name="openai-python",
            file_path="requirements.txt",
        )

    message = str(excinfo.value)

    assert "Read failed" in message

    assert EXPECTED_MAIN in message

    assert "connection refused" in message


@pytest.mark.asyncio
async def test_404_on_main_falls_back_to_master(
    monkeypatch,
):
    """main 返回 404 时回退 master，两者都 404 则返回空字符串。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(404),
                FakeResponse(404),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == ""

    assert client.urls == [
        EXPECTED_MAIN,
        EXPECTED_MASTER,
    ]


@pytest.mark.asyncio
async def test_404_on_master_returns_empty_without_retry(
    monkeypatch,
):
    """分支已经是 master 时不再回退，直接返回空字符串。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(404),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
        branch="master",
    )

    assert result == ""

    assert client.urls == [EXPECTED_MASTER]


@pytest.mark.asyncio
async def test_master_fallback_success(
    monkeypatch,
):
    """main 404 但 master 命中时返回 master 内容。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(404),
                FakeResponse(
                    200,
                    "fastapi==0.1.0",
                ),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert client.urls == [
        EXPECTED_MAIN,
        EXPECTED_MASTER,
    ]


@pytest.mark.asyncio
async def test_success_returns_text_unchanged(
    monkeypatch,
):
    """200 时原样返回文本，且不回退 master。"""

    client = install_client(
        monkeypatch,
        FakeAsyncClient(
            responses=[
                FakeResponse(
                    200,
                    "fastapi==0.1.0",
                ),
            ]
        ),
    )

    result = await FileReaderTool().execute(
        owner="openai",
        name="openai-python",
        file_path="requirements.txt",
    )

    assert result == "fastapi==0.1.0"

    assert client.urls == [EXPECTED_MAIN]
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

```python
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
    # 3. Human Review Approve -> Finalizer
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
```

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

    result = await critic.execute(
        context,
        {
            "repository_analysis_agent": {
                "repository": {}
            },
            "architecture_analysis_agent": {
                "architecture": {}
            },
            "technology_analysis_agent": {
                "technology": {}
            },
        },
    )

    assert result["passed"] is True
    assert result["errors"] == []
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

    assert (
        result.data[
            "repository_analysis"
        ][
            "repository"
        ][
            "repo"
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

*本文档由 `generate_project_code.py` 扫描工作区 `.py` 文件自动生成：共收录 **163 段代码**（非空文件），另有 15 个 0 字节空文件，见上方「空文件清单」。*
