"""
Critic Agent。

负责检查分析结果是否完整。

Phase 12 校验要求
=================

文档 15.2 把 Critic 作为分析闭环中的验证步骤，
因此它必须能发现「分析其实没有产出数据」，
而不只是检查 key 是否存在。

旧实现只检查 3 个 key 是否存在，
于是下面这种「跑过了但什么都没产出」的输入
也会被判为 passed=True：

    architecture_analysis_agent = {"files": [], "modules": []}

新实现分两层校验：

1. 存在性：分析步骤是否产出对应字段
2. 内容：该字段是否真的有数据
"""


from app.agents.base import BaseAgent


class CriticAgent(
    BaseAgent
):
    """
    分析结果检查 Agent。
    """

    name = "critic_agent"

    description = (
        "Validate repository analysis results"
    )

    # 逻辑字段 -> 可接受的别名
    REQUIRED_FIELDS = {
        "repository": (
            "repository",
            "repository_analysis",
            "repository_analysis_agent",
        ),
        "architecture": (
            "architecture",
            "architecture_analysis",
            "architecture_analysis_agent",
        ),
        "technology": (
            "technology",
            "technology_analysis",
            "technology_analysis_agent",
            "technology_stack",
        ),
        # Phase 12 的「Agent / Workflow / Skill / Tool Analysis」
        # 步骤产出被分析项目的自述结构。
        "project_structure": (
            "project_structure",
        ),
    }

    async def execute(
        self,
        context,
        input_data,
    ):
        errors = []

        for logical_name, aliases in (
            self.REQUIRED_FIELDS.items()
        ):

            actual_key = next(
                (
                    alias
                    for alias in aliases
                    if alias in input_data
                ),
                None,
            )

            if actual_key is None:
                errors.append(
                    f"{logical_name} missing"
                )

                continue

            if not self._has_content(
                logical_name,
                input_data.get(actual_key),
            ):
                errors.append(
                    f"{logical_name} is empty"
                )

        return {
            "passed": not errors,
            "errors": errors,
        }

    @classmethod
    def _has_content(
        cls,
        logical_name,
        value,
    ) -> bool:
        """
        判断字段是否真的带有数据。

        注意两点：

        1. Agent 输出通常是包装结构
           （例如 {"repository": {...}}），
           真正的数据在内层字段，
           因此先做一层解包再判断。

        2. project_structure 与 technology_stack
           允许「诚实的空」——
           例如项目没有 README 时
           project_structure.available 就是 False，
           这属于真实结论，不是分析失败。
           因此只要求该字段存在且结构正确。
        """

        if not isinstance(value, dict):
            return False

        value = cls._unwrap(
            logical_name,
            value,
        )

        if logical_name == "repository":

            return bool(value)

        if logical_name == "architecture":

            modules = value.get("modules")

            if isinstance(modules, list) and modules:
                return True

            directory_structure = value.get(
                "directory_structure"
            )

            if (
                isinstance(directory_structure, dict)
                and directory_structure.get("available")
            ):
                return True

            # 兼容只有 files 的旧结构。
            files = value.get("files")

            return bool(files)

        if logical_name == "technology":

            return bool(value)

        return True

    @classmethod
    def _unwrap(
        cls,
        logical_name,
        value,
    ):
        """
        把 Agent 输出的包装结构解开一层。

        例如 repository_analysis_agent 的值是

            {"repository": {...}, "readme": "..."}

        真正的判据在内层 repository 上，
        因此在包装层直接判断 non-empty
        会把「内层为空」误判成有数据。
        """

        for alias in cls.REQUIRED_FIELDS.get(
            logical_name,
            (),
        ):

            inner = value.get(alias)

            if isinstance(
                inner,
                (dict, list),
            ):

                return inner

        return value
