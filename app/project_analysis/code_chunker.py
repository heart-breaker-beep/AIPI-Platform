"""Markdown 文档切分器。"""

import re


class MarkdownChunker:
    """将 Markdown 文档切分成适合向量检索的文本块。"""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 150,
    ) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> list[str]:
        """将 Markdown 文本切分成多个 Chunk。"""

        sections = self._split_by_heading(text)

        chunks: list[str] = []

        for section in sections:
            chunks.extend(
                self._split_section(section)
            )

        return [
            chunk.strip()
            for chunk in chunks
            if chunk.strip()
        ]

    def _split_by_heading(
        self,
        text: str,
    ) -> list[str]:
        """优先按照 Markdown 标题划分语义章节。"""

        parts = re.split(
            r"(?=^#{1,6}\s+)",
            text,
            flags=re.MULTILINE,
        )

        return [
            part.strip()
            for part in parts
            if part.strip()
        ]

    def _split_section(
        self,
        section: str,
    ) -> list[str]:
        """将过长章节进一步切分。"""

        if len(section) <= self.chunk_size:
            return [section]

        chunks: list[str] = []

        start = 0

        while start < len(section):
            end = start + self.chunk_size

            chunk = section[start:end]

            chunks.append(chunk)

            if end >= len(section):
                break

            start = end - self.chunk_overlap

        return chunks