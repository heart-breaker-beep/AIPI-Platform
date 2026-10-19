# AIPI 后端分层

项目以 API → Service → Persistence 为主干。Service 协调分析组件与数据存储；分析组件通过通用 Workflow 引擎执行，通过 Integrations 调用外部服务。

```text
app/
├── api/                       # HTTP 路由、依赖注入、异常响应
│   ├── v1/analysis.py
│   ├── dependencies.py
│   └── error_handlers.py
├── services/                  # 用例入口与业务协调
│   ├── analysis_service.py     # 分析任务的生命周期和状态查询
│   ├── report_service.py       # 报告查询、文件回读和 JSON 重建
│   └── analysis_factory.py     # 组装 Workflow、Context、存储和客户端
├── analysis/                  # 分析业务的执行组件
│   ├── workflow.py            # 分析流程定义和执行协调
│   ├── nodes/
│   ├── agents/
│   ├── skills/
│   ├── tools/
│   ├── evidence/
│   ├── reporting/             # ReportDocumentBuilder 与报告渲染
│   ├── memory/
│   └── context/
├── workflow/                  # 通用执行、状态、重试和检查点机制
├── persistence/               # 持久层
│   ├── session.py             # Engine、连接池与 Session 工厂
│   ├── base.py                # ORM 模型的声明基类
│   ├── models/                # 表映射
│   └── repositories/          # 查询、保存和 ORM 数据转换
├── integrations/              # 外部服务和文件工具
│   ├── github/
│   ├── llm/
│   ├── embeddings/
│   ├── vector_store/
│   ├── base.py
│   └── report_export_tool.py
├── schemas/                   # HTTP 请求与响应的数据契约
├── core/                      # 配置、日志和通用异常
├── static/
└── main.py
```

## 调用与依赖规则

- `api/v1` 接收参数，调用注入的 Service；`api/dependencies.py` 提供 Session 和服务依赖。
- `services` 校验用例、控制事务、协调分析过程和运行状态投影。Service 中的 SQL 查询统一放入 Repository。
- `analysis` 实现分析流程、证据处理、报告生成和记忆筛选。Agent、Skill 使用 Context 中注入的工具和存储能力。
- `workflow` 只依赖自身和 `core`，通过注入的仓库与提交回调保存检查点，不访问具体 Session。
- `persistence` 管理 SQLAlchemy、ORM 模型和查询，不依赖 Service 或分析组件。检查点 Repository 可以使用通用的 `workflow.state` 数据类型完成序列化和恢复。
- `integrations` 封装 GitHub、LLM、Embedding、Qdrant 与报告文件导出，不依赖分析策略。
- `schemas` 与 `core` 提供数据定义和共享能力。

`services` 和 `analysis` 共同构成业务层。原先主要负责转发的 Domain Service 已移除；用例直接调用分析工作流执行组件。

## 状态和事务

`WorkflowState` 是运行状态；`analysis_runs` 保存面向接口查询的状态投影。用例执行后，由 `AnalysisService` 同步状态和错误信息。

数据库 Session 由请求作用域管理；Repository 默认只 `flush`，普通业务提交由 Service 控制。工作流通过组合根注入的 `session.commit` 在保存检查点后提交，使当前节点的证据和检查点一起持久化。单条证据写入使用 SAVEPOINT，失败不会破坏后续证据和检查点的写入。

`WorkflowContext.config` 只保留运行配置，不放数据库 Session；Skill 通过 `evidence_store` 使用存储能力。历史分析和任务查询由 `ProjectMemoryRepository` 实现，记忆的关键词筛选留在分析组件。

## 报告

`ReportService` 负责 Markdown、JSON 报告的读取和兜底。检查点不可用时仍可读取已导出的报告文件；JSON 文件缺失或损坏时，可以使用检查点数据和 `ReportDocumentBuilder` 重建。

## 检查

```bash
python scripts/check_dependencies.py
pytest tests/test_layering.py tests/test_analysis_service.py tests/test_analysis_factory.py tests/test_api_dependencies.py tests/test_report_service.py
```

依赖守卫同时检查绝对、相对和函数内导入，并拒绝旧目录的导入。真实 MySQL、GitHub、Ollama 和 Qdrant 测试需要相应的外部服务配置。

本次重构不改变数据库表结构、API 路径和报告文档格式；Alembic 的模型导入已更新到持久层。
