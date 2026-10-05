"""
文本切分器。

两个用途不同的切分器：

- MarkdownChunker     —— 切 README / 文档，按 markdown 标题分节
- PythonCodeChunker   —— 切 Python 源码，按 AST 的类 / 函数边界分块

两者不可互换：拿 MarkdownChunker 切源码会退化成固定窗口，
把函数从中间截断；见 PythonCodeChunker 的类文档。
"""

import ast
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


class PythonCodeChunker:
    """
    Python 源码切分器：按类 / 函数边界切，而不是按字符数。

    为什么需要它
    ============

    向量检索的质量取决于「一个 chunk 是不是一个完整语义单元」。

    MarkdownChunker 按 `^#{1,6}\\s+` 标题切分，这个正则在 Python 源码里
    几乎不命中（源码注释用的是 `#` 加空格，不是 `# 标题`），
    于是直接退化成「固定 1000 字符窗口 + 150 重叠」——
    一个 30 行的函数会被从中间截断，另一半落到下一个 chunk。
    检索回来的片段既缺上下文、又对不上行号。

    本类改用 AST 边界：每个节点都带 lineno 与 end_lineno，
    按这两个值切出来的 chunk 天然就是「一个类」或「一个函数」。

    比 Markdown 版多了什么
    ======================

    每个 chunk 带源码行号区间（line_start / line_end）。
    这是 RAG 产出可追溯证据的前提 ——
    没有行号，检索回来的片段就没法写成 `file.py:120-148` 这样的锚点，
    evidence 就退化成「一段不知道从哪来的代码」。

    解析失败时
    ==========

    语法错误、编码问题、f-string 在旧版解释器下的怪癖，
    都会让 ast.parse 抛异常。
    此时退回固定窗口切分，而不是让整个索引流程因单个坏文件中断。
    """

    # 单个 chunk 的目标上限（字符）。
    #
    # 取 1500 与 EvidenceAnalysisSkill.MAX_EVIDENCE_CHARS 保持一致：
    # 再长也会在落库那一步被截掉，白白占用向量库。
    MAX_CHARS = 1500

    # 模块头部最多取多少行（import 段，能反映技术栈）。
    MAX_HEAD_LINES = 40

    def __init__(
        self,
        max_chars: int = MAX_CHARS,
        max_head_lines: int = MAX_HEAD_LINES,
    ) -> None:

        self.max_chars = max_chars
        self.max_head_lines = max_head_lines

    def split(
        self,
        text: str,
        file_path: str = "",
    ) -> list[dict]:
        """
        把一份 Python 源码切成带行号的 chunk。

        返回：[{text, line_start, line_end, kind, symbol}, ...]

        行号是 1-based、闭区间，与编辑器显示的一致。
        """

        if not text or not text.strip():
            return []

        lines = text.splitlines()

        try:
            tree = ast.parse(text)

        except (SyntaxError, ValueError, RecursionError):

            # 解析不了的（半截文件 / 非 Python）走固定窗口，
            # 至少还能提供文本检索。
            return self._window_chunks(
                lines,
                0,
                len(lines),
                file_path,
            )

        chunks: list[dict] = []

        head = self._module_head(tree, lines, file_path)

        if head:
            chunks.append(head)

        for node in tree.body:

            if isinstance(
                node,
                (
                    ast.ClassDef,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                chunks.extend(
                    self._node_chunks(node, lines, file_path)
                )

        return chunks

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------

    def _module_head(
        self,
        tree: ast.Module,
        lines: list[str],
        file_path: str,
    ) -> dict | None:
        """
        模块头部（import 段 + 模块级常量）。

        单独成块的理由：技术栈类问题（"用了什么 ORM"）的答案
        基本都在 import 里，而这些行不属于任何类或函数，
        按定义边界切的话会被漏掉。
        """

        first_def = None

        for node in tree.body:

            if isinstance(
                node,
                (
                    ast.ClassDef,
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                first_def = node.lineno
                break

        end = first_def - 1 if first_def else len(lines)

        end = min(end, self.max_head_lines)

        if end <= 0:
            return None

        segment = "\n".join(lines[:end])

        if not segment.strip():
            return None

        header = self._header(file_path, 1, "module", None)

        return {
            "text": f"{header}\n{segment}"[: self.max_chars],
            "line_start": 1,
            "line_end": end,
            "kind": "module",
            "symbol": None,
        }

    def _node_chunks(
        self,
        node,
        lines: list[str],
        file_path: str,
        parent: str | None = None,
    ) -> list[dict]:
        """
        把一个类 / 函数节点切成 chunk。

        类按**方法**切，不按窗口切。

        理由：一个 400 行的类如果按 1500 字符窗口切，
        会得到 7 个边界落在任意位置的块 ——
        检索命中其中一个，拿回来的仍是半截方法。
        按方法切则每个 chunk 就是一个完整方法，
        类名与方法名还会写进 header，
        使「XX 类怎么处理鉴权」这类查询能直接命中目标方法。
        """

        keep = self.max_chars - 64  # 给 header 留的余量

        # --- 类：拆成「类头 + 逐个方法」---
        if isinstance(node, ast.ClassDef):

            parts = self._class_parts(
                node,
                lines,
                file_path,
                parent,
            )

            if parts:
                return parts

        # --- 函数 / 没有方法体的类：整体成块，过长再按行分 ---

        start = node.lineno
        end = getattr(node, "end_lineno", None) or start

        kind = (
            "class"
            if isinstance(node, ast.ClassDef)
            else "function"
        )

        symbol = f"{parent}.{node.name}" if parent else node.name

        return self._segment_chunks(
            lines,
            start,
            end,
            file_path,
            kind,
            symbol,
            keep,
        )

    def _class_parts(
        self,
        node: ast.ClassDef,
        lines: list[str],
        file_path: str,
        parent: str | None,
    ) -> list[dict]:
        """
        类 → 类头 chunk + 每个方法 chunk。

        类头（`class X(Base):` 加类文档字符串、类属性）单独成块：
        它承载「继承自谁」这个关键事实，
        而这块信息不属于任何一个方法。
        """

        methods = [
            item
            for item in node.body
            if isinstance(
                item,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
        ]

        if not methods:
            return []

        keep = self.max_chars - 64

        out: list[dict] = []

        head_end = methods[0].lineno - 1

        if head_end >= node.lineno:

            out.extend(
                self._segment_chunks(
                    lines,
                    node.lineno,
                    head_end,
                    file_path,
                    "class",
                    node.name,
                    keep,
                )
            )

        for method in methods:

            out.extend(
                self._node_chunks(
                    method,
                    lines,
                    file_path,
                    parent=node.name,
                )
            )

        return out

    def _segment_chunks(
        self,
        lines: list[str],
        start: int,
        end: int,
        file_path: str,
        kind: str,
        symbol: str,
        budget: int,
    ) -> list[dict]:
        """把 [start, end]（1-based 闭区间）切成一个或多个 chunk。"""

        header = self._header(file_path, start, kind, symbol)

        size = max(budget - len(header) - 1, 1)

        return [
            {
                "text": (
                    f"{header}\n"
                    + "\n".join(lines[seg_start:seg_end])
                )[: self.max_chars],
                "line_start": seg_start + 1,
                "line_end": seg_end,
                "kind": kind,
                "symbol": symbol,
            }
            for seg_start, seg_end in self._group_lines(
                lines,
                start - 1,
                end,
                size,
            )
        ]

    def _window_chunks(
        self,
        lines: list[str],
        start: int,
        end: int,
        file_path: str,
    ) -> list[dict]:
        """固定窗口切分（AST 不可用时的退路）。"""

        header = self._header(file_path, start + 1, "text", None)

        budget = max(self.max_chars - len(header) - 1, 1)

        return [
            {
                "text": (
                    f"{header}\n"
                    + "\n".join(lines[seg_start:seg_end])
                )[: self.max_chars],
                "line_start": seg_start + 1,
                "line_end": seg_end,
                "kind": "text",
                "symbol": None,
            }
            for seg_start, seg_end in self._group_lines(
                lines,
                start,
                end,
                budget,
            )
        ]

    @staticmethod
    def _group_lines(
        lines: list[str],
        start: int,
        end: int,
        budget: int,
    ) -> list[tuple[int, int]]:
        """
        把 [start, end) 切成若干段，每段拼起来不超过 budget 字符。

        按行分组而不是按字符切 ——
        字符切会切出半行，行号就对不上了。
        """

        groups: list[tuple[int, int]] = []

        seg_start = start
        size = 0

        index = start

        while index < end:

            line_len = len(lines[index]) + 1

            if size and size + line_len > budget:

                groups.append((seg_start, index))

                seg_start = index
                size = 0

                continue

            size += line_len
            index += 1

        if seg_start < end:
            groups.append((seg_start, end))

        return groups

    @staticmethod
    def _header(
        file_path: str,
        line: int,
        kind: str,
        symbol: str | None,
    ) -> str:
        """
        给 chunk 加一行来源标注。

        这行会一起被向量化：把文件路径与符号名放进检索文本，
        能让"哪个文件实现了鉴权"这类查询更容易命中，
        也便于人工核对检索结果来自哪里。
        """

        location = f"{file_path}:{line}" if file_path else f"line {line}"

        if symbol:
            return f"# {location} [{kind}] {symbol}"

        return f"# {location} [{kind}]"