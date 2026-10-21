# AIPI Platform - 快速开始

## 项目简介

AIPI Platform 是一个 **AI 驱动的 GitHub 项目智能分析平台**，基于 **Multi-Agent + Workflow + Memory** 架构，能够自动分析 GitHub 项目的技术栈、架构、Agent 实现等。

**核心特性：**
- 🤖 **Multi-Agent 协作**：Planner、Researcher、Critic 等多个 Agent 协同工作
- 📊 **Workflow 编排**：支持检查点与人工审批的 Workflow 引擎
- 🧠 **跨 Run 记忆**：支持多次分析的上下文记忆
- 📝 **自动生成报告**：生成 Markdown 和 JSON 格式的分析报告
- 🎯 **人工闸门**：Design Gate 和 Human Review 人工审核节点

**技术栈：**
- **后端**：FastAPI + SQLAlchemy + MySQL
- **AI**：DeepSeek API
- **架构**：API / Service / Persistence 分层 + 分析组件 + 通用 Workflow 引擎

---

## 🚀 启动方式

### 方式 1：Docker Compose（推荐 ⭐）

**使用 Docker Compose 启动应用，连接已配置的宿主机 MySQL。**

#### 步骤 1：准备配置文件

```bash
# 复制环境变量模板
cp .env.docker.example .env

# 编辑 .env 文件，填入你的配置
# 必填项：
# - DEEPSEEK_API_KEY=your_api_key_here
# - GITHUB_TOKEN=your_github_token
```

#### 步骤 2：启动服务

```bash
# 构建并启动所有服务
docker compose up -d --build

# 查看日志
docker compose logs -f aipi

# 查看所有服务状态
docker compose ps
```

#### 步骤 3：验证启动

```bash
# 健康检查
curl http://localhost:8000/health

# 查看 API 文档
open http://localhost:8000/docs
```

#### 步骤 4：停止服务

```bash
# 停止所有服务
docker compose down

# 停止并删除数据
docker compose down -v
```

**服务地址：**
- **API 服务**：http://localhost:8000
- **API 文档**：http://localhost:8000/docs
- **MySQL**：localhost:3306

---

### 方式 2：本地开发环境

**适合开发和调试，需要手动启动依赖服务。**

#### 步骤 1：安装 Python 依赖

```bash
# 推荐 Python 3.11
python --version  # 确认版本

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 步骤 2：启动依赖服务

启动 MySQL 8.0+ 并创建数据库 `aipi`，随后配置 `.env` 中的连接参数。当前 Compose 默认复用宿主机 MySQL；如需容器化 MySQL，先按 `docker-compose.yml` 注释启用服务和数据卷。

#### 步骤 3：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的配置
# 必填项：
DEEPSEEK_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token
DATABASE_URL=mysql+asyncmy://root:password@localhost:3306/aipi
```

#### 步骤 4：初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head
```

#### 步骤 5：启动应用

```bash
# 开发模式（支持热重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### 步骤 6：访问应用

- **API 服务**：http://localhost:8000
- **API 文档**：http://localhost:8000/docs
- **健康检查**：http://localhost:8000/health

---

## 📖 使用示例

### 1. 创建分析任务

```bash
curl -X POST "http://localhost:8000/api/v1/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/openai/openai-python",
    "question": "分析这个项目的 Agent 和 Workflow 实现"
  }'
```

**返回：**
```json
{
  "run_id": "uuid-xxx-xxx",
  "status": "WAITING_DESIGN",
  "repo_url": "https://github.com/openai/openai-python",
  "question": "分析这个项目的 Agent 和 Workflow 实现",
  "current_node": "design_gate",
  "progress": 20,
  "research_plan": {
    "tasks": ["repository_analysis_agent", "architecture_analysis_agent", ...],
    "reasoning": "..."
  }
}
```

### 2. 批准设计方案

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/{run_id}/approve"
```

### 3. 查询分析状态

```bash
curl "http://localhost:8000/api/v1/analysis/{run_id}"
```

### 4. 获取分析报告

```bash
# Markdown 报告
curl "http://localhost:8000/api/v1/analysis/{run_id}/report"

# JSON 报告
curl "http://localhost:8000/api/v1/analysis/{run_id}/report/json"
```

### 5. 深挖特定模块

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/{run_id}/deep-dive" \
  -H "Content-Type: application/json" \
  -d '{"module": "agent"}'
```

### 6. 生成学习路径

```bash
curl -X POST "http://localhost:8000/api/v1/analysis/{run_id}/learning-path" \
  -H "Content-Type: application/json" \
  -d '{"goal": "学习 Multi-Agent 实现"}'
```

---

## 🧪 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_analysis_api.py -v

# 查看测试覆盖率
pytest tests/ --cov=app --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

---

## 🏗️ 项目架构

### 分层结构

以 **API → Service → Persistence** 为主干，分析业务组件和通用工作流机制分别组织。

```text
app/
├── api/                 # HTTP 路由、依赖注入、异常响应
├── services/            # 用例协调、报告查询、依赖组装
├── analysis/            # 分析流程、节点、Agent、Skill、证据与报告
├── workflow/            # 通用引擎、状态、重试与检查点
├── persistence/         # 数据库连接、ORM 模型、Repository
│   ├── session.py
│   ├── base.py
│   ├── models/
│   └── repositories/
├── integrations/        # GitHub、LLM、文件导出
├── schemas/             # 接口请求与响应模型
├── core/                # 配置、日志与通用异常
├── static/
└── main.py
```

详细职责和事务规则见 [ARCHITECTURE.md](ARCHITECTURE.md)。运行 `python scripts/check_dependencies.py` 检查模块依赖边界。

### Workflow 流程

```
Start
  ↓
Planner Agent (生成分析方案)
  ↓
Design Gate (人工审批) ← 等待用户批准
  ↓
Plan Executor (执行分析任务)
  ├── Repository Analysis Agent
  ├── Architecture Analysis Agent
  ├── Technology Analysis Agent
  ├── Evidence Analysis Agent
  └── Critic Agent
  ↓
Human Review (人工审核) ← 可选
  ↓
Synthesis (综合报告)
  ↓
Finalizer (导出报告)
  ↓
End
```

---

## 🔧 配置说明

### 环境变量

| 变量 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | ✅ | - |
| `GITHUB_TOKEN` | GitHub Personal Access Token | ✅ | - |
| `DATABASE_URL` | MySQL 连接字符串 | ✅ | `mysql+asyncmy://...` |
| `LOG_LEVEL` | 日志级别 | ❌ | `INFO` |


### 获取 API Key

**DeepSeek API Key：**
1. 访问 https://platform.deepseek.com/
2. 注册并登录
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制并填入 `.env` 文件

**GitHub Token：**
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `public_repo` 权限
4. 生成并复制 Token
5. 填入 `.env` 文件

---

## 📝 常见问题

### Q1: Docker 启动失败

**问题：** `docker compose up -d` 报错

**解决：**
```bash
# 查看详细日志
docker compose logs

# 常见原因：
# 1. 端口被占用（3306, 6333, 8000）
# 2. .env 文件未配置或配置错误
# 3. Docker 资源不足

# 检查端口占用
netstat -ano | grep 8000
netstat -ano | grep 3306
netstat -ano | grep 6333

# 修改端口（编辑 docker-compose.yml）
```

### Q2: 数据库连接失败

**问题：** `Can't connect to MySQL server`

**解决：**
```bash
# 检查 MySQL 是否启动
docker compose ps mysql

# 查看 MySQL 日志
docker compose logs mysql

# 测试连接
mysql -h localhost -u root -p -P 3306

# 重建数据库
docker compose down mysql
docker compose up -d mysql
```

### Q3: 旧客户端仍传入 RAG 参数

平台已移除向量检索。`enable_rag` 暂时作为已弃用参数接受，但不生效；响应中的 `rag_enabled` 始终为 `false`。直接证据采集、历史报告与目标项目的 RAG 能力识别继续可用。

### Q4: DeepSeek API 调用失败

**问题：** `API key not found` 或 `Rate limit exceeded`

**解决：**
```bash
# 1. 检查 API Key 是否正确
cat .env | grep DEEPSEEK_API_KEY

# 2. 检查 API 额度
# 访问 https://platform.deepseek.com/usage

# 3. 检查网络连接
curl https://api.deepseek.com/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"
```

### Q5: 测试失败

**问题：** `pytest` 运行失败

**解决：**
```bash
# 查看失败的测试
pytest tests/ -v --tb=short

# 跳过需要外部服务的测试
pytest tests/ -v -m "not integration"

# 清理缓存
rm -rf .pytest_cache __pycache__
pytest tests/ -v
```

### Q6: 报告生成失败

**问题：** 分析完成但报告为空

**解决：**
```bash
# 检查报告目录权限
ls -la reports/

# 手动创建报告目录
mkdir -p reports

# 查看应用日志
docker compose logs aipi | grep ERROR

# 检查 Checkpoint
curl http://localhost:8000/api/v1/analysis/{run_id}
```

---

## 🔄 升级指南

### 重新构建 Docker 镜像

```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker compose up -d --build

# 或分步执行
docker build -t aipi:latest .
docker compose down
docker compose up -d
```

### 数据库迁移

```bash
# 进入容器
docker compose exec aipi bash

# 运行迁移
alembic upgrade head

# 退出容器
exit
```

### 清理旧数据

```bash
# 清理旧容器和镜像
docker compose down
docker system prune -a

# 重新构建
docker compose up -d --build
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `README.md` | 项目总览 |
| `ARCHITECTURE.md` | 架构设计详解 |
| `API.md` | API 接口文档 |
| `CONTRIBUTING.md` | 贡献指南 |
| `REFACTORING_DONE.md` | 重构完成报告 |
| `CLEANUP_REPORT.md` | 代码清理报告 |

---

## 🤝 贡献

欢迎贡献代码、报告 Bug、提出建议！

```bash
# Fork 项目
git clone https://github.com/your-username/aipi-platform.git

# 创建分支
git checkout -b feature/your-feature

# 提交代码
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature

# 创建 Pull Request
```

---

## 📄 许可证

MIT License

---

## 🆘 获取帮助

- **GitHub Issues**：https://github.com/your-username/aipi-platform/issues
- **文档**：查看 `docs/` 目录
- **日志**：`docker compose logs -f aipi`

---

**祝你使用愉快！** 🚀


## 分析过程 Trace

新建分析后，右侧运行状态下方会显示“分析过程”。可查看节点、Agent、文件读取、模型等待、异常和重试，切换“异常步骤”筛选，并复制文件路径。过程会在批准、重新规划等长请求执行期间独立刷新；刷新页面或重新打开历史任务可以恢复已记录的过程。

升级已有环境先执行：

```bash
python -m alembic upgrade head
```

本次迁移新增 `analysis_trace_streams` 与 `analysis_trace_events`。随后启动或重启应用进程；Docker 部署需重建应用镜像并在对应环境执行迁移。旧任务没有记录时显示空状态，不生成虚构历史。

新页面先提交 `defer_start=true` 取得任务 ID，再调用启动接口；旧创建请求仍沿用原行为：

```http
POST /api/v1/analysis
{"repo_url":"https://github.com/example/project","defer_start":true}

POST /api/v1/analysis/{run_id}/start
GET /api/v1/analysis/{run_id}/trace?after=0&limit=100
```

`next_cursor` 用于下一次增量查询；`has_more=true` 时继续读取。重复执行被拒绝时返回 HTTP 409。同一任务在多个页面打开时，执行中的任务不会再次显示可批准入口。

首版沿用长请求执行生命周期，刷新后会先查询记录，不会自动重跑任务。关闭页面后的持续执行和服务重启自动恢复不属于可靠后台调度能力。记录连接异常不等于任务失败，任务最终状态和报告以业务接口为准。

定期清理已结束且超过保留期的 trace（不删除报告或历史记忆）：

```bash
python -m scripts.purge_analysis_trace --days 30
```

该命令可由已有运维调度定期调用，项目不会自动新增定时任务。服务端不记录完整源码、模型提示词和 API 密钥；用量仅在模型提供方返回时显示。
