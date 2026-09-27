"""
Architecture Analysis Skill。

负责：

    GitHub Code Search
        ↓
    File Reader
        ↓
    Architecture information
"""

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

        files = await code_search.execute(
            keyword=keyword,
            repo=repository,
        )

        architecture = {
            "files": files,
            "modules": [],
        }

        branch = input_data.get(
            "branch",
            "main",
        )

        for item in files:

            if isinstance(
                item,
                dict,
            ):
                file_path = item.get(
                    "path"
                )
            else:
                file_path = str(item)

            if not file_path:
                continue

            content = await file_reader.execute(
                owner=owner,
                name=repo,
                file_path=file_path,
                branch=branch,
            )

            architecture[
                "modules"
            ].append(
                {
                    "file_path": file_path,
                    "content": content,
                }
            )

        return architecture