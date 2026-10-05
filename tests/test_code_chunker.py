"""
PythonCodeChunker 单元测试。

不依赖任何外部服务（纯 AST + 字符串处理），
与 test_indexer / test_retrieval 那类集成测试不同。

重点覆盖「行号必须准」这条：
RAG 检索回来的片段要写进报告当证据，
行号错了就等于给了个假的出处 ——
比没有出处更糟，因为看起来是可信的。
"""

from app.project_analysis.code_chunker import (
    PythonCodeChunker,
)


SOURCE = '''"""模块文档。"""

import os
from typing import Any


class Service:
    """服务。"""

    def run(self, value):
        return value

    def stop(self):
        return None


def helper(a, b):
    return a + b
'''


def test_chunk_line_numbers_match_real_definitions():
    """每个 chunk 的首行必须真的是它声称的那个定义。"""

    chunker = PythonCodeChunker()

    chunks = chunker.split(SOURCE, "app/service.py")

    by_symbol = {
        chunk["symbol"]: chunk
        for chunk in chunks
        if chunk["symbol"]
    }

    lines = SOURCE.splitlines()

    # class Service 定义在第 8 行
    service = by_symbol["Service"]
    assert lines[service["line_start"] - 1].startswith("class Service")

    # def run 定义在第 12 行
    run = by_symbol["Service.run"]
    assert lines[run["line_start"] - 1].strip().startswith("def run")

    # def stop
    stop = by_symbol["Service.stop"]
    assert lines[stop["line_start"] - 1].strip().startswith("def stop")

    # def helper
    helper = by_symbol["helper"]
    assert lines[helper["line_start"] - 1].strip().startswith("def helper")


def test_class_is_split_by_method_not_by_window():
    """
    类必须按方法切，不能按字符窗口切。

    按窗口切会让 chunk 边界落在任意位置，
    检索命中一个方法却拿回半截代码。
    """

    chunks = PythonCodeChunker().split(SOURCE, "app/service.py")

    symbols = {chunk["symbol"] for chunk in chunks}

    assert "Service.run" in symbols
    assert "Service.stop" in symbols

    # 每个方法各自成块，且都是 function 类型
    run_chunks = [c for c in chunks if c["symbol"] == "Service.run"]
    assert len(run_chunks) == 1
    assert run_chunks[0]["kind"] == "function"


def test_module_head_covers_imports():
    """import 段要单独成块 —— 技术栈类问题的答案在这里。"""

    chunks = PythonCodeChunker().split(SOURCE, "app/service.py")

    heads = [c for c in chunks if c["kind"] == "module"]

    assert len(heads) == 1
    assert "import os" in heads[0]["text"]
    assert heads[0]["line_start"] == 1


def test_chunk_carries_location_header():
    """header 要带文件与行号，检索结果才可核对。"""

    chunks = PythonCodeChunker().split(SOURCE, "app/service.py")

    run = [c for c in chunks if c["symbol"] == "Service.run"][0]

    assert "app/service.py" in run["text"]
    assert "Service.run" in run["text"]


def test_long_function_is_split_with_continuous_line_ranges():
    """
    超长函数要按行续切，且各段行号必须连续、不重叠。

    字符切分会切出半行，行号就对不上了。
    """

    body = "\n".join(
        f"    value_{index} = {index} * 2" for index in range(400)
    )

    source = f"def big():\n{body}\n    return value_0\n"

    chunks = PythonCodeChunker(max_chars=600).split(source, "big.py")

    assert len(chunks) > 1, "应该被切分成多段"

    for chunk in chunks:
        assert len(chunk["text"]) <= 600

    # 行号连续且不重叠
    for previous, current in zip(chunks, chunks[1:]):
        assert current["line_start"] == previous["line_end"] + 1


def test_unparsable_source_falls_back_without_crashing():
    """语法错误的文件不能中断索引流程。"""

    broken = "def oops(:\n    this is not python\n"

    chunks = PythonCodeChunker().split(broken, "broken.py")

    assert chunks, "退路也该产出 chunk"
    assert all(chunk["kind"] == "text" for chunk in chunks)
    assert chunks[0]["line_start"] == 1


def test_empty_input_returns_nothing():
    chunker = PythonCodeChunker()

    assert chunker.split("") == []
    assert chunker.split("   \n\n  ") == []
