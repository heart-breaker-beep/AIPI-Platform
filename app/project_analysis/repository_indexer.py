"""Repository 文档索引。"""

from app.tools.file_reader_tool import FileReaderTool
from app.embeddings.ollama import OllamaEmbedding
from app.vector_store.qdrant import QdrantVectorStore


class RepositoryIndexer:


    def __init__(self):

        self.loader = FileReaderTool()

        self.embedding = (
            OllamaEmbedding()
        )

        self.vector_store = (
            QdrantVectorStore(
                collection_name=
                "repositories"
            )
        )


    async def index(
        self,
        owner: str,
        name: str,
        branch: str = "main",
    ):
        content = await (
            self.loader
            .read_file(
                owner,
                name,
                "README.md",
                branch,
            )
        )


        if not content:
            return 0


        vector = (
            self.embedding
            .embed(content)
        )


        self.vector_store.create_collection(
            vector_size=len(vector)
        )


        self.vector_store.insert(
            vector=vector,
            payload={
                "owner":owner,
                "name":name,
                "source":"README.md",
                "text":content,
            }
        )


        return 1
