"""
Code Structure Extractor。

用 Python AST 从**真实源码**中抽取被分析项目的结构信号。

为什么需要它
============

在此之前，报告 04-09 章（Agent 架构 / Workflow / Skill /
Tool / RAG / Memory）唯一的来源是

    ArchitectureAnalysisSkill._extract_project_structure

它对被分析项目的 README 做关键词匹配，
再把命中的行按逗号切碎当条目。

结果是：一个 README 里没写 "skill" 二字的项目，
即使代码里有一整套 Skill 类，
报告也只能写「未声明该能力」；
而一个 README 写得漂亮但代码空心的项目，
反而能拿到一堆看似完整的条目。

本模块把「代码怎么说」变成一等证据：
每个信号都带文件路径与行号，
可以逐条打开源码复核。

抽取范围
========

只做**静态符号识别**，不做语义推断：

    class 定义      -> 类名 + 基类
    函数定义        -> 函数名 + 装饰器
    import          -> 模块名
    关键调用        -> StateGraph / .add_node / .add_edge 等

不解析调用图、不推断数据流、不判断代码质量。

诚实性约束
==========

- 只有拿到具体符号与行号才会产出条目，不猜。
- 语法解析失败的文件记入 unparsed，
  由调用方如实展示，而不是静默丢弃。
- 一个文件解析失败不影响其它文件。
"""

import ast
import re


def _symbol_pattern(keyword: str):
    """
    构造「符号名里出现该关键词」的模式。

    坑点：不能直接写 r"[^a-z]" 配 IGNORECASE，
    因为 re.IGNORECASE 会让 [^a-z] 连大写字母
    一起排除，于是 PlannerAgent / BaseToolBase
    这类 camelCase 名字反而匹配不上。

    两侧分别处理：

        左侧 (?:^|[^A-Za-z])  大小写都算字母，
                              不受 IGNORECASE 影响
        右侧 (?:$|(?-i:[^a-z]))  用作用域关掉 IGNORECASE，
                              这样 [^a-z] 才真的是
                              「不是小写字母」，
                              camelCase 边界与 _ / 数字都能命中

    已知局限（刻意宽进，宁可多留证据）：
    Toolkit、Retool、agentic 这类词会被命中。
    在被分析项目的类名里出现频率很低，
    而且误判只是多一条待人工复核的证据，
    不会伪造出不存在的结论。
    """

    return re.compile(
        rf"(?:^|[^A-Za-z]){keyword}"
        rf"|{keyword}(?:$|(?-i:[^a-z]))",
        re.IGNORECASE,
    )


def _parent_directory(file_path: str) -> str:
    """取文件所在目录，用于路径信号去重。"""

    text = str(file_path).replace("\\", "/")

    if "/" not in text:
        return text

    directory = text.rsplit("/", 1)[0]

    return directory + "/" if directory else text


class CodeStructureExtractor:
    """从 Python 源码中抽取六个维度的结构信号。"""

    # 与 ArchitectureAnalysisSkill.STRUCTURE_KEYWORDS
    # 保持同一组维度名，
    # 这样两层结果才能按维度合并。
    DIMENSIONS = (
        "agents",
        "workflow",
        "skills",
        "tools",
        "rag",
        "memory",
    )

    # 单个维度最多产出多少条目 / 证据。
    MAX_ITEMS = 12

    MAX_EVIDENCE = 6

    # 实现明细：单个维度最多记录多少条，
    # 每条最多记多少个被调用函数 / 字面量。
    #
    # 明细比条目重得多（一条约 200-400 字节），
    # 上限要收紧，否则 state_data 会明显膨胀。
    MAX_DETAILS = 6

    MAX_CALLS = 6

    MAX_LITERALS = 5

    # 抽取字面量时要忽略的噪声。
    #
    # 形如 "utf-8" / "GET" / "id" 的字符串
    # 到处都是，对理解实现没有帮助，
    # 反而会把真正有信息量的阈值（0.85）
    # 和状态名（"duplicate_suspected"）挤掉。
    LITERAL_NOISE = frozenset(
        {
            "utf-8",
            "utf8",
            "ascii",
            "get",
            "post",
            "put",
            "delete",
            "patch",
            "head",
            "options",
            "json",
            "text",
            "html",
            "text/plain",
            "text/html",
            "application/json",
            "application/x-www-form-urlencoded",
            "content-type",
            "content_length",
            "authorization",
            "bearer",
            "user-agent",
            "id",
            "pk",
            "name",
            "type",
            "kind",
            "status",
            "state",
            "data",
            "value",
            "key",
            "message",
            "error",
            "detail",
            "none",
            "true",
            "false",
            "null",
            "info",
            "debug",
            "warning",
            "system",
            "user",
            "assistant",
        }
    )

    # 调用链里要忽略的内建 / 通用函数名。
    CALL_NOISE = frozenset(
        {
            "print",
            "len",
            "str",
            "int",
            "float",
            "bool",
            "list",
            "dict",
            "set",
            "tuple",
            "range",
            "enumerate",
            "zip",
            "isinstance",
            "issubclass",
            "getattr",
            "setattr",
            "hasattr",
            "super",
            "format",
            "repr",
            "type",
            "min",
            "max",
            "sum",
            "sorted",
            "any",
            "all",
            "open",
            "__init__",
            "__repr__",
            "__str__",
            "__eq__",
            "__hash__",
        }
    )

    # 只有这些扩展名会被 AST 解析。
    PYTHON_EXTENSIONS = (".py",)

    # --------------------------------------------------------------
    # 识别规则
    # --------------------------------------------------------------

    # 类名命中即算该维度的信号。
    #
    # 覆盖 Agent / BaseAgent / PlannerAgent / BaseTool 等写法。
    CLASS_NAME_PATTERNS = {
        "agents": _symbol_pattern("agent"),
        "skills": _symbol_pattern("skill"),
        "tools": _symbol_pattern("tool"),
        "memory": re.compile(
            r"(memory|checkpoint|saver|session)",
            re.IGNORECASE,
        ),
    }

    # 基类名命中即算该维度的信号。
    #
    # 例如 class FinanceAgent(BaseAgent)、
    # class SearchTool(BaseTool)。
    BASE_NAME_PATTERNS = CLASS_NAME_PATTERNS

    # 文件路径命中即算该维度的信号。
    PATH_PATTERNS = {
        "agents": re.compile(
            r"(^|[/_\-.])agents?([/_\-.]|$)",
        ),
        "workflow": re.compile(
            r"(workflow|graph|pipeline|nodes?|state)",
        ),
        "skills": re.compile(
            r"(^|[/_\-.])skills?([/_\-.]|$)",
        ),
        "tools": re.compile(
            r"(^|[/_\-.])tools?([/_\-.]|$)",
        ),
        "rag": re.compile(
            r"(rag|retriev|embedding|vector)",
        ),
        "memory": re.compile(
            r"(memory|checkpoint|session)",
        ),
    }

    # 导入模块名命中即算该维度的信号。
    #
    # agents 刻意不收 langgraph / langchain：
    # 这两个是编排框架，
    # `import langgraph.graph` 说明的是
    # 「用了图编排」，不是「实现了 Agent」。
    # 早期把 langgraph 同时算进 agents，
    # 导致任何用了 LangGraph 的项目
    # 都会凭空多出一批 agents 条目。
    IMPORT_PATTERNS = {
        "rag": re.compile(
            r"(qdrant|chromadb|chroma|faiss|"
            r"pgvector|sentence_transformers|"
            r"vectorstores|embeddings|milvus|weaviate)",
        ),
        "memory": re.compile(
            r"(checkpoint|memory|redis|saver)",
        ),
        "workflow": re.compile(
            r"(langgraph|langchain|prefect|airflow|"
            r"temporal|celery)",
        ),
        # 真正的多 Agent 框架。
        "agents": re.compile(
            r"(autogen|crewai|semantic_kernel|"
            r"langchain\.agents|langgraph\.prebuilt|"
            r"create_react_agent|swarm)",
        ),
    }

    # 类名 / 函数名命中即算 rag 信号。
    #
    # 只收「明确指向检索」的词，
    # 不收 search 这种过于宽泛的词
    # （一个 search_github_repo 不是 RAG）。
    #
    # rag 这三个字母必须带词边界：
    # 直接做子串匹配会命中 storage ——
    # 真实事故：src/app/core/config.py 里的
    # validate_storage_root 被判成了 RAG 实现。
    RAG_SYMBOL_PATTERN = re.compile(
        r"(?:retriev|embed|rerank|similarity_search"
        r"|vector_store|vectorstore)"
        r"|(?:(?:^|[^A-Za-z])rag"
        r"|rag(?:$|(?-i:[^a-z])))",
        re.IGNORECASE,
    )

    # Agent / Workflow 常见角色名。
    ROLE_PATTERN = re.compile(
        r"(planner|executor|critic|synthesizer|"
        r"researcher|supervisor|orchestrator|"
        r"coordinator|router)",
        re.IGNORECASE,
    )

    # 这些属性的调用参数会被原样记录（图谱节点与边）。
    GRAPH_CALL_ATTRIBUTES = (
        "add_node",
        "add_edge",
        "add_conditional_edges",
        "set_entry_point",
        "set_finish_point",
    )

    # 图谱构造函数名。
    GRAPH_CONSTRUCTORS = (
        "StateGraph",
        "MessageGraph",
    )

    # 工具装饰器名。
    TOOL_DECORATORS = (
        "tool",
        "mcp.tool",
    )

    # --------------------------------------------------------------
    # 入口
    # --------------------------------------------------------------

    @classmethod
    def extract(
        cls,
        files: list,
        extra_paths=None,
        max_details=None,
        include_source=False,
    ) -> dict:
        """
        从若干源文件抽取结构信号。

        files:
            [
                {"file_path": "src/app/graph.py",
                 "content": "<源码全文>"},
                ...
            ]

        只接受**未截断**的源码：
        截断过的 Python 几乎必然语法错误。

        max_details:
            单个维度最多记录多少条实现明细。
            默认用 MAX_DETAILS；
            深挖模式会传一个更大的值。

        include_source:
            明细里是否附上源码片段。

            默认 False —— 默认报告只展示「要点 + 证据锚点」，
            明细里的源码片段根本不会被渲染，
            但每条约 1.5KB，六维 × 六条能凭空撑大
            checkpoint 的 state_data。
            深挖模式（ModuleDeepDiveSkill）传 True，
            因为它要展示源码。

        extra_paths:
            只有路径、没有内容的文件
            （通常是仓库文件树里没被读取的部分）。
            它们只参与路径信号，
            这样「存在 src/agents/ 目录」这条证据
            不会因为该目录下的文件没被读到而丢失。

        返回：

            {
                "available": True,
                "dimensions": {
                    "agents": {"items": [...],
                               "evidence": [...]},
                    ...
                },
                "unparsed": [
                    {"file_path": ..., "error": ...}
                ],
                "parsed_files": 3,
            }
        """

        dimensions = {
            name: {
                "items": [],
                "evidence": [],
                # 实现明细：比 items 重，
                # 但能说清「这个模块具体怎么做的」。
                "details": [],
            }
            for name in cls.DIMENSIONS
        }

        unparsed = []

        parsed_files = 0

        # 每条证据的 text 在全局去重，
        # 避免同一个类在多个文件里
        # 把同一个条目刷满。
        seen_items = {
            name: set() for name in cls.DIMENSIONS
        }

        if not isinstance(files, list):
            files = []

        for item in files:

            if not isinstance(item, dict):
                continue

            file_path = item.get("file_path")

            content = item.get("content")

            if not file_path or not isinstance(
                content,
                str,
            ):
                continue

            if not cls._is_python(file_path):
                continue

            try:

                tree = ast.parse(content)

            except (SyntaxError, ValueError) as error:

                unparsed.append(
                    {
                        "file_path": file_path,
                        "error": (
                            f"{type(error).__name__}: "
                            f"{error}"
                        ),
                    }
                )

                continue

            parsed_files += 1

            cls._scan_module(
                tree,
                file_path,
                dimensions,
                seen_items,
            )

            cls._collect_details(
                tree,
                file_path,
                dimensions,
                content,
                max_details,
                include_source,
            )

        # 路径信号在所有符号扫描完之后再收集。
        #
        # 顺序很重要：_add 是按顺序填满
        # MAX_ITEMS 就停止的，
        # 符号（class / 调用）比「路径长这样」
        # 有价值得多，不能让它被路径挤掉。
        path_candidates = []

        for item in files:

            if not isinstance(item, dict):
                continue

            file_path = item.get("file_path")

            if file_path:
                path_candidates.append(file_path)

        if isinstance(extra_paths, list):
            path_candidates += [
                path
                for path in extra_paths
                if isinstance(path, str)
            ]

        for file_path in path_candidates:

            cls._collect_path_signal(
                file_path,
                dimensions,
                seen_items,
            )

        return {
            "available": parsed_files > 0,
            "dimensions": dimensions,
            "unparsed": unparsed,
            "parsed_files": parsed_files,
        }

    # --------------------------------------------------------------
    # 单文件扫描
    # --------------------------------------------------------------

    @classmethod
    def _scan_module(
        cls,
        tree,
        file_path: str,
        dimensions: dict,
        seen_items: dict,
    ) -> None:
        """扫描一个已解析的模块。"""

        for node in ast.walk(tree):

            if isinstance(
                node,
                (ast.Import, ast.ImportFrom),
            ):
                cls._collect_import(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

            elif isinstance(
                node,
                ast.ClassDef,
            ):
                cls._collect_class(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

            elif isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                cls._collect_function(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

            elif isinstance(node, ast.Call):
                cls._collect_call(
                    node,
                    file_path,
                    dimensions,
                    seen_items,
                )

    @classmethod
    def _collect_import(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """import 语句 -> 维度信号。"""

        if isinstance(node, ast.Import):

            modules = [
                alias.name
                for alias in node.names
            ]

        else:

            module = node.module or ""

            modules = [module] if module else []

            # from x import y 时，y 也可能是
            # 有信号的名字（例如 SqliteSaver）。
            modules += [
                alias.name
                for alias in node.names
            ]

        for module in modules:

            if not module:
                continue

            for dimension, pattern in (
                cls.IMPORT_PATTERNS.items()
            ):

                if not pattern.search(module):
                    continue

                cls._add(
                    dimension,
                    f"import {module}",
                    file_path,
                    node.lineno,
                    dimensions,
                    seen_items,
                )

    @classmethod
    def _collect_class(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """class 定义 -> 维度信号。"""

        bases = []

        for base in node.bases:

            text = cls._unparse(base)

            if text:
                bases.append(text)

        label = f"class {node.name}"

        if bases:
            label += f"({', '.join(bases)})"

        matched = set()

        for dimension, pattern in (
            cls.CLASS_NAME_PATTERNS.items()
        ):

            if pattern.search(node.name):
                matched.add(dimension)

            if any(
                pattern.search(base)
                for base in bases
            ):
                matched.add(dimension)

        if cls.ROLE_PATTERN.search(node.name):
            matched.add("agents")

        # tools 维度额外接受
        # 「在 tool 装饰器下的类」
        # 与名字里带 tool 的类，
        # 前一条已覆盖。
        for dimension in matched:

            cls._add(
                dimension,
                label,
                file_path,
                node.lineno,
                dimensions,
                seen_items,
            )

    @classmethod
    def _collect_function(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """函数定义 -> 维度信号。"""

        decorators = []

        for decorator in node.decorator_list:

            text = cls._unparse(decorator)

            if text:
                decorators.append(text)

        label = f"def {node.name}"

        if decorators:
            label = (
                f"@{', @'.join(decorators)} "
                f"{label}"
            )

        matched = set()

        # langchain 风格的工具声明。
        if any(
            cls._is_tool_decorator(decorator)
            for decorator in decorators
        ):
            matched.add("tools")

        if cls.RAG_SYMBOL_PATTERN.search(node.name):
            matched.add("rag")

        if cls.ROLE_PATTERN.search(node.name):
            matched.add("agents")

        for dimension in matched:

            cls._add(
                dimension,
                label,
                file_path,
                node.lineno,
                dimensions,
                seen_items,
            )

    @classmethod
    def _collect_call(
        cls,
        node,
        file_path,
        dimensions,
        seen_items,
    ) -> None:
        """
        关键调用 -> 维度信号。

        Workflow 维度最有价值的部分在这里：
        StateGraph 的节点名与边
        会以源码原文的形式被记录下来。
        """

        func = node.func

        # StateGraph(...) —— 图谱构造。
        if (
            isinstance(func, ast.Name)
            and func.id in cls.GRAPH_CONSTRUCTORS
        ):

            cls._add(
                "workflow",
                f"{func.id}(...)",
                file_path,
                node.lineno,
                dimensions,
                seen_items,
            )

            return

        if not isinstance(func, ast.Attribute):
            return

        if func.attr not in cls.GRAPH_CALL_ATTRIBUTES:
            return

        target = cls._unparse(func.value)

        arguments = []

        for argument in node.args:

            text = cls._unparse(argument)

            if text:
                arguments.append(text)

        label = (
            f"{target}.{func.attr}"
            f"({', '.join(arguments)})"
        )

        cls._add(
            "workflow",
            label,
            file_path,
            node.lineno,
            dimensions,
            seen_items,
        )

    # --------------------------------------------------------------
    # 实现明细
    # --------------------------------------------------------------

    @classmethod
    def _collect_details(
        cls,
        tree,
        file_path: str,
        dimensions: dict,
        content: str | None = None,
        max_details: int | None = None,
        include_source: bool = False,
    ) -> None:
        """
        收集「这个模块具体怎么做的」。

        与 _scan_module 的区别：

            _scan_module  抽符号名字，供比较与检索
            _collect_details  抽函数签名 / 调用链 /
                              关键字面量 / 类的方法表，
                              供报告展示实现细节

        最有价值的是 workflow：
        add_node('duplicate_check',
                 self._node_duplicate_check)
        会被解析成那个函数本身，
        于是报告能写出「这个节点做了什么」，
        而不只是「有这么个节点」。
        """

        symbols = cls._build_symbol_table(tree)

        for node in ast.walk(tree):

            if isinstance(node, ast.Call):

                cls._detail_from_graph_call(
                    node,
                    symbols,
                    file_path,
                    dimensions,
                    content,
                    max_details,
                    include_source,
                )

        # 类：给出基类与方法表。
        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                cls._detail_from_class(
                    node,
                    file_path,
                    dimensions,
                    content,
                    max_details,
                    include_source,
                )

        # 函数：给出签名、调用链与字面量。
        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):

                cls._detail_from_function(
                    node,
                    file_path,
                    dimensions,
                    content,
                    max_details,
                    include_source,
                )

    @classmethod
    def _detail_from_graph_call(
        cls,
        node,
        symbols,
        file_path,
        dimensions,
        content=None,
        max_details=None,
        include_source=False,
    ) -> None:
        """
        把 add_node / add_edge 解析成工作流节点明细。
        """

        function = node.func

        if not isinstance(function, ast.Attribute):
            return

        # 只为「带处理函数」的调用产出明细。
        #
        # add_edge 的拓扑已经作为条目记录，
        # 再产一条什么都解析不出来的明细
        # 只会挤占 MAX_DETAILS 配额。
        if function.attr not in (
            "add_node",
            "add_conditional_edges",
        ):
            return

        if not node.args:
            return

        first = cls._unparse(node.args[0])

        target = cls._unparse(function.value)

        entry = {
            "kind": "graph",
            "name": first.strip("'\"") or first,
            "file_path": file_path,
            "line": node.lineno,
            "signature": (
                f"{target}.{function.attr}"
                f"({', '.join(cls._unparse(a) for a in node.args)})"
            ),
            "calls": [],
            "literals": [],
        }

        # add_node 的第二个实参是处理函数，
        # 解析它能拿到真正的实现。
        if (
            function.attr == "add_node"
            and len(node.args) >= 2
        ):

            symbol_name = cls._called_symbol(
                node.args[1]
            )

            if symbol_name:

                definition = symbols.get(
                    symbol_name
                )

                if definition is not None:

                    entry["symbol"] = symbol_name

                    entry["signature"] = (
                        cls._signature(definition)
                    )

                    entry["calls"] = cls._calls_in(
                        definition
                    )

                    entry["literals"] = (
                        cls._literals_in(definition)
                    )

                    if include_source:

                        entry["source"] = (
                            cls._source_segment(
                                content,
                                definition,
                            )
                        )

        cls._add_detail(
            "workflow",
            entry,
            dimensions,
            max_details,
        )

    @classmethod
    def _detail_from_class(
        cls,
        node,
        file_path,
        dimensions,
        content=None,
        max_details=None,
        include_source=False,
    ) -> None:
        """类明细：基类 + 方法表。"""

        bases = [
            rendered
            for rendered in (
                cls._unparse(base)
                for base in node.bases
            )
            if rendered
        ]

        label = f"class {node.name}"

        if bases:
            label += f"({', '.join(bases)})"

        methods = [
            child.name
            for child in node.body
            if isinstance(
                child,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            )
        ]

        entry = {
            "kind": "class",
            "name": node.name,
            "file_path": file_path,
            "line": node.lineno,
            "signature": label,
            "calls": [],
            "literals": [],
        }

        if methods:

            entry["methods"] = methods[
                : cls.MAX_CALLS
            ]

        if include_source:

            entry["source"] = cls._source_segment(
                content,
                node,
            )

        for dimension, pattern in (
            cls.CLASS_NAME_PATTERNS.items()
        ):

            matched = pattern.search(node.name) or any(
                pattern.search(base)
                for base in bases
            )

            if matched:

                cls._add_detail(
                    dimension,
                    entry,
                    dimensions,
                    max_details,
                )

        if cls.ROLE_PATTERN.search(node.name):

            cls._add_detail(
                "agents",
                entry,
                dimensions,
                max_details,
            )

    @classmethod
    def _detail_from_function(
        cls,
        node,
        file_path,
        dimensions,
        content=None,
        max_details=None,
        include_source=False,
    ) -> None:
        """函数明细：签名 + 调用链 + 字面量。"""

        decorators = [
            rendered
            for rendered in (
                cls._unparse(decorator)
                for decorator in node.decorator_list
            )
            if rendered
        ]

        entry = {
            "kind": "function",
            "name": node.name,
            "file_path": file_path,
            "line": node.lineno,
            "signature": cls._signature(node),
            "calls": cls._calls_in(node),
            "literals": cls._literals_in(node),
        }

        if include_source:

            entry["source"] = cls._source_segment(
                content,
                node,
            )

        if any(
            cls._is_tool_decorator(decorator)
            for decorator in decorators
        ):

            cls._add_detail(
                "tools",
                entry,
                dimensions,
                max_details,
            )

        if cls.RAG_SYMBOL_PATTERN.search(node.name):

            cls._add_detail(
                "rag",
                entry,
                dimensions,
                max_details,
            )

        if cls.ROLE_PATTERN.search(node.name):

            cls._add_detail(
                "agents",
                entry,
                dimensions,
                max_details,
            )

    @staticmethod
    def _add_detail(
        dimension,
        entry,
        dimensions,
        max_details=None,
    ) -> None:
        """登记一条明细（按 名称+位置 去重）。"""

        bucket = dimensions.get(dimension)

        if bucket is None:
            return

        limit = (
            max_details
            if isinstance(max_details, int)
            else CodeStructureExtractor.MAX_DETAILS
        )

        if len(bucket["details"]) >= limit:
            return

        key = (
            entry.get("name"),
            entry.get("file_path"),
            entry.get("line"),
        )

        for existing in bucket["details"]:

            if (
                existing.get("name"),
                existing.get("file_path"),
                existing.get("line"),
            ) == key:
                return

        bucket["details"].append(entry)

    # --------------------------------------------------------------
    # 路径信号
    # --------------------------------------------------------------

    @classmethod
    def dimensions_for_path(
        cls,
        file_path: str,
    ) -> list:
        """
        路径命中了哪些维度，按固定顺序返回。

        ArchitectureAnalysisSkill 用它做按维度配额：
        每个维度都有独立的样本名额，
        不会出现「workflow 文件太多、
        rag 文件一个都没读」的情况。
        """

        normalized = str(file_path).lower()

        return [
            dimension
            for dimension in cls.DIMENSIONS
            if cls.PATH_PATTERNS[
                dimension
            ].search(normalized)
        ]

    @classmethod
    def path_signal_count(
        cls,
        file_path: str,
    ) -> int:
        """
        路径命中多少个维度的信号。

        ArchitectureAnalysisSkill 用它决定
        优先读哪些文件：
        命中越多，越可能承载架构。

        与 _collect_path_signal 共用同一套 PATTERNS，
        避免两处规则漂移。
        """

        normalized = str(file_path).lower()

        return sum(
            1
            for pattern in cls.PATH_PATTERNS.values()
            if pattern.search(normalized)
        )

    @classmethod
    def _collect_path_signal(
        cls,
        file_path: str,
        dimensions,
        seen_items,
    ) -> None:
        """
        文件路径本身也是证据。

        「存在 src/agents/ 目录」这件事
        与「某个类叫 FinanceAgent」同样说明问题，
        而且前者在没读到那个文件时也能成立。

        按**目录**去重：
        src/agents/ 下有 30 个文件时，
        只记一条 `路径 src/agents/`，
        而不是把 30 个文件名刷满配额 ——
        否则真正有价值的类名会被挤出去。
        """

        normalized = file_path.lower()

        directory = _parent_directory(file_path)

        for dimension, pattern in (
            cls.PATH_PATTERNS.items()
        ):

            if not pattern.search(normalized):
                continue

            cls._add(
                dimension,
                f"路径 {directory}",
                directory,
                None,
                dimensions,
                seen_items,
            )

    # --------------------------------------------------------------
    # 工具方法
    # --------------------------------------------------------------

    @classmethod
    def _add(
        cls,
        dimension: str,
        text: str,
        file_path: str,
        line,
        dimensions: dict,
        seen_items: dict,
    ) -> None:
        """登记一条条目与对应的证据。"""

        bucket = dimensions.get(dimension)

        if bucket is None:
            return

        seen = seen_items[dimension]

        lowered = text.lower()

        # 同一个符号只记一次。
        if lowered in seen:
            return

        seen.add(lowered)

        if len(bucket["items"]) >= cls.MAX_ITEMS:
            return

        bucket["items"].append(text)

        if len(bucket["evidence"]) >= cls.MAX_EVIDENCE:
            return

        bucket["evidence"].append(
            {
                "file_path": file_path,
                "line_start": line,
                "line_end": line,
                "text": text,
            }
        )

    @classmethod
    def _is_python(
        cls,
        file_path: str,
    ) -> bool:
        """只解析 Python 文件。"""

        return str(file_path).lower().endswith(
            cls.PYTHON_EXTENSIONS
        )

    # 代码摘录的起始处：跳过这些前缀开头的行。
    SKIPPABLE_LINE_PREFIXES = (
        "import ",
        "from ",
    )

    @classmethod
    def meaningful_start(
        cls,
        content,
    ) -> int:
        """
        找出源码里第一行「有信息量」的内容的字符下标。

        为什么需要：代码摘录原本固定从第 1 行开始取，
        而 Python 文件开头必然是 import 块 ——
        截出来就是一堆

            import sqlite3
            import uuid
            from decimal import Decimal

        对理解项目毫无帮助。
        真实反馈：「这源码提取了一堆 import 根本没有用」。

        跳过开头的：

            空行 / 注释行
            模块级 docstring
            import / from 语句（含括号与反斜杠续行）

        返回第一行实际代码的位置。
        整份文件都跳完还没找到代码时返回 0，
        保持「从头取」的旧行为，不至于截出空串。

        必须处理**多行 import**：真实文件里常见

            from app.schemas.agent import (
                AgentRunListItem,
                AgentRunResponse,
            )

        这种写法的续行不以 import 开头，
        只看行首的话扫描器会停在第 2 行，
        摘录依然是一串 import 名单。
        """

        if not isinstance(content, str) or not content:
            return 0

        offset = 0

        in_docstring = False

        delimiter = ""

        # 多行 import 的括号深度与反斜杠续行。
        in_import = False

        import_depth = 0

        for line in content.splitlines(
            keepends=True
        ):

            stripped = line.strip()

            # 多行 import 的续行
            if in_import:

                offset += len(line)

                import_depth += (
                    line.count("(") - line.count(")")
                )

                if (
                    import_depth <= 0
                    and not line.rstrip().endswith("\\")
                ):
                    in_import = False

                continue

            if in_docstring:

                offset += len(line)

                if delimiter in stripped:
                    in_docstring = False

                continue

            # 空行与注释
            if not stripped or stripped.startswith("#"):

                offset += len(line)

                continue

            # 模块级 docstring
            if stripped.startswith(('"""', "'''")):

                delimiter = stripped[:3]

                # 单行写法："""xxx"""
                if stripped.count(delimiter) >= 2:

                    offset += len(line)

                    continue

                in_docstring = True

                offset += len(line)

                continue

            # import 段
            if stripped.startswith(
                cls.SKIPPABLE_LINE_PREFIXES
            ):

                offset += len(line)

                depth = (
                    line.count("(") - line.count(")")
                )

                # 括号未闭合或反斜杠续行时，
                # 后面的行还是这条 import 的一部分。
                if depth > 0 or line.rstrip().endswith(
                    "\\"
                ):

                    in_import = True

                    import_depth = depth

                continue

            # 第一行真正的代码
            break

        if offset >= len(content):
            return 0

        return offset

    @classmethod
    def _is_tool_decorator(
        cls,
        decorator: str,
    ) -> bool:
        """判断装饰器是否为 @tool 一类。"""

        if not decorator:
            return False

        lowered = decorator.lower()

        if lowered in cls.TOOL_DECORATORS:
            return True

        # 兼容 @tool(...) 带参数的形式。
        for name in cls.TOOL_DECORATORS:

            if lowered.startswith(name + "("):
                return True

        return lowered.endswith(".tool")

    # --------------------------------------------------------------
    # 函数体分析
    # --------------------------------------------------------------

    @classmethod
    def _signature(cls, node) -> str:
        """
        还原函数签名（含类型标注）。

        这是「下到函数体」的第一步：
        `def _node_duplicate_check(self, state: AgentState)
         -> AgentState` 远比一个名字有信息量。
        """

        arguments = node.args

        parts = []

        positional = list(arguments.posonlyargs) + list(
            arguments.args
        )

        # 默认值对齐到参数尾部。
        defaults = [None] * (
            len(positional) - len(arguments.defaults)
        ) + list(arguments.defaults)

        for argument, default in zip(
            positional,
            defaults,
        ):

            parts.append(
                cls._argument(argument, default)
            )

        if arguments.vararg:

            parts.append(
                "*" + cls._argument(arguments.vararg)
            )

        elif arguments.kwonlyargs:

            # 有仅关键字参数但没有 *args 时，
            # 需要显式一个 * 占位。
            parts.append("*")

        for argument, default in zip(
            arguments.kwonlyargs,
            arguments.kw_defaults,
        ):

            parts.append(
                cls._argument(argument, default)
            )

        if arguments.kwarg:

            parts.append(
                "**" + cls._argument(arguments.kwarg)
            )

        prefix = (
            "async def"
            if isinstance(node, ast.AsyncFunctionDef)
            else "def"
        )

        signature = (
            f"{prefix} {node.name}"
            f"({', '.join(parts)})"
        )

        returns = getattr(node, "returns", None)

        if returns is not None:

            rendered = cls._unparse(returns)

            if rendered:
                signature += f" -> {rendered}"

        return signature

    @classmethod
    def _argument(
        cls,
        argument,
        default=None,
    ) -> str:
        """渲染单个参数（含标注与默认值）。"""

        text = argument.arg

        annotation = getattr(
            argument,
            "annotation",
            None,
        )

        if annotation is not None:

            rendered = cls._unparse(annotation)

            if rendered:
                text += f": {rendered}"

        if default is not None:

            rendered = cls._unparse(default)

            if rendered:
                text += f" = {rendered}"

        return text

    @classmethod
    def _calls_in(cls, node) -> list:
        """
        函数体里调用了哪些自定义函数。

        只取被调用者的名字（`f()` 取 f，
        `obj.method()` 取 method），
        过滤掉内建函数与通用名，
        去重后保序。
        """

        calls = []

        seen = set()

        for child in ast.walk(node):

            if not isinstance(child, ast.Call):
                continue

            function = child.func

            if isinstance(function, ast.Name):

                name = function.id

            elif isinstance(function, ast.Attribute):

                name = function.attr

            else:

                continue

            lowered = name.lower()

            if lowered in cls.CALL_NOISE:
                continue

            # 单字符与全大写下划线常量不是函数调用。
            if len(name) < 3:
                continue

            if lowered in seen:
                continue

            seen.add(lowered)

            calls.append(name)

            if len(calls) >= cls.MAX_CALLS:
                break

        return calls

    @classmethod
    def _literals_in(cls, node) -> list:
        """
        函数体里出现的、有信息量的字面量。

        典型价值：阈值（0.85）、状态名
        （"duplicate_suspected"）、重试次数（3）。
        """

        literals = []

        seen = set()

        for child in ast.walk(node):

            if not isinstance(child, ast.Constant):
                continue

            value = child.value

            if not cls._is_interesting_literal(
                value
            ):
                continue

            rendered = repr(value)

            if rendered in seen:
                continue

            seen.add(rendered)

            literals.append(rendered)

            if len(literals) >= cls.MAX_LITERALS:
                break

        return literals

    @classmethod
    def _is_interesting_literal(
        cls,
        value,
    ) -> bool:
        """判断一个字面量是否值得记录。"""

        # bool 是 int 的子类，必须排在前面排除。
        if isinstance(value, bool):
            return False

        # 0.0 通常是初始化占位，
        # 真正的阈值（0.85）才值得记。
        if isinstance(value, float):
            return value != 0.0

        if isinstance(value, int):
            return abs(value) >= 10

        if isinstance(value, str):

            text = value.strip()

            if len(text) < 4:
                return False

            if text.lower() in cls.LITERAL_NOISE:
                return False

            if text.startswith(
                ("http://", "https://")
            ):
                return False

            # 纯符号 / 纯数字字符串没有信息量。
            if not any(
                char.isalnum() for char in text
            ):
                return False

            return True

        return False

    @classmethod
    def _build_symbol_table(
        cls,
        tree,
    ) -> dict:
        """
        建立 短名 -> 函数节点 的索引。

        用途：把
            builder.add_node('duplicate_check',
                             self._node_duplicate_check)
        解析到
            def _node_duplicate_check(self, state) -> AgentState

        只看短名（不带类名前缀），
        同名冲突时保留第一个 ——
        解析结果会带上文件与行号，
        人工复核时能看出解析得对不对。
        """

        table = {}

        for node in ast.walk(tree):

            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):

                table.setdefault(node.name, node)

        return table

    @staticmethod
    def _called_symbol(node):
        """
        从 add_node / add_edge 的实参里
        取出「被引用的函数名」。

        支持两种写法：

            self._node_duplicate_check   -> _node_duplicate_check
            _node_duplicate_check        -> _node_duplicate_check
        """

        if isinstance(node, ast.Attribute):

            return node.attr

        if isinstance(node, ast.Name):

            return node.id

        return None

    # 明细里附带的源码片段最多多少字符。
    #
    # 深挖报告要展示「这段代码长什么样」，
    # 因此明细可以带源码；
    # 但一个函数可能有几千字符，
    # 不设上限会让深挖产物失控。
    MAX_DETAIL_SOURCE_CHARS = 1500

    @classmethod
    def _source_segment(
        cls,
        content,
        node,
    ) -> str:
        """
        取出某个 AST 节点对应的源码原文。

        这是深挖报告与默认报告最大的差别：
        默认报告给签名，深挖给源码。
        """

        if not isinstance(content, str) or node is None:
            return ""

        try:

            segment = ast.get_source_segment(
                content,
                node,
            )

        except Exception:

            return ""

        if not segment:
            return ""

        segment = segment.strip()

        if len(segment) > cls.MAX_DETAIL_SOURCE_CHARS:

            segment = (
                segment[
                    : cls.MAX_DETAIL_SOURCE_CHARS
                ]
                + "\n# ...（已截断）"
            )

        return segment

    @staticmethod
    def _unparse(node) -> str:
        """
        把 AST 节点还原成源码文本。

        还原失败返回空串
        （个别节点在低版本 Python 上
         unparse 会抛异常）。
        """

        try:

            return ast.unparse(node).strip()

        except Exception:

            return ""
