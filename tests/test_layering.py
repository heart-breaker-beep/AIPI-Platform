"""
分层守卫：用 ast 扫描 import，断言依赖方向单向。

目标方向：

    api  →  services(Application)  →  domain  →  infrastructure

为什么用测试而不是文档：
「依赖倒置」写在 docstring 里不会阻止任何人加一行反向 import，
而一次反向 import 就足以把 domain 拖回基础设施细节。
这个测试让越界当场变成红灯。

三条规则（与 docs/backend-fix-execution-prompt.md 第 5 阶段一致）：

1. infrastructure 不得 import services / api / domain
2. domain 不得 import infrastructure / services / api，也不得直接用 sqlalchemy
3. api 只允许 import services / schemas / db / core

组合根（app/services/analysis_factory.py）是唯一「同时认识两边」的地方 ——
它属于 services，因此不违反规则 1。
"""

import ast
from pathlib import Path

import pytest


APP_DIR = Path(__file__).parent.parent / "app"


def imported_modules(path: Path) -> set:
    """列出该文件 import 的所有模块名（含函数内延迟 import）。"""

    tree = ast.parse(
        path.read_text(
            encoding="utf-8-sig"
        )
    )

    modules = set()

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            modules.update(
                alias.name
                for alias in node.names
            )

        elif isinstance(
            node,
            ast.ImportFrom,
        ) and node.module:

            modules.add(node.module)

    return modules


def layer_files(layer: str) -> list:
    """该层下的全部 Python 文件。"""

    return sorted(
        (APP_DIR / layer).rglob("*.py")
    )


def violations(
    layer: str,
    banned_prefixes: tuple,
) -> list:
    """返回 (文件, 模块) 形式的越界 import。"""

    found = []

    for path in layer_files(layer):

        for module in sorted(
            imported_modules(path)
        ):

            if module.startswith(banned_prefixes):

                found.append(
                    (
                        path.relative_to(
                            APP_DIR
                        ).as_posix(),
                        module,
                    )
                )

    return found


def test_infrastructure_does_not_import_upper_layers():
    """
    infrastructure 不得反向 import 上层。

    上层依赖下层是允许的；
    反过来的每一处都会让「换实现」变成「改业务代码」。
    """

    found = violations(
        "infrastructure",
        (
            "app.services",
            "app.api",
            "app.domain",
        ),
    )

    assert found == []


def test_domain_is_free_of_infrastructure_details():
    """
    domain 不得 import infrastructure / services / api / sqlalchemy。

    尤其 sqlalchemy：domain 里出现 Session、select，
    说明业务规则已经绑死在具体存储上。
    """

    found = violations(
        "domain",
        (
            "app.infrastructure",
            "app.services",
            "app.api",
            "sqlalchemy",
        ),
    )

    assert found == []


def test_api_only_talks_to_services():
    """api 只允许 import services / schemas / db / core。"""

    allowed = (
        "app.services",
        "app.schemas",
        "app.db",
        "app.core",
    )

    found = []

    for path in layer_files("api"):

        for module in sorted(
            imported_modules(path)
        ):

            if not module.startswith("app."):
                continue

            if module.startswith(allowed):
                continue

            found.append(
                (
                    path.relative_to(
                        APP_DIR
                    ).as_posix(),
                    module,
                )
            )

    assert found == []


def test_guard_actually_inspects_code():
    """
    守卫自身要能看见 import。

    否则一条写错路径的规则会永远「通过」——
    这类测试最危险的失败方式就是静默失效。
    """

    samples = imported_modules(
        APP_DIR / "api" / "v1" / "analysis.py"
    )

    assert "fastapi" in samples

    assert any(
        module.startswith("app.services")
        for module in samples
    )


@pytest.mark.parametrize(
    "layer",
    (
        "api",
        "domain",
        "infrastructure",
    ),
)
def test_layers_exist(layer):
    """三层目录都存在，规则没有指向空目录。"""

    assert layer_files(layer)
