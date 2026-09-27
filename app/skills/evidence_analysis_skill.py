"""
Evidence Analysis Skill。

支持：

1. Qdrant 语义检索结果
2. Repository / Architecture Agent 输出
3. Evidence MySQL 持久化
"""

from app.skills.base import BaseSkill
from app.services.evidence_service import (
    EvidenceService,
)


class EvidenceAnalysisSkill(
    BaseSkill
):
    """生成可追溯 Evidence。"""

    name = "evidence_analysis"

    description = (
        "Extract traceable evidence from "
        "repository analysis results."
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        evidence = []

        query_vector = input_data.get(
            "query_vector"
        )

        # 如果已经提供向量，则继续使用 Qdrant。
        if query_vector is not None:

            evidence.extend(
                await self._from_qdrant(
                    context,
                    query_vector,
                    input_data.get(
                        "limit",
                        5,
                    ),
                )
            )

        # 没有 query_vector 时，
        # 从 Architecture / Repository 结果生成源码证据。
        if not evidence:

            evidence.extend(
                self._from_analysis_results(
                    input_data
                )
            )

        # 去重。
        unique = []

        seen = set()

        for item in evidence:

            key = (
                item.get("file_path"),
                item.get("line_start"),
                item.get("line_end"),
                item.get("content"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(item)

        # Phase 9 Evidence 持久化。
        config = getattr(context, "config", {}) or {}
        session = config.get("session")

        repository_id = config.get(
            "repository_id"

        )

        if (
            session is not None
            and repository_id is not None
        ):
            service = EvidenceService(
                session
            )

            persisted = []

            for item in unique:

                record = (
                    await service.create_evidence(
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

                item = dict(item)

                item["evidence_id"] = (
                    record.id
                )

                persisted.append(item)

            unique = persisted

        return {
            "evidence": unique,
            "count": len(unique),
        }

    async def _from_qdrant(
        self,
        context,
        query_vector,
        limit,
    ):
        qdrant_tool = context.tools.get(
            "qdrant_search"
        )

        if qdrant_tool is None:
            raise RuntimeError(
                "Tool not found: qdrant_search"
            )

        results = await qdrant_tool.execute(
            query_vector=query_vector,
            limit=limit,
        )

        evidence = []

        for item in results:

            evidence.append(
                {
                    "source_type": item.get(
                        "source_type",
                        "repository",
                    ),
                    "source_url": item.get(
                        "source_url"
                    ),
                    "file_path": item.get(
                        "file_path"
                    ) or item.get(
                        "source"
                    ),
                    "line_start": item.get(
                        "line_start"
                    ),
                    "line_end": item.get(
                        "line_end"
                    ),
                    "content": item.get(
                        "text",
                        "",
                    ),
                    "metadata": item,
                }
            )

        return evidence

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

            evidence.append(
                {
                    "source_type": "github",
                    "source_url": repo_url,
                    "file_path": "README.md",
                    "line_start": 1,
                    "line_end": len(
                        readme.splitlines()
                    ),
                    "content": readme,
                    "metadata": {},
                }
            )

        architecture = input_data.get(
            "architecture"
        )

        if isinstance(
            architecture,
            dict,
        ):

            modules = architecture.get(
                "modules",
                [],
            )

            for module in modules:

                if not isinstance(
                    module,
                    dict,
                ):
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

                if not content:
                    continue

                evidence.append(
                    {
                        "source_type": "github",
                        "source_url": repo_url,
                        "file_path": file_path,
                        "line_start": 1,
                        "line_end": len(
                            str(content).splitlines()
                        ),
                        "content": str(content),
                        "metadata": {},
                    }
                )

        return evidence