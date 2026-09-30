"""
Architecture Analysis Skill。

负责：

    GitHub Code Search
        ↓
    File Reader
        ↓
    Architecture information

Phase 12 → Phase 13 数据契约补充
================================

除了 files / modules，
本 Skill 还会产出 project_structure：
从「被分析项目」的 README 与 GitHub topics 中
确定性抽取该项目自述的：

    agents / workflow / skills / tools
    rag / memory / extension

抽取规则：

- 纯字符串匹配 + README 行号定位
- 不使用 LLM，不做语义推断
- 每条结果都带 README 行号与原文片段，
  可以逐条人工复核
- 没匹配到就 declared=False 并给出原因，
  不编造数据

这样 Phase 13 的比较多的是
「被分析项目自述的结构」，
而不是 AIPI 自己的执行状态。
"""

import os
import re

from app.core.exceptions import ToolError
from app.project_analysis.analysis_focus import (
    AnalysisFocus,
)
from app.project_analysis.code_structure_extractor import (
    CodeStructureExtractor,
)
from app.skills.base import BaseSkill


class ArchitectureAnalysisSkill(
    BaseSkill
):
    """
    分析 Repository 架构。
    """

    name = "architecture_analysis"

    description = (
        "Analyze repository architecture"
    )

    # 项目自述结构的关键词表。
    #
    # 命中行会被原样记录（含行号），
    # 因此宁可多留证据，也不做二次推断。
    STRUCTURE_KEYWORDS = {
        "agents": (
            "agent",
            "planner",
            "executor",
            "critic",
            "synthesizer",
            "researcher",
            "supervisor",
            "orchestrator",
            "coordinator",
            "router",
        ),
        "workflow": (
            "workflow",
            "stategraph",
            "state graph",
            "state machine",
            "pipeline",
            "langgraph",
            "langchain",
            "interrupt",
            "graph",
        ),
        "skills": (
            "skill",
            "capability",
            "abilities",
        ),
        "tools": (
            "tool call",
            "tool calls",
            "tools",
            "function call",
        ),
        "rag": (
            "rag",
            "retrieval",
            "retrieve",
            "embedding",
            "pgvector",
            "vector",
            "corpus",
            "semantic search",
        ),
        "memory": (
            "memory",
            "checkpoint",
            "persist",
            "session state",
        ),
        "extension": (
            "plugin",
            "extension",
            "pluggable",
            "extensible",
            "mcp",
            "adapter",
        ),
    }

    # 从一个命中行里抽取「标识」：
    # README 中的 `反引号` 与 **粗体** 内容。
    _IDENTIFIER_PATTERN = re.compile(
        r"`([^`\n]+)`"
        r"|\*\*([^*\n]+)\*\*"
    )

    # 只有单个 token 的标识才作为 item，
    # 避免把 **fails closed** 这类短语
    # 当成结构化条目。
    _SINGLE_TOKEN_PATTERN = re.compile(
        r"[A-Za-z][A-Za-z0-9_.\-*]{1,39}"
    )

    # README 列表行的前缀。
    #
    # 列表行常被用来罗列能力，
    # 而且多数写成普通文字（不加粗、不加反引号），
    # 例如：
    #
    #     - supplier lookup, duplicate detection, categorization
    #
    # 仅靠粗体 / 反引号抽不到这类内容，
    # 因此列表行的逗号分段也作为条目。
    _BULLET_PATTERN = re.compile(
        r"^\s*[-*]\s+(.*)$"
    )

    # 列表分段作为条目的最大长度。
    #
    # 超过这个长度的多半是整句话，
    # 不适合当条目。
    MAX_BULLET_ITEM_CHARS = 60

    # 每个维度最多记录的命中行数。
    MAX_EVIDENCE_LINES = 4

    # 每个维度最多记录的标识数。
    MAX_ITEMS = 12

    # 代码证据与 README 自述合并后，
    # 单个维度最多保留多少个条目。
    #
    # 略大于 MAX_ITEMS：
    # 代码符号排在前面且通常先用满 12 个，
    # 这里留出余量，让 README 补充的条目
    # 不至于被全部挤掉。
    MAX_MERGED_ITEMS = 16

    # 允许接纳「未命中关键词的代码标识」的维度。
    #
    # 工具名通常以函数 / API 形式出现
    # （例如 read_webpage），
    # 无法预先写进关键词表，
    # 因此只有 tools 维度接受这类标识。
    #
    # 其余维度只接受命中本维度关键词的标识，
    # 避免 StateGraph / MODEL_* 这类
    # 其他维度的标识被重复计入。
    DIMENSIONS_ACCEPTING_CODE_IDENTIFIERS = (
        "tools",
    )

    # 目录结构：按扩展名 / 顶层目录统计的展示上限。
    MAX_EXTENSIONS = 12

    MAX_TOP_LEVEL_DIRS = 15

    MAX_KEY_FILES = 20

    # 关键文件：这些文件最能说明项目如何构建与部署。
    KEY_FILE_NAMES = (
        "README.md",
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "package.json",
        "tsconfig.json",
        "go.mod",
        "pom.xml",
        "Cargo.toml",
        "Gemfile",
        "Makefile",
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".env.example",
    )

    # 允许读取内容的文件类型（不含 .md，
    # README 已由 RepositoryAnalysisSkill 读取）。
    #
    # 刻意不含 .toml / .ini / .cfg / .yml / .json：
    # 这些是配置文件，由 TechnologyAnalysisSkill
    # 负责读取并抽取技术栈。
    # 本 Skill 的「关键源码」只用来抽取
    # Agent / Workflow / Tool 等代码结构，
    # 再读一遍配置文件纯属浪费配额
    # （旧版本 8 个配额里有 3-4 个是
    #   docker-compose.yml / pyproject.toml 这类文件，
    #   导致真正承载架构的 graph / nodes / tools
    #   一个都没读到）。
    SOURCE_EXTENSIONS = (
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".mjs",
        ".go",
        ".java",
        ".rs",
        ".rb",
        ".php",
        ".cs",
        ".kt",
        ".swift",
        ".vue",
    )

    # 读取源码时优先挑选的入口文件。
    #
    # 刻意不包含 __init__.py：
    # 它通常只是空的包声明，
    # 而且会命中很深的目录。
    PRIORITY_FILENAMES = (
        "main.py",
        "app.py",
        "server.py",
        "manage.py",
        "cli.py",
        "index.ts",
        "index.js",
        "main.ts",
        "main.js",
        "app.ts",
        "app.js",
    )

    # 这些路径最后才考虑。
    #
    # 它们能命中架构关键词（tests/test_agents.py
    # 名字里有 agent），但描述的是「项目怎么测自己」，
    # 不是「项目怎么组织 Agent」，
    # 放在最后避免挤掉真正的实现代码。
    LOW_PRIORITY_PATH_PATTERNS = (
        re.compile(r"(^|/)tests?/"),
        re.compile(r"(^|/)test_[^/]*$"),
        re.compile(r"_test\.[a-z]+$"),
        re.compile(r"(^|/)migrations?/"),
        re.compile(r"(^|/)alembic/versions/"),
        re.compile(r"(^|/)(demo_data|examples?|samples?)/"),
        re.compile(r"(^|/)scripts?/"),
    )

    # 最多读取多少个文件内容作为「关键源码」。
    #
    # 文件树可能有数百个文件，
    # 不限制会对 GitHub 发起数百次请求。
    #
    # 8 -> 12：不再把配额花在
    # docker-compose.yml 这类配置文件上。
    # 12 -> 20：改为按维度分配配额，
    # 每个维度都要留够样本。
    MAX_MODULES = 20

    # 每个维度的样本配额。
    #
    # 旧做法是全局挑 20 个「路径命中最多信号」的文件，
    # 结果取决于仓库目录结构：
    # agents/ 下文件多就全是 agents，
    # rag/ 只有 1 个文件就可能一个都进不来，
    # 于是报告里每个模块的详略极不均匀。
    #
    # 现在每个维度有独立名额，
    # 命中该维度的文件先按自己的配额挑，
    # 一个维度内部的明细深浅不再由别的维度决定。
    DIMENSION_QUOTAS = {
        "workflow": 4,
        "agents": 3,
        "tools": 3,
        "rag": 2,
        "memory": 2,
        "skills": 2,
    }

    # 重点维度与非重点维度的配额权重。
    #
    # 用户点名了重点时，配额按权重重新分配，
    # 而不是把非重点维度降到 0 ——
    # 报告里那些章节仍然要写，
    # 只是给更少的样本。
    #
    # 以 MAX_MODULES=20 为例：
    #
    #     1 个重点  重点 10，其余各 2   -> 20
    #     2 个重点  重点各 7，其余各 1   -> 18
    #     3 个重点  重点各 5，其余各 1   -> 18
    FOCUS_WEIGHT = 5

    BASE_WEIGHT = 1

    @classmethod
    def _quotas_for(
        cls,
        focus=None,
    ):
        """
        按本次重点算出各维度的采集配额。

        返回的是**有序**字典：
        重点维度排在前面，
        这样 _read_candidates 会先把它们的
        名额用满，不会被其它维度挤掉。

        没有识别出重点时返回默认配额，
        与旧行为完全一致。
        """

        if focus is None or not focus.is_focused:

            return dict(cls.DIMENSION_QUOTAS)

        weights = {}

        for name in cls.DIMENSION_QUOTAS:

            weights[name] = (
                cls.FOCUS_WEIGHT
                if focus.is_primary(name)
                else cls.BASE_WEIGHT
            )

        total = sum(weights.values())

        quotas = {}

        # 重点维度在前，且内部按用户在问题里
        # 提到的顺序排 —— 越靠前越重要。
        ordered = sorted(
            cls.DIMENSION_QUOTAS,
            key=lambda name: (
                0 if focus.is_primary(name) else 1,
                focus.rank(name),
                name,
            ),
        )

        for name in ordered:

            quotas[name] = max(
                1,
                cls.MAX_MODULES
                * weights[name]
                // total,
            )

        return quotas

    # 落库时最多保留多少个**源码正文**。
    #
    # 与 MAX_MODULES 分开是刻意的：
    #
    #   MAX_MODULES       读几个文件喂给 AST
    #   MAX_STORED_MODULES 存几个文件的正文进 state
    #
    # AST 抽取在内存里用全文，不受这个上限影响；
    # 但 modules 正文要写进 checkpoint，
    # 20 个文件 × 1200 字符 ≈ 24KB，
    # 而报告第 11 章只渲染 8 个 ——
    # 存 20 个有 12 个永远没人看。
    #
    # 真实事故：state_data 涨到 263KB，
    # 越过 asyncmy 单字段 256KB 的缓冲区分片上限，
    # 报告接口读 checkpoint 直接
    # Lost connection to MySQL server。
    MAX_STORED_MODULES = 8

    # 落库时最多保留多少个文件路径。
    #
    # 真实文件树可能有数百个文件，
    # 全部写入 checkpoint 会让
    # state_data 膨胀到数百 KB，
    # 进而撑爆 MySQL 的排序缓冲区
    # （OperationalError 1038 Out of sort memory）。
    # 真实总数见 directory_structure.total_files。
    MAX_FILE_PATHS = 60

    # 单个源码文件最多写入多少字符。
    #
    # 大型配置文件的全文（例如 28KB 的 CI 配置）
    # 同样会让 state_data 膨胀。
    MAX_MODULE_CHARS = 1200

    async def execute(
        self,
        context,
        input_data,
    ):
        code_search = context.tools.get(
            "github_code_search"
        )

        if code_search is None:
            raise RuntimeError(
                "Tool not found: github_code_search"
            )

        file_reader = context.tools.get(
            "file_reader"
        )

        if file_reader is None:
            raise RuntimeError(
                "Tool not found: file_reader"
            )

        owner = input_data.get(
            "owner"
        )

        repo = input_data.get(
            "repo"
        )

        if not owner or not repo:
            raise ValueError(
                "Architecture analysis requires "
                "'owner' and 'repo'."
            )

        repository = (
            f"{owner}/{repo}"
        )

        keyword = input_data.get(
            "keyword",
            "class",
        )

        branch = input_data.get(
            "branch",
            "main",
        )

        files = await code_search.execute(
            keyword=keyword,
            repo=repository,
        )

        # GitHub Code Search 的 repo: 限定符
        # 对多数仓库返回 0 条结果，
        # 因此真实的目录结构必须来自 Git Trees API。
        tree = await self._load_tree(
            context,
            owner,
            repo,
            branch,
        )

        if not files and tree:

            # Code Search 没有结果时，
            # 用真实文件树补全文件列表。
            files = [
                item.get("path")
                for item in tree
                if item.get("type") == "blob"
                and item.get("path")
            ]

        architecture = {
            # 只保留采样，真实总数见 directory_structure。
            "files": list(files)[: self.MAX_FILE_PATHS],
            "modules": [],
            "directory_structure": (
                self._build_directory_structure(
                    tree
                )
            ),
        }

        # AST 抽取需要**未截断**的源码：
        # 截断过的 Python 几乎必然语法错误，
        # 因此这里单独收一份全文，
        # 只在本次执行内使用，不写入 state
        # （modules 里存的仍是截断后的内容）。
        ast_sources = []

        # 本次分析的重点维度。
        #
        # research_plan 由 DesignGateNode 提升到顶层，
        # PlanExecutorNode 又把 state.data 整体
        # 作为 agent_input 传进来，因此这里能读到。
        focus = AnalysisFocus.from_plan(
            input_data.get("research_plan")
        )

        for file_path in self._read_candidates(
            files,
            self._quotas_for(focus),
        ):

            try:

                content = await file_reader.execute(
                    owner=owner,
                    name=repo,
                    file_path=file_path,
                    branch=branch,
                )

            except ToolError as error:

                # 单个文件读取失败（超时 / 网络抖动）
                # 不应该让整个分析失败：
                # 记录失败原因后继续读其它文件。
                architecture[
                    "modules"
                ].append(
                    {
                        "file_path": file_path,
                        "content": "",
                        "error": str(error)
                        or type(error).__name__,
                    }
                )

                continue

            # 只存够报告展示的量。
            # 全文已经喂给 AST 了，
            # 多存的正文没有任何读取方。
            if len(
                architecture["modules"]
            ) < self.MAX_STORED_MODULES:

                architecture[
                    "modules"
                ].append(
                    self._module_entry(
                        file_path,
                        content,
                    )
                )

            ast_sources.append(
                {
                    "file_path": file_path,
                    "content": content or "",
                }
            )

        # 从真实源码抽取结构信号。
        #
        # 除已读取的文件外，
        # 额外把整棵文件树的路径交给抽取器：
        # 配额只有 12 个，
        # 但「存在 src/agents/ 目录」这条证据
        # 不该因为该目录下的文件没被读到而丢失。
        code_structure = (
            CodeStructureExtractor.extract(
                ast_sources,
                extra_paths=[
                    path
                    for path in files
                    if isinstance(path, str)
                ],
            )
        )

        # Phase 12 → Phase 13 契约：
        # 产出被分析项目的自述结构。
        #
        # 现在由「代码证据」与「README 自述」共同构成，
        # 代码为主、README 为辅。
        architecture[
            "project_structure"
        ] = self._extract_project_structure(
            input_data,
            code_structure,
        )

        return architecture

    def _module_entry(
        self,
        file_path,
        content,
    ):
        """
        构建单个源码条目。

        两个处理：

        1. 跳过开头的 import 段
           否则摘录就是一堆 `import os`，
           对理解项目毫无帮助。
        2. 按 MAX_MODULE_CHARS 截断，
           避免大型文件把 state_data 撑爆。
        """

        text = str(content or "")

        start = CodeStructureExtractor.meaningful_start(
            text
        )

        excerpt = text[
            start: start + self.MAX_MODULE_CHARS
        ]

        entry = {
            "file_path": file_path,
            "content": excerpt,
        }

        # 摘录从第几行开始 ——
        # 证据层要用它标行号，
        # 否则会写成「file:1-30」但内容是第 30 行开始的。
        if start:

            entry["start_line"] = (
                text[:start].count("\n") + 1
            )

        if len(text) - start > self.MAX_MODULE_CHARS:
            entry["original_characters"] = len(text)
            entry["truncated"] = True

        return entry

    @staticmethod
    async def _load_tree(
        context,
        owner,
        name,
        branch,
    ):
        """
        获取仓库文件树。

        目录结构属于增强信息，
        拿不到时返回空列表，
        不应因此中断整个分析流程。
        """

        tool = context.tools.get(
            "github_repository"
        )

        if tool is None:
            return []

        get_tree = getattr(
            tool,
            "get_tree",
            None,
        )

        if not callable(get_tree):
            return []

        try:

            tree = await get_tree(
                owner=owner,
                name=name,
                branch=branch,
            )

        except ToolError:

            return []

        if not isinstance(tree, list):
            return []

        return tree

    def _build_directory_structure(
        self,
        tree,
    ):
        """
        从真实文件树构建目录结构。

        只做计数与归类，不做推断。
        """

        blobs = [
            item
            for item in tree
            if isinstance(item, dict)
            and item.get("type") == "blob"
            and item.get("path")
        ]

        if not blobs:

            return {
                "available": False,
                "reason": (
                    "未获取到仓库文件树，"
                    "无法生成目录结构。"
                ),
                "total_files": 0,
                "by_extension": {},
                "top_level_dirs": [],
                "key_files": [],
            }

        by_extension = {}
        top_level = {}
        key_files = []

        for blob in blobs:

            path = blob["path"]

            extension = (
                os.path.splitext(path)[1].lower()
                or "(无扩展名)"
            )

            by_extension[extension] = (
                by_extension.get(extension, 0) + 1
            )

            head = (
                path.split("/", 1)[0]
                if "/" in path
                else "(根目录)"
            )

            top_level[head] = (
                top_level.get(head, 0) + 1
            )

            if os.path.basename(path) in self.KEY_FILE_NAMES:
                key_files.append(path)

        return {
            "available": True,
            "source": "github git trees api",
            "total_files": len(blobs),
            "by_extension": dict(
                sorted(
                    by_extension.items(),
                    key=lambda item: -item[1],
                )[: self.MAX_EXTENSIONS]
            ),
            "top_level_dirs": [
                {
                    "name": name,
                    "file_count": count,
                }
                for name, count in sorted(
                    top_level.items(),
                    key=lambda item: -item[1],
                )[: self.MAX_TOP_LEVEL_DIRS]
            ],
            "key_files": sorted(
                key_files
            )[: self.MAX_KEY_FILES],
        }

    @staticmethod
    def _normalize_path(item):
        """文件列表项可能是 dict 或纯字符串。"""

        if isinstance(item, dict):
            return item.get("path")

        return str(item)

    def _read_candidates(
        self,
        files,
        quotas=None,
    ):
        """
        从文件列表里挑出要读取的关键源码。

        文件树可能有数百个文件，
        必须限制读取数量，
        否则会对 GitHub 发起数百次请求
        （本 Skill 是逐个文件读的，
        没有批量接口）。

        挑选顺序：

            1. 按维度配额挑路径命中该维度的文件
               （每个维度有独立名额，见 DIMENSION_QUOTAS）
            2. 入口文件（main.py / app.py ...）
            3. 其余源码
            4. 测试 / 迁移 / 示例（垫底）

        同一档内浅层路径优先。

        两次修正的由来：

        - 第一版按固定文件名列表挑，
          配额被 docker-compose.yml /
          pyproject.toml 这类配置文件占满，
          一个 88 个 .py 的项目
          连一个 Agent 类都没读到；
        - 第二版按「命中信号总数」全局排序，
          但仓库目录结构会决定结果：
          agents/ 文件多就挤掉 rag/，
          各模块详略极不均匀。
        """

        entry = []
        normal = []
        low = []

        if not quotas:

            quotas = self.DIMENSION_QUOTAS

        # 维度名 -> 候选文件（浅层优先）。
        by_dimension = {
            name: []
            for name in quotas
        }

        seen = set()

        for item in files:

            file_path = self._normalize_path(
                item
            )

            if not file_path:
                continue

            if file_path in seen:
                continue

            if not file_path.lower().endswith(
                self.SOURCE_EXTENSIONS
            ):
                continue

            basename = os.path.basename(
                file_path
            ).lower()

            # __init__.py 绝大多数只是空文件或转出声明，
            # 作为「关键源码」没有意义。
            #
            # 实测空的 __init__.py 还会让证据层
            # 因为「纯空白内容」而报错。
            if basename == "__init__.py":
                continue

            seen.add(file_path)

            if self._is_low_priority_path(
                file_path
            ):

                low.append(file_path)

                continue

            matched = (
                CodeStructureExtractor
                .dimensions_for_path(file_path)
            )

            if matched:

                for dimension in matched:

                    by_dimension[
                        dimension
                    ].append(file_path)

            elif basename in self.PRIORITY_FILENAMES:

                entry.append(file_path)

            else:

                normal.append(file_path)

        for bucket in (
            entry,
            normal,
            low,
            *by_dimension.values(),
        ):

            bucket.sort(
                key=lambda path: (
                    path.count("/"),
                    path,
                )
            )

        # 按维度配额取文件。
        #
        # 一个文件可能同时命中多个维度
        # （例如 services/workflow_service.py
        # 既像 workflow 又像 agents），
        # 取第一个有余额的维度即可，
        # 同一个文件不重复占名额。
        ordered = []

        taken = set()

        for dimension, quota in quotas.items():

            count = 0

            for path in by_dimension[dimension]:

                if count >= quota:
                    break

                if path in taken:
                    continue

                taken.add(path)

                ordered.append(path)

                count += 1

        # 配额之外、但仍命中维度的文件。
        #
        # 必须回填：
        # 如果一个仓库的源码全在 agents/ 下，
        # 配额只取 3 个，
        # 剩下 17 个名额就会空着，
        # 白白浪费掉读取机会。
        remaining_dimension = []

        for paths in by_dimension.values():

            for path in paths:

                if path not in taken:

                    remaining_dimension.append(path)

        remaining_dimension.sort(
            key=lambda path: (
                path.count("/"),
                path,
            )
        )

        for bucket in (
            entry,
            remaining_dimension,
            normal,
            low,
        ):

            for path in bucket:

                if len(ordered) >= self.MAX_MODULES:
                    break

                if path in taken:
                    continue

                taken.add(path)

                ordered.append(path)

        return ordered[: self.MAX_MODULES]

    def _is_low_priority_path(
        self,
        file_path,
    ) -> bool:
        """判断是否为测试 / 迁移 / 示例类路径。"""

        normalized = str(file_path).lower()

        return any(
            pattern.search(normalized)
            for pattern in (
                self.LOW_PRIORITY_PATH_PATTERNS
            )
        )

    def _extract_project_structure(
        self,
        input_data,
        code_structure=None,
    ):
        """
        抽取被分析项目的结构。

        数据来源（全部来自被分析项目本身）：

            code_structure      真实源码的 AST 抽取结果
            readme              目标项目 README 全文
            repository.topics   GitHub 官方话题标签
            repository.description  项目描述

        不读取任何 AIPI 自身的执行数据。

        代码为主、README 为辅：

        - items 里代码符号排在前面，
          README 条目补在后面；
        - evidence 保持「README 命中行」的原有含义，
          代码证据放在新增的 code_evidence 字段，
          两个字段分开是因为两条证据的性质不同 ——
          一个是「项目说自己有什么」，
          一个是「项目代码里确实有什么」；
        - declared_by 记录结论来自哪一侧。

        保持 declared / items / topics / evidence / reason
        这五个字段的原有含义与类型不变 ——
        报告层按它们渲染各维度章。
        """

        readme = input_data.get(
            "readme"
        )

        repository = input_data.get(
            "repository"
        )

        if not isinstance(
            repository,
            dict,
        ):
            repository = {}

        topics = repository.get(
            "topics"
        )

        if not isinstance(
            topics,
            list,
        ):
            topics = []

        description = repository.get(
            "description"
        )

        if not isinstance(
            description,
            str,
        ):
            description = ""

        code_dimensions = {}

        if isinstance(
            code_structure,
            dict,
        ):

            code_dimensions = (
                code_structure.get("dimensions")
                or {}
            )

            if not isinstance(
                code_dimensions,
                dict,
            ):
                code_dimensions = {}

        # 既没有 README / topics / description，
        # 也没有从代码里抽出任何信号时，
        # 才能诚实声明无法抽取。
        #
        # 旧版本只看 README 三件套，
        # 于是 README 为空的仓库
        # 即使代码结构完整也拿不到任何维度。
        if (
            not isinstance(readme, str)
            and not topics
            and not description
            and not self._has_code_signals(
                code_dimensions
            )
        ):
            return {
                "available": False,
                "basis": "code+readme+topics",
                "reason": (
                    "被分析项目没有可用 README、"
                    "topics 或 description，"
                    "也没有读取到任何源码，"
                    "无法抽取项目结构。"
                ),
                "dimensions": {},
                "code_extraction": (
                    self._code_extraction_meta(
                        code_structure
                    )
                ),
            }

        lines = (
            readme.splitlines()
            if isinstance(readme, str)
            else []
        )

        dimensions = {}

        for dimension, keywords in (
            self.STRUCTURE_KEYWORDS.items()
        ):
            dimensions[dimension] = (
                self._merge_dimension(
                    dimension,
                    self._extract_dimension_signals(
                        dimension,
                        keywords,
                        lines,
                        topics,
                        description,
                    ),
                    code_dimensions.get(
                        dimension
                    ),
                )
            )

        return {
            "available": True,
            "basis": "code+readme+topics",
            "reason": None,
            "dimensions": dimensions,
            "code_extraction": (
                self._code_extraction_meta(
                    code_structure
                )
            ),
        }

    @staticmethod
    def _has_code_signals(
        code_dimensions: dict,
    ) -> bool:
        """代码侧是否抽到了任何条目。"""

        if not isinstance(
            code_dimensions,
            dict,
        ):
            return False

        return any(
            isinstance(entry, dict)
            and entry.get("items")
            for entry in code_dimensions.values()
        )

    @staticmethod
    def _code_extraction_meta(
        code_structure,
    ) -> dict:
        """
        记录代码抽取的执行情况。

        解析失败的文件必须如实带出来，
        否则「没抽到东西」与
        「文件根本没解析成功」会混为一谈。
        """

        if not isinstance(
            code_structure,
            dict,
        ):
            return {
                "available": False,
                "reason": "未执行代码结构抽取。",
                "parsed_files": 0,
                "unparsed": [],
            }

        return {
            "available": bool(
                code_structure.get("available")
            ),
            "parsed_files": (
                code_structure.get(
                    "parsed_files",
                    0,
                )
            ),
            "unparsed": list(
                code_structure.get("unparsed")
                or []
            ),
        }

    def _merge_dimension(
        self,
        dimension: str,
        readme_entry: dict,
        code_entry,
    ) -> dict:
        """
        合并「代码证据」与「README 自述」。

        代码在前，README 在后。
        """

        if not isinstance(
            code_entry,
            dict,
        ):
            code_entry = {}

        code_items = [
            item
            for item in (
                code_entry.get("items") or []
            )
            if isinstance(item, str)
        ]

        code_evidence = [
            item
            for item in (
                code_entry.get("evidence") or []
            )
            if isinstance(item, dict)
        ]

        readme_items = list(
            readme_entry.get("items") or []
        )

        # 按小写去重，避免同一个符号
        # 被代码与 README 各记一次。
        seen = set()

        items = []

        for item in code_items + readme_items:

            lowered = item.lower()

            if lowered in seen:
                continue

            seen.add(lowered)

            if len(items) >= self.MAX_MERGED_ITEMS:
                break

            items.append(item)

        declared_by = None

        if code_items:
            declared_by = "code"

        if readme_items or readme_entry.get(
            "topics"
        ) or readme_entry.get("evidence"):

            declared_by = (
                "code+readme"
                if declared_by == "code"
                else "readme"
            )

        declared = declared_by is not None

        return {
            # 原字段：类型与含义都不变。
            "declared": declared,
            "items": items,
            "topics": readme_entry.get(
                "topics"
            )
            or [],
            "evidence": readme_entry.get(
                "evidence"
            )
            or [],
            "reason": (
                None
                if declared
                else (
                    "被分析项目的代码、README / "
                    "topics / description 中"
                    f"都没有 {dimension} 相关声明。"
                )
            ),

            # 新增字段：不改变上面五个的含义，
            # 只是把来源与代码证据显式带出来。
            "declared_by": declared_by,
            "code_evidence": code_evidence,
            # 实现明细：函数签名 / 调用链 / 关键常量。
            #
            # 必须在这里透传，
            # 否则抽取器辛苦解析出来的明细
            # 会在合并这一步被丢掉。
            "details": [
                item
                for item in (
                    code_entry.get("details") or []
                )
                if isinstance(item, dict)
            ],
        }

    def _extract_dimension_signals(
        self,
        dimension,
        keywords,
        lines,
        topics,
        description,
    ):
        """
        抽取单个维度的自述信号。

        返回：

            declared   是否在项目自述中被提到
            items      命中的标识（反引号 / 粗体单 token）
            topics     命中的 GitHub topics
            evidence   命中行（含行号与原文）
            reason     declared=False 时的说明
        """

        matched_topics = [
            topic
            for topic in topics
            if isinstance(topic, str)
            and self._line_matches(topic, keywords)
        ]

        items = []
        seen_items = set()

        # 先找出所有命中行。
        hits = [
            (index, line)
            for index, line in enumerate(lines, start=1)
            if line.strip()
            and self._line_matches(line, keywords)
        ]

        # 产生了标识的行优先作为证据。
        #
        # 否则 README 开头的徽章 / 标题行
        # 会把证据额度占满，
        # 真正带信息的行反而抽不到。
        identified = []
        plain = []

        for index, line in hits:

            if self._collect_items(
                line,
                keywords,
                items,
                seen_items,
                dimension=dimension,
            ):
                identified.append((index, line))
            else:
                plain.append((index, line))

        evidence = []

        for index, line in (
            identified + plain
        )[: self.MAX_EVIDENCE_LINES]:

            evidence.append(
                {
                    "file_path": "README.md",
                    "line_start": index,
                    "line_end": index,
                    "text": line.strip()[:200],
                }
            )

        # description 也是项目自述，
        # 但没有 README 行号，
        # 因此只用来补充 items，
        # 不计入 evidence 行。
        if description and self._line_matches(
            description,
            keywords,
        ):

            self._collect_items(
                description,
                keywords,
                items,
                seen_items,
                dimension=dimension,
            )

        declared = bool(
            evidence
            or items
            or matched_topics
        )

        return {
            "declared": declared,
            "items": items,
            "topics": matched_topics,
            "evidence": evidence,
            "reason": (
                None
                if declared
                else (
                    "被分析项目的 README / topics / "
                    f"description 中没有 {dimension} "
                    "相关声明。"
                )
            ),
        }

    @staticmethod
    def _line_matches(
        text,
        keywords,
    ):
        """判断文本是否命中关键词（词边界匹配）。"""

        lowered = text.lower()

        return any(
            re.search(
                r"\b" + re.escape(keyword) + r"\b",
                lowered,
            )
            for keyword in keywords
        )

    def _collect_items(
        self,
        text,
        keywords,
        items,
        seen_items,
        dimension,
    ):
        """
        从命中行里收集标识。

        规则（避免维度之间互相泄漏）：

        - **粗体** token 必须自身命中本维度关键词，
          避免把 **Executor** 这类角色名记进 tools 维度
        - `反引号` token 同样必须命中本维度关键词；
          只有 DIMENSIONS_ACCEPTING_CODE_IDENTIFIERS
          里的维度（tools）例外，
          因为它需要保留工具调用名

        返回是否收集到任何标识。
        """

        accept_code_identifiers = (
            dimension
            in self.DIMENSIONS_ACCEPTING_CODE_IDENTIFIERS
        )

        collected = False

        for match in (
            self._IDENTIFIER_PATTERN
            .finditer(text)
        ):

            code_token = match.group(1)

            bold_token = match.group(2)

            token = (
                code_token
                or bold_token
                or ""
            ).strip()

            if not self._SINGLE_TOKEN_PATTERN.fullmatch(
                token
            ):
                continue

            matches_keywords = self._line_matches(
                token,
                keywords,
            )

            if not matches_keywords:

                # 粗体 token 一律要求命中关键词。
                if bold_token is not None:
                    continue

                # 代码 token 只有特定维度例外。
                if not accept_code_identifiers:
                    continue

            lowered = token.lower()

            collected = True

            if lowered in seen_items:
                continue

            seen_items.add(lowered)

            if len(items) < self.MAX_ITEMS:
                items.append(token)

        if self._collect_bullet_phrases(
            text,
            items,
            seen_items,
        ):
            collected = True

        return collected

    def _collect_bullet_phrases(
        self,
        text,
        items,
        seen_items,
    ) -> bool:
        """
        把列表行的逗号分段作为条目。

        只对以 "- " / "* " 开头的行生效，
        因为这类行是 README 里最常见的
        「罗列能力」写法。

        条目是 README 原文的切片，
        不加工、不改写。
        """

        bullet = self._BULLET_PATTERN.match(text)

        if bullet is None:
            return False

        collected = False

        for segment in bullet.group(1).split(","):

            phrase = segment.strip()

            if not phrase:
                continue

            if len(phrase) > self.MAX_BULLET_ITEM_CHARS:
                continue

            collected = True

            lowered = phrase.lower()

            if lowered in seen_items:
                continue

            seen_items.add(lowered)

            if len(items) < self.MAX_ITEMS:
                items.append(phrase)

        return collected