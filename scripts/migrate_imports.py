"""
自动替换导入路径。

用法：
    python scripts/migrate_imports.py app/infrastructure/workflow/

这会自动将目录下所有 .py 文件的导入路径从旧结构替换为新结构。
"""

import re
import sys
from pathlib import Path


REPLACEMENTS = [
    # Workflow
    (r"from app\.workflow\.", "from app.infrastructure.workflow."),
    (r"import app\.workflow\.", "import app.infrastructure.workflow."),

    # Agents
    (r"from app\.agents\.", "from app.infrastructure.agents."),
    (r"import app\.agents\.", "import app.infrastructure.agents."),

    # Skills
    (r"from app\.skills\.", "from app.infrastructure.skills."),
    (r"import app\.skills\.", "import app.infrastructure.skills."),

    # Tools
    (r"from app\.tools\.", "from app.infrastructure.tools."),
    (r"import app\.tools\.", "import app.infrastructure.tools."),

    # Models
    (r"from app\.models\.", "from app.infrastructure.persistence.models."),
    (r"import app\.models\.", "import app.infrastructure.persistence.models."),

    # Repositories
    (r"from app\.repositories\.", "from app.infrastructure.persistence.repositories."),
    (r"import app\.repositories\.", "import app.infrastructure.persistence.repositories."),

    # Evidence
    (r"from app\.evidence\.", "from app.infrastructure.enrichment.evidence."),
    (r"import app\.evidence\.", "import app.infrastructure.enrichment.evidence."),

    # Memory
    (r"from app\.memory\.", "from app.infrastructure.enrichment.memory."),
    (r"import app\.memory\.", "import app.infrastructure.enrichment.memory."),

    # Context
    (r"from app\.context\.", "from app.infrastructure.enrichment.context."),
    (r"import app\.context\.", "import app.infrastructure.enrichment.context."),

    # Project Analysis
    (r"from app\.project_analysis\.", "from app.infrastructure.tools.project."),
    (r"import app\.project_analysis\.", "import app.infrastructure.tools.project."),

    # Orchestration → Domain
    (r"from app\.orchestration\.workflow_orchestrator", "from app.domain.analysis.workflow"),
    (r"import app\.orchestration\.workflow_orchestrator", "import app.domain.analysis.workflow"),
    (r"WorkflowOrchestrator", "AnalysisWorkflowOrchestrator"),
]


def replace_imports(file_path: Path) -> bool:
    """
    替换单个文件的导入路径。

    Args:
        file_path: 文件路径

    Returns:
        是否有更新
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[!] Error reading {file_path}: {e}")
        return False

    original = content

    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    if content != original:
        try:
            file_path.write_text(content, encoding="utf-8")
            print(f"[+] Updated: {file_path}")
            return True
        except Exception as e:
            print(f"[!] Error writing {file_path}: {e}")
            return False

    return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/migrate_imports.py <directory>")
        print("\nExamples:")
        print("  python scripts/migrate_imports.py app/infrastructure/workflow/")
        print("  python scripts/migrate_imports.py app/services/")
        print("  python scripts/migrate_imports.py app/api/")
        sys.exit(1)

    directory = Path(sys.argv[1])

    if not directory.exists():
        print(f"[!] Error: {directory} does not exist")
        sys.exit(1)

    if not directory.is_dir():
        print(f"[!] Error: {directory} is not a directory")
        sys.exit(1)

    print(f"[*] Scanning {directory} for Python files...\n")

    updated = 0
    total = 0

    for file_path in directory.rglob("*.py"):
        # 跳过 __pycache__
        if "__pycache__" in str(file_path):
            continue

        total += 1
        if replace_imports(file_path):
            updated += 1

    print(f"\n[*] Summary:")
    print(f"  Total files scanned: {total}")
    print(f"  Files updated: {updated}")
    print(f"  Files unchanged: {total - updated}")


if __name__ == "__main__":
    main()
