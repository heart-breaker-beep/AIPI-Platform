"""
Evidence Analysis Skill。

支持：

1. Repository / Architecture Agent 输出
2. Evidence MySQL 持久化
"""

from uuid import uuid4

from app.analysis.skills.base import BaseSkill
from app.core.trace import traced


class EvidenceAnalysisSkill(
    BaseSkill
):
    """生成可追溯 Evidence。"""

    name = "evidence_analysis"

    description = (
        "Extract traceable evidence from "
        "repository analysis results."
    )

    # 单条源码证据最多保存多少字符。
    MAX_EVIDENCE_CHARS = 1500

    @traced("skill")
    async def execute(
        self,
        context,
        input_data,
    ):
        evidence = self._from_analysis_results(input_data)

        # 去重。
        unique = []

        seen = set()

        for item in evidence:

            # 按位置去重，避免重复证据占用报告名额。
            key = (
                item.get("file_path"),
                item.get("line_start"),
                item.get("line_end"),
            )

            if key == (None, None, None):
                # 没有位置信息的（理论上不该有），退回按内容去重。
                key = item.get("content")

            if key in seen:
                continue

            seen.add(key)
            unique.append(item)

        # 存储能力由组合根注入；Skill 不创建或管理数据库 Session。
        config = getattr(context, "config", {}) or {}
        store = getattr(context, "evidence_store", None)

        repository_id = config.get(
            "repository_id"

        )

        persist_failures = []

        if (
            store is not None
            and repository_id is not None
        ):
            persisted = []

            for item in unique:

                # 单条证据落库失败不应中断整个分析，
                # 而且失败必须被**限制在这一条**里。
                #
                # 为什么用 SAVEPOINT：一条写入失败会让整个 session
                # 进入「需要回滚」状态，之后同一个 session 上的
                # 任何写入（后面的证据、以及 checkpoint）都会连锁失败。
                # 真实事故：一条 evidence 写失败，
                # 结果是这个 run 的证据与 checkpoint 全都没落库。
                # begin_nested() 只回滚这一条，session 继续可用。
                try:

                    async with store.isolated_write():

                        record = (
                            await store.create_evidence(
                                evidence_id=str(
                                    uuid4()
                                ),
                                repository_id=repository_id,
                                source_type=item[
                                    "source_type"
                                ],
                                source_url=item.get(
                                    "source_url"
                                ),
                                file_path=item.get(
                                    "file_path"
                                ),
                                line_start=item.get(
                                    "line_start"
                                ),
                                line_end=item.get(
                                    "line_end"
                                ),
                                content=item[
                                    "content"
                                ],
                                verification_status=(
                                    "UNVERIFIED"
                                ),
                            )
                        )

                except Exception as error:  # noqa: BLE001 - 单条失败由隔离写入处理。

                    persist_failures.append(
                        {
                            "file_path": item.get(
                                "file_path"
                            ),
                            "error": (
                                str(error)
                                or type(error).__name__
                            ),
                        }
                    )

                    continue

                item = dict(item)

                item["evidence_id"] = (
                    record.id
                )

                persisted.append(item)

            unique = persisted

        return {
            "evidence": unique,
            "count": len(unique),
            "persist_failures": persist_failures,
        }

    @staticmethod
    def _from_analysis_results(
        input_data,
    ):
        evidence = []

        repo_url = input_data.get(
            "repo_url"
        )

        readme = input_data.get(
            "readme"
        )

        if isinstance(
            readme,
            str,
        ) and readme.strip():

            # README 也要按源码证据的规则截断。
            #
            # 一份 README 动辄上万字符，
            # 不截断的话它会比整个源码证据集合还大，
            # 证据表很快被它一个人撑满。
            excerpt = readme[
                : EvidenceAnalysisSkill.MAX_EVIDENCE_CHARS
            ]

            evidence.append(
                {
                    "source_type": "github",
                    "source_url": repo_url,
                    "file_path": "README.md",
                    "line_start": 1,
                    # 行号跟着截断后的正文走，
                    # 否则会标成「README:1-800」却只有前 40 行。
                    "line_end": (
                        len(
                            excerpt.splitlines()
                        )
                        or 1
                    ),
                    "content": excerpt,
                    "metadata": {},
                }
            )

        modules = EvidenceAnalysisSkill._modules(
            input_data
        )

        for module in modules:

            if not isinstance(
                module,
                dict,
            ):
                continue

            # 读取失败的模块不生成证据，
            # 否则会把空内容当成源码证据。
            if module.get("error"):
                continue

            file_path = module.get(
                "file_path"
            )

            content = module.get(
                "content"
            )

            if isinstance(
                content,
                dict,
            ):
                content = content.get(
                    "content",
                    "",
                )

            # 纯空白也算「没有内容」。
            #
            # 真实事故：空的 __init__.py 只有 1 个换行符，
            # 通过 `if not content` 检查后
            # 被证据存储层以
            # "Evidence content cannot be empty." 拒绝，
            # 异常冒泡导致整个 5-Agent 计划 FAILED。
            content = str(content)

            if not content.strip():
                continue

            # 限制单条证据长度：
            # 源码文件可能有数万字符，
            # 全部落库会让证据表迅速膨胀。
            excerpt = content[
                : EvidenceAnalysisSkill.MAX_EVIDENCE_CHARS
            ]

            # 摘录可能跳过了开头的 import 段，
            # 行号要跟着偏移，
            # 否则会写成「file:1-30」但内容其实是第 30 行开始的。
            start_line = module.get(
                "start_line",
                1,
            )

            if not isinstance(
                start_line,
                int,
            ) or start_line < 1:
                start_line = 1

            evidence.append(
                {
                    "source_type": "github",
                    "source_url": repo_url,
                    "file_path": file_path,
                    "line_start": start_line,
                    "line_end": (
                        start_line
                        + len(excerpt.splitlines())
                        - 1
                    ),
                    "content": excerpt,
                    "metadata": {},
                }
            )

        return evidence

    @staticmethod
    def _modules(
        input_data,
    ) -> list:
        """
        取出架构分析产出的 modules。

        修复点：

        旧代码只读 input_data["architecture"]，
        但真实数据结构里没有这个 key
        （真实 key 是 architecture_analysis_agent，
        且 PlanExecutorNode 会把结果拍平到顶层 modules），
        因此这个分支以前从未执行过，
        导致 Evidence 只有 README、没有源码。
        """

        architecture = (
            input_data.get("architecture")
            or input_data.get(
                "architecture_analysis_agent"
            )
        )

        if isinstance(
            architecture,
            dict,
        ):

            modules = architecture.get(
                "modules"
            )

            if isinstance(modules, list):
                return modules

        modules = input_data.get("modules")

        if isinstance(modules, list):
            return modules

        return []
