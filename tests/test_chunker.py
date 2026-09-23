"""Markdown Chunker 测试。"""

from app.project_analysis.code_chunker import MarkdownChunker


def test_markdown_chunker():
    """测试 Markdown 是否可以按照章节切分。"""

    text = """# Introduction

This project is an AI Agent platform.

# Architecture

The system contains multiple agents and tools.

# HITL

Human approval is required for sensitive operations.
"""

    chunker = MarkdownChunker()

    chunks = chunker.split(text)

    assert len(chunks) == 3

    assert "Introduction" in chunks[0]
    assert "Architecture" in chunks[1]
    assert "HITL" in chunks[2]