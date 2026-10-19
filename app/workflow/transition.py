"""
Workflow节点流转关系。
"""


class Transition:


    def __init__(
        self,
        source,
        target,
        condition=None
    ):

        # 当前节点
        self.source = source


        # 下一节点
        self.target = target


        # 条件函数
        self.condition = condition