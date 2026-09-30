"""
CodeStructureExtractor 测试。

覆盖：

1. 符号识别（class / 函数 / 导入 / 图谱调用）
2. camelCase 名字边界（BaseTool / PlannerAgent）
3. 语法错误文件不拖垮其它文件
4. 路径信号按目录去重
5. 条目数量上限

全部只做静态解析，不联网。
"""

from app.project_analysis.code_structure_extractor import (
    CodeStructureExtractor,
)


def extract_one(
    file_path,
    content,
):
    """抽取单个文件，返回该次结果。"""

    return CodeStructureExtractor.extract(
        [
            {
                "file_path": file_path,
                "content": content,
            }
        ]
    )


def items_of(
    result,
    dimension,
):
    return result["dimensions"][dimension]["items"]


# ----------------------------------------------------------------
# 符号识别
# ----------------------------------------------------------------


def test_extracts_agent_classes_with_line_numbers():
    """Agent 类必须带真实行号。"""

    result = extract_one(
        "app/agents/finance.py",
        (
            "from abc import ABC\n"
            "\n"
            "class BaseAgent(ABC):\n"
            "    pass\n"
            "\n"
            "class InvoiceAgent(BaseAgent):\n"
            "    pass\n"
        ),
    )

    agents = result["dimensions"]["agents"]

    assert "class BaseAgent(ABC)" in agents["items"]

    assert "class InvoiceAgent(BaseAgent)" in agents["items"]

    # 行号必须指向真实定义位置。
    base_evidence = next(
        item
        for item in agents["evidence"]
        if item["text"] == "class BaseAgent(ABC)"
    )

    assert base_evidence["file_path"] == (
        "app/agents/finance.py"
    )

    assert base_evidence["line_start"] == 3


def test_camelcase_symbol_boundaries():
    """
    camelCase 名字必须被识别。

    回归点：用 [^a-z] 配 re.IGNORECASE 时，
    大写字母也会被排除，
    导致 BaseTool / PlannerAgent 这类名字漏掉。
    """

    result = extract_one(
        "app/tools/base.py",
        (
            "class BaseTool:\n"
            "    pass\n"
            "\n"
            "class MyToolbox:\n"
            "    pass\n"
        ),
    )

    tools = items_of(result, "tools")

    assert "class BaseTool" in tools

    # 小写紧跟的 Toolkit / Toolbox 不算
    # （见 _symbol_pattern 的说明）。
    assert "class MyToolbox" not in tools


def test_extracts_workflow_graph_nodes_and_edges():
    """
    Workflow 维度最有价值的部分：
    StateGraph 的节点与边要以源码原文形式记录。
    """

    result = extract_one(
        "app/graph.py",
        (
            "from langgraph.graph import StateGraph\n"
            "\n"
            "graph = StateGraph(AgentState)\n"
            "graph.add_node('intake', intake)\n"
            "graph.add_edge('intake', 'approve')\n"
        ),
    )

    workflow = result["dimensions"]["workflow"]

    assert "StateGraph(...)" in workflow["items"]

    assert (
        "graph.add_node('intake', intake)"
        in workflow["items"]
    )

    assert (
        "graph.add_edge('intake', 'approve')"
        in workflow["items"]
    )

    # 节点名必须带得回源码位置。
    edge = next(
        item
        for item in workflow["evidence"]
        if item["text"]
        == "graph.add_edge('intake', 'approve')"
    )

    assert edge["line_start"] == 5


def test_langgraph_import_is_not_an_agent_signal():
    """
    langgraph 是编排框架，属于 workflow。

    回归点：早期把 langgraph 也算进 agents，
    于是任何用 LangGraph 的项目
    都会凭空多出一批 agents 条目。
    """

    result = extract_one(
        "app/graph.py",
        "from langgraph.graph import StateGraph\n",
    )

    assert (
        "import langgraph.graph"
        in items_of(result, "workflow")
    )

    assert (
        "import langgraph.graph"
        not in items_of(result, "agents")
    )


def test_extracts_tool_decorator():
    """@tool 装饰器的函数算 Tool。"""

    result = extract_one(
        "app/search.py",
        (
            "from langchain_core.tools import tool\n"
            "\n"
            "@tool\n"
            "def web_search(query):\n"
            "    pass\n"
        ),
    )

    assert any(
        "web_search" in item
        for item in items_of(result, "tools")
    )


def test_extracts_rag_and_memory_signals():
    """RAG / Memory 从导入与符号识别。"""

    result = extract_one(
        "app/store.py",
        (
            "from qdrant_client import QdrantClient\n"
            "from langgraph.checkpoint.sqlite "
            "import SqliteSaver\n"
            "\n"
            "def retrieve_documents(query):\n"
            "    pass\n"
            "\n"
            "class CheckpointStore:\n"
            "    pass\n"
        ),
    )

    assert "import qdrant_client" in items_of(
        result,
        "rag",
    )

    assert "def retrieve_documents" in items_of(
        result,
        "rag",
    )

    assert "class CheckpointStore" in items_of(
        result,
        "memory",
    )


def test_storage_is_not_rag():
    """
    storage 里含 rag 三个字母，但不能算 RAG。

    真实事故：对某个仓库跑真实分析时，
    src/app/core/config.py 的
    validate_storage_root 被判成了 RAG 实现，
    于是 08 章凭空多出一条代码证据。
    """

    result = extract_one(
        "src/app/core/config.py",
        (
            "def validate_storage_root(value):\n"
            "    return value\n"
        ),
    )

    assert items_of(result, "rag") == []

    assert result["dimensions"]["rag"][
        "details"
    ] == []


def test_rag_word_boundary_still_matches():
    """带词边界的 rag 仍要能命中。"""

    result = extract_one(
        "src/app/rag/store.py",
        (
            "def rag_lookup(query):\n"
            "    return query\n"
            "\n"
            "def rerank_results(items):\n"
            "    return items\n"
        ),
    )

    rag = items_of(result, "rag")

    assert "def rag_lookup" in rag

    assert "def rerank_results" in rag


def test_generic_search_is_not_rag():
    """
    名字里只有 search 的函数不算 RAG。

    否则 search_github_repo 之类
    会把任何项目都判成有 RAG。
    """

    result = extract_one(
        "app/github.py",
        "def search_github_repos(q):\n    pass\n",
    )

    assert items_of(result, "rag") == []


# ----------------------------------------------------------------
# 容错
# ----------------------------------------------------------------


def test_syntax_error_is_recorded_not_raised():
    """
    语法错误的文件必须记入 unparsed，
    且不影响其它文件。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "broken.py",
                "content": "def f(:\n",
            },
            {
                "file_path": "app/agents/ok.py",
                "content": "class OkAgent:\n    pass\n",
            },
        ]
    )

    assert len(result["unparsed"]) == 1

    assert (
        result["unparsed"][0]["file_path"]
        == "broken.py"
    )

    assert "SyntaxError" in (
        result["unparsed"][0]["error"]
    )

    # 好文件照常产出。
    assert result["parsed_files"] == 1

    assert "class OkAgent" in items_of(
        result,
        "agents",
    )


def test_truncated_python_is_reported_not_guessed():
    """
    截断的源码会语法错误，必须如实上报。

    这是为什么 AST 抽取要用未截断的全文：
    截断过的 Python 抽不出任何符号，
    但绝不能因此声称「项目没有 Agent」。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "app/agents/half.py",
                "content": "class HalfAgent:\n    def ex",
            }
        ]
    )

    assert result["parsed_files"] == 0

    assert result["available"] is False

    assert len(result["unparsed"]) == 1


def test_non_python_files_are_skipped():
    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "docker-compose.yml",
                "content": "services:\n  api:\n",
            }
        ]
    )

    assert result["parsed_files"] == 0


def test_broken_input_does_not_raise():
    """结构异常时不能抛异常。"""

    result = CodeStructureExtractor.extract(
        "not-a-list"
    )

    assert result["parsed_files"] == 0

    result = CodeStructureExtractor.extract(
        [None, "x", {"file_path": "a.py"}]
    )

    assert result["parsed_files"] == 0


# ----------------------------------------------------------------
# 路径信号
# ----------------------------------------------------------------


def test_path_signal_is_deduped_by_directory():
    """
    同一目录下的多个文件只记一条路径信号。

    否则 src/agents/ 下有 30 个文件时，
    路径会把 MAX_ITEMS 刷满，
    真正有价值的类名被挤出去。
    """

    result = CodeStructureExtractor.extract(
        [],
        extra_paths=[
            "src/agents/a.py",
            "src/agents/b.py",
            "src/agents/c.py",
        ],
    )

    agents = items_of(result, "agents")

    assert agents == ["路径 src/agents/"]


def test_path_signal_covers_unread_files():
    """
    没被读取的文件也要贡献路径信号。

    配额只有 12 个，
    但「存在 src/agents/ 目录」这条证据
    不该因为该目录下的文件没被读到而丢失。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "src/main.py",
                "content": "print('x')\n",
            }
        ],
        extra_paths=["src/agents/未读取到的.py"],
    )

    assert "路径 src/agents/" in items_of(
        result,
        "agents",
    )


def test_symbols_rank_above_path_signals():
    """
    符号条目必须排在路径信号前面。

    _add 是按顺序填满 MAX_ITEMS 就停的，
    如果路径先写入，
    第一个类名就可能被挤掉。
    """

    result = CodeStructureExtractor.extract(
        [
            {
                "file_path": "src/agents/base.py",
                "content": (
                    "class RealAgent:\n    pass\n"
                ),
            }
        ]
    )

    agents = items_of(result, "agents")

    assert agents[0] == "class RealAgent"

    assert agents[-1] == "路径 src/agents/"


# ----------------------------------------------------------------
# 实现明细（下到函数体）
# ----------------------------------------------------------------


GRAPH_SOURCE = (
    "from langgraph.graph import StateGraph\n"
    "\n"
    "class WorkflowService:\n"
    "    def build(self):\n"
    "        builder = StateGraph(AgentState)\n"
    "        builder.add_node('duplicate_check',\n"
    "                          self._node_duplicate_check)\n"
    "        builder.add_edge('a', 'b')\n"
    "        return builder.compile()\n"
    "\n"
    "    def _node_duplicate_check(self, state: AgentState)"
    " -> AgentState:\n"
    "        found = find_similar_invoices(\n"
    "            state['vendor'], state['amount'])\n"
    "        if found.score >= 0.85:\n"
    "            state['status'] = 'duplicate_suspected'\n"
    "        return state\n"
)


def test_node_callback_is_resolved_to_definition():
    """
    add_node 的处理函数必须被解析到真实定义。

    这是「下到函数体」的核心：
    从「有这么个节点」变成
    「这个节点的签名与调用链是什么」。
    """

    result = extract_one(
        "src/app/services/workflow_service.py",
        GRAPH_SOURCE,
    )

    details = result["dimensions"]["workflow"][
        "details"
    ]

    node = next(
        item
        for item in details
        if item["name"] == "duplicate_check"
    )

    assert node["symbol"] == "_node_duplicate_check"

    assert node["signature"] == (
        "def _node_duplicate_check("
        "self, state: AgentState) -> AgentState"
    )

    assert "find_similar_invoices" in node["calls"]


def test_node_detail_carries_threshold_literals():
    """
    关键词面量必须被记录下来。

    0.85 这种阈值是理解实现的关键，
    只记符号名是拿不到的。
    """

    result = extract_one(
        "src/app/services/workflow_service.py",
        GRAPH_SOURCE,
    )

    node = next(
        item
        for item in result["dimensions"][
            "workflow"
        ]["details"]
        if item["name"] == "duplicate_check"
    )

    assert "0.85" in node["literals"]

    assert "'duplicate_suspected'" in node[
        "literals"
    ]


def test_add_edge_does_not_produce_a_detail():
    """
    add_edge 只记拓扑，不产明细。

    它解析不出处理函数，
    产一条空明细只会挤占 MAX_DETAILS。
    """

    result = extract_one(
        "src/app/services/workflow_service.py",
        GRAPH_SOURCE,
    )

    details = result["dimensions"]["workflow"][
        "details"
    ]

    signatures = [
        item["signature"] for item in details
    ]

    assert not any(
        "add_edge" in signature
        for signature in signatures
    )


def test_class_detail_lists_methods():
    """类明细要给出基类与方法表。"""

    result = extract_one(
        "src/app/tools/registry.py",
        (
            "class ToolRegistry(BaseToolkit):\n"
            "    def register(self, tool):\n"
            "        pass\n"
            "\n"
            "    def resolve(self, name):\n"
            "        pass\n"
        ),
    )

    detail = result["dimensions"]["tools"][
        "details"
    ][0]

    assert detail["signature"] == (
        "class ToolRegistry(BaseToolkit)"
    )

    assert detail["methods"] == [
        "register",
        "resolve",
    ]


def test_function_detail_has_signature_and_calls():
    """RAG 函数明细要带签名与调用链。"""

    result = extract_one(
        "src/app/rag/indexer.py",
        (
            "def retrieve_and_rank(query: str,"
            " top_k: int = 5) -> list:\n"
            "    vectors = embed_query(query)\n"
            "    return search_index(vectors, top_k)\n"
        ),
    )

    detail = result["dimensions"]["rag"][
        "details"
    ][0]

    assert detail["signature"] == (
        "def retrieve_and_rank(query: str,"
        " top_k: int = 5) -> list"
    )

    assert detail["calls"] == [
        "embed_query",
        "search_index",
    ]


def test_boring_literals_are_filtered():
    """
    噪声字面量不能把真正的阈值挤掉。

    "utf-8" / "id" 这类到处都是，
    0.0 通常只是初始化占位。
    """

    result = extract_one(
        "src/app/rag/loader.py",
        (
            "def retrieve_file(path):\n"
            "    raw = open(path, encoding='utf-8')\n"
            "    score = 0.0\n"
            "    limit = 25\n"
            "    label = 'not_found_in_index'\n"
            "    return limit\n"
        ),
    )

    literals = result["dimensions"]["rag"][
        "details"
    ][0]["literals"]

    assert "'utf-8'" not in literals

    assert "0.0" not in literals

    assert "25" in literals

    assert "'not_found_in_index'" in literals


def test_builtin_calls_are_filtered():
    """内建函数不能出现在调用链里。"""

    result = extract_one(
        "src/app/rag/util.py",
        (
            "def retrieve_all(items):\n"
            "    total = len(items)\n"
            "    return sorted(items)\n"
        ),
    )

    calls = result["dimensions"]["rag"][
        "details"
    ][0]["calls"]

    assert "len" not in calls

    assert "sorted" not in calls


def test_details_are_capped():
    """明细数量必须有上限，避免 state 膨胀。"""

    functions = "".join(
        f"def retrieve_{i}(q):\n"
        f"    return q\n"
        for i in range(30)
    )

    result = extract_one(
        "src/app/rag/many.py",
        functions,
    )

    details = result["dimensions"]["rag"][
        "details"
    ]

    assert len(details) == (
        CodeStructureExtractor.MAX_DETAILS
    )


def test_items_are_capped():
    """条目数量必须有上限，避免 state 膨胀。"""

    classes = "".join(
        f"class Agent{i}:\n    pass\n"
        for i in range(50)
    )

    result = extract_one(
        "src/agents/many.py",
        classes,
    )

    agents = result["dimensions"]["agents"]

    assert len(agents["items"]) == (
        CodeStructureExtractor.MAX_ITEMS
    )

    assert len(agents["evidence"]) == (
        CodeStructureExtractor.MAX_EVIDENCE
    )


# ----------------------------------------------------------------
# 代码摘录跳过 import 段
# ----------------------------------------------------------------


def test_meaningful_start_skips_import_block():
    """
    摘录必须跳过开头的 import 段。

    真实反馈：「这源码提取了一堆 import 根本没有用」。
    原因是摘录固定从第 1 行取，
    而 Python 文件开头必然是 import 块。
    """

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        '"""模块说明。"""\n'
        "\n"
        "import os\n"
        "import uuid\n"
        "from decimal import Decimal\n"
        "\n"
        "\n"
        "class WorkflowService:\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith(
        "class WorkflowService:"
    )


def test_meaningful_start_handles_multiline_docstring():

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        '"""\n'
        "多行\n"
        "说明\n"
        '"""\n'
        "import os\n"
        "\n"
        "class B:\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith("class B:")


def test_meaningful_start_falls_back_for_import_only_file():
    """
    整份文件只有 import 时回退到 0。

    不能返回 len(source)，那样摘录会是空串。
    """

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = "import os\nimport sys\n"

    assert (
        CodeStructureExtractor.meaningful_start(
            source
        )
        == 0
    )


def test_module_entry_records_start_line():
    """
    摘录跳过了多少行必须记下来 ——
    否则证据会写成「file:1-30」
    但内容其实是第 30 行开始的。
    """

    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    source = (
        "import os\n"
        "import uuid\n"
        "\n"
        "\n"
        "class Real:\n"
        "    pass\n"
    )

    entry = ArchitectureAnalysisSkill()._module_entry(
        "f.py",
        source,
    )

    assert entry["content"].startswith("class Real:")

    assert entry["start_line"] == 5


def test_module_entry_without_imports_has_no_start_line():

    from app.skills.architecture_analysis_skill import (
        ArchitectureAnalysisSkill,
    )

    entry = ArchitectureAnalysisSkill()._module_entry(
        "f.py",
        "class A:\n    pass\n",
    )

    assert "start_line" not in entry

    assert entry["content"].startswith("class A:")


def test_meaningful_start_handles_multiline_import():
    """
    多行 import 的续行也必须跳过。

    真实事故：workflow_service.py 里

        from app.schemas.agent import (
            AgentRunListItem,
            ...
        )

    只看行首的话，扫描器会停在第 2 行
    （`    AgentRunListItem,` 不以 import 开头），
    摘录依然是一串 import 名单。
    """

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        "import os\n"
        "from app.schemas.agent import (\n"
        "    AgentRunListItem,\n"
        "    AgentRunResponse,\n"
        ")\n"
        "\n"
        "class AgentState(TypedDict):\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith(
        "class AgentState"
    )


def test_meaningful_start_handles_backslash_continuation():

    from app.project_analysis.code_structure_extractor import (
        CodeStructureExtractor,
    )

    source = (
        "from app.core import a, \\n"
        "    b, c\n"
        "\n"
        "class Real:\n"
        "    pass\n"
    )

    start = CodeStructureExtractor.meaningful_start(
        source
    )

    assert source[start:].startswith("class Real:")
