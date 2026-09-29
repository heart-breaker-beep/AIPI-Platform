"""
Comparison Agent。

负责基于两个已经完成的 Analysis Run
以及对应 Evidence，生成多项目比较结果。

Phase 13 不让 LLM 凭空生成结论，
只比较 Analysis Result 中已经存在的结构化事实。

真实数据来源（RunMemory.load() 的顶层结构）：

    run_id / status / current_node / question
    repository / research_plan / final_report
    agent_outputs / task_results / evidences / workflow_state

注意：

    project["analysis"] 这个结构在真实数据中并不存在，
    因此所有维度都必须从上面这些真实字段读取。

各维度真实数据来源：

    agent            workflow_state.data.executed_tasks
    workflow         workflow_state.data.research_plan
    rag              workflow_state.data.technology_stack.embedding
    database         workflow_state.data.technology_stack.database
    deployment       workflow_state.data.technology_stack.deployment
    code_complexity  workflow_state.data.repository（language / size）
                     + architecture_analysis_agent（files / modules）
                     + technology_stack.source_files

    skill / tool / memory / extension：

        当前 Analysis Workflow 并未提取被分析项目的
        对应结构，真实数据不存在，
        因此返回 NOT_AVAILABLE 并给出明确原因，
        而不是因为字段名写错而“看起来没有数据”。

Evidence：

    引用必须来自 project["evidences"][*]["id"]（真实 Evidence ID）。
    归因规则是确定性的：

        维度值中的字符串叶子值会被拆成 token，
        若某个 token 出现在某条 Evidence 的 content 中，
        则该 Evidence 被引用。

    只取字符串叶子值、不取 dict key，
    是为了避免 JSON 结构名（tasks / question 等）
    与 Evidence 内容产生巧合匹配。

    该规则不会生成、不会猜测、不会以下标冒充 Evidence ID。
"""

import re

from dataclasses import dataclass
from typing import Any

from app.agents.base import BaseAgent


@dataclass(frozen=True)
class DimensionExtraction:
    """单个项目在某个维度上的真实数据提取结果。"""

    # 维度值
    value: Any = None

    # 真实来源字段路径，便于审计
    source: str | None = None

    # 真实数据是否存在
    available: bool = False

    # 不可用原因（available 为 False 时说明是数据缺失）
    reason: str | None = None


class ComparisonAgent(BaseAgent):
    """多项目比较 Agent。"""

    name = "comparison_agent"

    description = (
        "Compare multiple GitHub project "
        "analysis results using evidence."
    )

    DIMENSIONS = (
        "agent",
        "workflow",
        "skill",
        "tool",
        "rag",
        "memory",
        "database",
        "deployment",
        "code_complexity",
        "extension",
    )

    # 维度值中可参与 Evidence 归因的 token。
    #
    # 至少 4 个字符，避免过短的通用词造成巧合匹配。
    _TOKEN_PATTERN = re.compile(
        r"[A-Za-z][A-Za-z0-9_.\-]{3,}"
    )

    async def execute(
        self,
        context,
        input_data,
    ) -> dict[str, Any]:
        """
        比较两个项目。

        input_data:
            {
                "project_a": {...},
                "project_b": {...}
            }

        其中 project 必须是 RunMemory.load() 的真实返回结构。
        """

        project_a = input_data.get(
            "project_a"
        )

        project_b = input_data.get(
            "project_b"
        )

        if not isinstance(project_a, dict):
            raise ValueError(
                "project_a must be a dictionary."
            )

        if not isinstance(project_b, dict):
            raise ValueError(
                "project_b must be a dictionary."
            )

        comparison = {}

        for dimension in self.DIMENSIONS:
            comparison[dimension] = (
                self._compare_dimension(
                    project_a,
                    project_b,
                    dimension,
                )
            )

        return {
            "comparison": comparison,
            "projects": [
                self._project_summary(
                    project_a
                ),
                self._project_summary(
                    project_b
                ),
            ],
            # 只有比较结果确实引用了真实 Evidence 时
            # evidence_based 才为 True。
            "evidence_based": (
                self._is_evidence_based(
                    comparison
                )
            ),
        }

    @staticmethod
    def _is_evidence_based(
        comparison: dict[str, Any],
    ) -> bool:
        """
        根据实际 Evidence 引用情况计算 evidence_based。

        不能因为 API 成功返回而置 True，
        也不能因为有 dimensions 而置 True。
        """

        for result in comparison.values():

            if not isinstance(result, dict):
                continue

            for side in (
                "project_a",
                "project_b",
            ):

                value = result.get(side)

                if not isinstance(value, dict):
                    continue

                if value.get("evidence_ids"):
                    return True

        return False

    @classmethod
    def _compare_dimension(
        cls,
        project_a: dict[str, Any],
        project_b: dict[str, Any],
        dimension: str,
    ) -> dict[str, Any]:
        """比较单个维度。"""

        extraction_a = cls._extract_dimension(
            project_a,
            dimension,
        )

        extraction_b = cls._extract_dimension(
            project_b,
            dimension,
        )

        if (
            not extraction_a.available
            and not extraction_b.available
        ):
            relation = "NOT_AVAILABLE"

        elif (
            not extraction_a.available
            or not extraction_b.available
        ):
            relation = "ONE_SIDE_UNAVAILABLE"

        elif extraction_a.value == extraction_b.value:
            relation = "SAME"

        else:
            relation = "DIFFERENT"

        return {
            "relation": relation,

            # 真实来源字段，便于确认数据不是凭空产生的。
            "source": (
                extraction_a.source
                or extraction_b.source
            ),

            "project_a": cls._build_side(
                project_a,
                extraction_a,
            ),

            "project_b": cls._build_side(
                project_b,
                extraction_b,
            ),
        }

    @classmethod
    def _build_side(
        cls,
        project: dict[str, Any],
        extraction: DimensionExtraction,
    ) -> dict[str, Any]:
        """构建单侧比较结果。"""

        evidence_ids: list[str] = []

        if extraction.available:
            evidence_ids = (
                cls._attribute_evidence_ids(
                    project,
                    extraction.value,
                )
            )

        return {
            "value": extraction.value,
            "evidence_ids": evidence_ids,
            "available": extraction.available,
            "unavailable_reason": (
                extraction.reason
            ),
        }

    @classmethod
    def _extract_dimension(
        cls,
        project: dict[str, Any],
        dimension: str,
    ) -> DimensionExtraction:
        """
        从真实 Analysis Result 中提取某个维度。

        不进行主观推断：
        只读取真实存在的字段，
        读不到就返回 available=False 并说明原因。
        """

        data = cls._workflow_data(
            project
        )

        technology = data.get(
            "technology_stack"
        )

        if not isinstance(
            technology,
            dict,
        ):
            technology = None

        if dimension == "agent":
            return cls._extract_agent(data)

        if dimension == "workflow":
            return cls._extract_workflow(data)

        if dimension in {
            "rag",
            "database",
            "deployment",
        }:
            return cls._extract_technology(
                technology,
                dimension,
            )

        if dimension == "code_complexity":
            return cls._extract_code_complexity(
                data,
                technology,
            )

        return cls._unavailable_dimension(
            dimension
        )

    @staticmethod
    def _workflow_data(
        project: dict[str, Any],
    ) -> dict[str, Any]:
        """读取 workflow_state.data（真实业务数据所在位置）。"""

        workflow_state = project.get(
            "workflow_state"
        )

        if not isinstance(
            workflow_state,
            dict,
        ):
            return {}

        data = workflow_state.get(
            "data"
        )

        if not isinstance(
            data,
            dict,
        ):
            return {}

        return data

    @staticmethod
    def _extract_agent(
        data: dict[str, Any],
    ) -> DimensionExtraction:
        """Agent 维度：真实 Agent 执行列表。"""

        executed_tasks = data.get(
            "executed_tasks"
        )

        if (
            not isinstance(
                executed_tasks,
                list,
            )
            or not executed_tasks
        ):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    "executed_tasks。"
                ),
            )

        return DimensionExtraction(
            value={
                "count": len(executed_tasks),
                "agents": list(executed_tasks),
            },
            source=(
                "workflow_state.data."
                "executed_tasks"
            ),
            available=True,
        )

    @staticmethod
    def _extract_workflow(
        data: dict[str, Any],
    ) -> DimensionExtraction:
        """Workflow 维度：真实 Research Plan。"""

        research_plan = data.get(
            "research_plan"
        )

        if research_plan is None:
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    "research_plan。"
                ),
            )

        # research_plan["question"] 是本次分析请求，
        # 属于 Run 元数据，不是被分析项目的属性。
        # 若不剔除，两个项目只要提问不同
        # 就会让 workflow 维度被判为 DIFFERENT。
        plan = research_plan

        if isinstance(
            research_plan,
            dict,
        ):
            plan = {
                key: value
                for key, value in (
                    research_plan.items()
                )
                if key != "question"
            }

        # 只使用 research_plan 本身。
        #
        # 不把 workflow_state.status / current_node
        # 放进维度值：它们是本次 Run 的执行状态，
        # 不是被分析项目的属性。
        # 例如 status="COMPLETED" 会让 token "completed"
        # 与 README Evidence 巧合匹配，
        # 从而产生看起来合理、实际无意义的 Evidence 引用。
        return DimensionExtraction(
            value=plan,
            source=(
                "workflow_state.data."
                "research_plan"
            ),
            available=True,
        )

    @staticmethod
    def _extract_technology(
        technology: dict[str, Any] | None,
        dimension: str,
    ) -> DimensionExtraction:
        """
        技术栈相关维度。

        rag 使用 technology_stack.embedding：
        该字段是 TechnologyAnalysisSkill 对
        向量库 / Embedding（qdrant / chromadb）
        的真实检测结果，是当前真实数据中
        与 RAG 最直接对应的字段。
        """

        key = {
            "rag": "embedding",
            "database": "database",
            "deployment": "deployment",
        }[dimension]

        if (
            technology is None
            or key not in technology
        ):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    f"technology_stack.{key}。"
                ),
            )

        return DimensionExtraction(
            value=technology.get(key),
            source=(
                "workflow_state.data."
                f"technology_stack.{key}"
            ),
            available=True,
        )

    @staticmethod
    def _extract_code_complexity(
        data: dict[str, Any],
        technology: dict[str, Any] | None,
    ) -> DimensionExtraction:
        """代码复杂度维度：仓库规模与架构分析结果。"""

        repository = data.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            repository = None

        architecture = data.get(
            "architecture_analysis_agent"
        )

        if not isinstance(
            architecture,
            dict,
        ):
            architecture = {}

        if (
            repository is None
            and not architecture
        ):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实 Analysis Workflow 未产生 "
                    "repository 与 "
                    "architecture_analysis_agent 数据。"
                ),
            )

        files = architecture.get(
            "files"
        )

        modules = architecture.get(
            "modules"
        )

        source_files = None

        if technology is not None:
            source_files = technology.get(
                "source_files"
            )

        return DimensionExtraction(
            value={
                "language": (
                    repository or {}
                ).get("language"),
                "size_kb": (
                    repository or {}
                ).get("size"),
                "file_count": (
                    len(files)
                    if isinstance(
                        files,
                        list,
                    )
                    else None
                ),
                "module_count": (
                    len(modules)
                    if isinstance(
                        modules,
                        list,
                    )
                    else None
                ),
                "source_files": source_files,
            },
            source=(
                "workflow_state.data.repository + "
                "architecture_analysis_agent + "
                "technology_stack.source_files"
            ),
            available=True,
        )

    @staticmethod
    def _unavailable_dimension(
        dimension: str,
    ) -> DimensionExtraction:
        """
        真实数据不存在时的显式结果。

        与“字段名写错导致读不到”区分开：
        这里是当前 Analysis Workflow
        确实没有提取被分析项目的该结构。
        """

        return DimensionExtraction(
            available=False,
            reason=(
                "当前 Analysis Workflow 未提取"
                "被分析项目的 "
                f"{dimension} 结构，"
                "真实数据不存在。"
            ),
        )

    @classmethod
    def _attribute_evidence_ids(
        cls,
        project: dict[str, Any],
        value: Any,
    ) -> list[str]:
        """
        把真实 Evidence 归因到维度值。

        Evidence ID 只能来自 project["evidences"][*]["id"]。
        """

        evidences = project.get(
            "evidences"
        )

        if not isinstance(
            evidences,
            list,
        ):
            return []

        tokens = cls._specific_tokens(
            value
        )

        if not tokens:
            return []

        evidence_ids: list[str] = []

        for evidence in evidences:

            if not isinstance(
                evidence,
                dict,
            ):
                continue

            evidence_id = evidence.get("id")

            content = evidence.get("content")

            if (
                not isinstance(
                    evidence_id,
                    str,
                )
                or not evidence_id
            ):
                continue

            if not isinstance(content, str):
                continue

            if evidence_id in evidence_ids:
                continue

            lowered = content.lower()

            if any(
                token in lowered
                for token in tokens
            ):
                evidence_ids.append(
                    evidence_id
                )

        return evidence_ids

    @classmethod
    def _specific_tokens(
        cls,
        value: Any,
    ) -> set[str]:
        """
        提取维度值中的字面量 token。

        只取字符串叶子值，不取 dict key，
        避免 JSON 结构名（tasks / question 等）
        与 Evidence 内容产生巧合匹配。
        """

        tokens: set[str] = set()

        def visit(item: Any) -> None:

            if isinstance(item, dict):

                for child in item.values():
                    visit(child)

            elif isinstance(
                item,
                (list, tuple),
            ):

                for child in item:
                    visit(child)

            elif isinstance(item, str):

                for token in (
                    cls._TOKEN_PATTERN
                    .findall(item)
                ):
                    tokens.add(
                        token.lower()
                    )

        visit(value)

        return tokens

    @staticmethod
    def _project_summary(
        project: dict[str, Any],
    ) -> dict[str, Any]:
        """生成项目基本信息摘要。"""

        repository = project.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            repository = {}

        return {
            "run_id": project.get(
                "run_id"
            ),
            "repository_id": repository.get(
                "id"
            ),
            "repository_url": repository.get(
                "url"
            ),
            "repository_name": repository.get(
                "name"
            ),
            "status": project.get(
                "status"
            ),
        }
