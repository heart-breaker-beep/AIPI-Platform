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
import sys
from pathlib import Path
from typing import NamedTuple

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

KNOWN_ISSUES = """1. **`BaseNode` 重复定义**
   - `app/workflow/node.py::BaseNode` 与 `app/workflow/nodes/base.py::BaseNode` 是两个完全独立的同名类
   - 当前 `StartNode` / `EndNode` / `AnalysisNode` 继承前者，`AgentNode` / `ToolNode` / `SkillNode` / `HumanNode` 继承后者

2. **`app/main.py` 的模块级 `WorkflowContext` 装配不完整**
   - 该文件现已可正常导入（`from app import tools` 与 `create_skill_registry` 的名称都已对上）
   - 但文件末尾在**模块级**构造 `WorkflowContext`：`tools=tools` 传入的是 `app.tools` **模块对象**，
     而 `WorkflowContext.tools` 的注解是 `dict`；`agents={}` 也是空的，没有装配任何 Agent
   - 这段装配写在模块顶层且未接入任何启动流程，仍属于草稿

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
   - 暂停判定已扩展为 `PAUSED` / `WAITING_HUMAN` / `WAITING_DESIGN` 三态
     （`WorkflowEngine.PAUSE_STATUSES`），`HumanNode` 触发的暂停现在能被引擎识别
   - 主循环 `while current_node:` 仍没有最大步数保护，编排中出现环会一直执行
   - `retry_count` 是 `state` 上的全局预算，不是每个节点独立计数

9. **未配置 `GITHUB_TOKEN` 时 Code Search 仍不可用**
   - `GitHubCodeSearchTool` 已支持自动带 `Authorization` 头，但 GitHub Code Search API 强制认证
   - 未配置 token 时真实调用会返回 401

10. **Phase 6 完成标准尚未全部达成**
   - 实施文档 §9.7 要求每个 Tool 具备「输入 Schema / 输出 Schema / 异常处理 / 日志 / 测试」
   - 当前 7 个 Tool 均未定义 Pydantic Schema，也均未接入 `app/core/logging.py`

11. **Agent 接口已换代，`AgentNode` 未同步**
   - `BaseAgent` 已从 `run(state, context)` 改为 `execute(context, input_data)`，并改为持有 `skill_registry`
   - 全部 6 个领域 Agent 都已按新接口实现，`AgentRuntime.execute(agent_name, context, input_data)` 也已适配
   - 但 `app/workflow/nodes/agent_node.py` 仍在调用 `self.agent.run(state, context)`，属于旧接口残留

12. **Skill 内硬编码 Tool 名与实参不匹配**
   - 各 Skill 直接以 `context.tools["github_repository"]` 之类取工具，键名写死，缺键即 `KeyError`，没有降级或报错提示
   - `ArchitectureAnalysisSkill` 调用 `file_reader.execute(**input_data, path=file)`，但 `FileReaderTool.execute` 的形参是 `file_path`；且 `github_code_search` 需要 `keyword` / `repo`，与 `input_data` 不一定对得上
   - `ReportGenerationSkill` 调用 `exporter.execute(data=input_data)`，而 `ReportExportTool.execute` 的形参是 `title` / `content` / `filename`

13. **Skill 输出键名与 `CriticAgent` 校验字段不一致**
   - `SkillNode` 把每个 Skill 的结果写入 `state.data[node.name]`，即 `repository_analysis` / `architecture_analysis` / `technology_analysis`
   - `CriticAgent` 检查的却是 `repository` / `architecture` / `technology`，两者对不上，`passed` 会恒为 `False`
   - `PlannerAgent` 返回的 `tasks` 列表目前也没有任何代码消费，Workflow 尚未真正按计划驱动 Agent 执行

14. **证据链能力尚未对外暴露**
   - `app/evidence/`（Store / Verifier / Traceability）、`EvidenceService`
     与 `app/schemas/evidence.py` 均已实现并有测试覆盖
   - 但 `app/api/` 下没有任何证据相关路由，`app/main.py` 也未装配 `EvidenceService`，
     目前只能由测试或脚本直接调用，尚未形成可访问的接口"""



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
        KNOWN_ISSUES,
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


if __name__ == "__main__":
    sys.exit(main())
