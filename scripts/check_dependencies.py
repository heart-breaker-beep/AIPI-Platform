"""
检查依赖方向是否符合架构规则。

架构规则：
    API → Domain ← Infrastructure

违规示例：
    - Domain 不能导入 Infrastructure
    - API 不能直接导入 Infrastructure（应该通过 Domain）

用法：
    python scripts/check_dependencies.py
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple


class DependencyViolation:
    """依赖违规"""

    def __init__(self, file_path: Path, module: str, reason: str):
        self.file_path = file_path
        self.module = module
        self.reason = reason

    def __str__(self):
        return f"❌ {self.file_path}\n   imports {self.module}\n   {self.reason}"


def check_file_imports(file_path: Path) -> List[DependencyViolation]:
    """
    检查单个文件的导入是否违反规则。

    Args:
        file_path: 文件路径

    Returns:
        违规列表
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))
    except SyntaxError:
        # 跳过语法错误的文件
        return []
    except Exception:
        return []

    violations = []
    file_str = str(file_path)

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""

            # 规则 1: Domain 不能导入 Infrastructure
            if "domain" in file_str and "infrastructure" in module:
                violations.append(
                    DependencyViolation(
                        file_path,
                        module,
                        "Domain layer cannot depend on Infrastructure layer",
                    )
                )

            # 规则 2: API 不能直接导入 Infrastructure（应该通过 Domain）
            # 例外：API 可以导入 persistence.models（用于 ORM 查询）
            if "api" in file_str and "infrastructure" in module:
                # 允许导入 models（用于 ORM）
                if not ("persistence.models" in module or "schemas" in module):
                    violations.append(
                        DependencyViolation(
                            file_path,
                            module,
                            "API layer should depend on Domain, not Infrastructure directly",
                        )
                    )

            # 规则 3: Infrastructure 不能导入 Domain 的具体实现
            # （Infrastructure 只能导入 Domain 的接口）
            if "infrastructure" in file_str and "domain" in module:
                # 允许导入接口定义（如果有的话）
                if ".service" in module or ".workflow" in module:
                    violations.append(
                        DependencyViolation(
                            file_path,
                            module,
                            "Infrastructure should not depend on Domain services",
                        )
                    )

    return violations


def main():
    """主函数"""
    app_dir = Path("app")

    if not app_dir.exists():
        print("❌ Error: app/ directory not found")
        print("   Please run this script from the project root")
        sys.exit(1)

    print("🔍 Checking dependency violations...\n")

    all_violations = []

    # 扫描所有 Python 文件
    for file_path in app_dir.rglob("*.py"):
        # 跳过 __pycache__
        if "__pycache__" in str(file_path):
            continue

        violations = check_file_imports(file_path)
        all_violations.extend(violations)

    # 输出结果
    if all_violations:
        print("❌ Found dependency violations:\n")
        for violation in all_violations:
            print(violation)
            print()

        print(f"📊 Total violations: {len(all_violations)}")
        sys.exit(1)
    else:
        print("✅ No dependency violations found!")
        print("   All dependencies follow the architecture rules:")
        print("   API → Domain ← Infrastructure")
        sys.exit(0)


if __name__ == "__main__":
    main()
