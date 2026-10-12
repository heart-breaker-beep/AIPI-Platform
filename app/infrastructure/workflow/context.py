"""
Workflow 执行上下文。

负责向 Workflow / Node / Agent 提供：

- Agent
- Tool
- Skill
- Config
- Memory
- Context Manager

其中 Memory / Context Manager 为可选能力，
用于兼容 Phase 10 以前的调用方式。
"""

from dataclasses import dataclass


@dataclass
class WorkflowContext:
    """
    Workflow 运行环境。

    当前阶段：

        Workflow
            ↓
        WorkflowContext
            ├── Agents
            ├── Tools
            ├── Skills
            ├── Config
            ├── Memory
            └── Context Manager
    """

    # Agent 集合
    agents: dict

    # Tool 集合
    tools: dict

    # Skill 集合
    skills: dict

    # Workflow 配置
    config: dict

    # Phase 11 Memory 能力
    #
    # 使用 object 避免 Workflow 层
    # 与具体 MemoryManager 实现产生强耦合。
    memory_manager: object | None = None

    # Phase 11 Context Manager
    #
    # 使用 object 避免 Workflow 层
    # 与具体 ContextManager 实现产生强耦合。
    context_manager: object | None = None