"""GitHub URL Parser 测试。"""

import pytest

from app.tools.github.parser import parse_github_url


def test_parse_github_url():
    """测试标准 GitHub Repository URL。"""

    owner, name = parse_github_url(
        "https://github.com/abc/agent-project"
    )

    assert owner == "abc"
    assert name == "agent-project"


def test_parse_git_url():
    """测试 .git 结尾的 Repository URL。"""

    owner, name = parse_github_url(
        "https://github.com/abc/agent-project.git"
    )

    assert owner == "abc"
    assert name == "agent-project"


def test_invalid_github_url():
    """测试非 GitHub URL。"""

    with pytest.raises(ValueError):
        parse_github_url(
            "https://gitlab.com/abc/project"
        )