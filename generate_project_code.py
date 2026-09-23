"""生成 PROJECT_CODE.md。

扫描工作区源码，按分层结构输出「目录树 + 逐文件完整源码」文档。
源码内容直接从源文件读取，不做任何改写。

用法:
    python generate_project_code.py
"""

from __future__ import annotations

import sys
from pathlib import Path

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

# 章节定义：(章节标题, 章节说明, [文件相对路径])
SECTIONS: list[tuple[str, str, list[str]]] = [
    (
        "二、入口层",
        "FastAPI 应用装配：日志、异常处理、路由挂载",
        ["app/main.py"],
    ),
    (
        "三、API 层",
        "HTTP 路由定义，负责接收请求、注入数据库 Session、调用 Service",
        ["app/api/v1/analysis.py"],
    ),
    (
        "四、数据契约层（Schemas）",
        "接口的请求体与响应体定义，被 API 层与 Service 层共同引用",
        [
            "app/schemas/analysis.py",
            "app/schemas/error.py",
        ],
    ),
    (
        "五、业务服务层（Services）",
        "业务编排：校验入参、组合 DAO 与工具层、掌控事务边界",
        [
            "app/services/analysis_service.py",
            "app/services/repository_service.py",
        ],
    ),
    (
        "六、数据访问层（Repositories）",
        "表级别的数据访问对象（DAO），只负责 SQL 与对象映射",
        [
            "app/repositories/__init__.py",
            "app/repositories/repository.py",
            "app/repositories/repository_basic.py",
            "app/repositories/analysis_run.py",
        ],
    ),
    (
        "七、数据模型层（Models）",
        "SQLAlchemy ORM 表结构定义",
        [
            "app/models/__init__.py",
            "app/models/repository.py",
            "app/models/analysis_run.py",
            "app/models/analysis_task.py",
        ],
    ),
    (
        "八、数据库层（DB）",
        "ORM 基类与异步 Engine / Session 管理",
        [
            "app/db/base.py",
            "app/db/session.py",
        ],
    ),
    (
        "九、核心基础设施层（Core）",
        "配置、日志、异常体系与全局异常处理器，贯穿所有分层",
        [
            "app/core/config.py",
            "app/core/exceptions.py",
            "app/core/error_handlers.py",
            "app/core/logging.py",
        ],
    ),
    (
        "十、Workflow 层（Workflow）",
        "自研工作流引擎：状态、上下文、节点、流转、重试、检查点与执行引擎",
        [
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
        ],
    ),
    (
        "十一、Workflow 节点层（Workflow Nodes）",
        "各类节点的具体实现：开始 / 结束 / 分析 / Agent / Tool / Skill / 人工审核",
        [
            "app/workflow/nodes/base.py",
            "app/workflow/nodes/start_node.py",
            "app/workflow/nodes/end_node.py",
            "app/workflow/nodes/analysis_node.py",
            "app/workflow/nodes/agent_node.py",
            "app/workflow/nodes/tool_node.py",
            "app/workflow/nodes/skill_node.py",
            "app/workflow/nodes/human_node.py",
        ],
    ),
    (
        "十二、Agent 层（Agents）",
        "Agent 抽象接口、运行环境，以及 Planner 等具体 Agent",
        [
            "app/agents/base.py",
            "app/agents/planner.py",
            "app/agents/researcher.py",
            "app/agents/critic.py",
            "app/agents/runtime.py",
        ],
    ),
    (
        "十三、LLM 能力层（LLM）",
        "大模型调用的抽象接口与 DeepSeek 实现",
        [
            "app/llm/base.py",
            "app/llm/deepseek.py",
        ],
    ),
    (
        "十四、工具层（Tools）",
        "Tool 抽象基类与具体工具：文件读取、代码搜索、依赖分析、语义检索、数据库查询与报告导出",
        [
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
        ],
    ),
    (
        "十五、项目分析层（Project Analysis）",
        "文档切分、向量索引构建",
        [
            "app/project_analysis/code_chunker.py",
            "app/project_analysis/project_indexer.py",
            "app/project_analysis/repository_indexer.py",
        ],
    ),
    (
        "十六、AI 能力层（Embeddings）",
        "文本向量化的抽象接口与 Ollama 本地实现",
        [
            "app/embeddings/base.py",
            "app/embeddings/ollama.py",
        ],
    ),
    (
        "十七、向量存储层（Vector Store）",
        "Qdrant Collection 管理、向量写入与相似度检索",
        ["app/vector_store/qdrant.py"],
    ),
    (
        "十八、数据库迁移层（Alembic）",
        "Alembic 异步运行环境与版本化迁移脚本",
        [
            "alembic/env.py",
            "alembic/versions/479571222143_create_initial_analysis_tables.py",
        ],
    ),
    (
        "十九、测试层（Tests）",
        "单元测试与集成测试",
        [
            "tests/test_analysis_api.py",
            "tests/test_chunker.py",
            "tests/test_config.py",
            "tests/test_database.py",
            "tests/test_dependency_analyzer_tool.py",
            "tests/test_embedding.py",
            "tests/test_embedding_qdrant.py",
            "tests/test_exceptions.py",
            "tests/test_github_client.py",
            "tests/test_github_code_search_tool.py",
            "tests/test_github_parser.py",
            "tests/test_indexer.py",
            "tests/test_mysql_query_tool.py",
            "tests/test_qdrant.py",
            "tests/test_qdrant_search_tool.py",
            "tests/test_report_export_tool.py",
            "tests/test_repository_crud.py",
            "tests/test_repository_pipeline.py",
            "tests/test_repository_service.py",
            "tests/test_retrieval.py",
            "tests/test_tools.py",
            "tests/test_workflow.py",
        ],
    ),
]

# 每个文件的「层级」与「职责」
DESCRIPTIONS: dict[str, tuple[str, str]] = {
    # 入口层
    "app/main.py": (
        "入口层",
        "FastAPI 应用初始化、日志初始化、全局异常注册、路由挂载",
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
    # 业务服务层
    "app/services/analysis_service.py": (
        "业务服务层（Services）",
        "Analysis 任务的业务编排——校验 URL、创建或复用 Repository、创建 Analysis Run 并提交事务",
    ),
    "app/services/repository_service.py": (
        "业务服务层（Services）",
        "Repository 查询 / 创建 / GitHub 数据同步。依赖工具层的 `GitHubRepositoryTool` 与 `parse_github_url`",
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
        "Skill 节点 `SkillNode`，封装 Skill 调用并把结果追加到 `state.outputs`",
    ),
    "app/workflow/nodes/human_node.py": (
        "Workflow 节点层",
        "HITL 人工审核节点 `HumanNode`（name=`human_review`），把 status 置为 WAITING_HUMAN 以暂停流程",
    ),
    # Agent 层
    "app/agents/base.py": (
        "Agent 层（Agents）",
        "Agent 抽象基类 `BaseAgent`，定义 `run(state, context)` 与 `name` 标识",
    ),
    "app/agents/planner.py": (
        "Agent 层（Agents）",
        "任务规划 Agent `PlannerAgent`（name=`planner`），读取 `state.data[\"query\"]` 构造提示词，调用 `context.llm.chat()` 生成计划并写回 `state.data[\"plan\"]`",
    ),
    "app/agents/researcher.py": (
        "Agent 层（Agents）",
        "**空文件**（0 字节），预留的研究 Agent 占位",
    ),
    "app/agents/critic.py": (
        "Agent 层（Agents）",
        "**空文件**（0 字节），预留的评审 Agent 占位",
    ),
    "app/agents/runtime.py": (
        "Agent 层（Agents）",
        "Agent 运行环境 `AgentRuntime`，持有 llm / tools / skills，`execute()` 把自身作为 context 传给 Agent 的 `run()`",
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
}

# 测试层描述
TEST_DESCRIPTIONS: dict[str, str] = {
    "tests/test_analysis_api.py": "API 端到端测试（健康检查、创建任务、查询任务、参数校验、404 场景）",
    "tests/test_chunker.py": "Markdown 切分器单元测试",
    "tests/test_config.py": "配置加载单元测试",
    "tests/test_database.py": "MySQL 连接连通性测试（需数据库可用）",
    "tests/test_dependency_analyzer_tool.py": "依赖分析工具测试（解析本项目，断言 frameworks 字段存在）",
    "tests/test_embedding.py": "Ollama Embedding 单元测试（需 Ollama 服务可用）",
    "tests/test_embedding_qdrant.py": "Embedding → Qdrant 写入 → 语义检索集成测试",
    "tests/test_exceptions.py": "异常体系单元测试",
    "tests/test_github_client.py": "GitHub REST API 工具测试（需外网可用）",
    "tests/test_github_code_search_tool.py": "GitHub 源码搜索工具测试（fake client + fake settings，覆盖返回结果与 token 认证头）",
    "tests/test_github_parser.py": "GitHub URL 解析单元测试",
    "tests/test_indexer.py": "DocumentIndexer 集成测试（Chunk → Embedding → Qdrant）",
    "tests/test_mysql_query_tool.py": "MySQL 查询工具测试（FakeSession 模拟查询结果）",
    "tests/test_qdrant.py": "Qdrant 向量存储层单元测试（造数据 → 检索 → 断言排序）",
    "tests/test_qdrant_search_tool.py": "语义检索工具测试（FakeVectorStore 返回固定 payload）",
    "tests/test_report_export_tool.py": "报告导出工具测试（写出 Markdown 到 test_reports/）",
    "tests/test_repository_crud.py": "数据访问层测试（创建、按 URL 查、按 ID 查）；运行前会清理同 URL 残留记录以保证可重复运行",
    "tests/test_repository_pipeline.py": "端到端管道测试（Service 拉取仓库 → Indexer 建立索引）",
    "tests/test_repository_service.py": "业务服务层测试（不存在时创建、存在时复用）",
    "tests/test_retrieval.py": "语义检索测试（建立索引 → 用自然语言问题检索 → 断言命中）",
    "tests/test_tools.py": "工具层测试（`GitHubRepositoryTool` 取仓库、`FileReaderTool` 读文件）",
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
    ┌───────────────────────────┐   ┌─────────────────────────┐
    │  Agent 层  app/agents/    │   │  LLM 能力层  app/llm/    │
    │  BaseAgent / AgentRuntime │──▶│  BaseLLM / DeepSeekLLM  │
    └───────────────────────────┘   └─────────────────────────┘

    贯穿各层：app/core/（配置、日志、异常、异常处理器）
    数据契约：app/schemas/（被 API 层与 Service 层共同引用）
```"""

KNOWN_ISSUES = """1. **`BaseNode` 重复定义**
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
   - 当前 7 个 Tool 均未定义 Pydantic Schema，也均未接入 `app/core/logging.py`"""


def note_for(rel: str, is_dir: bool) -> str:
    """返回目录树中某一项的注释。"""

    if rel in TREE_NOTES:
        return TREE_NOTES[rel]

    if not is_dir and rel.endswith("__init__.py"):
        if (ROOT / rel).stat().st_size == 0:
            return "(空)"

    return ""


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

    for title, blurb, files in SECTIONS:
        body.append(f"## {title}")
        body.append("")
        body.append(blurb)
        body.append("")

        for rel in files:
            path = ROOT / rel

            if not path.exists():
                raise SystemExit(f"章节中声明的文件不存在: {rel}")

            layer, duty = DESCRIPTIONS.get(
                rel,
                ("测试层", TEST_DESCRIPTIONS.get(rel, "")),
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
        "## 二十、附录",
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
        KNOWN_ISSUES,
        "",
        "---",
        "",
        f"*本文档由 `generate_project_code.py` 从工作区源文件直接读取生成："
        f"共收录 **{blocks} 段代码**"
        f"（`app/` + `alembic/` + `tests/` 中的非空 `.py` 文件）。"
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


if __name__ == "__main__":
    sys.exit(main())
