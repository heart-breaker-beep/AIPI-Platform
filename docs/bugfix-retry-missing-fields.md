# Bug 修复：项目运行到 100% 时 Retry 失败

## 问题描述

项目分析运行到 100% (finalizer 节点) 时失败，点击 Retry 后仍然失败，错误信息：

```
ValueError: Repository analysis requires 'owner' and 'repo'.
```

## 根本原因

### 1. 字段丢失的链路

在 Workflow 的生命周期中，`owner` 和 `repo` 字段经历了以下过程：

1. **初始创建**：`start_analysis` 时从 `repo_url` 解析出 `owner` 和 `repo`
2. **正常执行**：这些字段存在于运行时的 `state.data` 中
3. **Checkpoint 保存**：通过 `StateManager` 瘦身后保存到数据库
4. **Retry 加载**：从 checkpoint 恢复时，字段已经不在 `state.data` 中

### 2. Retry 逻辑的缺陷

在 `app/domain/analysis/workflow.py` 的三个恢复方法中：

- `retry_workflow()` (197-241行)
- `approve_workflow()` (84-132行)  
- `resume_workflow()` (152-195行)

虽然都有补全 `owner` 和 `repo` 的逻辑：

```python
if not state.data.get("owner") or not state.data.get("repo"):
    owner, repo = parse_github_url(repo_url)
    state.data["owner"] = owner
    state.data["repo"] = repo
```

**但是补全后没有保存！**

随后调用 `engine.retry()` / `engine.resume()` 时，引擎会重新从数据库加载 checkpoint，导致刚补全的字段丢失。

### 3. 调用时序问题

```
orchestrator.retry_workflow()
  ├─ load checkpoint (缺失 owner/repo)
  ├─ 补全 owner 和 repo (只在内存中)
  └─ engine.retry()
       └─ _restore() 重新加载 checkpoint (补全的字段丢失!)
            └─ run()
                 └─ 执行 repository_analysis_skill
                      └─ ValueError: 缺少 owner 和 repo
```

## 修复方案

在补全 `owner` 和 `repo` 后，立即保存 checkpoint：

```python
if not state.data.get("owner") or not state.data.get("repo"):
    owner, repo = parse_github_url(repo_url)
    state.data["owner"] = owner
    state.data["repo"] = repo
    
    # 保存补全后的 state，否则 engine.retry 会重新加载旧 checkpoint
    await self.checkpoint_manager.save(state)
```

修改的文件：
- `app/domain/analysis/workflow.py` (3处)

## 影响范围

修复后，以下场景都能正确恢复缺失的字段：

1. ✅ Retry 失败的 run
2. ✅ Approve 设计闸门后继续执行
3. ✅ Resume 暂停的 run

## 测试验证

可以通过以下步骤验证修复：

1. 创建一个新的分析任务
2. 等待运行到 plan_executor 或更后的节点
3. 点击 Retry 按钮
4. 观察是否能成功恢复并继续执行

预期结果：
- ✅ 不再出现 "Repository analysis requires 'owner' and 'repo'" 错误
- ✅ Retry 能正常完成分析
- ✅ 最终生成完整的报告

## 相关问题

这个 bug 的出现与以下设计有关：

1. **State 瘦身策略**：为了避免 checkpoint 超过 180KB 限制，`StateManager` 会删除部分字段
2. **字段依赖隐式**：`repository_analysis_skill` 依赖 `owner` 和 `repo`，但这些字段可能在瘦身时被移除
3. **双重加载**：orchestrator 层和 engine 层都会加载 checkpoint，容易产生不一致

## 后续优化建议

1. **标记关键字段**：在 `StateManager` 中明确标记 `owner`、`repo`、`repo_url` 为不可瘦身的关键字段
2. **统一恢复入口**：避免 orchestrator 和 engine 重复加载 checkpoint
3. **字段验证**：在 Workflow 开始执行前，验证必需字段是否存在

## 修复日期

2026-10-10
