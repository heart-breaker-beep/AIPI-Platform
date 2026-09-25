"""
Workflow 流程定义。

负责：

1. 注册 Workflow Node
2. 保存 Node
3. 注册 Transition
4. 保存 Transition

真正执行 Workflow 的职责由 WorkflowEngine 负责。
"""

from app.workflow.node import BaseNode
from app.workflow.transition import Transition


class Workflow:
    """
    Workflow 流程定义。

    Workflow 本身只负责描述：

        Node
          +
        Transition

    不负责真正执行。

    真正执行由：

        WorkflowEngine

    完成。
    """

    def __init__(self) -> None:
        # 保存所有 Workflow Node
        #
        # {
        #     "start": StartNode(),
        #     "analysis": AnalysisNode(),
        # }
        self.nodes: dict[str, BaseNode] = {}

        # 保存 Workflow 流转关系
        self.transitions: list[Transition] = []

    def add_node(
        self,
        node: BaseNode,
    ) -> None:
        """
        注册 Workflow Node。
        """

        if not node.name:
            raise ValueError(
                "Workflow node name cannot be empty"
            )

        if node.name in self.nodes:
            raise ValueError(
                f"Workflow node already exists: {node.name}"
            )

        self.nodes[node.name] = node

    def add_transition(
        self,
        transition: Transition,
    ) -> None:
        """
        注册 Workflow Transition。
        """

        self.transitions.append(
            transition
        )

    def get_node(
        self,
        name: str,
    ) -> BaseNode | None:
        """
        根据名称获取 Node。
        """

        return self.nodes.get(name)