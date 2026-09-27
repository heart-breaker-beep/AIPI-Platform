"""
Repository Analysis Skill。

负责：
- 获取 GitHub Repository 基本信息
- 获取 README
- 分析项目依赖
"""

from app.skills.base import BaseSkill


class RepositoryAnalysisSkill(
    BaseSkill
):
    """GitHub Repository 分析 Skill。"""

    name = "repository_analysis"

    description = (
        "Analyze github repository information"
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        """
        执行仓库分析。

        input_data 至少需要：

        {
            "owner": "xxx",
            "repo": "xxx"
        }

        可选：

        {
            "project_path": "..."
        }
        """

        # 从 Context 获取工具
        github_tool = context.tools.get(
            "github_repository"
        )

        if github_tool is None:
            raise RuntimeError(
                "Tool not found: github_repository"
            )

        file_reader = context.tools.get(
            "file_reader"
        )

        if file_reader is None:
            raise RuntimeError(
                "Tool not found: file_reader"
            )

        dependency_tool = context.tools.get(
            "dependency_analyzer"
        )

        if dependency_tool is None:
            raise RuntimeError(
                "Tool not found: dependency_analyzer"
            )

        owner = input_data.get(
            "owner"
        )

        repo = input_data.get(
            "repo"
        )

        if not owner or not repo:
            raise ValueError(
                "Repository analysis requires "
                "'owner' and 'repo'."
            )

        project_path = input_data.get(
            "project_path"
        )

        result = {}

        # 获取仓库基本信息
        result["repository"] = (
            await github_tool.execute(
                owner=owner,
                name=repo,
            )
        )

        # 获取 README
        result["readme"] = (
            await file_reader.execute(
                owner=owner,
                name=repo,
                file_path="README.md",
                branch=input_data.get(
                    "branch",
                    "main",
                ),
            )
        )

        # 有本地项目目录时才执行依赖分析
        if project_path:
            result["dependencies"] = (
                await dependency_tool.execute(
                    project_path=project_path,
                )
            )
        else:
            # GitHub 远程仓库尚未提供本地目录
            result["dependencies"] = {}

        return result