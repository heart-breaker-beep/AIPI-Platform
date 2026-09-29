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

    # GitHub REST API 返回 84 个字段，
    # 其中 30 多个是各类 API URL（archive_url / blobs_url ...），
    # 分析与报告都不使用。
    #
    # 该结构会被保存两份
    # （state.data["repository_analysis_agent"] 与
    #   PlanExecutorNode 拍平后的 state.data["repository"]），
    # 全量保存会让 checkpoint.state_data 凭空多出约 30KB。
    REPOSITORY_FIELDS = (
        "id",
        "name",
        "full_name",
        "owner",
        "description",
        "html_url",
        "url",
        "homepage",
        "language",
        "topics",
        "default_branch",
        "size",
        "stargazers_count",
        "forks_count",
        "watchers_count",
        "open_issues_count",
        "subscribers_count",
        "license",
        "created_at",
        "updated_at",
        "pushed_at",
        "archived",
        "disabled",
        "fork",
        "visibility",
    )

    @classmethod
    def _select_repository_fields(
        cls,
        repository,
    ) -> dict:
        """只保留分析真正使用的仓库字段。"""

        if not isinstance(
            repository,
            dict,
        ):
            return repository

        return {
            key: repository[key]
            for key in cls.REPOSITORY_FIELDS
            if key in repository
        }

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

        # 获取仓库基本信息（只保留分析使用的字段）
        result["repository"] = (
            self._select_repository_fields(
                await github_tool.execute(
                    owner=owner,
                    name=repo,
                )
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