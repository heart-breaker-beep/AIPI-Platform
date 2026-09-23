"""
Dependency Analyzer Tool。

分析项目依赖和部署配置。
"""

from pathlib import Path

from app.tools.base import BaseTool


class DependencyAnalyzerTool(BaseTool):

    """
    项目依赖分析工具。

    分析:

    - requirements.txt
    - pyproject.toml
    - package.json
    - Dockerfile
    - docker-compose.yml
    """

    name = "dependency_analyzer"


    async def execute(
        self,
        project_path: str,
    ) -> dict:


        result = {

            "python_version": None,

            "frameworks": [],

            "database": [],

            "llm": [],

            "embedding": [],

            "deployment": [],

        }

        path = Path(project_path)

        await self._parse_requirements(
            path,
            result
        )

        await self._parse_docker(
            path,
            result
        )

        return result
    async def _parse_requirements(
        self,
        path: Path,
        result: dict
    ):

        file = path / "requirements.txt"


        if not file.exists():

            return
        content = file.read_text(
            encoding="utf-8"
        )

        dependencies = content.lower()

        if "fastapi" in dependencies:

            result["frameworks"].append(
                "FastAPI"
            )

        if "qdrant" in dependencies:

            result["embedding"].append(
                "Qdrant"
            )

        if "sqlalchemy" in dependencies:

            result["database"].append(
                "SQLAlchemy"
            )

        if "deepseek" in dependencies:

            result["llm"].append(
                "DeepSeek"
            )

    async def _parse_docker(
        self,
        path: Path,
        result: dict
    ):

        docker_file = path / "docker-compose.yml"


        if docker_file.exists():

            result["deployment"].append(
                "Docker Compose"
            )