# 后端 Bug / 冗余 / 分层修复 —— 执行提示词

> 用法：把本文件「提示词正文」整体交给编码 Agent 执行（例如在 Claude Code 里输入「按 docs/backend-fix-execution-prompt.md 执行」）。
> 来源：2026-10-12 后端代码审查。所有 `file:line` 基于审查时的工作区（目录已迁移到 `app/domain` + `app/infrastructure`，尚未提交），执行前先核对行号是否漂移。

---

## 提示词正文

你是本仓库（FastAPI + async SQLAlchemy + 自研 Workflow 引擎 + LLM Skills 的 GitHub 项目分析平台）的后端工程师。请按下面的阶段顺序修复全部问题。

### 全局约束

1. **先读后改**：每一项修改前先读相关文件，核对问题确实存在；行号若漂移，以代码语义为准。发现问题描述与代码不符时，停下来在汇报中说明，不要硬改。
2. **风格一致**：保持项目现有风格（中文 docstring / 注释解释"为什么"、纵向展开的调用格式、`get_logger`）。不引入新的第三方依赖。
3. **行为不变原则**：冗余清理、抽公共代码属于纯重构，API 响应结构和报告内容不能变化。
4. **每个阶段结束都要验证**，全部通过后单独提交一次（提交信息用中文 conventional commit，如 `fix(workflow): ...`）。验证命令：

   ```bash
   python -m pytest -q -p no:cacheprovider \
     --deselect tests/test_embedding_qdrant.py::test_embedding_to_qdrant \
     --deselect tests/test_indexer.py::test_document_indexer \
     --deselect tests/test_qdrant.py::test_qdrant_vector_search \
     --deselect tests/test_retrieval.py::test_semantic_retrieval
   python -m ruff check app --select F,B --ignore B008
   ```

   被 deselect 的 4 个测试依赖本地 Qdrant 服务，属于环境问题。基线：272 passed。每个阶段结束后 passed 数只能因"删除对应死代码的测试"而减少，并需在汇报中列出删了哪些。
5. **Bug 修复必须带回归测试**：先写能复现问题的失败测试，再修。
6. **不做的事**：不改前端 `app/static/`（除非字段变更必须同步）、不改 Docker 配置、不 `--no-verify`、不 force push。

### 第 0 阶段：建立基线

1. `git checkout -b fix/backend-review-2026-10-12`。
2. 当前工作区有一次未提交的大规模目录迁移（`app/agents`、`app/skills` 等 → `app/infrastructure/...`，新增 `app/domain/`）。先跑一遍验证命令确认 272 passed，然后 **把 `git status` 摘要给用户看，经用户同意后** 将迁移作为基线单独提交：`refactor: 迁移到 domain / infrastructure 分层`。只 `git add` `app/`、`alembic/`、`tests/`、`scripts/`、`docs/`、`GETTING_STARTED.md`。**不要**提交根目录的 `a.py`、`agent loop.py`、`test_request.json`（第 5 阶段单独处理）。

### 第 1 阶段：正确性 Bug（高优先级）

#### 1.1 启动时 `initial_data` 丢字段（重构回归）

- 现状：`app/services/analysis_service.py:190` 组装了完整的 `initial_data`（含 `run_id`/`owner`/`repo`/`rag_enabled`），但只把其中几个参数传给 `domain_service.start_analysis`；`app/domain/analysis/service.py:68` 又重新组装了一份，结果**丢了 `run_id`/`owner`/`repo`**，还把键名写成了 **`enable_rag`**，而读取方 `app/infrastructure/skills/evidence_analysis_skill.py:228` 和 `_to_response` 读的是 `rag_enabled`。后果：RAG 按次开关失效；首次 run 缺 owner/repo。
- 修复：
  - Domain `start_analysis` 签名改为 `start_analysis(run_id, repository_id, initial_data: dict)`，原样往下传，不再自己拼字典。Application 层负责组装唯一一份 `initial_data`。
  - 删掉 `app/domain/analysis/workflow.py` 中 approve / resume / retry 三处 `parse_github_url` 回填（约 106、174、223 行，均为 `except Exception: pass`）。换成**统一的身份字段补齐**：Orchestrator 的 approve/resume/retry 新增参数 `identity: dict`，执行 `state.data.update(identity)` 后保存 checkpoint，再交给 engine。`identity` 由 Application 层从数据库 `Repository` 行构造（`run_id`/`repository_id`/`repo_url`/`owner`/`repo`），写一个私有方法 `_identity_data(run, repository)` 复用，用于兼容早期缺字段的 checkpoint。
- 回归测试：`start` 后的首个 checkpoint `state.data` 必须包含 `owner`、`repo`、`run_id`、`rag_enabled`，且不包含 `enable_rag`；`enable_rag=True` 而全局 `RAG_ENABLED=False` 时，evidence skill 收到的 `rag_enabled` 为 True。
- 同步更新 `docs/bugfix-retry-missing-fields.md`：「根本原因」一节原先归因于 StateManager 瘦身，这是错误的（StateManager 从未删除这几个字段）。改为：重构时 Domain 层重新组装 initial_data 漏掉了字段；修复方式见 1.1。

#### 1.2 失败信息和重试次数没有同步到 run 表

- 现状：`app/services/analysis_service.py:1041` 用 `workflow_status == "failed"`（小写）判断，而常量是 `"FAILED"`；`data["error_message"]` 也没有任何代码写入。`AnalysisRun` 模型（`app/infrastructure/persistence/models/analysis_run.py`）**根本没有 `error_message` 列**。`retry_count` 也不再同步（旧版 `_sync_run` 是同步的）。
- 修复：
  - 给 `AnalysisRun` 加 `error_message: Mapped[str | None]`（`Text`，nullable），新建 alembic 迁移（`down_revision` 取当前 head，用 `alembic heads` 确认）。
  - `_sync_state_to_run` 改用已有但未使用的 `AnalysisRunRepository.update_runtime_state`（`analysis_run.py:80`），扩展参数 `error_message`。FAILED 时写 `state.errors[-1]`（截断到 2000 字符），非 FAILED 时清空。状态比较用 `WorkflowStatus` 常量。
  - `AnalysisResponse`（`app/schemas/analysis.py`）新增 `error_message: str | None = None`，`_to_response` 和 `list_analyses` 都要填。前端若已有错误展示位就顺带接上，没有则不改前端。
- 回归测试：节点抛异常后 run 的 `status=FAILED`，`error_message` 非空，`retry_count` 与 state 一致。

#### 1.3 checkpoint 只 flush 不 commit

- 现状：`CheckpointRepository.save`（`app/infrastructure/persistence/repositories/checkpoint.py:60`）只 `flush`；整条 workflow 在一个请求内同步执行，直到 `analysis_service.py:224` 才 commit。进程中途崩溃会丢失全部 checkpoint，其他请求也读不到进行中的状态。
- 修复：在 `CheckpointManager.save`（`app/infrastructure/workflow/checkpoint.py`）里，repository 保存完成后 `commit`。Repository 本身保持"只做数据访问"。session 配置了 `expire_on_commit=False`（`app/db/session.py:44`），commit 后 ORM 对象仍可用，但要确认 `create_analysis` 等流程在中途 commit 后仍正确。
- 注意：中途 commit 会把同一 session 里已 flush 的 evidence 一起提交，这是期望行为。在注释里写明。
- 回归测试：用一个统计 commit 次数的 fake session / repository，断言每个节点保存后都发生了 commit。

#### 1.4 checkpoint 大小保护漏掉了 `outputs`

- 现状：`finalizer_node.py:69-71`、`agent_node.py:51`、`synthesis_node.py:83` 把完整结果 `append` 进 `state.outputs`，但 `CheckpointManager.save` 只瘦身 `data`，完整报告仍会写进 `outputs` 列，可能再次触发 256KB asyncmy 读取失败（见 `state_manager.py` 顶部注释）。`state.outputs` 在业务上没有读取方（仅 checkpoint 存取）。
- 修复：
  - 参照 `plan_executor_node.py` 的 `_output_marker`，把它提到 `nodes/base.py`（或公共模块）作为共享函数，上述三个节点都改为只追加精简标记。
  - 兜底：`StateManager` 增加对 `outputs` 的整体大小检查。超过 `MAX_OUTPUTS_BYTES`（如 20_000）时，每项只保留 `agent`/`keys` 级别的标记。
- 回归测试：finalizer 产出 200KB 报告后，`checkpoint.save` 传给 repository 的 `outputs` 序列化后小于阈值。

#### 1.5 重试机制实际没生效

- 现状：
  - 整个 app 没有任何地方 `raise RetryableError`，`engine.py:225-240` 的自动重试只在测试中被触发。
  - `state.reset_retry()` 从未被调用，`retry_count` 是整个 run 共用的，且会跨 checkpoint 保留。
  - `engine.retry()`（约 311 行）只清空 `errors`，不重置 `retry_count`。
  - 重试之间没有退避。
- 修复：
  - 节点执行成功后 `state.reset_retry()`，让计数变成"每个节点"的。
  - `engine.retry()` 中 `state.retry_count = 0`，因为手动重试相当于重新给预算。
  - `_execute_node` 的重试分支加指数退避：`await asyncio.sleep(min(2 ** retry_count, 10))`。退避基数做成 `RetryPolicy` 的参数，测试里设为 0。
  - 把瞬时错误映射为 `RetryableError`，只处理这两处，不要大面积改：
    - `GitHubRepositoryTool`：`httpx.TimeoutException`、HTTP 429/502/503/504 改为 raise `RetryableError`（或让 `ToolError` 子类化出 `RetryableToolError(ToolError, RetryableError)`，以保持现有 `except ToolError` 仍能捕获。**优先这种方式**）。
    - `LLMChatTool` 目前把所有异常降级为 `available=False`，**保持不变**，因为技能层依赖这个降级契约。
  - 删除 `WorkflowState.max_retry` / `can_retry`，它们和 `RetryPolicy` 重复且无人调用。保留 `increase_retry` / `reset_retry`。
- 回归测试：节点第一次抛 `RetryableToolError`、第二次成功，最终 COMPLETED，下一个节点开始时 `retry_count == 0`；手动 retry 后 `retry_count == 0`。

#### 1.6 技能层 Bug

- `app/infrastructure/skills/architecture_analysis_skill.py:545`：读取失败的条目也占用 `MAX_STORED_MODULES`（8）名额，前 8 个都失败时一份真实源码都存不下。改为失败条目单独计数（或不计入 `modules` 容量），只有成功读取的才占名额。补测试。
- `app/infrastructure/skills/module_deep_dive_skill.py:309`：`get_tree` 未捕获 `ToolError`，一次超时就导致整个深挖失败；docstring 声称失败返回空列表。与 `architecture_analysis_skill.py:691-701` 保持一致（捕获 + 打日志 + 返回 `[]`）。这两份 `_load_tree` 会在第 4 阶段合并，此处先修行为并补测试。
- `app/infrastructure/skills/learning_path_skill.py:389`：`_core_files` 没有跳过带 `error` 的模块，会让 LLM 推荐它没读到的文件。参照 `report_synthesis_skill.py:741` 过滤掉。补测试。
- `app/infrastructure/skills/evidence_analysis_skill.py:147-190`：逐条 `create_evidence` 失败后继续使用同一个 session，flush 失败后 session 进入需回滚状态，后续写入（包括 checkpoint）会连锁失败。每条写入包在 `async with session.begin_nested():`（SAVEPOINT）里，失败只回滚该条。补测试（可用 SQLite 内存库或 mock 断言 `begin_nested` 被调用）。
- README 证据（`evidence_analysis_skill.py:416-427`）把整份 README 存进 DB 和 state，模块证据却截断到 `MAX_EVIDENCE_CHARS=1500`。README 证据同样截断到 `MAX_EVIDENCE_CHARS`。

#### 1.7 小问题

- `app/infrastructure/workflow/nodes/start_node.py:23` 设置的 `"RUNNING"` 不是 `WorkflowStatus` 常量，改为 `WorkflowStatus.ANALYZING`；`end_node.py:23`、`human_node.py:37` 的字符串字面量改用常量。确认 `_sync_state_to_run` 的映射表不再需要兜底未知状态。
- `QdrantSearchTool.search`（`app/infrastructure/tools/qdrant_search_tool.py:44`）不带 `repository_id` 过滤，存在跨仓库串数据风险。该路径实际已死（见 3.2），在 3.2 中随之删除；若决定保留，则必须加 `repository_id` 过滤。

### 第 2 阶段：资源与阻塞

- `app/infrastructure/tools/llm_chat_tool.py:67`：每次 `execute` 都新建 `AsyncOpenAI` 且从不关闭，每次 LLM 调用泄漏一个连接池。改为在工具实例上惰性创建并缓存 `self._llm`（已有 `self._llm` 字段，复用它），并提供 `async def aclose()`。
- 同步阻塞 IO 放到线程里执行（`await asyncio.to_thread(...)`），不要换库：
  - `app/infrastructure/tools/rag_retrieval_tool.py:102-108`：同步 embed + `QdrantClient.query_points`，每个 run 6 次。
  - `app/infrastructure/tools/project/rag_indexer.py:143,151,180`：`_embed_and_store`、`upsert_many`、`delete_by_repository`。
  - `app/infrastructure/tools/report_export_tool.py:63,102`：`write_text`。
  - `app/infrastructure/tools/dependency_analyzer_tool.py:76`。
- `app/infrastructure/skills/evidence_analysis_skill.py:308-309` 自行 new `OllamaEmbedding()` / `QdrantVectorStore()`。改为从 `context.tools` 取已注册的实例（`rag_retrieval` 工具已持有这两个对象），不再每次调用重建。
- `app/infrastructure/workflow/context_factory.py:61` 的 `_context_cache` 按工厂实例缓存，但工厂每次请求都会重建，缓存永远命中不了。删除这个缓存（不要改成全局单例，因为 context 持有 request 级 session）。在 FastAPI lifespan（`app/main.py`）中，为进程级可复用的无状态客户端（LLM client）提供关闭钩子；如果改动面过大，只做 LLM client 的复用，并在汇报中说明。
- 测试：`LLMChatTool` 连续调用两次只构造一次 client；`rag_retrieval_tool` 的同步调用经由 `to_thread`（mock 断言即可）。

### 第 3 阶段：删除死代码

删除前，先对每个符号在 `app/ tests/ scripts/ alembic/` 全量 grep，确认引用情况与下表一致。若某一项出现了表中未列出的引用，**保留该项**并在汇报中说明。

#### 3.1 无任何引用 → 直接删

| 位置 | 内容 |
|---|---|
| `app/infrastructure/workflow/nodes/analysis_node.py` | 整个文件（`workflow.py:42` 的注释一并更新） |
| `app/infrastructure/workflow/nodes/tool_node.py` | 整个文件 |
| `app/infrastructure/workflow/result.py` | `NodeResult` |
| `app/infrastructure/tools/project/repository_indexer.py` | 整个文件，连带 `QdrantVectorStore.insert`（`app/vector_store/qdrant.py:190`，它的唯一调用方） |
| `app/infrastructure/persistence/repositories/analysis_run.py:67` | `update_status`（`update_runtime_state` 在 1.2 中启用，保留） |
| `app/infrastructure/persistence/repositories/base.py:78,101` | `get_all`、`update` |
| 各 Repository 子类 | 只调用 `super()` 的 `get_by_id` 覆写 |
| `app/infrastructure/enrichment/context/manager.py:137` | `ContextManager._truncate` |
| `app/infrastructure/tools/__init__.py` | 未使用的 re-export |
| `app/infrastructure/workflow/state_manager.py:199-205` | 对 `evidence_analysis_agent` 的瘦身（该键已无写入方） |
| `app/infrastructure/persistence/repositories/*.py` | ruff F401 报出的未用 `AsyncSession` import |

#### 3.2 死路径 / 安全隐患 → 删

- `QdrantSearchTool` 及其注册（`context_factory.py:92`），以及 `evidence_analysis_skill.py` 中依赖 `input_data["query_vector"]` 的 `_from_qdrant` 分支。app 内没有代码写 `query_vector`，只有 `tests/test_evidence_skill.py` 构造了它。同步删除或改写对应测试。RAG 通路统一走 `RagRetrievalTool`。
- `MySQLQueryTool` 及其注册（`context_factory.py:93`）：无调用方，且能执行任意原始 SQL，删除。对应测试 `tests/test_mysql_query_tool.py` 一并删除。

#### 3.3 仅测试使用 → 删除代码与对应测试

- `SkillNode`（`nodes/skill_node.py`）及 `tests/test_skill_node.py`。若某些测试借用 `SkillNode` 来测其他东西，就改用 `AgentNode`。
- `NodeExecutionError`（`workflow/exceptions.py:14`）、`Workflow.get_node`（`workflow.py:81`）。
- `DocumentIndexer`（`tools/project/project_indexer.py`）及 `tests/test_indexer.py`、`tests/test_retrieval.py` 中仅针对它的用例。
- `StateManager.fit_state_data` / `_size` 及模块级 `MAX_STATE_BYTES`（`state_manager.py:24,274,287`）：测试改为直接调 `prepare_for_persistence` / `_estimate_size` / `StateManager.MAX_STATE_BYTES`。

#### 3.4 其他重复

- `EvidenceVerifier.validate_status`（`enrichment/evidence/verifier.py:31`）与 `EvidenceStore.validate_status`（`store.py:62`）完全相同，保留一份（放在 store），另一处改为调用它。
- `engine.py:221` 的 `except NonRetryableError: raise` 与 `RetryPolicy.is_retryable` 重复判断。去掉 engine 中这一分支，统一由 policy 判断。
- `CheckpointManager.save`（`checkpoint.py:43`）与 `StateManager.prepare_for_persistence`（`state_manager.py:107`）对同一份数据各 deepcopy 一次。保留 `CheckpointManager` 中的那次，`prepare_for_persistence` 增加参数 `copy: bool = True`，由 manager 传 `False`。

### 第 4 阶段：技能层去重（纯重构，报告输出不得变化）

先为下面涉及的技能补「输出快照」测试：固定 fake LLM 返回值和 fake tool，断言 `result` 字典完全相等。重构后快照必须一致。

1. 新建 `app/infrastructure/skills/_common.py`，收拢以下内容：
   - `as_text_list(value, *, max_items, max_chars)`：合并 `module_deep_dive_skill.py:1205`、`learning_path_skill.py:608`、`report_synthesis_skill.py:905` 的三份 `_as_text_list`。三者只是上限参数不同，通过参数保留原值。
   - `load_tree(tool, owner, repo, branch)`：合并 `architecture_analysis_skill.py:661` 与 `module_deep_dive_skill.py:285`，采用 1.6 修复后的容错行为。
   - `SOURCE_EXTENSIONS`、`SKIP_PATH_PATTERNS` 等重复常量（`architecture_analysis_skill.py:230/273`、`module_deep_dive_skill.py:399/424`）。合并时**取并集**，并检查结果是否改变两边的筛选，若改变就保留各自差异部分。
   - 六维度元组和标题：`report_synthesis_skill.py:86-103`、`module_deep_dive_skill.py:95` 改为引用 `AnalysisFocus.DIMENSIONS` / `TITLES`。
   - `HISTORY_RULES` 提示词片段：`report_synthesis_skill.py:258-266` 与 `learning_path_skill.py:433-441` 逐字相同。
   - `export_markdown(...)`、`unavailable_result(...)`、`readme_excerpt(...)`、`project_overview(...)` 等重复辅助函数（`_export`、`_unavailable`、`_readme`、`_project_overview`，位置见审查报告）。
   - evidence 映射成 facts 的逻辑（`report_synthesis_skill.py:598-670`、`module_deep_dive_skill.py:668-710`、`learning_path_skill.py:358-369`）。
2. 新建 `LLMSkillBase(BaseSkill)`，模板方法 `_call_llm(context, input_data, *, system, facts, instruction) -> dict | None` 封装通用流程：取 `llm_chat` 工具、构建 history 块、拼两条 message、检查 `available`、`parse_json_object`、失败时返回 unavailable。`report_synthesis`、`learning_path`、`module_deep_dive` 改为继承它。`planner_agent.py:170-204` 也可复用 `_call_llm`，但它是 Agent 不是 Skill，用组合方式（调用模块级函数）而不是继承。
3. 删除只做转发的 `_parse` 包装（`module_deep_dive_skill.py:1192`、`report_synthesis_skill.py:817`），直接调用 `parse_json_object`。
4. 统一 `_build_prompt` 的 `json.dumps` 参数（`ensure_ascii=False, default=str`）。

### 第 5 阶段：架构分层对齐

目标：依赖方向单向且可验证：`api → services(Application) → domain → infrastructure`。Infrastructure 不得反向 import `app.services` / `app.api` / `app.domain`。

1. **消除 Infrastructure → Services 的反向依赖**
   - `app/infrastructure/skills/evidence_analysis_skill.py:16` import 了 `app.services.evidence_service.EvidenceService`。`EvidenceService` 对 `store/verifier/traceability` 几乎是纯透传，所以 skill 改为直接使用 `app/infrastructure/enrichment/evidence/` 下的 store。`EvidenceService` 若因此没有生产调用方（只剩 `tests/test_evidence_service.py`），就删掉它，测试迁移到 store。
   - `ReportService.build_document`（`app/services/report_service.py`）是纯数据变换，并且被 `report_generation_skill.py:192` 反向 import；`report_service.py:447` 又反向 import `ReportGenerationSkill`，形成循环。把 `ReportService` 移到 `app/infrastructure/reporting/report_document.py`（类名保持不变），`app/services/report_service.py` 删除，调用方（`analysis_service.py:694`、`report_generation_skill.py`、`tests/test_phase14.py`）改 import 路径。确认移动后不再需要函数内延迟 import。
2. **应用层不再绕过领域层**
   - `app/services/analysis_service.py` 直接使用了 `CheckpointRepository`（`_to_response`）和 `select(Repository)`（`list_analyses`）。前者改为通过 domain service 的 `get_analysis_state`；后者在 `RepositoryRepository` 增加 `get_many(ids)`，替换内联查询。
   - `ModuleDeepDiveSkill.MODULES` 的校验：模块列表移到 `app/domain/analysis/` 下作为领域常量（如 `constants.py` 的 `DEEP_DIVE_MODULES`），skill 和 application service 都从这里引用。
   - 读磁盘报告（`AnalysisWorkflowOrchestrator.get_report_from_disk` / `get_json_report_path`，以及 `analysis_service.get_report_json` 里的 `json.loads(Path(...).read_text())`）属于 IO，移到 `app/infrastructure/reporting/report_store.py`（`ReportStore` 类，`reports` 目录作为构造参数）。由 factory 注入 domain service，domain 层不再 import `pathlib`。
3. **Domain 层依赖倒置做实（文档说的就要做到）**
   - 新建 `app/domain/analysis/ports.py`，用 `typing.Protocol` 定义 `WorkflowEnginePort`、`CheckpointPort`、`ContextFactoryPort`、`RunRepositoryPort`、`ReportStorePort`，只声明 domain 实际调用到的方法。
   - `domain/analysis/workflow.py`、`service.py` 的构造参数加上这些 Protocol 类型注解，删除 `from app.infrastructure...` 的 import（`WorkflowState` 的创建通过注入的 `state_factory` 或 engine 提供的工厂方法完成）。`parse_github_url` 的 import 随 1.1 的回填删除一起消失。
   - `app/domain/analysis/factory.py` 是组合根（composition root），允许 import infrastructure。把它移到 `app/services/` 或 `app/bootstrap.py`，让 `app/domain/` 目录本身零 infrastructure 依赖。
   - 更新 `app/domain/__init__.py`、`app/infrastructure/__init__.py` 的 docstring，如实描述依赖方向。
4. **透传层处理**：用户之前决定保留 domain service（`app/domain/analysis/service.py`）。本阶段**保留**它，但必须把 1.1 中"两层各拼一次参数"的问题彻底消除：domain service 只做转发 + 业务规则，不再重复组装数据。
5. **加一道分层守卫测试** `tests/test_layering.py`：用 `ast` 扫描源码 import，断言：
   - `app/infrastructure/**` 不 import `app.services` / `app.api` / `app.domain`
   - `app/domain/**` 不 import `app.infrastructure` / `app.services` / `app.api` / `sqlalchemy`
   - `app/api/**` 只 import `app.services`、`app.schemas`、`app.db`、`app.core`
6. **根目录杂项**：`a.py`、`agent loop.py`、`test_request.json` 是试验脚本，不属于后端。先列给用户确认，再删除或移到 `scripts/playground/`。`a.py` 和 `agent loop.py` 读取了 `.env` 中的密钥变量，**不要**把它们的内容输出到汇报中。

### 第 6 阶段：收尾

1. 完整跑一遍验证命令，并 `python -c "import app.main"` 确认应用能导入。若本地 MySQL 可用，执行 `alembic upgrade head` 验证新迁移；若不可用，在汇报中说明未验证。
2. 更新记忆文件 `aipi-code-redundancy.md`：把 2026-10-12 那一节标为"已修复"，记录保留下来的取舍。
3. 汇报格式（中文，简洁）：
   - 每个阶段：改了什么、新增了哪些测试、删了哪些文件或测试
   - 最终测试数字（passed / deselected）与 ruff 结果
   - 与本提示词不一致或没有做的项，以及原因
   - 需要用户手动验证的点（例如前端 RAG 开关、真实 GitHub 仓库端到端跑一次）

---

## 附：问题与阶段对照

| 编号 | 问题 | 阶段 |
|---|---|---|
| B1 | initial_data 丢 owner/repo/run_id，`enable_rag` 键名错 | 1.1 |
| B2 | error_message 从不落库，大小写判断错，retry_count 未同步 | 1.2 |
| B3 | checkpoint 只 flush 不 commit | 1.3 |
| B4 | `state.outputs` 未瘦身 | 1.4 |
| B5 | 重试从不触发，计数不重置，无退避 | 1.5 |
| B6 | 技能层：失败模块占名额、`get_tree` 未容错、`core_files` 含失败文件、session 连锁失败 | 1.6 |
| B7 | LLM client 泄漏、async 内同步阻塞 | 2 |
| R1 | 死代码 / 仅测试使用 / 危险工具 | 3 |
| R2 | 技能间约 450~500 行复制 | 4 |
| L1 | infrastructure → services 反向依赖与循环 import | 5.1 |
| L2 | 应用层绕过领域层，IO 放在 domain | 5.2 |
| L3 | "依赖倒置"只写在文档里 | 5.3 |
