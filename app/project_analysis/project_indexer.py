"""文档索引服务：负责 Chunk、Embedding 和向量存储。"""

from app.embeddings.ollama import OllamaEmbedding
from app.project_analysis.code_chunker import MarkdownChunker
from app.vector_store.qdrant import QdrantVectorStore


class DocumentIndexer:
    """将文档切分并建立 Qdrant 向量索引。"""

    def __init__(
        self,
        collection_name: str = "github_projects",
    ) -> None:
        self.chunker = MarkdownChunker()
        self.embedding = OllamaEmbedding()
        self.vector_store = QdrantVectorStore(
            collection_name=collection_name,
        )

        self.vector_store.create_collection(
            vector_size=1024,
        )

    def index_document(
        self,
        document_id: str,
        text: str,
        metadata: dict,
    ) -> int:
        """将一份文档切分、向量化并写入 Qdrant。"""

        chunks = self.chunker.split(text)

        for index, chunk in enumerate(chunks):
            vector = self.embedding.embed(chunk)

            point_id = self._build_point_id(
                document_id,
                index,
            )

            payload = {
                **metadata,
                "document_id": document_id,
                "chunk_index": index,
                "text": chunk,
            }

            self.vector_store.upsert(
                point_id=point_id,
                vector=vector,
                payload=payload,
            )

        return len(chunks)

    @staticmethod
    def _build_point_id(
        document_id: str,
        chunk_index: int,
    ) -> int:
        """根据文档 ID 和 Chunk 序号生成稳定的整数 ID。"""

        import hashlib

        value = f"{document_id}:{chunk_index}"

        digest = hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

        return int(digest[:16], 16) % (2**63 - 1)