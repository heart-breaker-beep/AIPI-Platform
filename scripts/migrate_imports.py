"""将历史模块导入更新到当前目录；用法：python scripts/migrate_imports.py tests。"""

import re
import sys
from pathlib import Path

MODULE_MOVES = {
    "app.infrastructure.workflow.analysis_workflow": "app.analysis.workflow",
    "app.infrastructure.workflow.context_factory": "app.services.analysis_factory",
    "app.infrastructure.workflow.nodes": "app.analysis.nodes",
    "app.infrastructure.workflow": "app.workflow",
    "app.infrastructure.persistence": "app.persistence",
    "app.infrastructure.enrichment.evidence": "app.analysis.evidence",
    "app.infrastructure.enrichment.memory": "app.analysis.memory",
    "app.infrastructure.enrichment.context": "app.analysis.context",
    "app.infrastructure.agents": "app.analysis.agents",
    "app.infrastructure.skills": "app.analysis.skills",
    "app.infrastructure.reporting": "app.analysis.reporting",
    "app.infrastructure.tools.github": "app.integrations.github",
    "app.infrastructure.tools.file_reader_tool": "app.integrations.github.file_reader_tool",
    "app.infrastructure.tools.llm_chat_tool": "app.integrations.llm.chat_tool",
    "app.infrastructure.tools.report_export_tool": "app.integrations.report_export_tool",
    "app.infrastructure.tools.base": "app.integrations.base",
    "app.infrastructure.tools": "app.analysis.tools",
    "app.domain.analysis.workflow": "app.analysis.workflow",
    "app.core.error_handlers": "app.api.error_handlers",
    "app.db.session.get_db": "app.api.dependencies.get_db",
    "app.db": "app.persistence",
    "app.embeddings": "app.integrations.embeddings",
    "app.vector_store": "app.integrations.vector_store",
    "app.llm": "app.integrations.llm",
    "app.agents": "app.analysis.agents",
    "app.skills": "app.analysis.skills",
    "app.models": "app.persistence.models",
    "app.repositories": "app.persistence.repositories",
    "app.evidence": "app.analysis.evidence",
    "app.memory": "app.analysis.memory",
    "app.context": "app.analysis.context",
    "app.project_analysis": "app.analysis.tools.project",
    "app.orchestration.workflow_orchestrator": "app.analysis.workflow",
}


def replace_imports(file_path: Path) -> bool:
    original = file_path.read_text(encoding="utf-8-sig")
    content = original
    for source, target in sorted(
        MODULE_MOVES.items(), key=lambda pair: len(pair[0]), reverse=True
    ):
        content = re.sub(rf"(?<![\w.]){re.escape(source)}\b", target, content)
    content = re.sub(
        r"\bWorkflowOrchestrator\b", "AnalysisWorkflowOrchestrator", content
    )
    # get_db 是 HTTP 依赖，不属于持久层的 Session 工厂。
    content = content.replace(
        "from app.persistence.session import get_db",
        "from app.api.dependencies import get_db",
    )
    if content == original:
        return False
    file_path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_dir():
        print("Usage: python scripts/migrate_imports.py <directory>")
        return 1
    files = [
        path
        for path in Path(sys.argv[1]).rglob("*.py")
        if "__pycache__" not in path.parts
    ]
    updated = sum(replace_imports(path) for path in files)
    print(f"Updated {updated}/{len(files)} Python files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
