"""
Workflow流程定义。
"""


class Workflow:


    def __init__(self):

        # Node集合
        self.nodes = {}


        # Transition集合
        self.transitions = []

    def add_node(
        self,
        node
    ):

        self.nodes[
            node.name
        ] = node


    def add_transition(
        self,
        transition
    ):

        self.transitions.append(
            transition
        )