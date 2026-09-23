# AI Agent / GitHub 开源项目智能分析平台
## 详细 Phase 开发实施文档

> 项目名称：AI Agent / GitHub Project Intelligence Platform（AIPI Platform）
>
> 开发目标：面向 AI 应用开发 / Agent 应用开发岗位，自己实现一个具备 Multi-Agent、Skill、Tool Calling、自研 Workflow、RAG、Memory、Context、HITL、Checkpoint、Retry、Evidence 等能力的 GitHub AI Agent 项目智能分析平台。
>
> 技术约束：
> - 不使用 LangGraph `StateGraph`
> - Workflow Engine 自研
> - MySQL 负责结构化业务数据
> - Qdrant 负责向量与语义检索
> - FastAPI 负责后端 API
> - 当前阶段不开发前端
> - Redis / Celery 放到后续长任务阶段
>
> 本文档不是“功能列表”，而是一份可以直接按照顺序执行的个人开发路线。每个 Phase 都包含：目标、要做什么、目录、核心设计、实现顺序、测试方式、完成标准、下一阶段依赖。

---

# 1. 整体开发路线

整个项目按照“基础工程 → 数据层 → Workflow → Tool → Skill → Agent → 证据 → 企业级流程控制 → Memory/Context → 完整闭环 → 扩展 → 工程化”的顺序开发。

```text
Phase 0
开发环境 + 项目骨架
        ↓
Phase 1
Config / Logging / Exception / 基础工程
        ↓
Phase 2
FastAPI API Layer
        ↓
Phase 3
MySQL + SQLAlchemy + Alembic
        ↓
Phase 4
Qdrant + Embedding + Retrieval
        ↓
Phase 5
自研 Workflow Engine
        ↓
Phase 6
Tool Layer
        ↓
Phase 7
Skill Layer
        ↓
Phase 8
Multi-Agent Layer
        ↓
Phase 9
Evidence / Claim / Citation
        ↓
Phase 10
HITL / Checkpoint / Pause / Resume / Retry
        ↓
Phase 11
Memory / Context Manager
        ↓
Phase 12
单项目完整业务闭环
        ↓
Phase 13
多项目分析与比较
        ↓
Phase 14
Learning Path / Report / Export
        ↓
Phase 15
测试 / Docker / 日志 / 审计 / 优化
```

---

# 2. 开发原则

## 2.1 不要一开始就写 Agent

正确顺序：

```text
系统基础设施
    ↓
Workflow
    ↓
Tool
    ↓
Skill
    ↓
Agent
```

因为 Agent 最终需要依赖：

```text
Agent
 ├── Workflow
 ├── Skill
 ├── Tool
 ├── Context
 ├── Memory
 └── Evidence
```

如果这些基础设施不存在，Agent 代码很容易变成大量散乱的 LLM 调用。

---

## 2.2 每个 Phase 都必须有可运行结果

每完成一个 Phase，都应该满足：

```text
代码可以运行
+
至少有测试
+
可以通过 API / CLI / 测试脚本验证
+
Git Commit
```

不要出现：

```text
Phase 0
Phase 1
Phase 2
Phase 3
全部写完
最后才测试
```

---

## 2.3 一个 Phase 不要一次做太多

例如 Phase 5 Workflow Engine 不要一天直接实现：

```text
Workflow
Node
State
Transition
Checkpoint
Retry
Pause
Resume
HITL
Event
```

应该：

```text
BaseNode
 ↓
Workflow
 ↓
State
 ↓
Transition
 ↓
Checkpoint
 ↓
Retry
 ↓
Pause
 ↓
Resume
 ↓
HITL
```

逐步增加。

---

# 3. Phase 0 —— 开发环境与项目骨架

## 3.1 目标

完成项目初始化，使项目具备：

- Python 开发环境
- Git
- 基础目录
- FastAPI 最小启动能力
- 测试框架
- `.env` 配置
- README
- 基础依赖管理

这一阶段不做：

- Agent
- Workflow
- MySQL 业务表
- Qdrant 检索
- Skill
- RAG

---

## 3.2 建议目录

```text
AI-Agent-GitHub-Project-Intelligence-Platform/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── v1/
│   │
│   ├── core/
│   │
│   ├── db/
│   │
│   ├── schemas/
│   │
│   ├── workflow/
│   │
│   ├── agents/
│   │
│   ├── skills/
│   │
│   ├── tools/
│   │
│   ├── memory/
│   │
│   ├── context/
│   │
│   ├── evidence/
│   │
│   └── services/
│
├── tests/
├── scripts/
├── docs/
├── migrations/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── Dockerfile
```

---

## 3.3 首批依赖

建议先安装：

```text
fastapi
uvicorn
pydantic
pydantic-settings
python-dotenv
pytest
pytest-asyncio
httpx
```

数据库和 Qdrant 依赖可以在对应 Phase 再加入。

---

## 3.4 第一个运行目标

实现：

```http
GET /health
```

返回：

```json
{
  "status": "ok"
}
```

---

## 3.5 完成标准

必须能够：

```text
启动 FastAPI
    ↓
访问 /health
    ↓
返回 200
```

并且：

```bash
pytest
```

可以正常执行。

---

# 4. Phase 1 —— Config / Logging / Exception

## 4.1 目标

把基础工程规范建立起来。

包括：

```text
Config
Logging
Exception
Error Response
Environment
```

---

## 4.2 Config

建议：

```text
app/core/config.py
```

配置：

```text
APP_NAME
APP_ENV
DEBUG

MYSQL_HOST
MYSQL_PORT
MYSQL_DATABASE
MYSQL_USER
MYSQL_PASSWORD

QDRANT_HOST
QDRANT_PORT

LLM_PROVIDER
LLM_API_KEY
LLM_MODEL

EMBEDDING_PROVIDER
EMBEDDING_MODEL

GITHUB_TOKEN
```

统一：

```text
.env
 ↓
Settings
 ↓
业务代码
```

不要在业务代码写：

```python
api_key = "xxx"
```

---

## 4.3 Logging

建立：

```text
app/core/logging.py
```

至少支持：

```text
INFO
WARNING
ERROR
DEBUG
```

建议日志包含：

```text
timestamp
level
module
run_id
message
```

Agent / Workflow 日志尤其需要 `run_id`。

例如：

```text
[INFO] run_id=abc123 node=planner message="planner started"
```

---

## 4.4 Exception

建立统一异常：

```text
ApplicationError
ValidationError
WorkflowError
ToolError
AgentError
RepositoryError
LLMError
RetryableError
NonRetryableError
```

---

## 4.5 完成标准

测试：

```text
错误输入
 ↓
统一异常
 ↓
统一 HTTP 响应
```

日志中可以定位：

```text
哪个 run
哪个 node
哪个 agent
什么错误
```

---

# 5. Phase 2 —— FastAPI API Layer

## 5.1 目标

先把系统 API 设计完整。

此时 API 可以暂时不真正执行 Agent。

---

## 5.2 创建分析任务

```http
POST /api/v1/analysis
```

请求：

```json
{
  "repository_url": "https://github.com/adityamhaske/Multi-Agent-Research-Assistant",
  "question": "分析这个项目的Multi-Agent和Workflow"
}
```

返回：

```json
{
  "run_id": "xxx",
  "status": "CREATED"
}
```

---

## 5.3 查询任务

```http
GET /api/v1/analysis/{run_id}
```

返回：

```json
{
  "run_id": "xxx",
  "status": "ANALYZING",
  "current_node": "project_analysis",
  "progress": 40
}
```

---

## 5.4 控制接口

准备：

```http
POST /api/v1/analysis/{run_id}/approve
POST /api/v1/analysis/{run_id}/pause
POST /api/v1/analysis/{run_id}/resume
POST /api/v1/analysis/{run_id}/retry
```

---

## 5.5 报告

```http
GET /api/v1/analysis/{run_id}/report
```

---

## 5.6 完成标准

即使暂时没有 Agent，API 也应该可以：

```text
创建 Run
查询 Run
修改状态
返回错误
```

---

# 6. Phase 3 —— MySQL 数据层

## 6.1 目标

建立整个系统的结构化数据持久化。

建议：

```text
SQLAlchemy 2.x
+
Alembic
+
PyMySQL / asyncmy
```

---

## 6.2 第一批表

### repositories

保存：

```text
id
url
owner
name
description
default_branch
language
stars
forks
created_at
updated_at
```

---

### analysis_runs

代表一次分析任务：

```text
id
repository_id
question
status
current_node
retry_count
created_at
updated_at
```

---

### research_plans

保存 Planner 的研究计划：

```text
id
run_id
goal
analysis_dimensions
tasks
status
```

---

### analysis_tasks

保存具体任务：

```text
id
run_id
task_type
status
input
output
error
retry_count
```

---

### agent_outputs

保存：

```text
run_id
agent_name
task_id
input
output
status
created_at
```

---

## 6.3 后续表

继续增加：

```text
evidences
claims
citations
reports
checkpoints
audit_logs
repository_agents
repository_skills
repository_tools
repository_workflows
```

---

## 6.4 Repository Pattern

不要让 Agent 直接：

```python
session.query(...)
```

建议：

```text
Agent
 ↓
Service
 ↓
Repository
 ↓
SQLAlchemy
 ↓
MySQL
```

例如：

```text
AnalysisRunRepository
RepositoryRepository
EvidenceRepository
CheckpointRepository
```

---

## 6.5 完成标准

能够：

```text
创建 Repository
创建 Analysis Run
查询 Analysis Run
更新状态
保存 Agent Output
```

并且：

```bash
alembic upgrade head
```

可以正常执行。

---

# 7. Phase 4 —— Qdrant / RAG

## 7.1 目标

建立项目源码和文档的语义检索能力。

---

## 7.2 数据来源

第一版：

```text
README.md
docs/
源码文件
配置文件
requirements.txt
pyproject.toml
Dockerfile
```

---

## 7.3 数据流程

```text
GitHub Repository
       ↓
文件读取
       ↓
Chunk
       ↓
Embedding
       ↓
Qdrant
```

---

## 7.4 Chunk Metadata

每个向量至少保存：

```text
repository_id
file_path
language
chunk_index
content
source_type
```

例如：

```json
{
  "repository_id": 1,
  "file_path": "app/agents/research_agent.py",
  "language": "python",
  "chunk_index": 3
}
```

---

## 7.5 Search

实现：

```text
QdrantSearchService
```

输入：

```text
"Workflow在哪里实现？"
```

输出：

```text
workflow.py
graph.py
agent.py
```

---

## 7.6 完成标准

可以完成：

```text
代码导入
 ↓
Embedding
 ↓
Qdrant
 ↓
自然语言查询
 ↓
返回相关代码片段
```

---

# 8. Phase 5 —— 自研 Workflow Engine

这是核心阶段。

## 8.1 目标

不使用：

```text
LangGraph StateGraph
```

自己实现：

```text
Workflow
Node
State
Transition
Checkpoint
RetryPolicy
Interrupt
Event
```

---

# 8.2 第一版只做最小 Workflow

先实现：

```text
Start
 ↓
Node A
 ↓
Node B
 ↓
Node C
 ↓
End
```

---

## 8.3 BaseNode

建议接口：

```python
class BaseNode:

    name: str

    async def execute(
        self,
        state,
        context
    ):
        raise NotImplementedError
```

---

## 8.4 Workflow

负责：

```text
读取当前Node
执行Node
更新State
决定下一个Node
处理异常
```

---

## 8.5 State

保存：

```text
run_id
status
current_node
repository
research_plan
task_results
agent_outputs
evidences
retry_count
errors
```

---

## 8.6 State Transition

例如：

```text
CREATED
 ↓
PLANNING
 ↓
WAITING_DESIGN
 ↓
ANALYZING
 ↓
VERIFYING
 ↓
SYNTHESIZING
 ↓
WAITING_REVIEW
 ↓
FINALIZING
 ↓
COMPLETED
```

异常：

```text
FAILED
RETRYING
PAUSED
```

---

## 8.7 完成标准

必须证明：

```text
Workflow能够顺序执行Node
Workflow能够保存State
Node失败能够捕获
能够知道当前执行到哪里
```

---

# 9. Phase 6 —— Tool Layer

## 9.1 目标

建立统一 Tool 抽象。

第一批 Tool：

```text
GitHubRepositoryTool
GitHubCodeSearchTool
FileReaderTool
DependencyAnalyzerTool
QdrantSearchTool
MySQLQueryTool
ReportExportTool
```

---

## 9.2 BaseTool

```python
class BaseTool:

    name: str
    description: str

    async def execute(
        self,
        input_data,
        context
    ):
        ...
```

---

## 9.3 GitHubRepositoryTool

负责：

```text
获取 Repository 信息
获取分支
获取文件树
获取文件
```

---

## 9.4 GitHubCodeSearchTool

负责：

```text
搜索类
搜索函数
搜索关键词
搜索Agent
搜索Workflow
搜索Skill
搜索Tool
```

---

## 9.5 FileReaderTool

负责：

```text
读取文件
限制文件大小
处理编码
返回行号
```

---

## 9.6 DependencyAnalyzerTool

分析：

```text
requirements.txt
pyproject.toml
package.json
Dockerfile
docker-compose.yml
```

得到：

```text
Python版本
框架
数据库
LLM
Embedding
部署组件
```

---

## 9.7 完成标准

每个 Tool 都必须有：

```text
输入Schema
输出Schema
异常处理
日志
测试
```

---

# 10. Phase 7 —— Skill Layer

## 10.1 目标

将多个 Tool 组合成可复用能力。

---

## 10.2 Skill 与 Tool

关系：

```text
Agent
 ↓
Skill
 ↓
多个 Tool
```

例如：

```text
CodeArchitectureAnalysisSkill
 ├── CodeSearchTool
 ├── FileReaderTool
 ├── DependencyAnalyzerTool
 └── QdrantSearchTool
```

---

## 10.3 外部 Skill

通用能力优先考虑：

```text
Web Research
Web Reader / Browser
Document / PDF Parsing
```

---

## 10.4 自研 Skill

核心能力：

```text
GitHub Repository Analysis
Code / Architecture Analysis
Agent / Workflow Analysis
Evidence Verification
Project Comparison
```

---

## 10.5 BaseSkill

建议：

```python
class BaseSkill:

    name: str
    description: str

    async def execute(
        self,
        context,
        input_data
    ):
        ...
```

---

## 10.6 完成标准

至少跑通：

```text
RepositoryAnalysisSkill
CodeArchitectureAnalysisSkill
AgentWorkflowAnalysisSkill
```

---

# 11. Phase 8 —— Multi-Agent Layer

## 11.1 目标

实现 5 个核心 Agent。

```text
1. Requirement & Planner Agent
2. Project Agent
3. Technology Agent
4. Code & Architecture Agent
5. Synthesis & Critic Agent
```

---

# 11.2 Requirement & Planner Agent

输入：

```text
用户问题
Repository URL
```

输出：

```text
分析目标
分析维度
Research Plan
Analysis Tasks
```

它负责：

> 决定“分析什么”。

不负责最终分析。

---

# 11.3 Project Agent

负责：

```text
项目是什么
解决什么问题
用户如何使用
输入是什么
输出是什么
核心功能
运行方式
```

---

# 11.4 Technology Agent

负责：

```text
Python
Framework
LLM
Embedding
Agent Framework
Workflow
RAG
Database
Redis
Docker
```

重要结论必须尽量绑定 Evidence。

---

# 11.5 Code & Architecture Agent

这是核心 Agent。

分析：

```text
目录
模块
类
函数
调用关系
数据流
Agent
Workflow
Skill
Tool
Database
执行流程
```

---

# 11.6 Synthesis & Critic Agent

负责：

```text
汇总
检查
纠错
冲突检测
最终综合
```

重点检查：

```text
有没有遗漏
有没有无证据结论
README和源码是否冲突
Agent判断是否正确
Workflow判断是否正确
```

---

# 11.7 完成标准

输入：

```text
GitHub Repository
+
用户问题
```

至少可以输出：

```text
项目概览
+
技术栈
+
Agent分析
+
Workflow分析
+
源码架构分析
```

---

# 12. Phase 9 —— Evidence / Claim / Citation

## 12.1 目标

让系统从：

```text
LLM说了什么
```

升级到：

```text
LLM为什么这么说
```

---

## 12.2 Evidence

模型：

```text
Evidence
├── source_type
├── repository_id
├── file_path
├── line_start
├── line_end
├── content
└── url
```

---

## 12.3 Claim

例如：

```text
Claim：

该项目存在多个Agent。
```

---

## 12.4 Citation

关系：

```text
Claim
 ↓
Evidence
 ↓
Source
 ↓
File
 ↓
Line
```

---

## 12.5 Evidence状态

建议：

```text
VERIFIED
UNVERIFIED
CONFLICT
```

---

## 12.6 完成标准

报告中的重要结论可以追溯到：

```text
Repository
 ↓
File
 ↓
Line
 ↓
Evidence
 ↓
Claim
```

---

# 13. Phase 10 —— HITL / Checkpoint / Pause / Resume / Retry

这是企业级 Workflow 能力的重要部分。

---

## 13.1 Design Gate

流程：

```text
Planner
 ↓
Research Plan
 ↓
WAITING_DESIGN
 ↓
用户Approve
 ↓
ANALYZING
```

---

## 13.2 Pause

用户：

```text
POST /pause
```

Workflow：

```text
ANALYZING
 ↓
PAUSED
```

保存：

```text
current_node
state
task results
retry count
```

---

## 13.3 Checkpoint

例如：

```text
Task 1
 ↓
Checkpoint

Task 2
 ↓
Checkpoint

Task 3
```

Task 3失败：

```text
恢复
 ↓
Task 3
```

不用重新执行前两个任务。

---

## 13.4 Resume

```text
POST /resume
```

流程：

```text
MySQL
 ↓
读取Checkpoint
 ↓
恢复WorkflowState
 ↓
恢复当前Node
 ↓
继续执行
```

---

## 13.5 Retry

设计：

```text
RetryPolicy
```

例如：

```text
max_retries = 3
```

可Retry：

```text
Timeout
Temporary Network Error
LLM Temporary Error
GitHub API Temporary Error
```

不可Retry：

```text
Invalid Input
Invalid Repository
Permission Denied
```

---

## 13.6 完成标准

至少验证：

```text
人工审核
✓

暂停
✓

恢复
✓

Node失败
✓

Retry
✓

Checkpoint恢复
✓
```

---

# 14. Phase 11 —— Memory / Context Manager

## 14.1 Memory

第一版不要做过度复杂的长期记忆。

先做：

```text
Run Memory
Project Memory
```

---

## 14.2 Run Memory

保存：

```text
用户问题
Research Plan
Agent Outputs
Evidence
当前状态
```

---

## 14.3 Project Memory

记录：

```text
某个Repository历史分析结果
```

例如：

```text
Repository A

第一次：
技术栈分析

第二次：
Workflow分析

第三次：
源码变化
```

---

# 14.4 Context Manager

不能：

```text
整个Repository
 ↓
全部塞进Prompt
```

应该：

```text
用户问题
+
Research Plan
+
Repository Metadata
+
目录
+
相关源码
+
Evidence
+
历史结果
        ↓
Context Manager
        ↓
LLM
```

---

## 14.5 Context流程

```text
Question
 ↓
Intent
 ↓
Retrieve
 ↓
Filter
 ↓
Rank
 ↓
Context Assemble
 ↓
LLM
```

---

## 14.6 完成标准

用户问：

```text
这个项目Workflow怎么实现？
```

系统能够自动找到：

```text
Workflow相关代码
+
Agent相关代码
+
配置
+
Evidence
```

而不是加载整个Repository。

---

# 15. Phase 12 —— 第一个完整业务闭环

这是非常关键的里程碑。

使用：

```text
adityamhaske/Multi-Agent-Research-Assistant
```

作为第一个真实分析对象。

---

## 15.1 用户输入

```text
帮我分析：

https://github.com/adityamhaske/Multi-Agent-Research-Assistant

重点分析：

1. Multi-Agent
2. Workflow
3. Skill
4. Tool
5. RAG
6. Memory
7. 数据库
```

---

## 15.2 完整执行

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
Agent / Workflow / Skill / Tool Analysis
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

---

## 15.3 第一版报告

至少包含：

```text
项目概览
技术栈
目录结构
Agent架构
Workflow
Skill
Tool
RAG
Memory
数据库
关键源码
Evidence
```

---

# 16. Phase 13 —— 多项目比较

## 16.1 目标

支持：

```text
Project A
+
Project B
```

---

## 16.2 流程

```text
Repository A
 ↓
Analysis A

Repository B
 ↓
Analysis B

        ↓

Comparison Agent
```

---

## 16.3 比较维度

```text
Agent数量
Workflow
Skill
Tool
RAG
Memory
Database
部署
代码复杂度
扩展方式
```

比较必须基于：

```text
Analysis Result
+
Evidence
```

不能让 LLM 凭空判断。

---

# 17. Phase 14 —— Learning Path / Report / Export

## 17.1 Learning Path

输入：

```text
项目
+
用户目标
```

输出：

```text
学习顺序
需要掌握的技术
核心源码
推荐阅读路径
项目改造建议
```

---

## 17.2 Report Service

不要让 Agent 自己负责文件生成。

采用：

```text
Agent
 ↓
Structured Report Data
 ↓
Report Service
 ↓
Markdown
JSON
```

后续再增加：

```text
PDF
```

---

## 17.3 最终报告结构

```text
01 项目概览
02 项目解决的问题
03 用户使用方式
04 技术栈
05 系统架构
06 用户输入 → 系统执行 → 最终输出
07 Agent架构
08 Workflow
09 Skill
10 Tool
11 Memory
12 RAG
13 数据库
14 API
15 核心源码分析
16 Evidence
17 Claim-Citation
18 项目比较
19 学习路线
20 改造建议
21 附录
```

---

# 18. Phase 15 —— 测试 / Docker / 审计 / 优化

## 18.1 测试层级

### Unit Test

测试：

```text
Tool
Skill
Agent
Workflow Node
Repository
Context
Evidence
```

---

### Integration Test

测试：

```text
FastAPI
+
MySQL
+
Qdrant
+
Workflow
```

---

### End-to-End Test

测试：

```text
用户请求
 ↓
Planner
 ↓
Workflow
 ↓
Agent
 ↓
Tool
 ↓
Evidence
 ↓
Report
```

---

# 18.2 Audit Log

记录：

```text
run_id
node
agent
tool
skill
input
output
status
error
timestamp
```

例如：

```text
run=001
node=code_analysis
agent=CodeArchitectureAgent
tool=GitHubCodeSearchTool
status=SUCCESS
```

---

# 18.3 Docker

最终再做：

```text
FastAPI
MySQL
Qdrant
```

Docker Compose：

```text
api
mysql
qdrant
```

后续需要长任务时再考虑：

```text
Redis
Celery
Worker
```

不要一开始就把所有基础设施都加进来。

---

# 19. 推荐的 Git Commit 节奏

每个小功能完成就提交。

例如：

```text
feat: initialize project structure

feat: add application config

feat: add logging system

feat: add exception handling

feat: add analysis api

feat: add mysql connection

feat: add repository models

feat: add qdrant service

feat: implement workflow node

feat: implement workflow engine

feat: add github repository tool

feat: add code search tool

feat: add repository analysis skill

feat: add planner agent

feat: add project analysis agent

feat: add technology analysis agent

feat: add code architecture agent

feat: add evidence system

feat: add checkpoint

feat: add retry mechanism

feat: add human review

feat: add memory

feat: add context manager

feat: complete end-to-end analysis

feat: add project comparison

feat: add report export

chore: dockerize application
```

---

# 20. 每个 Phase 的完成检查表

## Phase 0

```text
[ ] Python环境
[ ] Git
[ ] 项目目录
[ ] FastAPI启动
[ ] /health
[ ] pytest
[ ] README
```

## Phase 1

```text
[ ] Config
[ ] .env
[ ] Logging
[ ] Exception
[ ] Error Response
```

## Phase 2

```text
[ ] 创建Analysis
[ ] 查询Analysis
[ ] Approve
[ ] Pause
[ ] Resume
[ ] Retry
[ ] Report
```

## Phase 3

```text
[ ] MySQL连接
[ ] SQLAlchemy
[ ] Alembic
[ ] Repository
[ ] AnalysisRun
[ ] ResearchPlan
[ ] AnalysisTask
[ ] AgentOutput
```

## Phase 4

```text
[ ] Qdrant连接
[ ] Collection
[ ] Embedding
[ ] Chunk
[ ] Upsert
[ ] Search
```

## Phase 5

```text
[ ] Node
[ ] Workflow
[ ] State
[ ] Transition
[ ] Checkpoint
[ ] Retry
[ ] Pause
[ ] Resume
```

## Phase 6

```text
[ ] GitHub Repository Tool
[ ] Code Search Tool
[ ] File Reader Tool
[ ] Dependency Tool
[ ] Qdrant Tool
[ ] MySQL Tool
```

## Phase 7

```text
[ ] BaseSkill
[ ] Skill Manager
[ ] Repository Analysis Skill
[ ] Code Architecture Skill
[ ] Agent Workflow Skill
[ ] Evidence Skill
```

## Phase 8

```text
[ ] Planner Agent
[ ] Project Agent
[ ] Technology Agent
[ ] Code Architecture Agent
[ ] Critic Agent
```

## Phase 9

```text
[ ] Evidence
[ ] Claim
[ ] Citation
[ ] Evidence Verification
[ ] Source Traceability
```

## Phase 10

```text
[ ] Design Gate
[ ] Human Approve
[ ] Pause
[ ] Resume
[ ] Checkpoint
[ ] Retry
[ ] Retry Policy
```

## Phase 11

```text
[ ] Run Memory
[ ] Project Memory
[ ] Context Manager
[ ] Retrieval
[ ] Context Filtering
[ ] Context Assembly
```

## Phase 12

```text
[ ] 单项目完整分析
[ ] Agent协作
[ ] Workflow执行
[ ] Evidence
[ ] Critic
[ ] HITL
[ ] Report
```

## Phase 13

```text
[ ] 多项目分析
[ ] Comparison Agent
[ ] Evidence-based Comparison
```

## Phase 14

```text
[ ] Learning Path
[ ] Markdown Report
[ ] JSON Report
[ ] Report Service
```

## Phase 15

```text
[ ] Unit Test
[ ] Integration Test
[ ] E2E Test
[ ] Audit Log
[ ] Docker
[ ] Docker Compose
[ ] README
[ ] Demo
```

---

# 21. 最终项目架构

完成之后，你的项目应该形成：

```text
                         User
                          │
                          ▼
                       FastAPI
                          │
                          ▼
                  Analysis Service
                          │
                          ▼
                  Workflow Engine
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
           Planner     Project     Technology
           Agent       Agent       Agent
              │           │           │
              └───────────┼───────────┘
                          ▼
                Code Architecture
                       Agent
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
           Skills       Tools      Context
              │           │           │
              └───────────┼───────────┘
                          ▼
                    Evidence System
                          │
                          ▼
                   Critic Agent
                          │
                 ┌────────┴────────┐
                 │                 │
               PASS              FAIL
                 │                 │
                 │               Retry
                 │                 │
                 └────────┬────────┘
                          ▼
                    Synthesis
                          │
                          ▼
                    Human Review
                          │
                          ▼
                      Report
```

底层：

```text
                  ┌───────────────┐
                  │     MySQL     │
                  │               │
                  │ Run           │
                  │ Task          │
                  │ Agent Output  │
                  │ Evidence      │
                  │ Checkpoint    │
                  │ Audit Log     │
                  └───────────────┘

                  ┌───────────────┐
                  │    Qdrant     │
                  │               │
                  │ Source Code   │
                  │ README        │
                  │ Documents     │
                  │ Evidence      │
                  │ Analysis      │
                  └───────────────┘
```

---

# 22. 你真正开始开发时的第一条路线

不要现在直接开始 Phase 8 Agent。

你的第一轮开发应该严格执行：

```text
Day / Step 1
Phase 0
项目骨架
        ↓
Step 2
Phase 1
Config + Logging + Exception
        ↓
Step 3
Phase 2
FastAPI
        ↓
Step 4
Phase 3
MySQL
        ↓
Step 5
Phase 4
Qdrant
        ↓
Step 6
Phase 5
Workflow Engine
        ↓
Step 7
Phase 6
Tool
        ↓
Step 8
Phase 7
Skill
        ↓
Step 9
Phase 8
Agent
        ↓
Step 10
Phase 9
Evidence
        ↓
Step 11
Phase 10
HITL + Checkpoint + Retry
        ↓
Step 12
Phase 11
Memory + Context
        ↓
Step 13
Phase 12
完整闭环
```

**Phase 12 是第一个真正的里程碑。**

在 Phase 12 之前，你是在“搭建 Agent 平台”。

到了 Phase 12，你才真正得到：

> **一个能够输入 GitHub AI Agent 项目 → 自动研究源码 → Multi-Agent 协作 → Tool / Skill 调用 → Workflow 编排 → Evidence 验证 → Human Review → 输出项目分析报告的完整 AI 应用。**

这也与你原来的项目定位一致：核心不是简单总结 README，而是让 Multi-Agent 真正研究 GitHub Agent 项目的代码、架构以及 Agent / Workflow / Skill / Tool，并将关键结论与源码证据关联起来。fileciteturn8file2

---

# 23. 开发时最重要的几个“不要”

### 不要 1：不要先做前端

现在：

```text
FastAPI
+
CLI
+
Swagger
```

完全够你开发。

---

### 不要 2：不要一开始做 5 个 Agent

顺序：

```text
Planner
 ↓
Project
 ↓
Technology
 ↓
Code
 ↓
Critic
```

一个一个做。

---

### 不要 3：不要让 Agent 直接操作数据库

不要：

```text
Agent → SQLAlchemy
```

应该：

```text
Agent
 ↓
Service / Repository
 ↓
MySQL
```

---

### 不要 4：不要让 Agent 自己控制 Workflow

不要：

```text
Agent决定下一节点
Agent修改Workflow状态
```

应该：

```text
Agent
 ↓
返回结构化结果
 ↓
Workflow Engine
 ↓
决定下一步
```

---

### 不要 5：不要所有东西都做成 Skill

你的设计已经明确：

```text
通用能力
→ 外部Skill

核心业务能力
→ 自研Skill
```

这样才能体现：

```text
External Skill Integration
+
Custom Skill Development
```

而不是单纯堆 Skill。fileciteturn8file0

---

### 不要 6：不要让 LLM 凭空分析源码

正确：

```text
Tool
 ↓
Source
 ↓
Evidence
 ↓
Context
 ↓
Agent
 ↓
Claim
```

而不是：

```text
LLM
 ↓
“我觉得这个项目应该是这样”
```

---

### 不要 7：不要最后才测试

每个 Phase：

```text
实现
 ↓
测试
 ↓
修复
 ↓
Commit
 ↓
下一Phase
```

---

# 24. 最终开发目标

最终你真正拿去写简历的，不应该只是：

> “GitHub 项目分析 Agent”

而应该能够描述成：

> **基于 Python / FastAPI 自研 Multi-Agent Workflow 平台，构建 GitHub AI Agent 开源项目智能分析系统；通过自研 Workflow Engine 实现任务编排、状态持久化、Checkpoint、Pause/Resume、Retry 与 HITL，通过 Skill / Tool 抽象实现 GitHub 仓库、代码检索、依赖分析和向量检索能力，并基于 MySQL + Qdrant 构建结构化数据与源码知识存储，通过 Evidence / Claim-Citation 实现分析结论的源码级可追溯，最终完成项目架构、Agent、Workflow、Skill、Tool、RAG、Memory 等维度的自动化分析与报告生成。**

这就是你整个项目应该最终达到的工程形态。原项目设计中的技术目标也是围绕 `Multi-Agent + External Skill Integration + Custom Skill + Tool Calling + Workflow + Memory + Context + Evidence + HITL + Retry + Checkpoint + FastAPI + MySQL + Qdrant` 展开的。fileciteturn8file1
