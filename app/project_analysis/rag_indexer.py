"""
仓库源码索引器。

把仓库的 .py 源码切分、向量化并写入 Qdrant，
供分析过程中的语义检索（RAG）使用。

在整条 RAG 链路里的位置
========================

    索引（本模块）  →  Qdrant  →  检索  →  Evidence

在此之前，链路只有后半截：
`QdrantContextRetriever` / `QdrantSearchTool` / `_from_qdrant` 都在，
测试也齐，但**没有任何生产代码往 Qdrant 里写**，
所以集合始终是空的，检索必然无结果。

本模块补的就是写入这一环。

只索引 .py
==========

刻意跳过 README 等文档：

- README 已经被完整喂给综合分析（6000 字符上限），
  并且已经是 evidence 的第一条，
  再索引一遍不会带来任何新信息，只会挤占检索名额；
- 源码才是结构分析覆盖不足、需要语义检索补位的地方。

与 DocumentIndexer 的分工
=========================

`DocumentIndexer`（project_indexer.py）是早期原型：
用 MarkdownChunker 切分、payload 里只有 document_id / chunk_index / text。
它没有行号、没有文件路径，检索结果无法还原成可追溯的 evidence
（这也是它至今没被接进主链路的原因之一）。

本模块是面向源码的正式实现：
按 AST 边界切分、payload 带全锚点字段。

并发
====

文件读取刻意保持串行。

`FileReaderTool` 走 GitHub API，单文件约 0.9 秒；
改用 asyncio.gather 能显著缩短总时长，
但也会同时打出 N 个请求，
在未认证（60 次/小时）或令牌额度紧张时容易被限流。
当前按串行设计并在配置里限制文件数，先把链路跑通；
要提速的话，在 `_read_extra` 里加并发 + 信号量即可。
"""

from app.core.logging import get_logger
from app.project_analysis.code_chunker import PythonCodeChunker


logger = get_logger(__name__)


class RagIndexer:
    """把仓库源码写入 Qdrant，建立可检索的向量索引。"""

    # 每批提交多少个 chunk 做 embedding。
    #
    # 实测单条 44ms、批量摊薄 36ms（bge-m3 / Ollama），
    # 提速有限，所以批量主要是为了减少 HTTP 往返次数而不是吞吐。
    EMBED_BATCH = 16

    # 单个文件最多贡献多少 chunk，避免一个巨型文件独占索引。
    MAX_CHUNKS_PER_FILE = 40

    def __init__(
        self,
        file_reader=None,
        embedding=None,
        vector_store=None,
        chunker=None,
    ) -> None:

        self.file_reader = file_reader
        self.embedding = embedding
        self.vector_store = vector_store
        self.chunker = chunker or PythonCodeChunker()

    # ------------------------------------------------------------------
    # 入口
    # ------------------------------------------------------------------

    async def index_repository(
        self,
        *,
        repository_id: int,
        run_id: str,
        repo_url: str,
        owner: str,
        name: str,
        branch: str,
        known_files: list[dict] | None = None,
        extra_file_paths: list[str] | None = None,
        max_files: int = 80,
    ) -> dict:
        """
        为一个仓库建立向量索引。

        known_files
            已经读过、正文已在内存里的文件
            （PlanExecutorNode 拍平到 state.data["modules"] 的那批）。
            走这条路不需要额外请求 GitHub，是免费的。

        extra_file_paths
            额外要拉取的文件路径。
            这才是 RAG 相对结构分析的增量来源 ——
            检索的覆盖面因此能超出"已经被读过的文件"。

        返回一份统计，用于日志与 workflow state。
        """

        known_files = known_files or []
        extra_file_paths = extra_file_paths or []

        sources = await self._collect_sources(
            known_files,
            extra_file_paths,
            max_files,
            owner=owner,
            name=name,
            branch=branch,
        )

        if not sources:
            logger.warning(
                "RAG 索引：没有可索引的 .py 文件，跳过。"
            )
            return {"indexed": False, "reason": "no_python_files"}

        # 集合必须先存在。
        #
        # 漏掉这一步的后果很隐蔽：新环境的 Qdrant 里没有
        # github_projects 集合，delete / upsert 都会 404，
        # 而调用方（_from_rag）把异常兜底成"没有检索结果"，
        # 于是 RAG 静默失效 —— 报告照常产出，
        # 只是永远没有检索证据，从外部完全看不出来。
        self._ensure_collection()

        # 先清库再写。
        #
        # 不清的话，文件改动后新旧 chunk 会共存，
        # 检索可能返回已经不存在的代码 ——
        # 那种错误没有任何外部迹象，极难发现。
        try:
            self.vector_store.delete_by_repository(
                repository_id
            )
        except Exception as error:  # noqa: BLE001
            logger.warning(
                "RAG 索引：清理旧向量失败（继续索引）：%s",
                error,
            )

        chunks: list[dict] = []

        for file_path, content in sources:

            file_chunks = self.chunker.split(
                content,
                file_path,
            )[: self.MAX_CHUNKS_PER_FILE]

            for chunk in file_chunks:
                chunks.append(
                    {
                        **chunk,
                        "file_path": file_path,
                    }
                )

        if not chunks:
            return {"indexed": False, "reason": "no_chunks"}

        written = self._embed_and_store(
            chunks,
            repository_id=repository_id,
            run_id=run_id,
            repo_url=repo_url,
        )

        summary = {
            "indexed": True,
            "repository_id": repository_id,
            "files": len(sources),
            "chunks": written,
        }

        logger.info(
            "RAG 索引完成：仓库 %s，%s 个文件，%s 个 chunk",
            repository_id,
            len(sources),
            written,
        )

        return summary

    def _ensure_collection(self) -> None:
        """
        确保向量集合存在，且维度与当前 embedding 模型匹配。

        维度是探测出来的，不是写死的 1024 ——
        换 embedding 模型（bge-m3 之外还有 mxbai-embed-large 等）
        维度就会变，写死会让 upsert 全部失败。
        探测只花一次 embedding 调用（约 40ms）。

        create_collection 内部已判断"存在即返回"，
        所以重复调用是安全的。
        """

        try:
            probe = self.embedding.embed("dimension")
            dimension = len(probe)

        except Exception as error:  # noqa: BLE001
            logger.warning(
                "RAG 索引：探测 embedding 维度失败，按默认 1024 处理：%s",
                error,
            )
            dimension = 1024

        self.vector_store.create_collection(
            vector_size=dimension
        )

    # ------------------------------------------------------------------
    # 取材
    # ------------------------------------------------------------------

    async def _read_extra(
        self,
        owner: str,
        name: str,
        branch: str,
        paths: list[str],
    ) -> list[tuple[str, str]]:
        """逐个读取额外文件。单个失败不影响整体。"""

        out: list[tuple[str, str]] = []

        for path in paths:

            try:
                content = await self.file_reader.execute(
                    owner=owner,
                    name=name,
                    file_path=path,
                    branch=branch,
                )

            except Exception as error:  # noqa: BLE001
                logger.warning(
                    "RAG 索引：读取 %s 失败，跳过：%s",
                    path,
                    error,
                )
                continue

            if isinstance(content, str) and content.strip():
                out.append((path, content))

        return out

    async def _collect_sources(
        self,
        known_files: list[dict],
        extra_file_paths: list[str],
        max_files: int,
        *,
        owner: str,
        name: str,
        branch: str,
    ) -> list[tuple[str, str]]:
        """
        汇总待索引的文件正文。

        先收已经在内存里的（免费），
        再按剩余名额去 GitHub 补读额外文件（贵，所以放在后面）。

        只保留 .py：非 Python 文件切不出有意义的结构边界，
        且 README 那类文档本来就已经在喂给 LLM 的通道里。
        """

        sources: list[tuple[str, str]] = []
        seen: set[str] = set()

        for item in known_files:

            if not isinstance(item, dict):
                continue

            path = item.get("file_path")
            content = item.get("content")

            if isinstance(content, dict):
                content = content.get("content", "")

            if not path or not isinstance(content, str):
                continue

            if path in seen:
                continue

            if not self._is_python(path) or not content.strip():
                continue

            seen.add(path)
            sources.append((path, content))

            if len(sources) >= max_files:
                return sources

        remaining = max_files - len(sources)

        if remaining <= 0 or self.file_reader is None:
            return sources

        candidates = [
            path
            for path in extra_file_paths
            if path not in seen and self._is_python(path)
        ][:remaining]

        sources.extend(
            await self._read_extra(
                owner,
                name,
                branch,
                candidates,
            )
        )

        return sources

    @staticmethod
    def _is_python(path: str) -> bool:
        return str(path).endswith(".py")

    # ------------------------------------------------------------------
    # 写入
    # ------------------------------------------------------------------

    def _embed_and_store(
        self,
        chunks: list[dict],
        *,
        repository_id: int,
        run_id: str,
        repo_url: str,
    ) -> int:
        """
        分批嵌入并写入 Qdrant。

        payload 必须带全 file_path / line_start / line_end ——
        证据链路（`evidence_analysis_skill._from_qdrant`）就是按这几个
        字段把检索结果还原成 `file.py:120-148` 这种可追溯锚点的。
        缺了行号，检索结果就只是一段来路不明的代码。
        """

        written = 0

        for start in range(0, len(chunks), self.EMBED_BATCH):

            batch = chunks[start : start + self.EMBED_BATCH]

            vectors = self.embedding.embed_batch(
                [item["text"] for item in batch]
            )

            points = []

            for item, vector in zip(batch, vectors):

                points.append(
                    {
                        "id": self._point_id(
                            repository_id,
                            item["file_path"],
                            item["line_start"],
                        ),
                        "vector": vector,
                        "payload": {
                            "repository_id": repository_id,
                            "run_id": run_id,
                            "source_type": "github",
                            "source_url": repo_url,
                            "file_path": item["file_path"],
                            "line_start": item["line_start"],
                            "line_end": item["line_end"],
                            "kind": item.get("kind"),
                            "symbol": item.get("symbol"),
                            "text": item["text"],
                        },
                    }
                )

            self.vector_store.upsert_many(points)

            written += len(points)

        return written

    @staticmethod
    def _point_id(
        repository_id: int,
        file_path: str,
        line_start: int,
    ) -> int:
        """
        由 (仓库, 文件, 起始行) 生成稳定的整数 ID。

        稳定 ID 让重复索引变成幂等写入而不是不断追加，
        也让"同一个位置"不会被存成两份。
        """

        import hashlib

        raw = f"{repository_id}:{file_path}:{line_start}"

        digest = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()

        return int(digest[:15], 16)
