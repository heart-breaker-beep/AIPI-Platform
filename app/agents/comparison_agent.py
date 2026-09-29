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

    agent / workflow / skill / tool
    memory / extension
                     workflow_state.data.project_structure
                       .dimensions.<name>

    rag              workflow_state.data.project_structure
                       .dimensions.rag
                     （拿不到时回退 technology_stack.embedding，
                       并在 source 中标注该回退）

    database         workflow_state.data.technology_stack.database

    deployment       workflow_state.data.technology_stack.deployment

    code_complexity  workflow_state.data.repository（language / size）
                     + architecture_analysis_agent（files / modules）
                     + directory_structure（total_files / by_extension）
                     + technology_stack.source_files

关于 project_structure
======================

它由 ArchitectureAnalysisSkill 从
**被分析项目自己**的 README 与 GitHub topics 中
确定性抽取，每条都带 README 行号。

它描述的是「被分析项目自述的结构」，
不是 AIPI 自身的执行状态 —— 这是本 Agent 的核心约束。

刻意不再回退到
    executed_tasks（AIPI 执行了哪 5 个 Agent）
    research_plan （AIPI 生成的研究计划）
因为那两个字段描述的是 **AIPI 这个分析平台自己**，
用来比较被分析项目会得到
「看似合理、实际错误」的结论
（任何两个项目都会得到 SAME）。

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

    # Phase 13 维度名 -> 被分析项目自述结构里的维度名。
    #
    # 这些维度的数据来自被分析项目自己的 README / topics，
    # 而不是 AIPI 自身的执行数据。
    PROJECT_STRUCTURE_DIMENSIONS = {
        "agent": "agents",
        "workflow": "workflow",
        "skill": "skills",
        "tool": "tools",
        # rag 也来自该结构，
        # 但会额外补上向量库检测信息，
        # 因此走独立的 _extract_rag。
        "rag": "rag",
        "memory": "memory",
        "extension": "extension",
    }

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

        # rag 要在通用分支之前判断：
        # 它在 project_structure 的基础上
        # 还要补向量库检测信息。
        if dimension == "rag":
            return cls._extract_rag(
                data,
                technology,
            )

        if dimension in cls.PROJECT_STRUCTURE_DIMENSIONS:
            return cls._extract_project_dimension(
                data,
                dimension,
            )

        if dimension in {
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

    @classmethod
    def _extract_project_dimension(
        cls,
        data: dict[str, Any],
        dimension: str,
    ) -> DimensionExtraction:
        """
        从被分析项目的自述结构里取某个维度。

        数据来源：
        ArchitectureAnalysisSkill 产出的
        workflow_state.data.project_structure，
        它基于被分析项目自己的 README 与 GitHub topics，
        每条都带 README 行号可复核。

        刻意不回退到 executed_tasks / research_plan：
        那是 AIPI 自己的执行数据。
        """

        structure = data.get(
            "project_structure"
        )

        if (
            not isinstance(structure, dict)
            or not structure.get("available")
        ):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实数据不存在：该 run 未产出"
                    "被分析项目的自述结构"
                    "（project_structure），"
                    "因此没有项目级事实可比较。"
                ),
            )

        key = cls.PROJECT_STRUCTURE_DIMENSIONS[
            dimension
        ]

        entry = (
            structure.get("dimensions")
            or {}
        ).get(key)

        if not isinstance(entry, dict):
            return DimensionExtraction(
                available=False,
                reason=(
                    "真实数据不存在："
                    f"project_structure 无 {key} 维度。"
                ),
            )

        declared = bool(
            entry.get("declared")
        )

        # value 里刻意不放 reason / evidence 行号：
        # 那些是「证据出处」，两个项目天然不同，
        # 放进来会让任何两个项目都被判成 DIFFERENT。
        #
        # 这里比较的是「项目自述了哪些能力」，
        # 所以只取 declared / items / topics。
        return DimensionExtraction(
            value={
                "declared": declared,
                "items": sorted(
                    entry.get("items") or []
                ),
                "topics": sorted(
                    entry.get("topics") or []
                ),
                "basis": structure.get("basis"),
            },
            source=(
                "workflow_state.data."
                "project_structure.dimensions."
                f"{key}"
            ),
            available=True,
        )

    @classmethod
    def _extract_rag(
        cls,
        data: dict[str, Any],
        technology: dict[str, Any] | None,
    ) -> DimensionExtraction:
        """
        RAG 维度。

        主来源是被分析项目 README 里的 rag 声明；
        technology_stack.embedding 只作辅助信息，
        它只是「是否检测到向量库」，
        不能单独代表完整的 RAG 实现
        （检测关键词只有 qdrant / chromadb 两个）。

        只有在完全没有 project_structure 时，
        才退回 embedding 近似，并在 source 里标注。
        """

        embedding = None

        if technology is not None:
            embedding = technology.get(
                "embedding"
            )

        extraction = cls._extract_project_dimension(
            data,
            "rag",
        )

        if extraction.available:

            extraction.value[
                "vector_store_detected"
            ] = sorted(embedding or [])

            return extraction

        if embedding:

            return DimensionExtraction(
                value={
                    "declared": None,
                    "items": [],
                    "topics": [],
                    "vector_store_detected": sorted(
                        embedding
                    ),
                    "approximate": True,
                },
                source=(
                    "workflow_state.data."
                    "technology_stack.embedding"
                    "（近似：仅表示检测到向量库）"
                ),
                available=True,
            )

        return extraction

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
        """
        代码规模维度：仓库体积与目录结构统计。

        说明：这些是**规模**指标，不是复杂度指标。

        repository.size 是 GitHub API 的仓库体积（KB，含 .git），
        与圈复杂度 / 耦合度无关；
        directory_structure 给出的是文件数与文件类型分布。

        当前 Analysis Workflow 没有产出
        类数 / 函数数 / 代码行数 / 圈复杂度，
        因此这里只做规模比较，命名沿用 Phase 13 文档的
        code_complexity 维度名。
        """

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

        directory_structure = architecture.get(
            "directory_structure"
        )

        if not isinstance(
            directory_structure,
            dict,
        ):
            directory_structure = {}

        # 只取文件数最多的前 5 种类型，
        # 避免维度值过大。
        file_types = directory_structure.get(
            "by_extension"
        )

        if not isinstance(
            file_types,
            dict,
        ):
            file_types = {}

        return DimensionExtraction(
            value={
                "language": (
                    repository or {}
                ).get("language"),
                "size_kb": (
                    repository or {}
                ).get("size"),
                "total_files": (
                    directory_structure.get(
                        "total_files"
                    )
                ),
                "file_types": dict(
                    sorted(
                        file_types.items(),
                        key=lambda item: -item[1],
                    )[:5]
                ),
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
                "architecture_analysis_agent"
                "（含 directory_structure）+ "
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
