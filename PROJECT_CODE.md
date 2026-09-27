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
│   │   ├── error.py
│   │   └── evidence.py
│   ├── services/                                                    # ── 业务服务层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis_service.py
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
│   │   │   ├── end_node.py
│   │   │   ├── human_node.py
│   │   │   ├── skill_node.py
│   │   │   ├── start_node.py
│   │   │   └── tool_node.py
│   │   ├── __init__.py                                              # (空)
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
├── test_reports/                                                    # 测试产生的报告输出目录
│   └── test.md
├── tests/                                                           # ── 测试层 ──
│   ├── test_agent_registry.py
│   ├── test_agent_runtime.py
│   ├── test_analysis_api.py
│   ├── test_chunker.py
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
│   ├── test_github_client.py
│   ├── test_github_code_search_tool.py
│   ├── test_github_parser.py
│   ├── test_indexer.py
│   ├── test_memory.py
│   ├── test_mysql_query_tool.py
│   ├── test_phase10.py
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
│   └── test_workflow.py
├── .env                                                             # 本地环境变量（已 gitignore）
├── .env.example                                                     # 环境变量模板
├── .gitignore
├── a.py                                                             # Agent Loop 实验草稿（未纳入 app/）
├── agent loop.py                                                    # Agent Loop 草稿片段
├── AI-Agent-GitHub-Project-Intelligence-Platform-详细Phase开发实施文档.md
├── AI-Agent-GitHub-Project-Intelligence-Platform-项目设计文档.md
├── alembic.ini                                                      # Alembic 配置
├── generate_project_code.py                                         # 本文档生成脚本
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

from app.api.v1.analysis import router as analysis_router
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

logger = get_logger(__name__)


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


# 注册 v1 API。
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
    """创建 GitHub 项目分析任务。"""

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
    """根据 run_id 查询分析任务。"""

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
    """通过 Design Gate。"""

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
    """暂停分析任务。"""

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
    """恢复分析任务。"""

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
    """重试失败的分析任务。"""

    return await analysis_service.retry_analysis(
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

## 四、数据契约层（Schemas）

接口的请求体与响应体定义，被 API 层与 Service 层共同引用

### 📄 `app/schemas/analysis.py`

**层级**：数据契约层（Schemas） · **职责**：Analysis 接口的请求体与响应体定义

```python
"""Analysis API 的请求和响应数据模型。"""

from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisCreateRequest(BaseModel):
    """创建项目分析任务时的请求参数。"""

    repo_url: str = Field(
        ...,
        min_length=1,
        description="GitHub repository URL",
    )

    question: str | None = Field(
        default=None,
        max_length=5000,
        description="本次项目分析问题，用于 Run Memory 和 Context Manager",
    )


class AnalysisResponse(BaseModel):
    """分析任务的基础响应信息。"""

    run_id: str
    status: str
    repo_url: str
    created_at: datetime
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

## 五、业务服务层（Services）

业务编排：校验入参、组合 DAO 与工具层、掌控事务边界

### 📄 `app/services/analysis_service.py`

**层级**：业务服务层（Services） · **职责**：Analysis 任务的业务编排——校验 URL、创建或复用 Repository、创建 Analysis Run 并提交事务

```python
"""Analysis 任务业务逻辑。"""

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ValidationError
from app.core.logging import get_logger, log_with_run_id
from app.repositories.analysis_run import (
    AnalysisRunRepository,
)
from app.repositories.repository_basic import (
    RepositoryRepository,
)
from app.schemas.analysis import (
    AnalysisCreateRequest,
    AnalysisResponse,
)
from app.models.repository import Repository


logger = get_logger(__name__)


class AnalysisService:
    """负责 Analysis 任务的业务编排。"""

    async def create_analysis(
        self,
        session: AsyncSession,
        request: AnalysisCreateRequest,
    ) -> AnalysisResponse:
        """创建 Repository 和 Analysis Run。"""

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

        repository_repo = RepositoryRepository(
            session
        )

        analysis_run_repo = AnalysisRunRepository(
            session
        )

        repository = await repository_repo.get_by_url(
            repo_url
        )

        if repository is None:
            repository = await repository_repo.create(
                url=repo_url,
                owner=owner,
                name=name,
            )

        run_id = str(uuid4())

        # Phase 11：
        # 将用户问题真正保存到 AnalysisRun。
        run = await analysis_run_repo.create(
            run_id=run_id,
            repository_id=repository.id,
            question=request.question,
        )

        await session.commit()

        log_with_run_id(
            logger,
            level=20,
            message="analysis task created",
            run_id=run_id,
        )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def get_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """根据 run_id 查询分析任务。"""

        repository_run = AnalysisRunRepository(
            session
        )

        run = await repository_run.get_by_id(
            run_id
        )

        if run is None:
            raise ValidationError(
                f"Analysis run not found: {run_id}"
            )

        repository_repo = RepositoryRepository(
            session
        )

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    @staticmethod
    def _parse_github_url(
        repo_url: str,
    ) -> tuple[str, str]:
        """解析 GitHub owner 和 repository name。"""

        path = repo_url.rstrip("/").split("/")

        if len(path) < 2:
            raise ValidationError(
                "Invalid GitHub repository URL."
            )

        owner = path[-2]
        name = path[-1]

        if not owner or not name:
            raise ValidationError(
                "Invalid GitHub repository URL."
            )

        return owner, name

    async def approve_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """通过 Design Gate。"""

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
            "pending",
            "WAITING_DESIGN",
            "WAITING_DESIGN_APPROVAL",
        }:
            raise ValidationError(
                f"Analysis run cannot be approved "
                f"from status: {run.status}"
            )

        await run_repo.update_runtime_state(
            run,
            status="ANALYZING",
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def pause_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """人工暂停 Analysis Run。"""

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

        if run.status != "ANALYZING":
            raise ValidationError(
                f"Analysis run cannot be paused "
                f"from status: {run.status}"
            )

        await run_repo.update_runtime_state(
            run,
            status="PAUSED",
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def resume_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """从 Checkpoint 恢复 Analysis Run。"""

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
            "PAUSED",
            "WAITING_HUMAN",
        }:
            raise ValidationError(
                f"Analysis run cannot be resumed "
                f"from status: {run.status}"
            )

        await run_repo.update_runtime_state(
            run,
            status="ANALYZING",
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )

    async def retry_analysis(
        self,
        session: AsyncSession,
        run_id: str,
    ) -> AnalysisResponse:
        """重新执行失败的 Analysis Run。"""

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

        await run_repo.update_runtime_state(
            run,
            status="RETRYING",
            retry_count=run.retry_count + 1,
        )

        await session.commit()

        repository = await session.get(
            Repository,
            run.repository_id,
        )

        if repository is None:
            raise ValidationError(
                f"Repository not found: {run.repository_id}"
            )

        return AnalysisResponse(
            run_id=run.id,
            status=run.status,
            repo_url=repository.url,
            created_at=run.created_at,
        )


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

Phase 10：
WorkflowState
    ↓
CheckpointManager
    ↓
Checkpoint Repository / MySQL

当前 Manager 负责状态序列化与恢复。
具体 MySQL 持久化由 Repository 完成。
"""

from copy import deepcopy
from typing import Any


class CheckpointManager:
    """
    Workflow Checkpoint 管理器。

    repository 可以是：
    - MySQL CheckpointRepository
    - 测试环境下的 MemoryCheckpointRepository
    """

    def __init__(
        self,
        repository=None,
    ) -> None:

        self.repository = repository

        # 测试 / 本地 fallback
        self._store: dict[str, Any] = {}

    async def save(
        self,
        state,
    ) -> str:
        """
        保存 WorkflowState。

        如果配置 Repository：
            保存到 MySQL

        否则：
            保存到内存
        """

        snapshot = deepcopy(state)

        snapshot.checkpoint_version += 1

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
        """
        根据 run_id 恢复最近一次 Checkpoint。
        """

        if self.repository is not None:

            state = await self.repository.get_latest(
                run_id
            )

            if state is None:
                return None

            return deepcopy(state)

        state = self._store.get(
            run_id
        )

        if state is None:
            return None

        return deepcopy(state)

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
from app.workflow.retry import RetryPolicy
from app.workflow.state import WorkflowStatus


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

            current_node = (
                self._get_next_node(
                    workflow,
                    state,
                    state.current_node,
                )
            )

            state.resume()

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

                state.errors.append(
                    str(error)
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
Agent类型Workflow节点。
"""


from .base import BaseNode



class AgentNode(BaseNode):
    """
    封装Agent执行。
    """


    def __init__(
        self,
        name,
        agent
    ):

        self.name = name

        self.agent = agent



    async def execute(
        self,
        state,
        context
    ):

        # 调用Agent
        result = await self.agent.run(
            state,
            context
        )


        # 保存结果
        state.outputs.append(
            result
        )


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

根据用户需求生成任务计划。


当前 Phase 8：

先实现固定规划。


Phase 9：

升级为：

LLM Dynamic Planning


"""


from app.agents.base import BaseAgent




class PlannerAgent(
    BaseAgent
):


    name = (
        "planner_agent"
    )



    async def execute(
        self,
        context,
        input_data
    ):



        # 当前先定义固定分析流程

        # 后续由LLM动态决定

        tasks = [



            "repository_analysis_agent",



            "architecture_analysis_agent",



            "technology_analysis_agent",



            "evidence_analysis_agent",



            "critic_agent"

        ]



        return {


            "tasks":

                tasks

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


负责：

检查其他 Agent 输出质量。


例如：

- 是否缺少关键结果
- 是否分析失败
- 是否需要重新执行


后续 Phase 会扩展：

Retry

Human Review

Validation


"""


from app.agents.base import BaseAgent




class CriticAgent(
    BaseAgent
):


    name = (
        "critic_agent"
    )
    async def execute(
        self,
        context,
        input_data
    ):
        errors = []
        # 必须存在的分析结果

        required_fields = [

            "repository",

            "architecture",

            "technology"

        ]
        for field in required_fields:


            if field not in input_data:


                errors.append(

                    f"{field} missing"

                )

        return {

            # 是否通过检查

            "passed":

                len(errors) == 0,
            # 错误列表

            "errors":

                errors

        }
```

### 📄 `app/agents/agent_registry.py`

**层级**：Agent 层（Agents） · **职责**：Agent 注册中心 `AgentRegistry`：按 `agent.name` 注册与获取；`create_agent_registry(skill_registry)` 在启动时构造全部 6 个领域 Agent

```python
"""
Agent Registry。


作用：

统一管理系统中的 Agent。


类似 SkillRegistry：

SkillRegistry:
    管理 Skill


AgentRegistry:
    管理 Agent



避免业务代码：

RepositoryAnalysisAgent()

TechnologyAgent()

大量硬编码创建。


"""


from app.agents.planner_agent import (
    PlannerAgent
)


from app.agents.repository_analysis_agent import (
    RepositoryAnalysisAgent
)


from app.agents.architecture_analysis_agent import (
    ArchitectureAnalysisAgent
)


from app.agents.technology_analysis_agent import (
    TechnologyAnalysisAgent
)


from app.agents.evidence_analysis_agent import (
    EvidenceAnalysisAgent
)


from app.agents.critic_agent import (
    CriticAgent
)





class AgentRegistry:
    """
    Agent 管理器。


    保存：

    {
        agent_name:
            agent_instance
    }

    """



    def __init__(self):


        # 保存所有Agent实例

        self.agents = {}



    def register(
        self,
        agent
    ):

        """
        注册 Agent。

        """

        self.agents[
            agent.name
        ] = agent




    def get(
        self,
        name
    ):

        """
        根据名称获取 Agent。
        """

        return self.agents.get(
            name
        )





def create_agent_registry(
    skill_registry
):
    """
    创建默认 Agent 集合。


    项目启动时调用。

    """

    registry = AgentRegistry()



    # 初始化所有领域Agent

    agents = [
        # 任务规划Agent

        PlannerAgent(
            skill_registry
        ),

        # 仓库分析Agent

        RepositoryAnalysisAgent(
            skill_registry
        ),



        # 架构分析Agent

        ArchitectureAnalysisAgent(
            skill_registry
        ),



        # 技术栈分析Agent

        TechnologyAnalysisAgent(
            skill_registry
        ),



        # 证据分析Agent

        EvidenceAnalysisAgent(
            skill_registry
        ),



        # 结果检查Agent

        CriticAgent(
            skill_registry
        )

    ]



    # 注册到Registry

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
Repository Analysis Skill


负责分析 GitHub 项目基础信息。


执行流程:

RepositoryAnalysisSkill

        |
        |
        +---- GitHub Repository Tool
        |
        +---- File Reader Tool
        |
        +---- Dependency Analyzer Tool



输出:

{
    repository:{},

    readme:{},

    dependencies:{}

}

"""


from app.skills.base import BaseSkill




class RepositoryAnalysisSkill(
    BaseSkill
):


    # Skill名称

    name = "repository_analysis"



    description = (
        "Analyze github repository information"
    )



    async def execute(
        self,
        context,
        input_data
    ):
        """
        执行仓库分析。


        input_data:

        {
            "owner":"xxx",
            "repo":"xxx"
        }

        """


        result = {}



        # 从Context中获取工具

        github_tool = (
            context.tools[
                "github_repository"
            ]
        )


        file_reader = (
            context.tools[
                "file_reader"
            ]
        )


        dependency_tool = (
            context.tools[
                "dependency_analyzer"
            ]
        )



        # 获取仓库基本信息

        result["repository"] = (
            await github_tool.execute(
                **input_data
            )
        )



        # 获取README内容

        result["readme"] = (
            await file_reader.execute(

                **input_data,

                path="README.md"

            )
        )



        # 分析项目依赖

        result["dependencies"] = (
            await dependency_tool.execute(
                **input_data
            )
        )



        return result
```

### 📄 `app/skills/architecture_analysis_skill.py`

**层级**：Skill 层（Skills） · **职责**：架构分析能力 `ArchitectureAnalysisSkill`（name=`architecture_analysis`），用 `github_code_search` 搜出文件列表，再逐个用 `file_reader` 读取内容，产出 `{files, modules}`

```python
"""
Architecture Analysis Skill


负责分析项目代码结构。


主要分析:

- 文件结构
- 模块关系
- 核心代码


依赖:

Code Search Tool

File Reader Tool

"""


from app.skills.base import BaseSkill




class ArchitectureAnalysisSkill(
    BaseSkill
):


    name = "architecture_analysis"



    description = (
        "Analyze repository architecture"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取代码搜索工具

        code_search = (
            context.tools[
                "github_code_search"
            ]
        )


        file_reader = (
            context.tools[
                "file_reader"
            ]
        )



        # 搜索项目文件

        files = await code_search.execute(
            **input_data
        )



        architecture = {

            "files": files,

            "modules":[]

        }



        # 读取代码内容

        for file in files:


            content = await file_reader.execute(

                **input_data,

                path=file

            )


            architecture[
                "modules"
            ].append(
                content
            )



        return architecture
```

### 📄 `app/skills/technology_analysis_skill.py`

**层级**：Skill 层（Skills） · **职责**：技术栈分析能力 `TechnologyAnalysisSkill`（name=`technology_analysis`），调用 `dependency_analyzer` Tool，产出 `{technology_stack}`

```python
"""
Technology Analysis Skill


分析项目技术栈。


例如:

- Python
- FastAPI
- LangChain
- Vector DB
- Docker


"""


from app.skills.base import BaseSkill




class TechnologyAnalysisSkill(
    BaseSkill
):


    name = "technology_analysis"



    description = (
        "Analyze technology stack"
    )



    async def execute(
        self,
        context,
        input_data
    ):


        # 获取依赖分析工具

        dependency_tool = (
            context.tools[
                "dependency_analyzer"
            ]
        )



        dependencies = await dependency_tool.execute(
            **input_data
        )



        return {


            "technology_stack":

                dependencies

        }
```

### 📄 `app/skills/evidence_analysis_skill.py`

**层级**：Skill 层（Skills） · **职责**：证据追踪能力 `EvidenceAnalysisSkill`（name=`evidence_analysis`），调用 `qdrant_search` Tool 做语义检索，产出 `{evidence}`

```python
"""
Evidence Analysis Skill。

Phase 9：

Qdrant Retrieval
        ↓
Evidence Normalization
        ↓
Evidence Store

负责：

- 检索候选证据
- 标准化 Evidence
- 保存 Evidence
- 保留 Source / File / Line 信息
"""

from app.skills.base import BaseSkill


class EvidenceAnalysisSkill(
    BaseSkill
):

    name = "evidence_analysis"

    description = (
        "Extract traceable evidence "
        "from repository search results"
    )

    async def execute(
        self,
        context,
        input_data,
    ):

        # 获取 Qdrant 检索工具
        qdrant_tool = context.tools[
            "qdrant_search"
        ]

        # 执行语义检索
        results = await qdrant_tool.execute(
            **input_data
        )

        evidence = []

        for item in results:

            # 当前 Qdrant payload 中：
            #
            # text
            # source
            # document_id
            # chunk_index
            #
            # 可能存在，但不能假设一定存在。

            normalized = {
                "source_type": item.get(
                    "source_type",
                    "repository",
                ),
                "source_url": item.get(
                    "source_url"
                ),
                "file_path": item.get(
                    "file_path"
                ),
                "line_start": item.get(
                    "line_start"
                ),
                "line_end": item.get(
                    "line_end"
                ),
                "content": item.get(
                    "text",
                    ""
                ),
                "metadata": item,
            }

            # 不伪造源码行号。
            #
            # 当前索引器没有可靠保存
            # line_start / line_end，
            # 所以没有数据时保持 None。

            evidence.append(
                normalized
            )

        return {
            "evidence": evidence,
            "count": len(evidence),
        }
```

### 📄 `app/skills/report_generation_skill.py`

**层级**：Skill 层（Skills） · **职责**：报告生成能力 `ReportGenerationSkill`（name=`report_generation`），聚合各 Skill 结果并交给 `report_export` Tool 导出；Tool 缺失时直接返回结构化结果

```python
"""
Report Generation Skill


负责生成最终分析报告。


输入:

多个Skill / Agent分析结果


输出:

报告内容


"""


from app.skills.base import BaseSkill




class ReportGenerationSkill(
    BaseSkill
):
    """
    报告生成能力。
    """



    name = "report_generation"



    description = (
        "Generate final repository analysis report"
    )



    async def execute(
        self,
        context,
        input_data: dict
    ):
        """
        执行报告生成。


        input_data:

        {
            "repository": {},
            "architecture": {},
            "technology": {}
        }

        """


        # 获取报告导出工具

        exporter = (
            context.tools.get(
                "report_export"
            )
        )


        # 如果还没有接入真实导出工具

        # 返回结构化结果

        if exporter is None:

            return {


                "report":

                    input_data


            }

        report = await exporter.execute(

            data=input_data

        )
        return {


            "report":

                report

        }
```

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

        async with httpx.AsyncClient() as client:


            response = await client.get(
                url,
                timeout=10,
            )

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
"""Analysis API 测试，验证任务创建、查询和参数校验。"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    """测试健康检查接口。"""

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_create_analysis():
    """测试创建 GitHub 项目分析任务。"""

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url": "https://github.com/openai/openai-python"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "run_id" in data
    assert data["status"] == "pending"
    assert (
        data["repo_url"]
        == "https://github.com/openai/openai-python"
    )


def test_get_analysis():
    """测试根据 run_id 查询分析任务。"""

    # 先创建任务，再使用返回的 run_id 查询。
    # 这样可以验证创建和查询两个接口之间的数据链路。
    create_response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url": "https://github.com/openai/openai-python"
        },
    )

    run_id = create_response.json()["run_id"]

    response = client.get(
        f"/api/v1/analysis/{run_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == run_id
    assert data["status"] == "pending"


def test_invalid_repository_url():
    """测试非法 Repository URL。"""

    response = client.post(
        "/api/v1/analysis",
        json={
            "repo_url": "https://example.com/test"
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_analysis_not_found():
    """测试查询不存在的分析任务。"""

    response = client.get(
        "/api/v1/analysis/not-exist-run-id"
    )

    assert response.status_code == 400

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
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
            "repo": kwargs["repo"],
            "owner": kwargs["owner"],
            "name": kwargs["repo"],
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
        "repo": "test-project"
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

            "name":
            kwargs["repo"]

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
            kwargs["repo"]

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

7. **Agent 接口已换代，`AgentNode` 未同步**
   - `BaseAgent` 已从 `run(state, context)` 改为 `execute(context, input_data)`，并改为持有 `skill_registry`
   - 全部 6 个领域 Agent 都已按新接口实现，`AgentRuntime.execute(agent_name, context, input_data)` 也已适配
   - 但 `app/workflow/nodes/agent_node.py` 仍在调用 `self.agent.run(state, context)`，属于旧接口残留

8. **Skill 内硬编码 Tool 名与实参不匹配**
   - 各 Skill 直接以 `context.tools["github_repository"]` 之类取工具，键名写死，缺键即 `KeyError`，没有降级或报错提示
   - `ArchitectureAnalysisSkill` 调用 `file_reader.execute(**input_data, path=file)`，但 `FileReaderTool.execute` 的形参是 `file_path`；且 `github_code_search` 需要 `keyword` / `repo`，与 `input_data` 不一定对得上
   - `ReportGenerationSkill` 调用 `exporter.execute(data=input_data)`，而 `ReportExportTool.execute` 的形参是 `title` / `content` / `filename`

9. **Skill 输出键名与 `CriticAgent` 校验字段不一致**
   - `SkillNode` 把每个 Skill 的结果写入 `state.data[node.name]`，即 `repository_analysis` / `architecture_analysis` / `technology_analysis`
   - `CriticAgent` 检查的却是 `repository` / `architecture` / `technology`，两者对不上，`passed` 会恒为 `False`
   - `PlannerAgent` 返回的 `tasks` 列表目前也没有任何代码消费，Workflow 尚未真正按计划驱动 Agent 执行

10. **证据链能力尚未对外暴露**
   - `app/evidence/`（Store / Verifier / Traceability）、`EvidenceService`
     与 `app/schemas/evidence.py` 均已实现并有测试覆盖
   - 但 `app/api/` 下没有任何证据相关路由，`app/main.py` 也未装配 `EvidenceService`，
     目前只能由测试或脚本直接调用，尚未形成可访问的接口

---

*本文档由 `generate_project_code.py` 扫描工作区 `.py` 文件自动生成：共收录 **143 段代码**（非空文件），另有 15 个 0 字节空文件，见上方「空文件清单」。*
