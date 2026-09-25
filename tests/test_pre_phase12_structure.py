"""
Phase 12 前置结构修复回归测试。

验证：

1. Workflow 存在且可以注册 Node / Transition
2. 两个 BaseNode import 实际指向同一个类
3. WorkflowContext 保持旧字段兼容
4. WorkflowContext 支持 Phase 11 Memory / Context
5. WorkflowError 已统一
6. RepositoryRepository 已统一
7. FastAPI main 可以正常导入
"""

from app.core.exceptions import WorkflowError
from app.repositories.repository import (
    RepositoryRepository as RepositoryRepositoryFromMain,
)
from app.repositories.repository_basic import (
    RepositoryRepository as RepositoryRepositoryFromBasic,
)
from app.workflow.context import WorkflowContext
from app.workflow.node import (
    BaseNode as BaseNodeFromWorkflow,
)
from app.workflow.nodes.base import (
    BaseNode as BaseNodeFromNodes,
)
from app.workflow.transition import Transition
from app.workflow.workflow import Workflow
from app.workflow.exceptions import (
    NodeExecutionError,
    WorkflowError as WorkflowErrorFromWorkflow,
)


class DemoNode(BaseNodeFromWorkflow):
    """
    测试 Node。
    """

    name = "demo"

    async def execute(
        self,
        state,
        context,
    ):
        return state


def test_base_node_is_unified():
    """
    两个历史 import 路径必须得到同一个 BaseNode。
    """

    assert (
        BaseNodeFromWorkflow
        is BaseNodeFromNodes
    )


def test_workflow_can_register_node():
    """
    Workflow 可以正常注册 Node。
    """

    workflow = Workflow()

    node = DemoNode()

    workflow.add_node(node)

    assert (
        workflow.get_node("demo")
        is node
    )

    assert (
        workflow.nodes["demo"]
        is node
    )


def test_workflow_can_register_transition():
    """
    Workflow 可以正常注册 Transition。
    """

    workflow = Workflow()

    transition = Transition(
        "start",
        "demo",
    )

    workflow.add_transition(
        transition
    )

    assert len(
        workflow.transitions
    ) == 1

    assert (
        workflow.transitions[0]
        is transition
    )


def test_workflow_context_backward_compatible():
    """
    原有四字段 WorkflowContext 仍然可用。
    """

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
    )

    assert context.agents == {}
    assert context.tools == {}
    assert context.skills == {}
    assert context.config == {}

    assert (
        context.memory_manager
        is None
    )

    assert (
        context.context_manager
        is None
    )


def test_workflow_context_supports_phase11_components():
    """
    WorkflowContext 可以携带 Memory / Context Manager。
    """

    memory_manager = object()
    context_manager = object()

    context = WorkflowContext(
        agents={},
        tools={},
        skills={},
        config={},
        memory_manager=memory_manager,
        context_manager=context_manager,
    )

    assert (
        context.memory_manager
        is memory_manager
    )

    assert (
        context.context_manager
        is context_manager
    )


def test_repository_repository_is_unified():
    """
    两个历史 Repository import 路径
    必须指向同一个实现。
    """

    assert (
        RepositoryRepositoryFromMain
        is RepositoryRepositoryFromBasic
    )


def test_workflow_error_is_unified():
    """
    Workflow 层不能再定义第二份 WorkflowError。
    """

    assert (
        WorkflowErrorFromWorkflow
        is WorkflowError
    )

    assert issubclass(
        NodeExecutionError,
        WorkflowError,
    )


def test_fastapi_application_imports():
    """
    main.py 应用可以正常导入。

    该测试同时验证：
    main.py 不再执行错误的模块级
    WorkflowContext 草稿装配。
    """

    from app.main import app

    assert app is not None