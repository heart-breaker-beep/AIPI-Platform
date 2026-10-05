"""
RAG 检索工具。

按**维度**分别做语义检索，把命中结果整理成 evidence 形态。

为什么要按维度分别检索
======================

旧实现（`EvidenceAnalysisSkill._from_qdrant`）整个 run 只用一个 query_vector，
也就是"用一句话检索整个仓库"。这有两个问题：

1. 六个维度关心的东西完全不同 ——
   Agent 架构要看类与编排，Workflow 要看状态流转，
   RAG 要看向量库调用。一个向量表达不了六种意图，
   检索结果会整体偏向提问里字面提到的那个方向。

2. 结果会集中：一个粗粒度查询的前 10 条
   很可能全来自同一个目录。

按维度各查一次再合并，每个维度都有自己的名额，
覆盖面因此能摊开。

只返回证据形态，不返回原始 vector
================================

调用方（EvidenceAnalysisSkill）需要的是
"能写进报告、带文件与行号"的证据条目，
所以这里直接把 Qdrant payload 映射成
{source_type, source_url, file_path, line_start, line_end, content}，
与 `_from_qdrant` 的产出保持同一形态。
"""

from app.project_analysis.analysis_focus import AnalysisFocus
from app.tools.base import BaseTool


class RagRetrievalTool(BaseTool):
    """按维度检索仓库向量索引，产出带行号的证据条目。"""

    name = "rag_retrieval"

    # 低于这个长度的 chunk 不作为证据。
    #
    # 由来：A/B 实测发现，模块头 chunk（文件开头的 import 段）
    # 在六个维度查询下都容易命中 —— 它们短、且堆满了
    # agent / workflow / tool 这类术语，相似度天然偏高。
    # 结果是一批 75~270 字符的碎片挤进证据清单，
    # 对「Agent 怎么编排」这类问题毫无证据价值，
    # 却占掉有限的名额（RAG_MAX_EVIDENCE）。
    #
    # 取 150 是折中：
    # 真正的 import 段落（多行）仍会保留，
    # 只有单行碎片被挡掉 ——
    # 单行 import 作为"可追溯的证据"本来就站不住脚。
    MIN_CHUNK_CHARS = 150

    def __init__(
        self,
        embedding=None,
        vector_store=None,
    ) -> None:

        self.embedding = embedding
        self.vector_store = vector_store

    async def execute(
        self,
        question: str = "",
        dimensions: list[str] | None = None,
        repository_id: int | None = None,
        limit_per_dimension: int = 3,
        max_items: int = 12,
    ) -> list[dict]:
        """
        按维度检索并合并。

        repository_id 为 None 时直接返回空 ——
        宁可没有检索结果，也不能跨仓库乱捞：
        拿别的项目的源码当证据，报告里看不出任何异常。
        """

        if self.embedding is None or self.vector_store is None:
            return []

        if repository_id is None:
            return []

        dimensions = dimensions or []

        if not dimensions:
            return []

        # 维度名 -> 该维度命中的证据（按相似度降序）
        collected: list[tuple[float, dict]] = []
        seen: set[tuple] = set()

        for dimension in dimensions:

            query = self._build_query(dimension, question)

            try:
                vector = self.embedding.embed(query)

                hits = self.vector_store.search(
                    query_vector=vector,
                    limit=limit_per_dimension,
                    repository_id=repository_id,
                )

            except Exception:  # noqa: BLE001
                # 单个维度检索失败不该中断整个分析：
                # 其余维度照常，证据不足时还有结构分析那条路兜底。
                continue

            for hit in hits:

                item = self._to_evidence(
                    hit,
                    dimension,
                    question,
                )

                if item is None:
                    continue

                key = (
                    item["file_path"],
                    item["line_start"],
                    item["line_end"],
                )

                if key in seen:
                    continue

                seen.add(key)
                collected.append((getattr(hit, "score", 0.0), item))

        # 按相似度降序，取前 max_items。
        #
        # 排序放在合并之后、按维度取数之后：
        # 若先排序再截断，名额会被少数高分维度吃光，
        # 就退回到"一个粗粒度查询"的老问题上了。
        collected.sort(key=lambda pair: pair[0], reverse=True)

        return [item for _, item in collected[:max_items]]

    # ------------------------------------------------------------------

    @staticmethod
    def _build_query(
        dimension: str,
        question: str,
    ) -> str:
        """
        构造该维度的检索语句。

        必须带上**该维度自己的关键词**，不能只放展示名。

        为什么：如果查询只是「维度名 + 用户问题」，
        六个查询里真正有区分度的只有那两三个字，
        其余全是同一段问题文本 ——
        六个向量会高度相似，检索回同一批结果，
        「按维度分别检索」就退化成了「查六遍相同的东西」。
        A/B 实测确认过这一点。

        所以把 AnalysisFocus.KEYWORDS 里该维度的术语铺进去，
        让每个查询的语义重心真正落在自己的维度上。
        bge-m3 中英混排表现好，中文术语与英文标识符一起给，
        命中率高于只给一种。
        """

        title = AnalysisFocus.TITLES.get(dimension, dimension)

        terms = AnalysisFocus.KEYWORDS.get(dimension, ())

        parts = [
            f"{title} ({dimension})",
            " ".join(terms[:6]),
        ]

        if question and question.strip():
            parts.append(question.strip())

        return " ".join(part for part in parts if part)

    @classmethod
    def _to_evidence(
        cls,
        hit,
        dimension: str,
        question: str,
    ) -> dict | None:
        """把一条 Qdrant 命中映射成 evidence 条目。"""

        payload = getattr(hit, "payload", None)

        if not isinstance(payload, dict):
            return None

        text = payload.get("text")

        if not isinstance(text, str) or not text.strip():
            return None

        if len(text) < cls.MIN_CHUNK_CHARS:
            return None

        return {
            "source_type": payload.get(
                "source_type",
                "github",
            ),
            "source_url": payload.get("source_url"),
            "file_path": payload.get("file_path"),
            "line_start": payload.get("line_start"),
            "line_end": payload.get("line_end"),
            "content": text,
            "metadata": {
                "retrieved_for": dimension,
                "query": question,
                "kind": payload.get("kind"),
                "symbol": payload.get("symbol"),
                "score": getattr(hit, "score", None),
                "origin": "rag",
            },
        }
