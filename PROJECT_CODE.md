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
├── alembic/                                                         # 数据库迁移（Alembic）
│   ├── versions/                                                    # 迁移脚本
│   │   └── 479571222143_create_initial_analysis_tables.py
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── app/                                                             # 应用主包
│   ├── agents/                                                      # ── Agent 层 ──
│   │   ├── base.py
│   │   ├── critic.py
│   │   ├── planner.py
│   │   ├── researcher.py
│   │   └── runtime.py
│   ├── api/                                                         # ── API 层 ──
│   │   ├── v1/                                                      # v1 路由
│   │   │   ├── __init__.py                                          # (空)
│   │   │   └── analysis.py
│   │   └── __init__.py                                              # (空)
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
│   ├── llm/                                                         # ── LLM 能力层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── base.py
│   │   └── deepseek.py
│   ├── models/                                                      # ── 数据模型层 ──
│   │   ├── __init__.py
│   │   ├── analysis_run.py
│   │   ├── analysis_task.py
│   │   └── repository.py
│   ├── project_analysis/                                            # ── 项目分析层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── code_chunker.py
│   │   ├── project_indexer.py
│   │   └── repository_indexer.py
│   ├── repositories/                                                # ── 数据访问层 ──
│   │   ├── __init__.py
│   │   ├── analysis_run.py
│   │   ├── repository.py
│   │   └── repository_basic.py
│   ├── schemas/                                                     # ── 数据契约层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis.py
│   │   └── error.py
│   ├── services/                                                    # ── 业务服务层 ──
│   │   ├── __init__.py                                              # (空)
│   │   ├── analysis_service.py
│   │   └── repository_service.py
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
│   ├── test_analysis_api.py
│   ├── test_chunker.py
│   ├── test_config.py
│   ├── test_database.py
│   ├── test_dependency_analyzer_tool.py
│   ├── test_embedding.py
│   ├── test_embedding_qdrant.py
│   ├── test_exceptions.py
│   ├── test_github_client.py
│   ├── test_github_code_search_tool.py
│   ├── test_github_parser.py
│   ├── test_indexer.py
│   ├── test_mysql_query_tool.py
│   ├── test_qdrant.py
│   ├── test_qdrant_search_tool.py
│   ├── test_report_export_tool.py
│   ├── test_repository_crud.py
│   ├── test_repository_pipeline.py
│   ├── test_repository_service.py
│   ├── test_retrieval.py
│   ├── test_tools.py
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
    ┌───────────────────────────┐   ┌─────────────────────────┐
    │  Agent 层  app/agents/    │   │  LLM 能力层  app/llm/    │
    │  BaseAgent / AgentRuntime │──▶│  BaseLLM / DeepSeekLLM  │
    └───────────────────────────┘   └─────────────────────────┘

    贯穿各层：app/core/（配置、日志、异常、异常处理器）
    数据契约：app/schemas/（被 API 层与 Service 层共同引用）
```

---

## 二、入口层

FastAPI 应用装配：日志、异常处理、路由挂载

### 📄 `app/main.py`

**层级**：入口层 · **职责**：FastAPI 应用初始化、日志初始化、全局异常注册、路由挂载

```python
"""FastAPI 应用入口：负责应用初始化、日志、异常处理和 API 路由注册。"""

from fastapi import FastAPI

from app.api.v1.analysis import router as analysis_router
from app.core.config import get_settings
from app.core.error_handlers import (
    application_error_handler,
    unexpected_error_handler,
)
from app.core.exceptions import ApplicationError
from app.core.logging import get_logger, setup_logging


settings = get_settings()

# 应用启动时初始化全局日志，保证各模块使用统一的日志格式。
setup_logging()
logger = get_logger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    description="AI Agent GitHub Project Intelligence Platform",
    version="0.1.0",
    debug=settings.DEBUG,
)

# 所有业务异常统一转换成标准 HTTP 错误响应，
# 避免每个 API 都单独处理异常。
app.add_exception_handler(
    ApplicationError,
    application_error_handler,
)

# 捕获未预期异常，避免直接向客户端暴露内部错误信息。
app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)

# 注册 v1 API。
# 后续 Workflow、Agent、Project 等接口都会继续挂载到这里。
app.include_router(
    analysis_router,
    prefix="/api/v1",
)


@app.get("/health", tags=["System"])
async def health_check():
    """健康检查接口，用于确认 API 服务是否正常运行。"""
    return {
        "status": "ok",
        "environment": settings.APP_ENV,
    }


@app.get("/", tags=["System"])
async def root():
    """项目根路径，返回应用基本信息。"""
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
from app.services.analysis_service import analysis_service


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
```

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

        run = await analysis_run_repo.create(
            run_id=run_id,
            repository_id=repository.id,
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

        # 当前先根据 repository_id 查询项目。
        repository = await session.get(
            __import__(
                "app.models.repository",
                fromlist=["Repository"],
            ).Repository,
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
```

### 📄 `app/repositories/repository.py`

**层级**：数据访问层（Repositories） · **职责**：`repositories` 表的数据访问（**全字段版**，`create()` 内部 commit）

```python
"""Repository 数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository


class RepositoryRepository:
    """负责 repositories 表的数据库操作。"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_url(
        self,
        url: str,
    ) -> Repository | None:
        """根据 GitHub URL 查询项目。"""

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
        """根据 Repository ID 查询项目。"""

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
        """创建一个 Repository 记录。"""

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

        self.session.add(repository)

        await self.session.commit()
        await self.session.refresh(repository)

        return repository
```

### 📄 `app/repositories/repository_basic.py`

**层级**：数据访问层（Repositories） · **职责**：`repositories` 表的数据访问（**精简版**，`create()` 只 flush，事务交给调用方）

```python
"""GitHub Repository 数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository


class RepositoryRepository:
    """负责 repositories 表的数据访问。"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_url(
        self,
        url: str,
    ) -> Repository | None:
        """根据 GitHub URL 查询项目。"""

        result = await self.session.execute(
            select(Repository).where(
                Repository.url == url
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        *,
        url: str,
        owner: str,
        name: str,
    ) -> Repository:
        """创建 GitHub Repository 记录。"""

        repository = Repository(
            url=url,
            owner=owner,
            name=name,
        )

        self.session.add(repository)

        await self.session.flush()

        return repository
```

### 📄 `app/repositories/analysis_run.py`

**层级**：数据访问层（Repositories） · **职责**：`analysis_runs` 表的数据访问

```python
"""Analysis Run 数据访问层。"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analysis_run import AnalysisRun


class AnalysisRunRepository:
    """负责 analysis_runs 表的数据访问。"""

    def __init__(self, session: AsyncSession) -> None:
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
```

## 七、数据模型层（Models）

SQLAlchemy ORM 表结构定义

### 📄 `app/models/__init__.py`

**层级**：数据模型层（Models） · **职责**：模型统一导出（同时供 Alembic 迁移发现全部表）

```python
"""数据库模型统一导出。"""

from app.models.analysis_run import AnalysisRun
from app.models.analysis_task import AnalysisTask
from app.models.repository import Repository

__all__ = [
    "Repository",
    "AnalysisRun",
    "AnalysisTask",
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

## 十、Workflow 层（Workflow）

自研工作流引擎：状态、上下文、节点、流转、重试、检查点与执行引擎

### 📄 `app/workflow/state.py`

**层级**：Workflow 层（Workflow） · **职责**：Workflow 运行状态 `WorkflowState`：run_id、status、current_node、data、outputs、errors、retry_count

```python
"""
Workflow运行状态。
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WorkflowState:
    """
    保存一次Workflow执行过程中的状态。
    """

    # Workflow执行ID
    run_id: str

    # 当前状态
    status: str = "CREATED"

    # 当前执行节点
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

    # 重试次数
    retry_count: int = 0
```

### 📄 `app/workflow/context.py`

**层级**：Workflow 层（Workflow） · **职责**：Workflow 执行上下文 `WorkflowContext`：agents / tools / skills / config

```python
"""
Workflow执行上下文。
"""


from dataclasses import dataclass


@dataclass
class WorkflowContext:
    """
    保存Workflow运行环境。
    """

    # Agent集合
    agents: dict


    # Tool集合
    tools: dict


    # Skill集合
    skills: dict


    # 配置参数
    config: dict
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
Workflow重试策略。
"""


class RetryPolicy:
    def __init__(
        self,
        max_retry=3
    ):

        # 最大重试次数
        self.max_retry = max_retry

    def can_retry(
        self,
        count
    ):

        return (
            count < self.max_retry
        )
```

### 📄 `app/workflow/checkpoint.py`

**层级**：Workflow 层（Workflow） · **职责**：状态保存与恢复 `CheckpointManager`，内存实现：按 run_id 用 `deepcopy` 保存 `WorkflowState` 快照

```python
"""
Workflow状态保存。
"""

from copy import deepcopy


class CheckpointManager:
    """
    保存和恢复Workflow状态。

    当前为内存实现，按 run_id 保存 WorkflowState 快照。
    持久化到 MySQL 属于后续阶段。
    """

    def __init__(self):

        # run_id -> WorkflowState 快照
        self._store = {}

    async def save(
        self,
        state
    ):

        # 深拷贝，避免后续修改影响已保存的快照
        self._store[
            state.run_id
        ] = deepcopy(state)

        return state.run_id

    async def load(
        self,
        run_id
    ):

        state = self._store.get(
            run_id
        )

        if state is None:

            return None

        return deepcopy(state)
```

### 📄 `app/workflow/exceptions.py`

**层级**：Workflow 层（Workflow） · **职责**：Workflow 自有异常：`WorkflowError`（继承 `ApplicationError`，可被全局异常处理器捕获）/ `NodeExecutionError`

```python
"""
Workflow异常定义。
"""

from app.core.exceptions import (
    ApplicationError,
)


class WorkflowError(ApplicationError):
    """
    Workflow基础异常。

    继承 ApplicationError，使其能被全局异常处理器识别。
    """
    pass

class NodeExecutionError(WorkflowError):
    """
    Node执行失败异常。
    """

    pass
```

### 📄 `app/workflow/workflow.py`

**层级**：Workflow 层（Workflow） · **职责**：流程定义 `Workflow`：`add_node()` 注册节点、`add_transition()` 注册流转

```python
"""
Workflow流程定义。
"""


class Workflow:


    def __init__(self):

        # Node集合
        self.nodes = {}


        # Transition集合
        self.transitions = []

    def add_node(
        self,
        node
    ):

        self.nodes[
            node.name
        ] = node


    def add_transition(
        self,
        transition
    ):

        self.transitions.append(
            transition
        )
```

### 📄 `app/workflow/engine.py`

**层级**：Workflow 层（Workflow） · **职责**：执行引擎 `WorkflowEngine`：从 `start` 节点起循环执行，异常时记录 errors 并置 FAILED，正常结束置 COMPLETED；支持可选 `checkpoint` / `retry_policy`，`RetryableError` 按 `RetryPolicy` 重试，`PAUSED` 状态保存检查点后退出，`resume_from` 可从检查点恢复

```python
"""
Workflow执行引擎。
"""

from app.core.exceptions import (
    NonRetryableError,
    RetryableError,
)
from app.workflow.retry import RetryPolicy


class WorkflowEngine:

    # 暂停状态标识
    PAUSED_STATUS = "PAUSED"

    def __init__(
        self,
        checkpoint=None,
        retry_policy=None,
    ):

        # 检查点管理器，可选
        self.checkpoint = checkpoint

        # 节点重试策略
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
        执行Workflow。
        """

        if resume_from is not None:

            state = await self._restore(
                resume_from
            )

            # 当前节点已执行过，从它的下一节点继续
            current_node = self._get_next_node(
                workflow,
                state,
                state.current_node
            )

        else:

            current_node = "start"

        while current_node:


            # 获取节点
            node = workflow.nodes[
                current_node
            ]


            # 更新状态
            state.current_node = (
                current_node
            )

            try:

                # 执行节点
                state = await self._execute_node(
                    node,
                    state,
                    context
                )
            except Exception as e:

                state.errors.append(
                    str(e)
                )

                state.status = (
                    "FAILED"
                )

                return state

            # 暂停：保存检查点后退出，等待 Resume
            if state.status == self.PAUSED_STATUS:

                await self._save(state)

                return state

            # 每执行完一个节点保存一次检查点
            await self._save(state)

            # 查找下一节点
            current_node = (
                self._get_next_node(
                    workflow,
                    state,
                    current_node
                )
            )



        state.status = (
            "COMPLETED"
        )


        return state



    async def _execute_node(
        self,
        node,
        state,
        context
    ):
        """
        执行节点。

        可重试异常按 RetryPolicy 重试，
        不可重试异常直接抛出。
        """

        while True:

            try:

                return await node.execute(
                    state,
                    context
                )

            except NonRetryableError:

                raise

            except RetryableError as e:

                if not self.retry_policy.can_retry(
                    state.retry_count
                ):

                    raise e

                state.retry_count += 1



    async def _save(
        self,
        state
    ):
        """
        保存检查点，未配置时跳过。
        """

        if self.checkpoint is None:

            return

        await self.checkpoint.save(
            state
        )



    async def _restore(
        self,
        run_id
    ):
        """
        从检查点恢复状态。
        """

        if self.checkpoint is None:

            raise ValueError(
                "resume_from requires a checkpoint manager"
            )

        state = await self.checkpoint.load(
            run_id
        )

        if state is None:

            raise ValueError(
                f"Checkpoint not found: {run_id}"
            )

        # 恢复后重新进入运行态
        state.status = "RUNNING"

        return state



    def _get_next_node(
        self,
        workflow,
        state,
        current
    ):
        """
        获取下一执行节点。
        """
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

## 十一、Workflow 节点层（Workflow Nodes）

各类节点的具体实现：开始 / 结束 / 分析 / Agent / Tool / Skill / 人工审核

### 📄 `app/workflow/nodes/base.py`

**层级**：Workflow 节点层 · **职责**：节点基类 `BaseNode`（与 `app/workflow/node.py` 中的同名类重复定义）

```python
"""
Workflow节点基类。
"""

from abc import ABC, abstractmethod

class BaseNode(ABC):
    """
    所有Workflow节点的父类。
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
        执行节点。
        """

        pass
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

**层级**：Workflow 节点层 · **职责**：Skill 节点 `SkillNode`，封装 Skill 调用并把结果追加到 `state.outputs`

```python
"""
Skill类型Workflow节点。
"""


from .base import BaseNode

class SkillNode(BaseNode):
    """
    执行Skill能力。
    """

    def __init__(
        self,
        name,
        skill
    ):

        self.name = name

        self.skill = skill

    async def execute(
        self,
        state,
        context
    ):

        result = await self.skill.execute(
            state
        )

        state.outputs.append(
            result
        )


        return state
```

### 📄 `app/workflow/nodes/human_node.py`

**层级**：Workflow 节点层 · **职责**：HITL 人工审核节点 `HumanNode`（name=`human_review`），把 status 置为 WAITING_HUMAN 以暂停流程

```python
"""
Human-In-The-Loop节点。
"""

from .base import BaseNode

class HumanNode(BaseNode):
    """
    人工审核节点。
    """

    name = "human_review"

    async def execute(
        self,
        state,
        context
    ):

        # 暂停Workflow
        state.status = (
            "WAITING_HUMAN"
        )


        return state
```

## 十二、Agent 层（Agents）

Agent 抽象接口、运行环境，以及 Planner 等具体 Agent

### 📄 `app/agents/base.py`

**层级**：Agent 层（Agents） · **职责**：Agent 抽象基类 `BaseAgent`，定义 `run(state, context)` 与 `name` 标识

```python
"""
Agent抽象定义。
"""


from abc import ABC, abstractmethod



class BaseAgent(ABC):
    """
    Agent基础接口。
    """
    name: str

    @abstractmethod
    async def run(
        self,
        state,
        context
    ):
        """
        执行Agent任务。
        """

        pass
```

### 📄 `app/agents/planner.py`

**层级**：Agent 层（Agents） · **职责**：任务规划 Agent `PlannerAgent`（name=`planner`），读取 `state.data["query"]` 构造提示词，调用 `context.llm.chat()` 生成计划并写回 `state.data["plan"]`

```python
"""
任务规划Agent。
"""


from .base import BaseAgent



class PlannerAgent(BaseAgent):

    name="planner"

    async def run(
        self,
        state,
        context
    ):

        prompt = f"""
        用户需求:
        {state.data.get("query")}

        请生成分析计划。

        """
        result = await context.llm.chat(
            [
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        state.data[
            "plan"
        ] = result


        return state
```

### 📄 `app/agents/researcher.py`

**层级**：Agent 层（Agents） · **职责**：**空文件**（0 字节），预留的研究 Agent 占位

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/agents/critic.py`

**层级**：Agent 层（Agents） · **职责**：**空文件**（0 字节），预留的评审 Agent 占位

> 该文件为 **0 字节** 空文件，无源码内容。

### 📄 `app/agents/runtime.py`

**层级**：Agent 层（Agents） · **职责**：Agent 运行环境 `AgentRuntime`，持有 llm / tools / skills，`execute()` 把自身作为 context 传给 Agent 的 `run()`

```python
"""
Agent运行环境。
"""


class AgentRuntime:


    def __init__(
        self,
        llm,
        tools=None,
        skills=None
    ):

        self.llm = llm

        self.tools = tools or {}

        self.skills = skills or {}



    async def execute(
        self,
        agent,
        state
    ):

        result = await agent.run(
            state,
            self
        )


        return result
```

## 十三、LLM 能力层（LLM）

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

## 十四、工具层（Tools）

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

## 十五、项目分析层（Project Analysis）

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

## 十六、AI 能力层（Embeddings）

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

## 十七、向量存储层（Vector Store）

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

## 十八、数据库迁移层（Alembic）

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

## 十九、测试层（Tests）

单元测试与集成测试

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

---

## 二十、附录

### 空文件清单

以下 16 个文件均为 **0 字节**，其中绝大多数是用于将目录声明为 Python 包的标记文件：

| 文件路径 | 说明 |
|---|---|
| `app/__init__.py` | 包标记文件 |
| `app/agents/critic.py` | 预留占位，尚未实现 |
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

1. **`BaseNode` 重复定义**
   - `app/workflow/node.py::BaseNode` 与 `app/workflow/nodes/base.py::BaseNode` 是两个完全独立的同名类
   - 当前 `StartNode` / `EndNode` / `AnalysisNode` 继承前者，`AgentNode` / `ToolNode` / `SkillNode` / `HumanNode` 继承后者

2. **Skill 抽象缺失**
   - 仓库中还没有 `app/skills/` 包（`requirements.txt` 注释已描述该适配层）
   - `SkillNode` 已就位并调用 `skill.execute(state)`，等待 Skill 抽象基类补齐

3. **两个同名 `RepositoryRepository` 类**
   - `app/repositories/repository.py` — 全字段版，`create()` 内部 `commit()` + `refresh()`
   - `app/repositories/repository_basic.py` — 精简版，`create()` 只 `flush()`，事务由调用方掌控
   - 当前引用：`repository_service.py` 与 `test_repository_crud.py` 用全字段版；`analysis_service.py` 与 `repositories/__init__.py` 用精简版

4. **`WorkflowError` 有两份且错误码不同**
   - `app/core/exceptions.py::WorkflowError` — error_code 为 `WORKFLOW_ERROR`
   - `app/workflow/exceptions.py::WorkflowError` — 现继承 `ApplicationError`，error_code 为 `APPLICATION_ERROR`
   - 两者不是同一个类，各自的错误码不同

5. **文件名与类名不一致**
   - `app/project_analysis/code_chunker.py` 内部类为 `MarkdownChunker`
   - `app/project_analysis/project_indexer.py` 内部类为 `DocumentIndexer`

6. **`app/vector_store/qdrant.py` 的 `insert()` 方法**
   - 与 `upsert()` 功能重叠，仅 `RepositoryIndexer` 调用；`uuid` 导入专为此方法服务
   - 其 `PointStruct` 的 `id` 使用 UUID 字符串，而 `upsert()` 使用整数，两种 ID 类型混用

7. **两份重复的 GitHub URL 解析实现**
   - `app/services/analysis_service.py::_parse_github_url` — 基于字符串切分，不做域名校验
   - `app/tools/github/parser.py::parse_github_url` — 基于 `urlparse`，校验 `netloc == "github.com"` 并剥离 `.git` 后缀

8. **Workflow 引擎的行为边界**
   - 只把 `state.status == "PAUSED"` 视为暂停；`HumanNode` 设置的 `WAITING_HUMAN` 不会让引擎停下
   - 循环没有最大步数保护，编排中出现环会一直执行
   - `retry_count` 是 `state` 上的全局预算，不是每个节点独立计数

9. **未配置 `GITHUB_TOKEN` 时 Code Search 仍不可用**
   - `GitHubCodeSearchTool` 已支持自动带 `Authorization` 头，但 GitHub Code Search API 强制认证
   - 未配置 token 时真实调用会返回 401

10. **Phase 6 完成标准尚未全部达成**
   - 实施文档 §9.7 要求每个 Tool 具备「输入 Schema / 输出 Schema / 异常处理 / 日志 / 测试」
   - 当前 7 个 Tool 均未定义 Pydantic Schema，也均未接入 `app/core/logging.py`

---

*本文档由 `generate_project_code.py` 从工作区源文件直接读取生成：共收录 **83 段代码**（`app/` + `alembic/` + `tests/` 中的非空 `.py` 文件）。另有 16 个 0 字节空文件，见上方「空文件清单」。*
