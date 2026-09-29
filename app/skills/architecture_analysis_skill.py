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

    # 每个维度最多记录的命中行数。
    MAX_EVIDENCE_LINES = 4

    # 每个维度最多记录的标识数。
    MAX_ITEMS = 12

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
        ".toml",
        ".cfg",
        ".ini",
        ".yml",
        ".yaml",
        ".json",
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
        "docker-compose.yml",
        "docker-compose.yaml",
        "pyproject.toml",
        "requirements.txt",
        "package.json",
    )

    # 最多读取多少个文件内容作为「关键源码」。
    #
    # 文件树可能有数百个文件，
    # 不限制会对 GitHub 发起数百次请求。
    MAX_MODULES = 8

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

        for file_path in self._read_candidates(
            files
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

            architecture[
                "modules"
            ].append(
                self._module_entry(
                    file_path,
                    content,
                )
            )

        # Phase 12 → Phase 13 契约：
        # 产出被分析项目的自述结构。
        architecture[
            "project_structure"
        ] = self._extract_project_structure(
            input_data
        )

        return architecture

    def _module_entry(
        self,
        file_path,
        content,
    ):
        """
        构建单个源码条目。

        内容按 MAX_MODULE_CHARS 截断，
        避免大型文件把 state_data 撑爆。
        """

        text = str(content or "")

        entry = {
            "file_path": file_path,
            "content": text[: self.MAX_MODULE_CHARS],
        }

        if len(text) > self.MAX_MODULE_CHARS:
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
    ):
        """
        从文件列表里挑出要读取的关键源码。

        文件树可能有数百个文件，
        必须限制读取数量，
        否则会对 GitHub 发起数百次请求。
        """

        normal = []
        prioritized = []

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

            if basename in self.PRIORITY_FILENAMES:
                prioritized.append(file_path)
            else:
                normal.append(file_path)

        # 入口文件优先，且浅层路径优先：
        # 顶层 main.py 比深层的同名文件更能代表项目入口。
        prioritized.sort(
            key=lambda path: (
                path.count("/"),
                path,
            )
        )

        return (
            prioritized + normal
        )[: self.MAX_MODULES]

    def _extract_project_structure(
        self,
        input_data,
    ):
        """
        从被分析项目的 README 与 topics 中
        确定性抽取项目自述结构。

        数据来源（全部来自被分析项目本身）：

            readme              目标项目 README 全文
            repository.topics   GitHub 官方话题标签
            repository.description  项目描述

        不读取任何 AIPI 自身的执行数据。
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

        # 没有 README 也没有 topics / description 时，
        # 只能诚实声明无法抽取。
        if (
            not isinstance(readme, str)
            and not topics
            and not description
        ):
            return {
                "available": False,
                "basis": "readme+topics",
                "reason": (
                    "被分析项目没有可用 README、"
                    "topics 或 description，"
                    "无法抽取项目自述结构。"
                ),
                "dimensions": {},
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
                self._extract_dimension_signals(
                    dimension,
                    keywords,
                    lines,
                    topics,
                    description,
                )
            )

        return {
            "available": True,
            "basis": "readme+topics",
            "reason": None,
            "dimensions": dimensions,
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

        return collected