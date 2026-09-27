"""
Technology Analysis Skill。

支持：

1. 本地项目目录分析
2. GitHub Repository 远程文件分析
"""

from app.skills.base import BaseSkill


class TechnologyAnalysisSkill(
    BaseSkill
):
    """项目技术栈分析 Skill。"""

    name = "technology_analysis"

    description = (
        "Analyze GitHub project technology stack"
    )

    async def execute(
        self,
        context,
        input_data,
    ):
        project_path = input_data.get(
            "project_path"
        )

        # 本地项目：复用现有 DependencyAnalyzerTool。
        if project_path:

            dependency_tool = (
                context.tools.get(
                    "dependency_analyzer"
                )
            )

            if dependency_tool is None:
                raise RuntimeError(
                    "Tool not found: dependency_analyzer"
                )

            dependencies = (
                await dependency_tool.execute(
                    project_path=project_path,
                )
            )

            return {
                "technology_stack": dependencies
            }

        # GitHub 远程项目。
        return await self._analyze_remote(
            context,
            input_data,
        )

    async def _analyze_remote(
        self,
        context,
        input_data,
    ):
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
                "Technology analysis requires "
                "'owner' and 'repo'."
            )

        branch = input_data.get(
            "branch",
            "main",
        )

        target_files = [
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "Dockerfile",
            "docker-compose.yml",
        ]

        contents = {}

        for file_path in target_files:

            content = await file_reader.execute(
                owner=owner,
                name=repo,
                file_path=file_path,
                branch=branch,
            )

            if content:
                contents[file_path] = content

        all_content = "\n".join(
            contents.values()
        ).lower()

        frameworks = []
        databases = []
        llms = []
        embeddings = []
        deployment = []

        if "fastapi" in all_content:
            frameworks.append("FastAPI")

        if "django" in all_content:
            frameworks.append("Django")

        if "flask" in all_content:
            frameworks.append("Flask")

        if "langchain" in all_content:
            frameworks.append("LangChain")

        if "langgraph" in all_content:
            frameworks.append("LangGraph")

        if "sqlalchemy" in all_content:
            databases.append("SQLAlchemy")

        if "mysql" in all_content:
            databases.append("MySQL")

        if "postgres" in all_content:
            databases.append("PostgreSQL")

        if "qdrant" in all_content:
            embeddings.append("Qdrant")

        if "chromadb" in all_content:
            embeddings.append("ChromaDB")

        if "deepseek" in all_content:
            llms.append("DeepSeek")

        if "openai" in all_content:
            llms.append("OpenAI")

        if "ollama" in all_content:
            llms.append("Ollama")

        if "docker" in all_content:
            deployment.append("Docker")

        return {
            "technology_stack": {
                "frameworks": frameworks,
                "database": databases,
                "llm": llms,
                "embedding": embeddings,
                "deployment": deployment,
                "source_files": list(
                    contents.keys()
                ),
            }
        }