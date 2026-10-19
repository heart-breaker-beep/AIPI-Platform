"""检查 API、业务组件、通用引擎、持久层和外部集成的依赖边界。"""

import ast
from dataclasses import dataclass
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent / "app"
LEGACY_PREFIXES = (
    "app.db",
    "app.domain",
    "app.infrastructure",
    "app.llm",
    "app.embeddings",
    "app.vector_store",
)
ALLOWED = {
    "api": ("app.api", "app.services", "app.schemas", "app.core"),
    "services": (
        "app.services",
        "app.analysis",
        "app.workflow",
        "app.persistence",
        "app.integrations",
        "app.schemas",
        "app.core",
    ),
    "analysis": (
        "app.analysis",
        "app.workflow",
        "app.persistence.repositories",
        "app.integrations",
        "app.core",
    ),
    "workflow": ("app.workflow", "app.core"),
    "persistence": ("app.persistence", "app.core", "app.workflow.state"),
    "integrations": ("app.integrations", "app.core"),
    "schemas": ("app.schemas", "app.core"),
    "core": ("app.core",),
}


def matches(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(prefix + ".")


def imported_modules(path: Path, app_dir: Path = APP_DIR) -> set[str]:
    """包括延迟导入和相对导入，统一解析为完整模块名。"""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    package = list(path.resolve().relative_to(app_dir.resolve().parent).parts[:-1])
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                base = package[: len(package) - node.level + 1]
                if node.module:
                    base.extend(node.module.split("."))
                module = ".".join(base)
                if not node.module:
                    modules.update(f"{module}.{alias.name}" for alias in node.names)
            else:
                module = node.module or ""
            modules.add(module)
            # 同时检查 from app import services 这类包级导入。
            if module == "app" or module.startswith("app."):
                modules.update(f"{module}.{alias.name}" for alias in node.names)
    return modules


@dataclass
class DependencyViolation:
    file_path: Path
    module: str
    reason: str

    def __str__(self):
        return f"{self.file_path}: {self.module}: {self.reason}"


def check_file_imports(
    file_path: Path, app_dir: Path = APP_DIR
) -> list[DependencyViolation]:
    relative = file_path.resolve().relative_to(app_dir.resolve())
    layer = relative.parts[0]
    found = []
    for module in sorted(imported_modules(file_path, app_dir)):
        reason = None
        if any(matches(module, prefix) for prefix in LEGACY_PREFIXES):
            reason = "Removed package; use the current application layout"
        elif layer in (
            "analysis",
            "workflow",
            "integrations",
            "core",
            "schemas",
        ) and matches(module, "sqlalchemy"):
            reason = "Database implementation belongs in persistence"
        elif (
            layer == "services"
            and matches(module, "sqlalchemy")
            and module != "sqlalchemy.ext.asyncio"
        ):
            reason = "Services may coordinate Session transactions; SQL belongs in repositories"
        elif module.startswith("app.") and layer in ALLOWED:
            allowed = ALLOWED[layer]
            if relative.as_posix() == "api/dependencies.py":
                allowed = (*allowed, "app.persistence.session")
            if not any(matches(module, prefix) for prefix in allowed):
                reason = f"Dependency is outside the {layer} layer boundary"
        if reason:
            found.append(DependencyViolation(file_path, module, reason))
    return found


def check_dependencies(app_dir: Path = APP_DIR) -> list[DependencyViolation]:
    return [
        violation
        for path in sorted(app_dir.rglob("*.py"))
        for violation in check_file_imports(path, app_dir)
    ]


def main() -> int:
    violations = check_dependencies()
    for violation in violations:
        print(violation)
    print(f"Checked application dependencies: {len(violations)} violation(s).")
    return bool(violations)


if __name__ == "__main__":
    raise SystemExit(main())
