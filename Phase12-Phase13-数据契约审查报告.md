# Phase 12 → Phase 13 数据契约审查报告

> **审查对象**：AI Agent / GitHub 开源项目智能分析平台（AIPI Platform）
> **审查主题**：Phase 12 到底应该向 Phase 13 输出什么数据
> **审查日期**：2026-09-29
> **审查性质**：**只读审查**。未修改任何生产代码、测试、数据库、Alembic migration，未提交 Git。
> **审查方法**：以当前工作区真实源码 + Phase 开发实施文档 + 项目设计文档为依据；所有结论均来自实际阅读源码与对真实数据库的只读查询，未按文件名推断功能。

---

## 目录

1. [审查范围](#1-审查范围)
2. [Phase 12 文档要求](#2-phase-12-文档要求)
3. [当前真实 Workflow 数据流](#3-当前真实-workflow-数据流)
4. [当前真实 Analysis Result 结构](#4-当前真实-analysis-result-结构)
5. [数据语义分类](#5-数据语义分类)
6. [Phase 13 十维数据契约矩阵](#6-phase-13-十维数据契约矩阵)
7. [Agent 维度专项结论](#7-agent-维度专项结论)
8. [Workflow 维度专项结论](#8-workflow-维度专项结论)
9. [Skill / Tool / Memory / Extension 专项结论](#9-skill--tool--memory--extension-专项结论)
10. [RAG 专项结论](#10-rag-专项结论)
11. [Evidence 专项结论](#11-evidence-专项结论)
12. [Phase 13 当前实现审查](#12-phase-13-当前实现审查)
13. [真实 COMPLETED Run 验证结果](#13-真实-completed-run-验证结果)
14. [Phase 12 → Phase 13 契约缺口](#14-phase-12--phase-13-契约缺口按严重程度)
15. [最小修复路径](#15-最小修复路径方案不实施)
16. [当前 Phase 13 完成度判断](#16-当前-phase-13-完成度判断)
17. [附录 A：八个必答问题](#附录-a八个必答问题)
18. [附录 B：复核方法](#附录-b复核方法可复现)

---

## 1. 审查范围

### 1.1 文档（实际阅读的章节）

| 文档 | 章节 |
|---|---|
| `AI-Agent-GitHub-Project-Intelligence-Platform-详细Phase开发实施文档.md` | `15. Phase 12 —— 第一个完整业务闭环`（15.1 用户输入 / 15.2 完整执行 / 15.3 第一版报告）、`16. Phase 13 —— 多项目比较`（16.1 目标 / 16.2 流程 / 16.3 比较维度） |
| `AI-Agent-GitHub-Project-Intelligence-Platform-项目设计文档.md` | `3.1 场景 A：分析一个 GitHub Agent 项目`、`3.2 场景 B：多个 GitHub Agent 项目横向比较`、`6.1 Agent 层：核心 5 个 Agent`、`6 系统架构分层` |

### 1.2 源码（实际打开阅读）

```
app/api/v1/analysis.py
app/api/v1/comparison.py
app/services/analysis_service.py
app/services/analysis_workflow.py
app/services/repository_service.py
app/services/evidence_service.py
app/services/comparison_service.py
app/workflow/analysis_workflow.py
app/workflow/engine.py
app/workflow/state.py
app/workflow/checkpoint.py
app/workflow/nodes/{start_node, agent_node, design_gate_node, plan_executor_node,
                   human_node, finalizer_node, end_node}.py
app/agents/{base, planner_agent, repository_analysis_agent, architecture_analysis_agent,
            technology_analysis_agent, evidence_analysis_agent, critic_agent,
            agent_registry, comparison_agent}.py
app/skills/{repository_analysis_skill, architecture_analysis_skill, technology_analysis_skill,
            evidence_analysis_skill, report_generation_skill, registry}.py
app/tools/{github/github_repository_tool, github/github_code_search_tool, file_reader_tool,
           dependency_analyzer_tool, qdrant_search_tool, mysql_query_tool, report_export_tool}.py
app/memory/{run_memory, project_memory, manager}.py
app/context/manager.py
app/repositories/checkpoint.py
app/models/{repository, checkpoint}.py
app/schemas/comparison.py
```

### 1.3 真实数据库（只读查询，未修改）

- 表：`analysis_runs` / `repositories` / `evidences` / `checkpoints`
- 真实 run：
  - **Run A** = `d1d71c3e-a9b6-4073-8d3d-bbbfe0b11005`（`adityamhaske/Multi-Agent-Research-Assistant`）
  - **Run B** = `799049b1-3d51-4c2f-bbe5-81930ce59a23`（`smlfy/enterprise-workflow-agent-platform?utm_source=chatgpt.com`）

### 1.4 基准状态

- `pytest -q` → **127 passed**
- comparison 相关测试 → **33 passed**

> 注意：测试全绿**不能**证明 Phase 12 → Phase 13 的数据契约正确，这正是本报告要说明的问题（例如 `ReportGenerationSkill` 的硬编码段落从未被任何测试约束）。

---

## 2. Phase 12 文档要求

### 2.1 详细实施文档

**15.1 用户输入**（原文）要求重点分析 7 项：

```text
1. Multi-Agent
2. Workflow
3. Skill
4. Tool
5. RAG
6. Memory
7. 数据库
```

**15.2 完整执行**流程中包含一行**独立步骤**：

```text
User
 ↓
POST /analysis
 ↓
Analysis Run
 ↓
Planner Agent
 ↓
Research Plan
 ↓
Design Gate
 ↓
Human Approve
 ↓
Project Agent
 ↓
Technology Agent
 ↓
Code Architecture Agent
 ↓
Agent / Workflow / Skill / Tool Analysis      ← 独立步骤
 ↓
Evidence
 ↓
Critic
 ↓
Retry（如果需要）
 ↓
Synthesis
 ↓
Human Review
 ↓
Final Report
 ↓
COMPLETED
```

**15.3 第一版报告**必须至少包含 12 节：

```text
项目概览 / 技术栈 / 目录结构 / Agent架构 / Workflow / Skill
/ Tool / RAG / Memory / 数据库 / 关键源码 / Evidence
```

### 2.2 项目设计文档

- **3.1 场景 A**：要求回答 `项目是干什么的` / `技术栈` / `Agent 有哪些` / `Workflow 怎么运行` / `Tool、Skill 怎么调用` / `Memory、RAG 怎么实现` / `完整流程`
- **3.2 场景 B（多项目比较）** 的流程图，是本次审查最关键的文档依据：

```text
统一分析维度
    ↓
各项目独立分析
    ↓
技术事实标准化
```

> **「统一分析维度 + 技术事实标准化」就是 Phase 13 需要的输入契约。** 文档在设计阶段就要求存在一个「标准化后的技术事实」结构，而不是把原始执行状态直接交给下游。

- **6.1 Agent 层**：`核心 Agent 控制为 5 个` —— Requirement & Planner / Project / Technology / Code & Architecture / Synthesis & Critic

### 2.3 「哪些是结构化 Analysis Result 要求」

| 要求 | 文档出处 | 性质 | 应成为结构化 Analysis Result？ |
|---|---|---|---|
| Agent（项目有哪些 Agent） | 15.1 + 15.3 + 3.1 | 明确分析要求 | **是** |
| Workflow（项目 Workflow 怎么运行） | 15.1 + 15.3 + 3.1 | 明确分析要求 | **是** |
| Skill（项目 Skill 怎么调用） | 15.1 + 15.3 + 3.1 | 明确分析要求 | **是** |
| Tool（项目 Tool 怎么调用） | 15.1 + 15.3 + 3.1 | 明确分析要求 | **是** |
| RAG（项目 RAG 怎么实现） | 15.1 + 15.3 + 3.1 | 明确分析要求 | **是** |
| Memory（项目 Memory 怎么实现） | 15.1 + 15.3 + 3.1 | 明确分析要求 | **是** |
| 数据库 | 15.1 + 15.3 + 3.1 | 明确分析要求 | **是**（已实现） |
| 部署方式 | 3.2 第 9 项 | 明确分析要求 | **是**（已实现结构） |
| 代码复杂度 | 仅 Phase 13 16.3 | 派生指标 | 应为派生 |
| 扩展方式 | 仅 Phase 13 16.3 | 派生指标 | 应为派生 |
| 项目概览 / 技术栈 / Evidence | 15.3 | 报告展示 | **是** |
| 目录结构 / 关键源码 | 15.3 | 报告展示 | 可留在报告层 |

**核心判定**：Agent / Workflow / Skill / Tool / RAG / Memory 六项在 **15.1 用户输入、15.3 报告结构、3.1 场景 A** 三处均被明确要求，且 15.2 有独立流程步骤 —— **它们不是「报告展示」要求，而是明确的分析要求**。

---

## 3. 当前真实 Workflow 数据流

```text
POST /api/v1/analysis
  └─ app/api/v1/analysis.py :: create_analysis
     └─ app/services/analysis_service.py :: analysis_service.create_analysis          (:39)
        ├─ _parse_github_url(url)                                                    (:449)
        │     ⚠️ 只 strip ".git"，不 strip "?query"
        ├─ RepositoryService.get_or_create                                          (:43)
        │     ⚠️ 命中已存在行 → 直接 return（:66-67），永不回填 metadata
        └─ AnalysisRunRepository.create
           └─ AnalysisWorkflowRunner.start                                         (:167)
              ├─ build_context()                                                    (:101)
              │     注册 7 个 Tool + SkillRegistry + AgentRegistry
              │     + MemoryManager + ContextManager(retriever=None)
              ├─ build_analysis_workflow(context)
              │     app/workflow/analysis_workflow.py                               (:38)
              └─ WorkflowEngine.run()      app/workflow/engine.py                   (:44)
                 │
                 ├─ StartNode            → state.status = "RUNNING"
                 ├─ AgentNode("planner_agent")
                 │     └─ PlannerAgent.execute   app/agents/planner_agent.py        (:24)
                 │           tasks = [5 个硬编码 Agent 名]        ← 无 LLM 参与
                 │           research_plan = {plan_version, analysis_type,
                 │                            question, tasks, evidence_required}
                 ├─ DesignGateNode       → WAITING_DESIGN 暂停 + checkpoint
                 │     ↓ POST /analysis/{id}/approve → engine.resume
                 ├─ PlanExecutorNode.execute
                 │     app/workflow/nodes/plan_executor_node.py                     (:29)
                 │       for agent_name in state.data["planner_agent"]["tasks"]:
                 │           agent_input = dict(state.data)   (+ _context)
                 │           result = await context.agents[agent_name].execute(...)
                 │           state.data[agent_name] = result
                 │           state.data.update(result)      ← 结果被"拍平"合并进 state.data
                 │       state.data["executed_tasks"] = executed_tasks
                 │       │
                 │       ├─ RepositoryAnalysisAgent → RepositoryAnalysisSkill
                 │       │     → GitHubRepositoryTool + FileReaderTool
                 │       ├─ ArchitectureAnalysisAgent → ArchitectureAnalysisSkill
                 │       │     → GitHubCodeSearchTool(keyword="class") + FileReaderTool
                 │       ├─ TechnologyAnalysisAgent → TechnologyAnalysisSkill
                 │       │     → FileReaderTool ×5 配置文件
                 │       ├─ EvidenceAnalysisAgent → EvidenceAnalysisSkill
                 │       │     → EvidenceService（写 evidences 表）
                 │       └─ CriticAgent
                 │             app/agents/critic_agent.py                           (:30-58)
                 │             ⚠️ 只校验 3 个 key 存在性
                 ├─ HumanNode            → WAITING_HUMAN 暂停 + checkpoint
                 │     ↓ POST /analysis/{id}/approve → engine.resume
                 ├─ FinalizerNode.execute
                 │     app/workflow/nodes/finalizer_node.py                         (:29)
                 │       └─ ReportGenerationSkill.execute → _build_report()
                 │            └─ ReportExportTool.export_markdown
                 │                 → reports/{run_id}_analysis.md
                 │       state.data["final_report"] = {"report": {...}, "content": md}
                 └─ EndNode              → COMPLETED
                       └─ WorkflowEngine._save → CheckpointManager.save
                            → CheckpointRepository.save
                            → checkpoints.state_data（MySQL JSON 列，每个节点后写一版）

RunMemory.load(run_id)             app/memory/run_memory.py                         (:41)
  ├─ analysis_runs 行            → run_id / question / status / current_node
  ├─ repositories 行             → repository 摘要（⚠️ description/language 为 NULL）
  ├─ analysis_tasks 行           → task_results（⚠️ 实测恒为 []）
  ├─ checkpoints 最新版          → workflow_state{status, current_node, data,
  │                                 errors, retry_count, pause_reason,
  │                                 human_approved, checkpoint_version}
  │                              + research_plan / final_report / agent_outputs
  └─ evidences 行（按 repository）→ evidences[]

ComparisonService → ComparisonAgent      app/services/comparison_service.py        (:134)
```

---

## 4. 当前真实 Analysis Result 结构

### 4.1 `RunMemory.load()` 顶层 11 个 key（实测）

```python
['agent_outputs', 'current_node', 'evidences', 'final_report', 'question',
 'repository', 'research_plan', 'run_id', 'status', 'task_results', 'workflow_state']
```

**重要**：真实数据中**不存在 `project["analysis"]` 这个 key**。

### 4.2 `workflow_state.data` 的 25 个 key（实测 Run A）

| key | 类型 | size | 真实值摘要 |
|---|---|---|---|
| `architecture_analysis_agent` | dict | 2 | `{"files": [], "modules": []}` ← **空** |
| `files` / `modules` | list | 0 | `[]`（同上的拍平副本）← **空** |
| `count` | int | — | `1`（来自 evidence_analysis） |
| `critic_agent` | dict | 2 | `{"errors": [], "passed": true}` |
| `dependencies` | dict | 0 | `{}` ← **恒空**（远程模式不调用 dependency_analyzer） |
| `evidence` | list | 1 | README 全文对象 |
| `evidence_analysis_agent` | dict | 2 | `{"count": 1, "evidence": [...]}` |
| `executed_tasks` | list | 5 | **AIPI 的 5 个分析 Agent 名** |
| `final_report` | dict | 2 | `{"report": {...}, "content": markdown}` |
| `owner` / `repo` / `repo_url` / `repository_id` / `run_id` | — | — | Run 元数据 |
| `passed` | bool | — | `true`（critic） |
| `planner_agent` | dict | 2 | `{"tasks": [...], "research_plan": {...}}` |
| `question` | str | 75 | 用户提问 |
| `readme` | str | 14457 | 目标项目 README 全文 |
| `repository` | dict | **84** | **GitHub API 原始对象**（含 language / topics / size / description） |
| `research_plan` | dict | 5 | **AIPI 的研究计划** |
| `technology_analysis_agent` | dict | 1 | `{"technology_stack": {...}}` |
| `technology_stack` | dict | 6 | `{"llm":[], "database":["PostgreSQL"], "embedding":[], "deployment":[], "frameworks":[], "source_files":["docker-compose.yml"]}` |
| `errors` | list | 0 | — |

### 4.3 `agent_outputs` 真实形状（⚠️ 无 agent 名）

Run A（7 项）：

```text
[0] ['research_plan', 'tasks']                  ← planner_agent
[1] ['dependencies', 'readme', 'repository']    ← repository_analysis_agent
[2] ['files', 'modules']                        ← architecture_analysis_agent
[3] ['technology_stack']                        ← technology_analysis_agent
[4] ['count', 'evidence']                       ← evidence_analysis_agent
[5] ['errors', 'passed']                        ← critic_agent
[6] ['content', 'report']                        ← finalizer
```

Run B（8 项，多了一次重复的 `['dependencies','readme','repository']`）。

**这是位置型列表，每项不带 agent 名**，下游只能靠 key 形状反推归属。

---

## 5. 数据语义分类

> 这是本次审查的关键区分。**「有值」不等于「语义正确」。**

### 5.1 A 类 —— 被分析项目数据（描述目标 GitHub 项目）

| 字段 | 来源 | 真实性 |
|---|---|---|
| `workflow_state.data.repository` | GitHub REST `GET /repos/{owner}/{name}` | ✅ 84 个字段，含 `language` / `topics` / `size` / `description` |
| `...data.readme` | `FileReaderTool` 读目标项目 `README.md` | ✅ 14457 字符 |
| `...data.repository_analysis_agent` | 上述两者 + `dependencies` | ✅ |
| `...data.architecture_analysis_agent` / `files` / `modules` | `GitHubCodeSearchTool(keyword="class")` + `FileReaderTool` | ⚠️ 结构正确但**两份真实 run 实测均为空** |
| `...data.technology_analysis_agent` / `technology_stack` | `FileReaderTool` 读 5 个配置文件后关键词匹配 | ✅ 结构正确 |
| `...data.evidence` / `evidence_analysis_agent` | `EvidenceAnalysisSkill`（README 全文） | ✅ |
| `...data.dependencies` | 远程模式跳过 → `{}` | ⚠️ 恒空 |
| `project["repository"]`（DB 摘要） | `repositories` 表 | ⚠️ `description` / `language` / `default_branch` / `stars` / `forks` **全为 NULL** |
| `project["evidences"]`（DB 行） | `evidences` 表 | ✅ |

### 5.2 B 类 —— AIPI 自己的分析过程数据（**不是被分析项目**）

| 字段 | 说明 |
|---|---|
| `executed_tasks` | **AIPI 的 5 个分析 Agent 名**（`repository_analysis_agent` … `critic_agent`） |
| `research_plan` | **AIPI 生成的计划**（`PlannerAgent` 硬编码 5 步） |
| `planner_agent` | AIPI 的 Planner 输出 |
| `workflow_state.{status, current_node, errors, retry_count, human_approved, pause_reason, checkpoint_version}` | AIPI 的执行状态机状态 |
| `question` / `run_id` / `repository_id` | Run 元数据 |
| `owner` / `repo` / `repo_url` | Run 元数据（从 URL 解析） |
| `passed` / `count` / `errors` | Critic 与 Evidence Agent 的执行产物 |
| `final_report` | AIPI 生成的报告产物 |
| `agent_outputs` | AIPI 每次节点执行的**无名字位置型**输出列表 |
| `task_results` | `analysis_tasks` 表，**实测恒为 `[]`** |

> ⚠️ **判定：Phase 13 的 `Agent` 与 `Workflow` 两个维度当前所取的 `executed_tasks` 与 `research_plan`，均属 B 类。**

### 5.3 C 类 —— Evidence / 审计数据

| 字段 | 内容 |
|---|---|
| `project["evidences"][*]` | `id` / `source_type` / `source_url` / `file_path` / `line_start` / `line_end` / `content` / `verification_status` |
| `workflow_state.data.evidence[*]` | 同结构，但**多一个 `evidence_id`**（`EvidenceAnalysisSkill:134` 注入），与 DB 行的 `id` 是**同一值的两个字段名** |
| `final_report.report.path` | 报告文件路径，可回溯 |

---

## 6. Phase 13 十维数据契约矩阵

> 记法：✅ 语义正确　⚠️ 部分/近似　❌ 无数据或语义错误

| Phase 13 维度 | 文档要求 | 当前是否有**项目级**数据 | 当前真实字段 | 数据来源 | 是否可比较 | 是否有 Evidence | 问题 |
|---|---|---|---|---|---|---|---|
| **Agent** | 15.1/15.3/3.1：项目有哪些 Agent | ❌ **语义错误** | 现用 `executed_tasks`（B 类） | AIPI 管线 | 形式可比较，**恒 SAME** | ❌ | 无生产者；README 中有信号未提取 |
| **Workflow** | 15.1/15.3/3.1：项目 Workflow 怎么跑 | ❌ **语义错误** | 现用 `research_plan`（B 类） | AIPI 计划 | 形式可比较，**恒 SAME** | ⚠️ 靠 token 巧合 | 同上 |
| **Skill** | 15.1/15.3/3.1：Skill 怎么调用 | ❌ | 无 | — | ❌ NOT_AVAILABLE | ❌ | 无生产者 |
| **Tool** | 15.1/15.3/3.1：Tool 怎么调用 | ❌ | 无 | — | ❌ NOT_AVAILABLE | ❌ | 无生产者 |
| **RAG** | 15.1/15.3/3.1：RAG 怎么实现 | ⚠️ **近似** | `technology_stack.embedding` | 配置文件关键词 | ⚠️ 可比较（实为"向量库检测"） | ⚠️ | 无显式 RAG 字段；见第 10 节 |
| **Memory** | 15.1/15.3/3.1：Memory 怎么实现 | ❌ | 无 | — | ❌ NOT_AVAILABLE | ❌ | 无生产者 |
| **Database** | 15.1/15.3：数据库 | ✅ | `technology_stack.database` | 配置文件关键词 | ✅ 实测 `DIFFERENT` | ✅ `PostgreSQL` → README | 依赖 `source_files` 命中率 |
| **Deployment** | 3.2 第 9 项：部署方式 | ✅ | `technology_stack.deployment` | 配置文件关键词 | ✅ 实测 `SAME`（两边都空） | ❌（空值无 token） | 同上 |
| **Code Complexity** | 16.3 新增 | ⚠️ 部分 | `data.repository.{language, size}` + `architecture.{files, modules}` | GitHub API + code search | ✅ 实测 `DIFFERENT` | ⚠️ `python` → README | `files`/`modules` 恒空，「复杂度」退化为「仓库体积」 |
| **Extension** | 16.3 新增 | ❌ | 无 | — | ❌ NOT_AVAILABLE | ❌ | 无生产者 |

**统计：✅ 2 个　⚠️ 2 个　❌ 6 个**

> **必须强调：`有值 ≠ 语义正确`。** `executed_tasks` 与 `research_plan` 都有真实值、能产生 `SAME`/`DIFFERENT`，但它们描述的是 **AIPI 自己**，不是被分析项目。

---

## 7. Agent 维度专项结论

### 7.1 候选来源逐一核实

| 候选来源 | 实际是什么 | 能否作为项目 Agent 数量 |
|---|---|---|
| `executed_tasks` | AIPI 的 5 个分析 Agent | ❌ **明确不能** |
| `repository_analysis_agent` 输出 | `{repository, readme, dependencies}`，无 Agent 概念 | ❌ |
| `architecture_analysis_agent` 输出 | `{files, modules}`，是**原始代码搜索结果**，无 Agent 语义分类 | ❌ |
| `technology_stack` | 只匹配 fastapi / django / flask / langchain / langgraph 等框架名 | ⚠️ 能侧面反映「是否用了 Agent 框架」，但不是「有哪些 Agent」 |
| `readme` | **包含项目自己的 Agent 名**（实测提到 `Agent` / `Planner` / `Critic` / `Synthes`） | ⚠️ 信号在，但当前无任何代码解析它 |
| `data.repository.topics` | GitHub 官方话题标签，实测含 `ai-agents` / `langchain` / `langgraph` / `human-in-the-loop` | ⚠️ 真实结构化元数据，但当前无人使用 |
| GitHub 源码（经 `GitHubCodeSearchTool`） | 工具**已存在**且能读目标项目源码 | ✅ **最正确的来源，但当前用法是死的** |

### 7.2 结论

**当前代码从未真正提取过「被分析项目 Agent 信息」。**

**应该由谁负责？** 依据：

- `ArchitectureAnalysisSkill` 是**唯一**会读目标项目源码的 Skill（`GitHubCodeSearchTool(keyword="class")` + `FileReaderTool`），它已具备「拿到源码」的能力 —— 但它只把结果堆进 `files` / `modules`，**不做任何语义分类**，且 `keyword` 硬编码为 `"class"`、两份真实 run 实测 `files`/`modules` 都是空的。
- 现有 5 个 Agent 里没有「项目结构分析」的职责位；文档 15.2 的 `Agent / Workflow / Skill / Tool Analysis` 这一步**在代码中不存在对应实现**。
- 因此最合理的落点是**新增一个 Skill（+ 包装它的 Agent）**，消费已采集的 `readme` + GitHub 源码，产出项目级结构。
  - 塞进 `RepositoryAnalysisSkill` 会破坏其既有职责与测试；
  - 塞进 `ArchitectureAnalysisSkill` 会让「文件清单」与「语义结构」混在一起。

---

## 8. Workflow 维度专项结论

### 8.1 必须严格区分

| | AIPI Workflow | 被分析项目 Workflow |
|---|---|---|
| 数据位置 | `research_plan` / `executed_tasks` / `workflow_state.status` | **不存在** |
| 真实值 | `{tasks:[5个AIPI Agent], plan_version:1, analysis_type:"github_agent_project", evidence_required:true}` | — |
| 是否随项目变化 | ❌ 不变（`PlannerAgent` 硬编码） | — |

### 8.2 结论

**当前代码没有提取被分析项目 Workflow 信息。**

**最合理的 Phase 12 产出位置**：与 Agent 维度同一处 —— 同一次源码/README 结构分析即可产出 `workflow` 段落，因为项目 Workflow 与 Agent 拓扑本来就是同一份结构的两面。单独再开一个 Skill 会造成两份重复的源码解析。

**附带实测发现**：`research_plan` 除 `question` 外是常量，因此 **Workflow 维度在任何两个项目之间恒为 `SAME`**，不具区分力。

---

## 9. Skill / Tool / Memory / Extension 专项结论

### 9.1 为什么没有数据 —— 逐层向上追踪

| 层 | 实际情况 |
|---|---|
| `RepositoryAnalysisSkill` | 产出 `repository` / `readme` / `dependencies`，**不解析项目结构** |
| `ArchitectureAnalysisSkill` | 产出 `files` / `modules` 原始文件内容，**无语义分类**；两份真实 run 均为空 |
| `TechnologyAnalysisSkill` | 产出 `technology_stack`（6 个技术维度，全部是**框架 / 中间件名关键词匹配**），**不含 Skill / Tool / Memory 概念** |
| `EvidenceAnalysisSkill` | 产出 README 证据，**不做结构提取** |
| `ReportGenerationSkill` | **不是数据生产者**，只是把已有数据拼成 Markdown |

### 9.2 工具层的关键区分

| Tool | 分析对象 | 性质 |
|---|---|---|
| `github_repository` | **目标 GitHub 项目** | 分析仪器 |
| `file_reader` | **目标项目文件** | 分析仪器 |
| `github_code_search` | **目标项目源码** | 分析仪器 |
| `dependency_analyzer` | **目标项目本地目录** | 分析仪器（⚠️ 远程模式从不调用） |
| `qdrant_search` | **AIPI 自己的向量库** | AIPI 基础设施（⚠️ 真实链路从不触发：`query_vector` 从未提供） |
| `mysql_query` | **AIPI 自己的数据库** | AIPI 基础设施（⚠️ **注册了但全项目无人调用，死代码**） |
| `report_export` | **AIPI 的报告目录** | 输出装置 |

`MemoryManager` / `ProjectMemory` / `RunMemory` 读的是 **AIPI 自己的表**（`analysis_runs` / `analysis_tasks` / `checkpoints` / `evidences`）——「Project Memory」指「**同一个 repository 的历史分析记录**」，**不是**「被分析项目的 Memory 实现」。`ContextManager` 同理，为 AIPI 的分析 Agent 组装上下文。

### 9.3 结论

**AIPI 的 Skill / Tool / Memory 与被分析项目的 Skill / Tool / Memory 是完全不同的两个概念。** 前者是分析能力，后者是被分析对象。当前四个维度 `NOT_AVAILABLE` 是**诚实的** —— 真实数据确实不存在。

### 9.4 附带发现：报告层犯了同一个错

`app/skills/report_generation_skill.py`：

| 报告节 | 数据来源 | 问题 |
|---|---|---|
| `04 Agent 架构` | `data["executed_tasks"]`（:109-113） | **把 AIPI 的 5 个 Agent 当成项目 Agent 架构** |
| `05 Workflow` | `executed_tasks` + `research_plan`（:118-128） | **同上** |
| `06 Skill` | `repository` / `architecture` / `technology_stack`（:133-146） | **标签是 Skill，内容是别的东西** |
| `07 Tool` | **硬编码 6 个 AIPI 自己的 Tool 名**（:150-172） | **纯硬编码** |
| `09 Memory / Context` | **硬编码 `{"context_enabled": True, "memory_enabled": True}`**（:185-191） | **纯硬编码** |
| `10 数据库` | `technology_stack.database`（:195-215） | ✅ 正确 |

即：Phase 12 文档 15.3 要求的 12 节里，**Agent架构 / Workflow / Skill / Tool / Memory 五节全部是「断言或错标」**，不是从被分析项目提取的。这与 Phase 13 原始的 `project["analysis"]` bug **是同一种病的两个症状** —— 只不过报告里用硬编码常量假装有数据，比返回 `NOT_AVAILABLE` **更具误导性**。

---

## 10. RAG 专项结论

### 10.1 事实（可验证）

1. `TechnologyAnalysisSkill._analyze_remote()` 检测 `embedding` 字段的关键词**只有两个**：

```python
if "qdrant" in all_content:    embeddings.append("Qdrant")
if "chromadb" in all_content:  embeddings.append("ChromaDB")
```

2. 因此该字段实际语义 = **「在 5 个配置文件里是否出现 qdrant / chromadb 这两个向量数据库名」**。它检测的是**向量数据库**，不是 embedding model、不是 retriever、不是 chunking、不是「RAG 实现方式」。
3. `DependencyAnalyzerTool` 的 `embedding` 字段同样只匹配 `qdrant` → `"Qdrant"`。
4. 真实数据中**没有任何显式 RAG 字段**。真实 Run A 的 `embedding` = `[]`（只拿到 `docker-compose.yml`，其余 4 个配置文件 404）。
5. Phase 12 文档 **15.1 / 15.3 / 3.1 都把 RAG 列为分析要求**，但**没有规定字段名**，也没规定提取方式。

### 10.2 语义解释（判断，非事实）

向量数据库是 RAG 实现的必要组件，因此「检测到向量库」可以作为「**该项目技术栈包含 RAG 相关组件**」的一个**弱证据**。

### 10.3 不支持这个映射的地方

- 字段名是 `embedding` 不是 `rag`，直接叫 `rag` 是**断言了检测范围之外的东西**：一个用 OpenAI Embeddings + FAISS 的项目会得到 `embedding: []`，被误判为「没有 RAG」。
- 检测覆盖面只有 2 个关键词，**假阴性率极高**（真实 Run A 的 README 里含 LangChain / LangGraph，但 `frameworks` 也是空的）。
- 真实 Run A / B 的 `embedding` **都是空数组**，该维度当前的 `SAME` 结论**不包含任何 RAG 信息**。

### 10.4 最终建议

**不建议**把 `embedding` 当作 RAG 的正式答案。若必须保留一个值，应**降级命名并显式标注为近似**（例如维度名用 `rag_vector_store`，或在维度值中带回 `source: technology_stack.embedding` 的溯源）。**更正确的做法**是归入第 15 节的 Phase 12 修复：在项目结构分析里显式产出 `rag` 段落，检测范围扩到 `embedding model / vector store / retriever / chunking` 四类关键词。

---

## 11. Evidence 专项结论

### 11.1 这些 Evidence 是否真正对应被分析项目？

**是，但覆盖面极窄。** 真实 Run A 的 4 条 Evidence 全部是：

```text
id=55c64c81…  file=README.md  lines=1-215  verify=UNVERIFIED
id=35e63b87…  file=README.md  lines=1-215  verify=UNVERIFIED
id=04f476a2…  file=README.md  lines=1-243  verify=UNVERIFIED
id=c79ca9d5…  file=README.md  lines=1-243  verify=UNVERIFIED
```

**只有 README，且是 2 组重复**（215 行版与 243 行版，来自两次不同的分析）。真实 Run B 的 Evidence 数量为 **0**。

### 11.2 能否支撑 10 个维度？

| 维度 | Evidence 支撑 |
|---|---|
| Database | ⚠️ 弱（`PostgreSQL` 正好出现在 README 里，属 token 命中） |
| Code Complexity | ⚠️ 弱（`python` 出现在 README 里） |
| 其余 8 个 | ❌ 无 |

### 11.3 在哪个阶段生成？

`PlanExecutorNode` 执行第 4 个任务时，由 `EvidenceAnalysisAgent → EvidenceAnalysisSkill → EvidenceService.create_evidence()` 写入 `evidences` 表。

### 11.4 确定的代码缺陷

`EvidenceAnalysisSkill._from_analysis_results()` 有一个「从架构结果生成源码证据」的分支，读的是：

```python
architecture = input_data.get("architecture")     # evidence_analysis_skill.py:234
```

但真实 `state.data` 里的 key 是 `architecture_analysis_agent` 与被拍平的 `modules` / `files`，**从来没有 `architecture` 这个 key**。因此该分支**从未执行过**（`PlanExecutorNode` 传入的是 `dict(state.data)`）。即使架构结果非空，也拿不到源码级证据。**这解释了为什么 Evidence 100% 只有 README。**

### 11.5 某维度没有 Evidence 时该怎么办？

按文档判断：设计文档 3.2 场景 B 的要求是「**技术事实标准化**」+ Phase 13 16.3「**比较必须基于 Analysis Result + Evidence**」，**没有**规定「无证据时必须返回 NOT_AVAILABLE」。

- Phase 13 当前实现的处理是：**值可以有，`evidence_ids` 为空**。这与设计文档一致（比较基于 Analysis Result，Evidence 是增强的可追溯性）。
- 真正的问题不是「该不该 NOT_AVAILABLE」，而是 **Evidence 生成层产不出源码级证据** —— 这是 Phase 12 侧的缺口。

### 11.6 结论

**当前 Evidence 不足以支撑 Phase 13 的 Evidence-based Comparison。** 它只能对 README 中出现的少数技术名词提供弱佐证。

---

## 12. Phase 13 当前实现审查

| # | 问题 | 结论 |
|---|---|---|
| 1 | ComparisonAgent 期待什么结构？ | `RunMemory.load()` 的 11 个顶层 key：`workflow_state.data.*` 与 `evidences[*].id` |
| 2 | 实际收到什么结构？ | **与上面完全一致**（服务层直接传 `RunMemory.load()` 的返回） |
| 3 | 两者是否一致？ | **一致** |
| 4 | 路线 A 修复是否正确？ | **正确**。全项目 grep 确认：**没有任何生产代码产出 `agent_analysis` / `workflow_analysis` / `skill_analysis` / `tool_analysis` / `rag_analysis` / `memory_analysis` / `database_analysis` / `deployment_analysis` 等 key**（唯一命中是 `comparison_agent.py` 自身）。原 `project["analysis"]` 是一个**从未有生产者的虚构契约** |
| 5 | 哪些地方只是「兼容真实数据」？ | 全部 10 个维度的 `_extract_*` 都是新写的真实结构读取；`evidence_based` 由真实引用计算；`evidence_ids` 走真实 `id` 字段 |
| 6 | 哪些地方掩盖了 Phase 12 数据缺失？ | ① `rag ← technology_stack.embedding` 是语义近似；② `code_complexity` 退化为「仓库体积 + 语言」（`files`/`modules` 恒空）；③ `deployment` 两边都空时返回 `SAME`，读者易误读为「部署方式相同」，实际是「两边都没检测到」 |
| 7 | 是否存在把 AIPI 自身执行数据当成项目数据？ | **存在**（`agent ← executed_tasks`、`workflow ← research_plan`）。但**这不是 ComparisonAgent 引入的错**，而是 Phase 12 未提供项目级数据时的降级选择；其输出语义是错的（恒 `SAME`） |
| 8 | 是否存在「为了有结果而进行语义猜测」？ | **仅 `rag ← embedding` 一处**，其余维度没有猜测，`NOT_AVAILABLE` 是诚实返回 |

---

## 13. 真实 COMPLETED Run 验证结果

> 只读查询，未修改数据库。

### 13.1 两个 run 的真实差异

| 项 | Run A `d1d71c3e…` | Run B `799049b1…` |
|---|---|---|
| `workflow_state.data` key 数 | 25 | 25 |
| `readme` 长度 | **14457** | **0** ← 空 |
| `evidences` 数量 | **4** | **0** |
| `agent_outputs` 数量 | 7 | **8**（多了一次重复的 repository 分析） |
| `technology_stack.source_files` | `["docker-compose.yml"]` | `[]` |
| `technology_stack.database` | `["PostgreSQL"]` | `[]` |
| `architecture_analysis_agent` | `{files:[], modules:[]}` | `{files:[], modules:[]}` |
| `dependencies` | `{}` | `{}` |
| `task_results` | `[]` | `[]` |
| `data.repository.language` | `"Python"` | `"Python"` |
| `data.repository.size` | `8586` | `509` |

### 13.2 由真实数据暴露的两个新缺陷

**缺陷 1：`repositories` 表元数据全为 NULL**

```python
{id: 26, owner: 'adityamhaske', name: 'Multi-Agent-Research-Assistant',
 description: None, language: None, default_branch: None, stars: 0, forks: 0}
{id: 35, owner: 'smlfy', name: 'enterprise-workflow-agent-platform?utm_source=chatgpt.com',
 description: None, language: None, default_branch: None, stars: 0, forks: 0}
```

原因：`RepositoryService.get_or_create()` 只在仓库**不存在**时才调 GitHub 补全元数据（`:71-113`），已存在的行**直接 return**（`:66-67`），永不回填。因此 `RunMemory.load()` 顶层 `repository` 摘要永远缺 `description` / `language` / `stars` —— 而 GitHub API 的完整对象（84 字段）其实就存在 `workflow_state.data.repository` 里，只是没被暴露到顶层契约。

**缺陷 2：`_parse_github_url` 不剥离 query string**

```python
path = repo_url.rstrip("/").split("/")
name = path[-1]
if name.endswith(".git"):
    name = name[:-4]
# ← 没有处理 "?utm_source=..."
```

真实后果（Run B）：`repositories.name` = `"enterprise-workflow-agent-platform?utm_source=chatgpt.com"` → README 与配置文件全部 404 → `readme` 为空、`evidences` 为 0、`technology_stack` 全空。**Run B 实际上是一个被 URL 解析 bug 破坏的 run**，而 Phase 13 的比较结果里它照样以 `COMPLETED` 参与比较。

### 13.3 当前真实数据能支持 Phase 13 哪些维度

| 维度 | Phase 13 实测 | 数据来源语义 |
|---|---|---|
| agent | `SAME`（两边 5 个 AIPI Agent） | ❌ B 类 |
| workflow | `SAME`（除 question 外为常量） | ❌ B 类 |
| skill | `NOT_AVAILABLE` | — 真实缺失 |
| tool | `NOT_AVAILABLE` | — 真实缺失 |
| rag | `SAME`（两边 `embedding` 都空） | ⚠️ 近似，无信息量 |
| memory | `NOT_AVAILABLE` | — 真实缺失 |
| database | **`DIFFERENT`**（A: `["PostgreSQL"]` / B: `[]`） | ✅ 真实项目数据 |
| deployment | `SAME`（两边都空） | ✅ 真实但无信息量 |
| code_complexity | **`DIFFERENT`**（A: Python/8586KB / B: Python/509KB） | ⚠️ 部分真实 |
| extension | `NOT_AVAILABLE` | — 真实缺失 |

> **两个真实 COMPLETED run 之间，真正有区分力的维度只有 2 个（database、code_complexity），其中 1 个是近似的。**

---

## 14. Phase 12 → Phase 13 契约缺口（按严重程度）

| # | 严重度 | 缺口 | 影响 |
|---|---|---|---|
| **G1** | 🔴 致命 | **文档 15.2 的「Agent / Workflow / Skill / Tool Analysis」步骤没有任何实现**；也没有任何代码产出项目级 Agent / Workflow / Skill / Tool / Memory / Extension 结构 | Phase 13 的 10 个维度里 6 个永久 `NOT_AVAILABLE`；另 2 个语义错误 |
| **G2** | 🔴 致命 | **不存在设计文档 3.2 要求的「统一分析维度 / 技术事实标准化」层**；`RunMemory.load()` 直接暴露 WorkflowState 原始转储，A 类与 B 类数据混在同一层级、无命名区分 | 下游只能靠约定识别，Phase 13 的 agent / workflow 维度因此误取 B 类 |
| **G3** | 🟠 严重 | **报告层用硬编码 / 错标冒充分析结果**：`ReportGenerationSkill` 的 04 / 05 / 06 / 07 / 09 五节（Tool、Memory 纯硬编码常量） | Phase 12 的「验证闭环」是假的；比返回 `NOT_AVAILABLE` 更有误导性 |
| **G4** | 🟠 严重 | **CriticAgent 只校验 3 个 key 存在性**（`repository` / `architecture` / `technology`），且 `architecture` 命中的是**空结构** | `passed: true` 空洞，不能作为分析完整性的证据 |
| **G5** | 🟠 严重 | **`EvidenceAnalysisSkill` 源码证据分支因 key 名不匹配是死代码**（读 `"architecture"`，真实 key 是 `architecture_analysis_agent` / `modules`） | Evidence 100% 只有 README，无法支撑 Evidence-based Comparison |
| **G6** | 🟡 中 | **`_parse_github_url` 不剥离 query string** | 真实 Run B 被破坏：readme 空、evidence 0、tech stack 空 |
| **G7** | 🟡 中 | **`repositories` 表元数据永不回填**（`get_or_create` 提前 return） | `RunMemory` 顶层 `repository` 摘要缺 description / language / stars |
| **G8** | 🟡 中 | **`architecture_analysis_skill` 的 `keyword` 硬编码为 `"class"`，且真实 run 实测 `files`/`modules` 恒空** | `code_complexity` 退化为仓库体积；架构证据链断裂 |
| **G9** | 🟡 中 | **`agent_outputs` 是无 agent 名的位置型列表**（Run B 有 8 项且出现重复的 repository 输出） | 下游无法可靠定位「哪个输出来自哪个 Agent」 |
| **G10** | 🟢 低 | **`mysql_query` Tool 注册了但无人调用**（死代码）；`qdrant_search` 真实链路从不触发（`query_vector` 从未提供） | 资源浪费；`EvidenceAnalysisSkill` 的 Qdrant 分支不可达 |
| **G11** | 🟢 低 | **`dependencies` 在远程模式恒为 `{}`**（`dependency_analyzer` 需要本地路径） | 依赖分析事实上未生效 |
| **G12** | 🟢 低 | **`task_results` 恒为 `[]`**（`analysis_tasks` 表无写入者） | `RunMemory` 一个字段长期为空 |

---

## 15. 最小修复路径（方案，不实施）

**总体原则：不重构 Phase 12。** 只新增一个「项目结构分析」能力（1 Skill + 1 Agent），并修 3 处确定性的小缺陷。全部改动落在既有 `checkpoints.state_data` JSON 列内，**不需要新表**。

### P1 —— Phase 12 修复（必须，否则 Phase 13 无解）

| # | 文件 | 为什么改 | 修改目标 | 改完应产出什么数据 |
|---|---|---|---|---|
| **P1-1** | **新增** `app/skills/project_structure_analysis_skill.py` | G1：文档 15.2 要求的结构分析步骤缺失 | 消费已采集的 `readme` + `modules`（源码）+ `repository.topics`，产出**显式项目级结构** `{agents, workflow, skills, tools, rag, memory, extension}`。**确定性优先**：Python 用 `ast` 解析 import / class / 装饰器，目录路径模式匹配（`agents/`、`skills/`、`tools/`），配置文件名匹配；匹配不到就置 `null` 并附 `reason`。**禁止 LLM 猜测** | `state.data["project_structure"]`，每项含 `value` + `evidence`（file_path / line_start / line_end，来自真实源码行） |
| **P1-2** | **新增** `app/agents/project_structure_analysis_agent.py` | 保持 Agent → Skill 分层一致 | 薄包装，与其余 5 个 Agent 同构 | — |
| **P1-3** | `app/agents/agent_registry.py` | 注册新 Agent | 加入 `ProjectStructureAnalysisAgent(skill_registry)` | — |
| **P1-4** | `app/skills/registry.py` | 注册新 Skill | 加入 `ProjectStructureAnalysisSkill()` | — |
| **P1-5** | `app/agents/planner_agent.py` | 让新 Agent 真正进入执行链 | 把 `"project_structure_analysis_agent"` 加入 `tasks`（建议插在 `architecture_analysis_agent` 之后、`evidence_analysis_agent` 之前，保证 Evidence 能引用它） | `executed_tasks` 从 5 项变 6 项（⚠️ 注意这会让 `research_plan` / `executed_tasks` 变化） |
| **P1-6** | `app/skills/evidence_analysis_skill.py` | G5：源码证据分支是死代码 | `input_data.get("architecture")` → 同时兼容 `architecture_analysis_agent` 与拍平的 `modules`；并让新结构里的 `evidence` 条目也能落库 | Evidence 从「只有 README」扩展到「README + 真实源码行」 |
| **P1-7** | `app/skills/report_generation_skill.py` | G3：04 / 05 / 06 / 07 / 09 五节硬编码 / 错标 | 04 / 05 改读 `project_structure`；06 / 07 改读 `project_structure.skills` / `.tools`；09 改读 `project_structure.memory`；删掉所有硬编码常量，取不到就渲染「真实数据不存在」 | 报告 5 节从「断言」变为「派生」 |
| **P1-8**（可选） | `app/skills/architecture_analysis_skill.py` | G8：keyword 硬编码 `"class"`、结果恒空 | keyword 改为可配置 / 多关键词（如 `class`、`def`、`agent`、`skill`），或直接从 GitHub tree API 取目录结构 | `files` / `modules` 非空，`code_complexity` 与源码证据才有真实输入 |

**P1 涉及数据库 migration？→ 不需要**（全部写入既有 JSON 列 `checkpoints.state_data`）。

### P2 —— Phase 13 修复（小，且依赖 P1）

| # | 文件 | 为什么改 | 修改目标 |
|---|---|---|---|
| **P2-1** | `app/agents/comparison_agent.py` | Agent / Workflow 两维度当前取 B 类数据（语义错误） | `_extract_agent` / `_extract_workflow` 优先读 `workflow_state.data.project_structure.*`；读不到时**保持 `NOT_AVAILABLE` 并写明「Phase 12 未产出项目级结构」，不再退回 `executed_tasks` / `research_plan`** |
| **P2-2** | `app/agents/comparison_agent.py` | `rag ← embedding` 是语义近似 | 维度值改为读 `project_structure.rag`；若仍保留近似路径，必须让 `source` 明确标注为 `technology_stack.embedding`，并在维度值里带上 `approximate: true` |
| **P2-3** | `app/agents/comparison_agent.py` | `code_complexity` 依赖恒空的 `files` / `modules` | P1-8 落地后自动改善，无需额外改动 |

### P3 —— 数据质量修复（与 Phase 13 间接相关，建议同批做）

| # | 文件 | 为什么改 |
|---|---|---|
| **P3-1** | `app/services/analysis_service.py`（`_parse_github_url`） | G6：剥离 `?...` 与 `#...`，修复 Run B 那类被破坏的 run |
| **P3-2** | `app/services/repository_service.py`（`get_or_create`） | G7：对已存在但 `description` / `language` 为 NULL 的行做一次回填 |
| **P3-3** | `app/agents/critic_agent.py` | G4：`required_fields` 增加 `project_structure`，并让 `architecture` 校验**非空**（当前空结构也算通过） |
| **P3-4** | `app/services/analysis_workflow.py` | G10：删除无人使用的 `mysql_query` 注册（或明确保留并注释说明） |

### 15.1 不应该修改的文件

- `app/memory/run_memory.py` —— **契约稳定，Phase 13 已能正确消费**。P1-1 产出的 `project_structure` 会自动随 `workflow_state.data` 流到顶层，**不需要改 RunMemory**。
- `app/memory/project_memory.py`、`app/memory/manager.py`
- `app/workflow/engine.py`、`app/workflow/checkpoint.py`
- `app/repositories/*`、`app/models/*`、`app/db/*`、`alembic/*`
- `app/services/comparison_service.py`、`app/schemas/comparison.py`、`app/api/v1/comparison.py`
- 现有测试文件（P1 / P2 落地后需要**新增**断言，但不应削弱既有断言）

### 15.2 四个明确提问的回答

| 问题 | 回答 |
|---|---|
| **是否需要 DB migration？** | **不需要**。除非要做 `GET /api/v1/comparison/{id}`，那需要 `comparisons` 表 + migration，属 Phase 13 可选项，**不在最小路径上** |
| **是否需要修改 RunMemory？** | **不需要** |
| **是否需要修改 ComparisonAgent？** | **需要**，但属 P2 小改（2 个维度的数据来源 + 1 个近似标注），且**必须在 P1 之后** |
| **哪些属 Phase 12 修复，哪些属 Phase 13 修复？** | **Phase 12**：P1-1 ~ P1-8、P3-1 ~ P3-4（G1~G12 的根因都在 Phase 12）。**Phase 13**：P2-1 ~ P2-3。 |

---

## 16. 当前 Phase 13 完成度判断

| 验收项 | 判断 | 依据 |
|---|---|---|
| **多项目分析** | 🟡 **部分完成** | `POST /api/v1/comparison` 可用、返回真实 10 维度结构 ✅；`GET /api/v1/comparison/{id}` **不存在（实测 404）** ❌；10 维度中 6 个 `NOT_AVAILABLE`、2 个语义错误 🟡 |
| **Comparison Agent** | ✅ **完成** | 已改为读 `RunMemory.load()` 真实结构；全项目确认无 `agent_analysis` 类生产者，证明原 `analysis` 契约是虚构的；`evidence_ids` 用真实 `evidences[*]["id"]`；`evidence_based` 由真实引用计算，非硬编码；测试 33 passed（含 9 条真实结构回归） |
| **Evidence-based Comparison** | ❌ **未完成** | Evidence 100% 只有 README（源码分支因 key 名不匹配是死代码 G5），且 4 条中 2 组重复、`verification_status` 全 `UNVERIFIED`；只能对 `database` / `code_complexity` 两个维度提供 token 级弱佐证，支撑不了 16.3 的「比较必须基于 Analysis Result + Evidence」 |

### 最终判定

```text
Phase 13：❌ 不能标记 COMPLETE
```

**不是「差一点点」，而是根因在上一层：** Phase 12 文档 15.1 / 15.2 / 15.3 与设计文档 3.1 / 3.2 都明确要求产出**项目级**的 Agent / Workflow / Skill / Tool / RAG / Memory 结构化事实，并明确要求「统一分析维度 → 技术事实标准化」；当前 Phase 12 只产出了 repository / technology_stack / architecture（且后两者数据质量不佳）/ evidence（仅 README），**没有任何项目级结构分析**。Phase 13 的 `NOT_AVAILABLE` 是**诚实且正确**的表现，真实问题在 Phase 12 侧。

**同时必须指出**：本报告也证明对 ComparisonAgent 的路线 A 修复**方向是对的、实现是对的** —— 它把一个「读取虚构契约、恒返回 9 个 `NOT_AVAILABLE`、`evidence_based` 恒 `True`」的假通过，变成了一个**如实报告数据缺失**的诚实实现。在没有 P1 之前，它已经做到了当前数据结构下能做到的最好。

**另有一项与 Phase 13 无关但同源的缺陷需要单独记录**：`ReportGenerationSkill` 的 04 / 05 / 06 / 07 / 09 五节（其中 Tool、Memory 是纯硬编码常量）把 AIPI 自己的 Agent / Tool / Context 伪装成被分析项目的能力 —— 这与 Phase 13 最初的 bug 是同一个病，且**更具误导性，因为它不是返回「不可用」，而是输出看起来完整的报告**。建议在 P1-7 一并处理。

### 建议推进顺序

```text
P1-1 → P1-2 → P1-3 → P1-4 → P1-5     先打通项目级数据
P1-6 → P1-7                          再补 Evidence 与报告
P2-1 ~ P2-3                          最后收口 Phase 13
P3-1 ~ P3-4                          数据质量，可同批
```

---

## 附录 A：八个必答问题

| 编号 | 问题 | 回答 |
|---|---|---|
| **Q1** | Phase 12 当前是否真的已经产出了满足 Phase 13 所需的完整 Analysis Result？ | **部分**。已产出：`repository`（GitHub API 对象）、`technology_stack`、`evidences`、`readme`。未产出：**项目级** Agent / Workflow / Skill / Tool / RAG / Memory / Extension。依据见第 4 节（25 个 key 的真实内容）与第 6 节矩阵（6/10 维度无数据） |
| **Q2** | 10 个维度中，哪些已具备正确的项目级数据？ | **具备**：Database、Deployment（结构正确）。**部分**：Code Complexity（退化为仓库体积）、RAG（近似）。**没有**：Agent、Workflow、Skill、Tool、Memory、Extension |
| **Q3** | Agent 维度现在是否错误地比较了 AIPI 自身 Agent？ | **是**。取 `workflow_state.data.executed_tasks`，真实值是 AIPI 的 5 个分析 Agent，任何两个项目都相同 → 恒 `SAME` |
| **Q4** | Workflow 维度现在是否错误地比较了 AIPI 自身 research_plan？ | **是**。取 `workflow_state.data.research_plan`，由 `PlannerAgent` 硬编码产生，除 `question` 外为常量 → 恒 `SAME` |
| **Q5** | Skill / Tool / Memory / Extension 缺失数据的真正原因是什么？ | Phase 12 **从未实现**文档 15.2 的「Agent / Workflow / Skill / Tool Analysis」步骤；没有任何 Agent / Skill / Tool 对被分析项目做 Skill / Tool / Memory / Extension 的结构提取。现有 Skill 只产出 repository / readme / dependencies / files-modules / technology_stack / evidence。详见第 9 节 |
| **Q6** | RAG → `technology_stack.embedding` 是否合理？ | **事实**：该字段只匹配 `qdrant` / `chromadb` 两个向量库关键词。**不支持**：字段名是 embedding 不是 rag；不含 embedding model / retriever / chunking；两个真实 run 都是空数组，无信息量。**建议**：不作为正式答案，降级标注为近似（`rag_vector_store`）或归入 P1-1 显式产出 `rag` |
| **Q7** | Evidence 当前是否真正满足 Phase 13 的 Evidence-based Comparison 要求？ | **不满足**。Evidence 100% 只有 README（源码分支死代码 G5），4 条中 2 组重复，全部 `UNVERIFIED`；只能对 Database / Code Complexity 提供 token 级弱佐证 |
| **Q8** | Phase 13 当前应该走哪条路？ | **C（两者都需要），但顺序是 B 优先、A 极小。** 技术依据：① ComparisonAgent 已不再读假结构、已能从真实数据产出 6 个维度，路线 A 剩余工作只是「命名与语义澄清」，很小；② 6/10 维度缺失的根因在 Phase 12 没有产出项目级结构，不改 Phase 12，无论怎么改 ComparisonAgent 都拿不到数据；③ 但**不需要重构 Phase 12** —— 只需新增 1 个 Skill + 1 个 Agent 读取已存在的 `readme` / 源码 |

---

## 附录 B：复核方法（可复现）

以下脚本均为**只读**，可在项目根目录直接运行以复核本报告结论。要求：使用项目环境（含 `sqlalchemy` + `asyncmy`），并确保 `.env` 已配置数据库连接。

### B.1 复核真实 `RunMemory.load()` 结构与 Evidence

```python
import asyncio, json
from app.db.session import AsyncSessionLocal
from app.memory.run_memory import RunMemory

async def main():
    async with AsyncSessionLocal() as s:
        for rid in (
            "d1d71c3e-a9b6-4073-8d3d-bbbfe0b11005",
            "799049b1-3d51-4c2f-bbe5-81930ce59a23",
        ):
            p = await RunMemory(s).load(rid)
            print("run", rid[:8], "顶层 key:", sorted(p.keys()))
            print("  有 'analysis' 吗:", "analysis" in p)
            d = p["workflow_state"]["data"]
            print("  workflow_state.data key 数:", len(d))
            print("  含 'analysis' 吗:", "analysis" in d)
            print("  executed_tasks:", d.get("executed_tasks"))
            print("  technology_stack:", json.dumps(d.get("technology_stack"), ensure_ascii=True))
            print("  evidences:", [(e["id"][:8], e["file_path"]) for e in p["evidences"]])
            print()

asyncio.run(main())
```

### B.2 复核「没有任何代码产出 `*_analysis` key」

```bash
grep -rn "agent_analysis\|workflow_analysis\|skill_analysis\|tool_analysis\|rag_analysis\|memory_analysis\|database_analysis\|deployment_analysis\|code_complexity\|extensibility" app/ --include=*.py
```

预期：只命中 `app/agents/comparison_agent.py` 自身（消费者），**没有任何生产者**。

### B.3 复核 `ReportGenerationSkill` 的硬编码段落

```bash
sed -n '100,215p' app/skills/report_generation_skill.py
```

预期可见：`04 Agent 架构` ← `executed_tasks`；`07 Tool` ← 硬编码 Tool 名；`09 Memory / Context` ← `{"context_enabled": True, "memory_enabled": True}`。

### B.4 复核 `CriticAgent` 只校验 3 个字段

```bash
sed -n '28,60p' app/agents/critic_agent.py
```

### B.5 复核 `EvidenceAnalysisSkill` 的 key 名不匹配

```bash
grep -n 'input_data.get(' app/skills/evidence_analysis_skill.py
```

预期：出现 `input_data.get("architecture")`，而真实 key 是 `architecture_analysis_agent` / `modules`。

### B.6 复核 `repositories` 表元数据为空 & URL 未剥离 query

```python
import asyncio
from sqlalchemy import text
from app.db.session import AsyncSessionLocal

async def main():
    async with AsyncSessionLocal() as s:
        r = await s.execute(text(
            "SELECT id, owner, name, description, language, stars, forks "
            "FROM repositories WHERE id IN (26, 35)"))
        for row in r.mappings():
            print(dict(row))

asyncio.run(main())
```

### B.7 复核 Phase 13 真实端到端（需要先启动服务）

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8123
```

```python
import httpx
c = httpx.Client(timeout=90, trust_env=False)
r = c.post("http://127.0.0.1:8123/api/v1/comparison", json={"run_ids": [
    "d1d71c3e-a9b6-4073-8d3d-bbbfe0b11005",
    "799049b1-3d51-4c2f-bbe5-81930ce59a23",
]})
d = r.json()
print("evidence_based:", d["evidence_based"])
for k, v in d["comparison"].items():
    pa, pb = v["project_a"], v["project_b"]
    print(f"{k:16s} {v['relation']:22s} avail=({pa['available']},{pb['available']}) "
          f"evidence=({len(pa['evidence_ids'])},{len(pb['evidence_ids'])}) source={v.get('source')}")

# GET 接口验证（预期 404）
g = c.get(f"http://127.0.0.1:8123/api/v1/comparison/{d['comparison_id']}")
print("GET /comparison/{id} ->", g.status_code)
```

> 注意：`httpx` 需加 `trust_env=False`，否则本机系统代理会拦截 localhost 请求（实测返回 502）。

---

**报告结束**

> 本报告为只读审查产物，未修改任何生产代码、测试、数据库或 Alembic migration，未执行 Git 提交。
