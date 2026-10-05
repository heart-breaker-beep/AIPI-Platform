"""
Evidence Analysis Skill。

支持：

1. Qdrant 语义检索结果
2. Repository / Architecture Agent 输出
3. Evidence MySQL 持久化
"""

from app.core.config import get_settings
from app.core.logging import get_logger
from app.embeddings.ollama import OllamaEmbedding
from app.project_analysis.analysis_focus import AnalysisFocus
from app.project_analysis.rag_indexer import RagIndexer
from app.services.evidence_service import (
    EvidenceService,
)
from app.skills.base import BaseSkill
from app.vector_store.qdrant import QdrantVectorStore


logger = get_logger(__name__)


class EvidenceAnalysisSkill(
    BaseSkill
):
    """生成可追溯 Evidence。"""

    name = "evidence_analysis"

    description = (
        "Extract traceable evidence from "
        "repository analysis results."
    )

    # 单条源码证据最多保存多少字符。
    MAX_EVIDENCE_CHARS = 1500

    async def execute(
        self,
        context,
        input_data,
    ):
        # 两条来源**叠加**，而不是二选一。
        #
        # 旧实现是 `if not evidence:` ——
        # 一旦语义检索返回了结果，README 与模块证据会被整段跳过。
        # 那是「替换」不是「增强」：
        # 换来 5 条语义块，代价是丢掉 20 个模块的覆盖，
        # 在中小仓库上是净损失。
        evidence: list[dict] = []

        # 1. 语义检索（RAG 未开启时返回空列表）
        evidence.extend(
            await self._from_rag(
                context,
                input_data,
            )
        )

        # 2. 调用方直接给了向量时的单次检索。
        #
        # 这是引入按维度检索之前的旧协议，现在没有生产方使用
        # （没有任何代码往 state.data 里写 query_vector），
        # 但它仍是一条合法的证据来源，因此保持可用 ——
        # 关键同样是**叠加**：给了向量不再意味着跳过结构证据。
        query_vector = input_data.get(
            "query_vector"
        )

        if query_vector is not None:

            evidence.extend(
                await self._from_qdrant(
                    context,
                    query_vector,
                    input_data.get(
                        "limit",
                        5,
                    ),
                )
            )

        # 3. 结构分析产出的证据 —— 始终执行
        evidence.extend(
            self._from_analysis_results(
                input_data
            )
        )

        # 去重。
        unique = []

        seen = set()

        for item in evidence:

            # 按「位置」去重，不再把 content 也放进键。
            #
            # 叠加两条来源之后，同一个位置可能被
            # 结构证据与检索证据各产出一次；
            # 带 content 做键的话两者不等，
            # 同一段代码会在报告里出现两遍，白白占掉证据名额。
            key = (
                item.get("file_path"),
                item.get("line_start"),
                item.get("line_end"),
            )

            if key == (None, None, None):
                # 没有位置信息的（理论上不该有），退回按内容去重。
                key = item.get("content")

            if key in seen:
                continue

            seen.add(key)
            unique.append(item)

        # Phase 9 Evidence 持久化。
        config = getattr(context, "config", {}) or {}
        session = config.get("session")

        repository_id = config.get(
            "repository_id"

        )

        persist_failures = []

        if (
            session is not None
            and repository_id is not None
        ):
            service = EvidenceService(
                session
            )

            persisted = []

            for item in unique:

                # 单条证据落库失败不应中断整个分析：
                # 记录原因后继续处理其它证据。
                try:

                    record = (
                        await service.create_evidence(
                            repository_id=repository_id,
                            source_type=item[
                                "source_type"
                            ],
                            source_url=item.get(
                                "source_url"
                            ),
                            file_path=item.get(
                                "file_path"
                            ),
                            line_start=item.get(
                                "line_start"
                            ),
                            line_end=item.get(
                                "line_end"
                            ),
                            content=item[
                                "content"
                            ],
                            verification_status=(
                                "UNVERIFIED"
                            ),
                        )
                    )

                except Exception as error:

                    persist_failures.append(
                        {
                            "file_path": item.get(
                                "file_path"
                            ),
                            "error": (
                                str(error)
                                or type(error).__name__
                            ),
                        }
                    )

                    continue

                item = dict(item)

                item["evidence_id"] = (
                    record.id
                )

                persisted.append(item)

            unique = persisted

        return {
            "evidence": unique,
            "count": len(unique),
            "persist_failures": persist_failures,
        }

    async def _from_rag(
        self,
        context,
        input_data,
    ) -> list[dict]:
        """
        语义检索通路：先建索引，再按维度检索。

        RAG_ENABLED 为 false 时直接返回空列表，
        整条链路的行为与开启前完全一致。

        失败一律降级为空列表而不是抛异常：
        证据不足时结构分析那条通路仍然完整，
        不该因为 Ollama 没起、向量库连不上就让整次分析 FAILED。
        """

        settings = get_settings()

        # 按次开关优先：请求里给了 enable_rag 就用它，
        # 没给才回落到服务端配置。
        enabled = input_data.get("rag_enabled")

        if enabled is None:
            enabled = settings.RAG_ENABLED

        if not enabled:
            return []

        repository_id = input_data.get(
            "repository_id"
        )

        retriever = context.tools.get(
            "rag_retrieval"
        )

        if repository_id is None or retriever is None:
            return []

        try:
            summary = await self._index_repository(
                context,
                input_data,
                repository_id,
                settings,
            )

            logger.info(
                "RAG 索引结果：%s",
                summary,
            )

        except Exception as error:  # noqa: BLE001
            logger.warning(
                "RAG 索引失败，本次跳过语义检索：%s",
                error,
            )
            return []

        try:
            return await retriever.execute(
                question=input_data.get(
                    "question"
                )
                or "",
                # 六个维度各查一次。
                #
                # 不按 focus 收窄：focus 决定的是报告详略，
                # 而证据是全局的 —— 只看重点维度会让
                # 被压缩的那些章节拿不到任何检索结果。
                dimensions=list(
                    AnalysisFocus.DIMENSIONS
                ),
                repository_id=repository_id,
                limit_per_dimension=(
                    settings.RAG_LIMIT_PER_DIMENSION
                ),
                max_items=settings.RAG_MAX_EVIDENCE,
            )

        except Exception as error:  # noqa: BLE001
            logger.warning(
                "RAG 检索失败，本次无检索证据：%s",
                error,
            )
            return []

    async def _index_repository(
        self,
        context,
        input_data,
        repository_id,
        settings,
    ) -> dict:
        """把仓库源码写入向量库。"""

        indexer = RagIndexer(
            file_reader=context.tools.get(
                "file_reader"
            ),
            embedding=OllamaEmbedding(),
            vector_store=QdrantVectorStore(),
        )

        return await indexer.index_repository(
            repository_id=repository_id,
            run_id=str(
                input_data.get("run_id") or ""
            ),
            repo_url=str(
                input_data.get("repo_url") or ""
            ),
            owner=str(
                input_data.get("owner") or ""
            ),
            name=str(
                input_data.get("repo") or ""
            ),
            branch=str(
                input_data.get("branch") or "main"
            ),
            # 已经读过的文件：正文在内存里，不额外花请求
            known_files=input_data.get(
                "modules"
            )
            or [],
            # 结构分析筛出的候选路径：这才是检索覆盖面
            # 超出「已读文件」的增量来源
            extra_file_paths=input_data.get(
                "files"
            )
            or [],
            max_files=settings.RAG_INDEX_MAX_FILES,
        )

    async def _from_qdrant(
        self,
        context,
        query_vector,
        limit,
    ):
        qdrant_tool = context.tools.get(
            "qdrant_search"
        )

        if qdrant_tool is None:
            raise RuntimeError(
                "Tool not found: qdrant_search"
            )

        results = await qdrant_tool.execute(
            query_vector=query_vector,
            limit=limit,
        )

        evidence = []

        for item in results:

            evidence.append(
                {
                    "source_type": item.get(
                        "source_type",
                        "repository",
                    ),
                    "source_url": item.get(
                        "source_url"
                    ),
                    "file_path": item.get(
                        "file_path"
                    ) or item.get(
                        "source"
                    ),
                    "line_start": item.get(
                        "line_start"
                    ),
                    "line_end": item.get(
                        "line_end"
                    ),
                    "content": item.get(
                        "text",
                        "",
                    ),
                    "metadata": item,
                }
            )

        return evidence

    @staticmethod
    def _from_analysis_results(
        input_data,
    ):
        evidence = []

        repo_url = input_data.get(
            "repo_url"
        )

        readme = input_data.get(
            "readme"
        )

        if isinstance(
            readme,
            str,
        ) and readme.strip():

            evidence.append(
                {
                    "source_type": "github",
                    "source_url": repo_url,
                    "file_path": "README.md",
                    "line_start": 1,
                    "line_end": len(
                        readme.splitlines()
                    ),
                    "content": readme,
                    "metadata": {},
                }
            )

        modules = EvidenceAnalysisSkill._modules(
            input_data
        )

        for module in modules:

            if not isinstance(
                module,
                dict,
            ):
                continue

            # 读取失败的模块不生成证据，
            # 否则会把空内容当成源码证据。
            if module.get("error"):
                continue

            file_path = module.get(
                "file_path"
            )

            content = module.get(
                "content"
            )

            if isinstance(
                content,
                dict,
            ):
                content = content.get(
                    "content",
                    "",
                )

            # 纯空白也算「没有内容」。
            #
            # 真实事故：空的 __init__.py 只有 1 个换行符，
            # 通过 `if not content` 检查后
            # 被证据存储层以
            # "Evidence content cannot be empty." 拒绝，
            # 异常冒泡导致整个 5-Agent 计划 FAILED。
            content = str(content)

            if not content.strip():
                continue

            # 限制单条证据长度：
            # 源码文件可能有数万字符，
            # 全部落库会让证据表迅速膨胀。
            excerpt = content[
                : EvidenceAnalysisSkill.MAX_EVIDENCE_CHARS
            ]

            # 摘录可能跳过了开头的 import 段，
            # 行号要跟着偏移，
            # 否则会写成「file:1-30」但内容其实是第 30 行开始的。
            start_line = module.get(
                "start_line",
                1,
            )

            if not isinstance(
                start_line,
                int,
            ) or start_line < 1:
                start_line = 1

            evidence.append(
                {
                    "source_type": "github",
                    "source_url": repo_url,
                    "file_path": file_path,
                    "line_start": start_line,
                    "line_end": (
                        start_line
                        + len(excerpt.splitlines())
                        - 1
                    ),
                    "content": excerpt,
                    "metadata": {},
                }
            )

        return evidence

    @staticmethod
    def _modules(
        input_data,
    ) -> list:
        """
        取出架构分析产出的 modules。

        修复点：

        旧代码只读 input_data["architecture"]，
        但真实数据结构里没有这个 key
        （真实 key 是 architecture_analysis_agent，
        且 PlanExecutorNode 会把结果拍平到顶层 modules），
        因此这个分支以前从未执行过，
        导致 Evidence 只有 README、没有源码。
        """

        architecture = (
            input_data.get("architecture")
            or input_data.get(
                "architecture_analysis_agent"
            )
        )

        if isinstance(
            architecture,
            dict,
        ):

            modules = architecture.get(
                "modules"
            )

            if isinstance(modules, list):
                return modules

        modules = input_data.get("modules")

        if isinstance(modules, list):
            return modules

        return []