# Bug 修复：项目运行到 100% 时 Retry 失败

> 2026-10-12 修订：原文把根因归到 `StateManager` 瘦身，这个归因是错的 ——
> `StateManager.TRIM_ORDER` 只动 `final_report.content`、`readme`、`evidence`、
> `modules`，从来没有删过 `owner` / `repo` / `repo_url`。
> 下面是核对代码后重写的版本，并补上实际落地的修复与验证方式。

## 问题描述

项目分析运行到 100%（finalizer 节点）时失败，点击 Retry 后仍然失败，错误信息：

```
ValueError: Repository analysis requires 'owner' and 'repo'.
```

报错位置：`app/infrastructure/skills/repository_analysis_skill.py`，
判定逻辑是 `if not owner or not repo: raise ValueError(...)`。

## 根本原因

### 1. 新 run 的 checkpoint 从出生起就缺坐标

重构到 domain / infrastructure 分层时，`initial_data` 被组装了两份：

- Application 层（`app/services/analysis_service.py`）组装了完整的一份：
  `run_id` / `repository_id` / `repo_url` / `owner` / `repo` / `rag_enabled` / `question`
- Domain 层（`app/domain/analysis/service.py`）又重新拼了一份，
  只透传 `repo_url` 和 `question`，**丢掉了 `run_id` / `owner` / `repo`**，
  还把 `rag_enabled` 写成了 `enable_rag`（读取方要的是 `rag_enabled`）

于是首个 checkpoint 里就没有仓库坐标，RAG 按次开关也一并失效。

### 2. 恢复时的补齐靠反解 URL，且失败即静默

`approve_workflow()` / `resume_workflow()` / `retry_workflow()` 三个恢复入口
都用同一套写法补救：

```python
if not state.data.get("owner") or not state.data.get("repo"):
    repo_url = state.data.get("repo_url")
    if repo_url:                      # repo_url 也没有时，直接跳过
        try:
            owner, repo = parse_github_url(repo_url)
            ...
        except Exception:
            pass                      # 解析失败 = 什么都不补，且不留痕迹
```

指针全落在 `state.data["repo_url"]` 上：一旦这个字段也缺（本次事故就是这样），
`if repo_url:` 直接为空，`owner` / `repo` 一个都补不回来，
而且因为是静默跳过，日志里看不出「实际上没补」。

### 3. 补进内存的字段活不过下一次 checkpoint 加载

```
orchestrator.retry_workflow()
  |-- load checkpoint（缺 owner / repo）
  |-- 把字段补进内存里的 state（没有落盘）
  `-- engine.retry()
        `-- _restore() 重新从 checkpoint 读一份
              `-- 内存里补的字段丢了
                    `-- 执行 plan_executor -> 同一个 ValueError
```

编排器和引擎都各自加载一次 checkpoint，所以「补字段」和「重新加载」
必须靠一次显式落盘来串起来，否则补了等于没补。

## 修复方案（已落地）

### 1. `initial_data` 只组装一份

`AnalysisService.start_analysis(run_id, repository_id, initial_data)` 改为原样透传，
不再自己拼字典；Application 层负责组装唯一一份，字段名与读取方对齐。

### 2. 恢复入口统一补齐身份字段

`AnalysisWorkflowOrchestrator` 的 `approve_workflow()` / `resume_workflow()` /
`retry_workflow()` 新增 `identity: dict | None` 参数，
由 Application 层从 `repositories` 表构造（`_identity_data(run, repository)`）：

```python
{
    "run_id": run.id,
    "repository_id": run.repository_id,
    "repo_url": repository.url,
    "owner": repository.owner,
    "repo": repository.name,
}
```

用数据库里的 `owner` / `name` 而不是反解 URL：数据库才是权威来源，
反解是在猜，猜不到的形态（URL 不规范 / 字段缺失）正是这次事故的现场。

### 3. 补齐后立刻落盘

`_apply_identity(state, identity)` 把字段写进 `state.data` 并返回「是否真的改了」，
调用方据此落盘，再交给引擎：

```python
if self._apply_identity(state, identity):
    # 必须落盘：engine.retry / engine.resume 会重新从 checkpoint 加载 state，
    # 只改内存里的这一份等于没改。
    await self.checkpoint_manager.save(state)
```

`approve_workflow()` 本来就紧跟一次 `state.approve()` + `save()`，
身份字段随那次保存一起落盘。

### 修改的文件

- `app/services/analysis_service.py`：组装唯一的 `initial_data`；
  新增 `_identity_data()` / `_load_identity()`，在 approve / resume / retry 传入 `identity`
- `app/domain/analysis/service.py`：`start_analysis` 改为透传 `initial_data`；
  三个恢复方法透传 `identity`
- `app/domain/analysis/workflow.py`：新增 `_apply_identity()`，三个恢复方法补齐并落盘
- `tests/test_retry_identity_backfill.py`：回归测试（见下）

## 影响范围

修复后，以下场景都能正确恢复缺失的字段：

1. ✅ Retry 失败的 run
2. ✅ Approve 设计闸门后继续执行
3. ✅ Resume 暂停的 run
4. ✅ 老 checkpoint 里连 `repo_url` 都没有的形态（现在按仓库行补）

## 测试验证

### 回归测试

`tests/test_retry_identity_backfill.py` 用真实的 `WorkflowEngine` +
`CheckpointManager`（内存 store，`load` 会深拷贝，等价于数据库往返）覆盖：

| 用例 | 盯住的点 |
|------|----------|
| `test_in_memory_backfill_is_lost_after_engine_reload` | 反证：不落盘就一定原地再失败 |
| `test_retry_backfills_identity_and_persists_it` | 第一笔写入就带身份字段（早于 engine 重载） |
| `test_retry_without_identity_does_not_fake_success` | 拿不到坐标时不把 run 伪装成成功 |
| `test_resume_backfills_identity_before_reload` | Resume 同样先补后落盘 |
| `test_approve_backfills_identity` | Approve 通过闸门后继续执行不缺字段 |
| `test_apply_identity_reports_whether_it_wrote` | 无变化不写盘，有变化才写 |
| `test_identity_data_takes_owner_from_repository_row` | 身份字段来自仓库行，不是反解 URL |

修复前的逻辑（只反解 `repo_url`、不落盘）跑第一个恢复用例会得到
`status=FAILED` 与 `Repository analysis requires 'owner' and 'repo'.`，
即该用例在修复前确实是失败的。

### 手工验证

1. 创建一个新的分析任务
2. 等待运行到 design gate 之后（plan_executor 附近）
3. 点击 Retry / Approve / Resume
4. 观察不再出现 owner/repo 相关错误

预期结果：

- ✅ 不再出现 "Repository analysis requires 'owner' and 'repo'" 错误
- ✅ 恢复后能继续跑完并生成报告

### 运行方式

```bash
python -m pytest -q -p no:cacheprovider tests/test_retry_identity_backfill.py
```

全量回归按项目既有命令在项目容器内执行（相关用例依赖 MySQL / Qdrant）。

## 后续优化建议

1. **统一恢复入口**：编排器和引擎各加载一次 checkpoint（双重加载），
   本次靠「落盘一次」串起来；更彻底的做法是让引擎接收已加载的 state
2. **执行前校验必需字段**：Workflow 启动 / 恢复前校验
   `owner` / `repo` / `repo_url` 是否存在，缺就明确报错，
   而不是等 `repository_analysis_skill` 在深处抛异常
3. **关键字段标记为不可瘦身**：在 `StateManager` 中显式声明
   `owner` / `repo` / `repo_url` / `run_id` 不参与瘦身。
   当前 `TRIM_ORDER` 本来就没碰这些字段，这条是防止将来扩表时误伤

## 修复日期

2026-10-10 首次修复，2026-10-12 修订根因并补齐回归测试
