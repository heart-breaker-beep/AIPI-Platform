# AI Agent / GitHub 开源项目智能分析平台——项目设计文档

> **版本：V1 设计版（2026-09-21）**
>
> **项目定位**：参考 Multi-Agent-Research-Assistant 的 Research Workflow 思路，将原“企业竞品情报分析”业务改造成“AI Agent / GitHub 开源项目智能研究与分析”场景。
>
> **目标岗位**：AI 应用开发 / Agent 应用开发
>
> **核心技术目标**：Multi-Agent + External Skill Integration + Custom Skill + Tool Calling + Workflow + Memory + Context + Evidence + HITL + Retry + Checkpoint + FastAPI + MySQL + Qdrant。
>
> **技术约束**：
> - 不使用 LangGraph `StateGraph`
> - Workflow Engine 自研
> - MySQL 作为业务数据库
> - Qdrant 作为向量数据库
> - FastAPI 作为后端 API
> - Redis / Celery 作为后续长任务基础设施
> - 当前阶段不考虑前端
> - 第一阶段优先完成后端 + Workflow + 数据层 + CLI/API 演示

---

# 1. 项目概述

## 1.1 项目名称

**AI Agent / GitHub Project Intelligence Platform**

中文：

**AI Agent / GitHub 开源项目智能分析平台**

简称：

**AIPI Platform**

---

## 1.2 为什么从 Research Assistant 改造成 GitHub Agent 项目智能分析平台

原始 Research Assistant 的核心能力是：

> 用户提出一个复杂研究问题，系统自动拆解任务、检索资料、收集证据、批判性检查、生成带引用的研究报告。

这套能力可以迁移到 GitHub AI Agent 项目研究场景。

原来的：

```text
Research Question
    ↓
Research Tasks
    ↓
Research Report
```

重新设计为：

```text
Project Analysis Request
    ↓
Repository Identification
    ↓
Research Plan
    ↓
Multi-Agent Project Analysis
    ↓
Code / Architecture Evidence
    ↓
Agent / Workflow / Skill / Tool Analysis
    ↓
Project Comparison
    ↓
Critic Verification
    ↓
Human Review
    ↓
Project Intelligence Report
```

项目不再只是：

> “AI 帮用户总结 GitHub README”。

而是：

> **AI 自动研究 GitHub AI Agent 项目的源码、架构和运行机制，并把项目结构、Agent、Workflow、Skill、Tool、RAG、Memory、技术栈和关键证据组织成可追溯的分析报告。**

---

# 2. 为什么选择这个业务方向

相比金融、供应链、医疗等行业，这个方向有几个明显优势：

1. 业务理解成本低
2. 用户输入和输出非常直观
3. GitHub 项目本身就是数据源
4. Agent / Workflow / Skill / Tool 都是天然分析对象
5. 很容易体现源码分析能力
6. 很适合现场面试 Demo
7. 可以直接用于研究自己正在学习的 Agent 项目
8. 后续可以自然扩展到项目对比、技术选型和学习路线

---

# 3. 真实业务场景

## 3.1 场景 A：分析一个 GitHub Agent 项目

用户：

```text
请分析：
https://github.com/adityamhaske/Multi-Agent-Research-Assistant

重点告诉我：

1. 项目是干什么的
2. 技术栈
3. Agent 有哪些
4. Workflow 怎么运行
5. Tool / Skill 怎么调用
6. Memory / RAG 怎么实现
7. 用户输入到最终输出的完整流程
```

系统：

```text
Repository 获取
    ↓
项目结构分析
    ↓
README / 配置 / 依赖分析
    ↓
Project Agent
    ↓
Technology Agent
    ↓
Code & Architecture Agent
    ↓
Agent / Workflow / Skill / Tool 分析
    ↓
Evidence 提取
    ↓
Critic 验证
    ↓
最终项目分析报告
```

---

## 3.2 场景 B：多个 GitHub Agent 项目横向比较

用户：

```text
比较 Project A、Project B、Project C。

重点比较：

1. Multi-Agent
2. Workflow
3. Skill
4. Tool Calling
5. Memory
6. RAG
7. 数据库
8. API
9. 部署方式
```

系统：

```text
统一分析维度
    ↓
各项目独立分析
    ↓
技术事实标准化
    ↓
Evidence 校验
    ↓
横向比较
    ↓
差异分析
```

---

## 3.3 场景 C：源码架构深度分析

用户：

```text
帮我分析这个项目的源码结构，
重点解释：

agents/
workflow/
tools/
skills/
memory/
api/
models/
services/

分别负责什么。
```

系统输出：

```text
目录结构
    ↓
模块职责
    ↓
模块依赖
    ↓
调用关系
    ↓
核心执行链
    ↓
关键源码 Evidence
```

---

## 3.4 场景 D：分析 Agent 执行流程

用户：

```text
用户输入一个研究问题后，
这个项目内部到底是怎么执行的？

请从 API 到最终报告完整解释。
```

系统：

```text
API
 ↓
Request
 ↓
Workflow
 ↓
Planner
 ↓
Research Agents
 ↓
Skills
 ↓
Tools
 ↓
Evidence
 ↓
Synthesis
 ↓
Report
```

并为关键结论提供：

```text
文件
类 / 函数
源码位置
Evidence
```

---

## 3.5 场景 E：生成项目学习路线与改造建议

用户：

```text
我想学习这个项目，并把它改造成自己的简历项目。

告诉我：

1. 先学什么
2. 先看哪些源码
3. 哪些模块最重要
4. 可以怎么改造
5. 可以增加哪些 Agent / Skill
```

系统输出：

```text
项目架构
    ↓
核心源码路径
    ↓
技术知识依赖
    ↓
推荐学习顺序
    ↓
改造方向
    ↓
简历项目建议
```

---

# 4. 项目最终要解决的问题

传统 GitHub Agent 项目研究通常是：

```text
搜索 GitHub
    ↓
打开 README
    ↓
手动看目录
    ↓
搜索关键文件
    ↓
理解 Agent
    ↓
理解 Workflow
    ↓
理解 Tool / Skill
    ↓
自己画架构图
    ↓
自己整理学习笔记
```

存在的问题：

- README 往往只描述项目表面功能
- Agent / Workflow 的真实执行关系需要读源码才能理解
- Tool / Skill / Memory 分散在不同目录
- 技术栈信息分散在依赖、Docker、配置和源码中
- LLM 容易把没有证据的信息“猜出来”
- 很难追溯一个结论来自哪个文件
- 多项目横向比较非常耗时
- 项目更新后需要重新研究
- 陌生 Agent 项目缺少清晰学习路径

本项目希望变成：

```text
GitHub Repository
    ↓
Repository Analysis
    ↓
Project Understanding
    ↓
Architecture Analysis
    ↓
Agent / Workflow / Skill / Tool Analysis
    ↓
Code Evidence
    ↓
Critic Verification
    ↓
Project Comparison
    ↓
Learning Path
    ↓
Human Review
    ↓
Project Intelligence Report
```

核心不是：

> **“让 LLM 总结 README。”**

而是：

> **“让 Multi-Agent 系统真正研究 GitHub Agent 项目的代码和架构，并让关键结论可以回溯到源码 Evidence。”**

---

# 5. 核心业务闭环

```text
                    用户
                     │
                     ▼
          Project Analysis Request
                     │
                     ▼
       Requirement & Planner Agent
                     │
                     ▼
               Research Plan
                     │
                     ▼
              ┌─────────────┐
              │ Design Gate │
              │ Workflow/HITL│
              └──────┬──────┘
                     │ Approve
                     ▼
          Project Analysis Router
                     │
       ┌─────────────┼────────────────┐
       ▼             ▼                ▼
 Project Agent   Technology Agent   Code & Architecture
       │             │                │
       ▼             ▼                ▼
项目功能分析      技术栈分析        源码/架构分析
       │             │                │
       └─────────────┼────────────────┘
                     ▼
       Agent / Workflow / Skill / Tool
                  深度分析
                     │
                     ▼
               Evidence Store
                     │
                     ▼
          Synthesis & Critic Agent
                /          \
             FAIL           PASS
              │               │
              ▼               ▼
            Retry        Normalization
              │               │
              └───────┬───────┘
                      ▼
             Project Comparison
                      │
                      ▼
               Learning Path
                      │
                      ▼
                Review Gate
                /        \
            Reject       Approve
              │            │
              ▼            ▼
         Rework Draft    Finalizer
                           │
                           ▼
              Project Intelligence Report
```

---

# 6. 系统架构分层

本项目统一采用：

```text
Agent
Workflow
Skill
Tool
Memory
Context
Data / Artifact
Infrastructure
```

---

## 6.1 Agent 层：负责智能决策与分析

核心 Agent 控制为 **5 个**：

```text
1. Requirement & Planner Agent
2. Project Agent
3. Technology Agent
4. Code & Architecture Agent
5. Synthesis & Critic Agent
```

原则：

> **不要为了体现 Multi-Agent 而把每个小功能都拆成 Agent。**

---

## 6.2 Workflow 层：负责流程控制

Workflow 不负责产生最终业务结论，而负责：

```text
什么时候执行
执行哪个 Agent
是否等待人工
是否暂停
从哪里恢复
是否重试
是否进入下一阶段
```

核心节点：

```text
Planning Node
Design Gate
Project Analysis Router
Critic Node
Retry Node
Review Gate
Finalizer Node
```

基础设施：

```text
State
Checkpoint
Interrupt
RetryPolicy
Event
```

---

## 6.3 Skill 层：外部 Skill + 自研 Skill 混合

Skill 不是简单函数，也不是所有能力都必须自己实现。

本项目采用：

> **“通用能力优先复用外部 Skill，项目核心分析能力自行研发”**

这样既避免重复造轮子，又能体现 AI 应用开发中的 Skill 集成、组合与自研能力。

### Skill 分层

```text
Skill
│
├── External Skills
│   ├── Web Research Skill
│   ├── Web Reader / Browser Skill
│   └── Document / PDF Parsing Skill
│
└── Custom Skills
    ├── GitHub Repository Analysis Skill
    ├── Code / Architecture Analysis Skill
    ├── Agent / Workflow Analysis Skill
    ├── Evidence Verification Skill
    └── Project Comparison Skill
```

### 外部 Skill 的使用原则

外部 Skill 主要承担通用、成熟、与本项目核心差异化关系不大的能力：

```text
Web Research
Web Page Reading
Browser Interaction
PDF / Document Parsing
```

项目不需要重复实现这些基础能力，而是通过统一 Skill Adapter 接入。

```text
External Skill
      ↓
Skill Adapter
      ↓
统一 Skill Interface
      ↓
Agent
```

### 自研 Skill 的使用原则

与本项目核心业务逻辑强相关的能力自己实现：

```text
GitHub 项目分析
源码 / 架构分析
Agent / Workflow 分析
Evidence 验证
项目横向比较
```

这些能力直接决定项目的核心价值，也是简历中重点体现的自研部分。

### Skill 与 Tool 的关系

```text
Agent
  ↓
Skill
  ↓
Tool
```

但不是所有调用都必须经过 Skill：

```text
简单动作：

Agent
  ↓
Tool
```

复杂、可复用的业务能力：

```text
Agent
  ↓
Skill
  ↓
多个 Tool
```

例如：

```text
GitHub Repository Analysis Skill
        │
        ├── GitHub Repository Tool
        ├── File Reader Tool
        ├── Code Search Tool
        └── Dependency Analysis Tool
```

外部 Web Research Skill 也可以进一步调用：

```text
Web Research Skill
        │
        ├── Web Search Tool
        └── Web Reader Tool
```

### 本项目的 Skill 设计目标

不是：

> “所有功能都包装成 Skill。”

而是：

> **“让 Agent 能够组合外部通用 Skill 与自研业务 Skill，完成复杂项目研究任务。”**

---

## 6.4 Tool 层：负责具体外部动作

核心 Tool：

```text
github_repository
github_code_search
file_reader
dependency_analyzer
qdrant_search
mysql_query
report_export
```

原则：

```text
Agent
  ↓
Skill
  ↓
Tool
```

但并不是所有 Tool 都必须经过 Skill。

简单任务可以：

```text
Agent
  ↓
Tool
```

---

## 6.5 Memory 层

第一阶段只实现：

```text
Research Run Memory
```

保存：

```text
用户问题
项目
历史分析结果
Research Plan
Agent 输出
Evidence
最终报告
```

后续再扩展：

```text
Project Long-term Memory
User Preference Memory
Cross-project Memory
```

---

## 6.6 Context 层

负责把当前任务需要的信息组装给 Agent：

```text
用户问题
+
Research Plan
+
项目结构
+
源码片段
+
历史分析结果
+
Evidence
+
其他 Agent 输出
```

最终：

```text
Context Manager
       ↓
Agent Prompt
```

---

# 7. 五个核心 Agent

## 7.1 Requirement & Planner Agent

负责：

```text
需求理解
+
Repository 识别
+
分析维度确定
+
研究任务规划
```

输入：

```text
帮我分析 Multi-Agent-Research-Assistant，
重点研究 Agent、Workflow、Skill、Tool 和 RAG。
```

输出：

```json
{
  "analysis_type": "github_agent_project",
  "repositories": [
    "owner/repository"
  ],
  "dimensions": [
    "project",
    "technology",
    "architecture",
    "agent",
    "workflow",
    "skill",
    "tool",
    "rag",
    "memory"
  ]
}
```

然后生成：

```text
Research Plan
```

---

## 7.2 Project Agent

回答：

> **“这个 GitHub 项目到底是干什么的？”**

研究：

- 项目定位
- 核心功能
- 用户输入
- 系统输出
- 使用场景
- README / Docs
- API / CLI
- 运行方式
- 项目依赖

输出：

```json
{
  "repository": "owner/repo",
  "purpose": "",
  "features": [],
  "inputs": [],
  "outputs": [],
  "use_cases": [],
  "evidence_ids": []
}
```

---

## 7.3 Technology Agent

分析：

```text
Python
FastAPI
LLM
Embedding
Agent Framework
Workflow
RAG
Vector DB
MySQL / PostgreSQL
Redis
Celery
Docker
Authentication
Deployment
```

重点原则：

> **只有源码、依赖文件、配置文件或官方项目资料能够证明的信息，才能进入 VERIFIED 状态。**

---

## 7.4 Code & Architecture Agent

这是 GitHub 项目版最核心的 Agent。

负责：

```text
目录结构
 ↓
模块职责
 ↓
类 / 函数
 ↓
模块依赖
 ↓
API
 ↓
Workflow
 ↓
Agent
 ↓
Skill
 ↓
Tool
 ↓
Database
```

例如：

```text
backend/
├── agents/
├── workflow/
├── tools/
├── skills/
├── memory/
├── api/
├── models/
└── services/
```

分析：

```text
main.py
 ↓
FastAPI Router
 ↓
Workflow
 ↓
Planner
 ↓
Agent
 ↓
Skill
 ↓
Tool
 ↓
Database
```

输出：

```json
{
  "architecture": {},
  "modules": [],
  "dependencies": [],
  "execution_flow": [],
  "evidence_ids": []
}
```

---

## 7.5 Synthesis & Critic Agent

合并：

```text
Critic
+
Comparison
+
Synthesis
+
Finalization
```

负责：

### 质量检查

```text
是否遗漏核心模块
是否存在无证据结论
README 与源码是否冲突
Agent 职责是否理解正确
Workflow 是否存在错误推断
```

### 项目比较

统一比较：

```text
Multi-Agent
Workflow
Skill
Tool Calling
Memory
RAG
Database
API
Deployment
```

### 学习路线

生成：

```text
前置知识
 ↓
源码阅读顺序
 ↓
核心模块
 ↓
重点技术
 ↓
实践任务
```

### 最终报告

```text
Project Intelligence Report
```

---

# 8. Research Plan

## 8.1 Research Plan 数据结构

```json
{
  "plan_version": 1,
  "tasks": [
    {
      "task_id": "task_001",
      "repository": "owner/repo",
      "dimension": "architecture",
      "agent": "code_architecture_agent",
      "priority": "high",
      "dependencies": [],
      "evidence_required": true
    },
    {
      "task_id": "task_002",
      "repository": "owner/repo",
      "dimension": "technology",
      "agent": "technology_agent",
      "priority": "high",
      "dependencies": [],
      "evidence_required": true
    }
  ],
  "comparison_dimensions": [
    "agent",
    "workflow",
    "skill",
    "tool",
    "rag",
    "memory"
  ],
  "report_sections": [
    "Project Overview",
    "Architecture",
    "Agent",
    "Workflow",
    "Technology",
    "Evidence",
    "Learning Path"
  ]
}
```

---

## 8.2 Research Plan 生命周期

```text
Research Plan v1
      ↓
Human 修改
      ↓
Research Plan v2
      ↓
Design Gate Approve
      ↓
开始执行
```

支持：

```text
版本管理
人工修改
人工审批
任务追踪
Checkpoint
恢复执行
审计
```

---

# 9. Design Gate / HITL

Planner 生成计划后，不立即执行：

```text
WAITING_DESIGN_APPROVAL
```

用户可以：

```text
增加 Repository
删除 Repository
修改分析维度
增加源码分析范围
指定重点目录
修改报告结构
```

例如：

```text
原计划：

Project A

分析：
Agent
Workflow
Technology

用户修改：

Project A
Project B

增加：
Skill
Tool
Memory
RAG
源码执行流程
```

确认：

```text
DESIGN_APPROVED
```

继续执行。

---

# 10. Skill 设计

本项目的 Skill 分成两类：

```text
External Skill
    ↓
负责通用能力复用

Custom Skill
    ↓
负责项目核心分析能力
```

---

## 10.1 External Web Research Skill

**来源：外部现成 Skill / 第三方能力**

负责：

```text
Web Search
网页信息发现
公开资料研究
外部技术文档检索
```

适合用于：

```text
补充 GitHub README 中没有说明的技术资料
查询官方框架文档
验证项目依赖技术的公开资料
```

注意：

> Web Research Skill 只负责获取外部资料，不负责直接给出最终项目分析结论。

最终结论仍然需要进入 Evidence Verification 流程。

---

## 10.2 External Web Reader / Browser Skill

**来源：外部现成 Skill / 第三方能力**

负责：

```text
打开网页
读取网页正文
访问官方文档
处理动态网页
```

主要用于补充：

```text
GitHub Repository
官方 Documentation
Framework Documentation
Release Notes
```

如果 GitHub API 已经可以直接获取文件内容，则不需要为了简单读取操作而强制调用 Browser Skill。

---

## 10.3 External Document / PDF Parsing Skill

**来源：外部现成 Skill / 第三方能力**

负责：

```text
PDF 读取
文档解析
表格 / 文本提取
文档结构识别
```

主要用于分析：

```text
项目官方设计文档
技术白皮书
架构 PDF
开发文档
```

---

## 10.4 GitHub Repository Analysis Skill

**来源：自研**

这是项目第一个核心自研 Skill。

负责：

```text
Repository 获取
README 分析
目录树分析
关键配置识别
依赖文件识别
项目元信息提取
关键源码文件定位
```

内部可以组合：

```text
GitHub Repository Tool
File Reader Tool
Code Search Tool
Dependency Analysis Tool
```

输出：

```text
Repository Profile
Project Structure
Important Files
Dependencies
Evidence
```

---

## 10.5 Code / Architecture Analysis Skill

**来源：自研**

这是项目的核心差异化 Skill。

负责：

```text
目录分析
模块分析
依赖分析
调用链分析
数据流分析
核心执行链分析
```

例如：

```text
main.py
 ↓
FastAPI Router
 ↓
Service
 ↓
Workflow
 ↓
Agent
 ↓
Skill
 ↓
Tool
 ↓
Database
```

输出：

```text
Architecture Profile
Module Dependencies
Execution Flow
Source Evidence
```

---

## 10.6 Agent / Workflow Analysis Skill

**来源：自研**

负责：

```text
Agent 识别
Agent 职责分析
Workflow 识别
Workflow 状态分析
Agent 调用关系
Skill 调用关系
Tool 调用关系
```

最终形成：

```text
Agent
 ↓
Workflow
 ↓
Skill
 ↓
Tool
```

调用关系图。

---

## 10.7 Evidence Verification Skill

**来源：自研**

这是保证系统分析结果可信度的核心 Skill。

负责：

```text
Claim
 ↓
Evidence
 ↓
Source File
 ↓
Source Location
 ↓
Verification
```

状态：

```text
VERIFIED
UNVERIFIED
CONFLICT
```

例如：

```text
Claim:
“项目使用 Qdrant 作为向量数据库”

        ↓

Evidence:
docker-compose.yml
requirements.txt
config.py

        ↓

Verification:
VERIFIED
```

---

## 10.8 Project Comparison Skill

**来源：自研**

负责：

```text
统一分析维度
 ↓
结构化数据
 ↓
字段标准化
 ↓
Evidence 对齐
 ↓
横向比较
```

比较：

```text
Multi-Agent
Workflow
Skill
Tool Calling
Memory
RAG
Database
API
Deployment
```

该 Skill 不负责简单的“打分排名”，而是输出结构化差异：

```text
Project A:
Workflow = ...
Memory = ...

Project B:
Workflow = ...
Memory = ...

Difference:
...
```

---

## 10.9 Report Generation

报告生成不强制作为一个完全独立的自研 Skill。

第一阶段建议直接使用：

```text
Report Service
+
Markdown / JSON Export
```

后续如果需要复杂模板，再封装为：

```text
Report Generation Skill
```

这样可以避免为了“Skill 数量”而增加不必要的抽象。

---

## 10.10 Skill Adapter

为了统一外部 Skill 与自研 Skill，增加：

```text
Skill Adapter
```

统一接口：

```python
class Skill:
    name: str

    async def execute(
        self,
        context,
        input_data
    ):
        ...
```

外部 Skill：

```text
External Skill
      ↓
Skill Adapter
      ↓
Unified Skill Interface
```

自研 Skill：

```text
Custom Skill
      ↓
Unified Skill Interface
```

最终 Agent 不需要关心 Skill 是外部实现还是自研实现。

---

## 10.11 最终 Skill 目录

```text
skills/
│
├── external/
│   ├── web_research/
│   ├── web_reader/
│   └── document_parser/
│
├── github/
│   └── repository_analysis/
│
├── code/
│   └── architecture_analysis/
│
├── agent/
│   └── workflow_analysis/
│
├── evidence/
│   └── verification/
│
└── comparison/
    └── project_comparison/
```

最终关系：

```text
                    Agent
                      │
             ┌────────┴────────┐
             │                 │
       External Skills     Custom Skills
             │                 │
       Web Research       GitHub Analysis
       Web Reader         Code Architecture
       Document Parser    Agent Workflow
                          Evidence Verify
                          Project Comparison
             │                 │
             └────────┬────────┘
                      ▼
                  Tool Calling
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     GitHub          Code          Qdrant
      Tools         Tools          Tools
```

---

# 11. Tool Layer

## 11.1 GitHub Repository Tool

负责：

```text
Repository 信息
README
目录树
Commit
Release
文件内容
```

接口示例：

```python
class GitHubRepositoryTool:

    async def get_repository(
        self,
        owner: str,
        repo: str
    ):
        ...

    async def get_tree(
        self,
        owner: str,
        repo: str
    ):
        ...

    async def read_file(
        self,
        owner: str,
        repo: str,
        path: str
    ):
        ...
```

---

## 11.2 Code Search Tool

支持：

```text
关键词搜索
类搜索
函数搜索
Import 搜索
Agent 搜索
Tool 搜索
Workflow 搜索
Skill 搜索
```

例如：

```text
搜索：
StateGraph

返回：

workflow/graph.py
workflow/nodes.py
```

---

## 11.3 File Reader Tool

负责：

```text
README.md
requirements.txt
pyproject.toml
docker-compose.yml
.env.example
*.py
*.yaml
*.json
```

---

## 11.4 Dependency Analysis Tool

分析：

```text
requirements.txt
pyproject.toml
package.json
Dockerfile
docker-compose.yml
```

输出：

```text
Python
FastAPI
Qdrant
MySQL
Redis
LangChain
...
```

---

## 11.5 Qdrant Search Tool

用于：

```text
项目源码切片
项目文档
历史分析结果
项目知识库
```

进行语义检索。

---

## 11.6 MySQL Query Tool

用于查询：

```text
Repository
Analysis Run
Research Plan
Agent Profile
Evidence
Report
Project Change Event
```

等业务数据。

---

## 11.7 Report Export Tool

负责：

```text
Markdown
PDF
JSON
```

报告导出。

---

# 12. GitHub Source Priority

项目分析必须坚持：

> **源码 Evidence 优先于 LLM 推测。**

来源优先级：

```text
Level 1
实际源码
配置文件
依赖文件
Docker 文件

Level 2
官方 README
官方 Docs
GitHub Release

Level 3
官方 Blog
官方项目说明

Level 4
第三方技术文章
博客

Level 5
搜索摘要 / 未验证内容
```

例如：

```text
Claim：

项目使用 Qdrant。

Evidence：

pyproject.toml
docker-compose.yml
qdrant_client import
```

最终：

```text
VERIFIED
```

如果只有搜索结果说：

```text
“该项目可能使用 Qdrant”
```

则：

```text
UNVERIFIED
```

不能直接进入最终技术结论。

---

# 13. Evidence / Claim-Citation

Evidence Tracking 与 Claim-Citation Traceability 不合并。

## Evidence Tracking

解决：

> **系统收集了哪些证据？**

例如：

```text
Evidence #001
来源：
requirements.txt

内容：
qdrant-client

类型：
Dependency
```

---

## Claim-Citation Traceability

解决：

> **最终报告中的哪句话由哪些证据支持？**

例如：

```text
Claim：

项目使用 Qdrant 作为向量数据库。

       ↓

Evidence #001
requirements.txt

Evidence #002
docker-compose.yml
```

关系：

```text
Claim
 ↓
Evidence
 ↓
Source
 ↓
File / Line / URL
```

这样最终报告不是单纯 LLM 生成，而是：

```text
结论
+
证据
+
来源
```

---

# 14. Project Analysis Data Model

## 14.1 Repository

```text
repositories

id
github_url
owner
name
description
language
stars
forks
created_at
updated_at
```

---

## 14.2 Repository Architecture

```text
repository_architectures

id
repository_id
architecture_type
framework
backend
database
vector_database
cache
llm_provider
deployment
```

---

## 14.3 Agent Profile

```text
repository_agents

id
repository_id
agent_name
role
input
output
dependencies
evidence_ids
```

---

## 14.4 Skill Profile

```text
repository_skills

id
repository_id
skill_name
skill_type
description
source
adapter
tools
input_schema
output_schema
evidence_ids
```

其中：

```text
skill_type:
    external
    custom

source:
    third_party
    internal

adapter:
    Skill Adapter 名称
```

例如：

```json
{
  "skill_name": "web_research",
  "skill_type": "external",
  "source": "third_party"
}
```

以及：

```json
{
  "skill_name": "code_architecture_analysis",
  "skill_type": "custom",
  "source": "internal"
}
```

---

## 14.5 Tool Profile

```text
repository_tools

id
repository_id
tool_name
description
input_schema
output_schema
evidence_ids
```

---

## 14.6 Workflow Profile

```text
repository_workflows

id
repository_id
workflow_name
states
entry_point
exit_point
retry_policy
interrupt
resume
evidence_ids
```

---

## 14.7 Evidence

```text
evidences

id
repository_id
source_type
source_url
file_path
line_start
line_end
content
verification_status
created_at
```

---

# 15. Workflow State

第一阶段：

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
COMPARING
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

# 16. Checkpoint / Pause / Resume / Retry

每一个长任务保存：

```text
run_id
current_state
current_task
completed_tasks
failed_tasks
agent_outputs
evidence_ids
retry_count
context_snapshot
```

例如：

```text
Code Analysis
     ↓
读取 workflow/
     ↓
读取 agents/
     ↓
失败
     ↓
Checkpoint
     ↓
Retry
     ↓
继续分析
```

如果人工暂停：

```text
ANALYZING
    ↓
PAUSED
    ↓
Human Resume
    ↓
ANALYZING
```

---

# 17. Context Manager

Context Manager 负责：

```text
用户问题
+
Research Plan
+
Repository Metadata
+
Directory Tree
+
Code Snippets
+
Agent Outputs
+
Evidence
+
Memory
```

形成：

```text
Agent Context
```

避免：

```text
把整个 Repository
一次性塞进 Prompt
```

采用：

```text
按任务检索
+
按需加载
+
上下文裁剪
```

---

# 18. MySQL + Qdrant

## MySQL

保存结构化业务数据：

```text
repositories
analysis_runs
research_plans
analysis_tasks
agent_outputs
agent_profiles
skill_profiles
tool_profiles
workflow_profiles
evidences
claims
citations
reports
checkpoints
audit_logs
```

---

## Qdrant

保存：

```text
代码片段
README
项目文档
源码分析结果
历史报告
Evidence Embedding
```

用于：

```text
语义搜索
源码检索
项目知识检索
历史分析检索
```

关系：

```text
MySQL
结构化事实
       +
Qdrant
非结构化 / 语义知识
```

---

# 19. 最终报告

最终报告建议：

```text
1. 项目概览
2. 项目解决的问题
3. 技术栈
4. 系统架构
5. 用户输入 → 系统执行 → 最终输出
6. Agent 架构
7. Workflow
8. Skill
9. Tool
10. Memory
11. RAG
12. 数据库
13. API
14. 关键源码分析
15. Evidence
16. Claim-Citation
17. 项目优缺点
18. 学习路线
19. 改造建议
20. 附录
```

---

# 20. 一个完整 Demo

用户输入：

```text
帮我分析：
https://github.com/adityamhaske/Multi-Agent-Research-Assistant

我主要想学习它的 Multi-Agent Workflow，
并准备把它改造成自己的简历项目。
```

系统执行：

```text
① Requirement & Planner
        ↓
识别项目 + 分析目标
        ↓
② Research Plan
        ↓
③ Design Gate
        ↓
④ Project Agent
        ↓
⑤ Technology Agent
        ↓
⑥ Code & Architecture Agent
        ↓
⑦ Agent / Workflow / Skill Analysis
        ↓
⑧ Evidence Verification
        ↓
⑨ Synthesis & Critic
        ↓
⑩ Learning Path
        ↓
⑪ Human Review
        ↓
⑫ Final Report
```

最终：

```text
项目是什么
       ↓
用了什么技术
       ↓
有哪些 Agent
       ↓
Agent 怎么协作
       ↓
Workflow 怎么执行
       ↓
Skill 怎么封装
       ↓
Tool 怎么调用
       ↓
Memory 怎么实现
       ↓
RAG 怎么实现
       ↓
数据库怎么使用
       ↓
源码如何执行
       ↓
哪些结论有源码证据
       ↓
应该怎么学习
       ↓
应该怎么改造成自己的项目
```

---

# 21. MVP / V2 / V3

## MVP

第一阶段只实现：

```text
FastAPI
MySQL
Qdrant
自研 Workflow Engine

5 Agent
4~6 Skill
GitHub Tool
Code Search Tool
File Reader Tool
Dependency Tool

Research Plan
HITL
Checkpoint
Retry
Evidence
基础 Memory
Context Manager
Markdown Report
```

---

## V2

增加：

```text
GitHub 多项目比较
源码语义检索
Qdrant RAG
Claim-Citation
项目学习路线
PDF Export
SSE
Project Change Detection
```

---

## V3

增加：

```text
Scheduled Project Monitoring
GitHub Commit Analysis
Release Analysis
多模型 Provider
BYOK
Token / Cost Tracking
Audit Dashboard
Evaluation
Observability
Docker 部署
```

---

# 22. 暂时不要做

为了避免项目再次变得过于复杂，第一版明确不做：

```text
10+ Agent
动态 Agent 创建
Skill Marketplace
Skill 热加载
复杂 RBAC
复杂多租户
多层长期 Memory
复杂 Context Compression
动态 Workflow DSL
Celery 分布式集群
Redis Cluster
Browser Agent
Code Execution Agent
完整前端
```

---

# 23. 最终技术架构

```text
                        User
                         │
                         ▼
                    FastAPI API
                         │
                         ▼
              ┌────────────────────┐
              │   Workflow Engine  │
              └─────────┬──────────┘
                        │
                        ▼
             Requirement & Planner
                        │
                        ▼
                   Research Plan
                        │
                        ▼
                    Design Gate
                        │
                        ▼
             Project Analysis Router
                        │
       ┌────────────────┼─────────────────┐
       ▼                ▼                 ▼
 Project Agent     Technology Agent   Code & Architecture
       │                │                 │
       └────────────────┼─────────────────┘
                        ▼
             Skill / Tool Execution
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       GitHub        Code Search     File Reader
        Tool            Tool           Tool
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                 Evidence Store
                   │          │
                   ▼          ▼
                MySQL       Qdrant
                   │          │
                   └────┬─────┘
                        ▼
             Synthesis & Critic
                        │
                        ▼
                  Review Gate
                        │
                        ▼
                    Report
```

---

# 24. 推荐开发顺序

严格按照：

```text
01. 项目骨架
        ↓
02. FastAPI
        ↓
03. MySQL
        ↓
04. Qdrant
        ↓
05. Repository 数据模型
        ↓
06. Analysis Run 数据模型
        ↓
07. Research Plan
        ↓
08. Workflow State
        ↓
09. Workflow Node
        ↓
10. Workflow Router
        ↓
11. Checkpoint
        ↓
12. GitHub Repository Tool
        ↓
13. File Reader Tool
        ↓
14. Code Search Tool
        ↓
15. Requirement & Planner Agent
        ↓
16. Design Gate
        ↓
17. Project Agent
        ↓
18. Technology Agent
        ↓
19. Code & Architecture Agent
        ↓
20. Evidence System
        ↓
21. Synthesis & Critic Agent
        ↓
22. Retry
        ↓
23. Project Comparison
        ↓
24. Learning Path
        ↓
25. Report Generation
        ↓
26. HITL Review
        ↓
27. Memory
        ↓
28. Context Manager
        ↓
29. Docker
```

---

# 25. 简历项目定位

项目名称建议：

**AI Agent / GitHub 开源项目智能研究与分析平台**

简历可以突出：

```text
Multi-Agent
+
Workflow Engine
+
Skill
+
Tool Calling
+
Code Analysis
+
RAG
+
Memory
+
HITL
+
Checkpoint
+
Retry
+
Evidence
+
FastAPI
+
MySQL
+
Qdrant
```

项目核心亮点不是：

> “做了一个 GitHub README 总结器。”

而是：

> **构建了一个面向 AI Agent 开源项目的 Multi-Agent Research Platform，通过自研 Workflow Engine 编排项目理解、技术分析、源码架构分析、Evidence 验证与报告生成，并通过 Skill / Tool 抽象实现 GitHub、代码检索、依赖分析和知识检索能力。**

---

# 25.5 Skill 采用“外部复用 + 核心自研”策略

本项目不要求所有 Skill 都自行实现。

最终策略：

```text
通用能力
    → 优先接入外部 Skill

核心业务能力
    → 自研 Skill
```

### 外部 Skill

```text
Web Research
Web Reader / Browser
Document / PDF Parsing
```

### 自研 Skill

```text
GitHub Repository Analysis
Code / Architecture Analysis
Agent / Workflow Analysis
Evidence Verification
Project Comparison
```

### 这样设计的原因

1. 避免重复实现成熟的通用能力
2. 降低项目开发量
3. 体现外部能力集成能力
4. 保留核心业务逻辑的自主实现
5. 更符合实际 AI Agent 应用开发中的组合式架构

因此简历中可以强调：

```text
Multi-Agent
+
Custom Skill Development
+
External Skill Integration
+
Tool Calling
+
Workflow
+
Evidence Verification
+
Memory / Context
```

而不是简单强调：

> “实现了很多 Skill”。

---

# 26. 与原 Competitive Intelligence 项目的迁移关系

本项目不是推倒重来。

原项目的底层工程架构继续保留：

```text
FastAPI
MySQL
Qdrant
Workflow
Agent
Skill
Tool
Memory
Context
HITL
Checkpoint
Retry
Evidence
Report
```

主要改变的是业务对象：

| 原 Competitive Intelligence | 新 GitHub Project Intelligence |
|---|---|
| Competitor | Repository / Project |
| Product Analysis | Project Analysis |
| Technology Analysis | Technology Analysis |
| Pricing Analysis | Code & Architecture Analysis |
| Market Analysis | Workflow Analysis |
| Customer Analysis | Agent / Skill Analysis |
| News / Change | Commit / Release / Project Change |
| Comparison | Project Comparison |
| Competitive Report | Project Intelligence Report |
| Competitor Profile | Project Profile |
| Competitor Event | Project Change Event |

因此：

> **这不是重新开发一个完全不同的 Agent 平台，而是在已有企业级 Agent Workflow 架构上，把业务领域从“竞品情报”迁移到了“GitHub AI Agent 项目智能分析”。**

