"""
Repository 数据访问层兼容入口。

真正的 RepositoryRepository 实现位于：

    app.repositories.repository_basic
"""

from app.repositories.repository_basic import (
    RepositoryRepository,
)


__all__ = [
    "RepositoryRepository",
]