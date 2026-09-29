"""
Comparison API 数据契约。
"""

from typing import Any

from pydantic import BaseModel, Field


class ComparisonCreateRequest(BaseModel):
    """创建多项目比较请求。"""

    run_ids: list[str] = Field(
        ...,
        min_length=2,
        max_length=2,
        description=(
            "两个已经完成的 Analysis Run ID"
        ),
    )


class ComparisonProjectResponse(BaseModel):
    """比较项目摘要。"""

    run_id: str
    repository_id: int | None = None
    repository_url: str | None = None
    repository_name: str | None = None
    status: str


class ComparisonResponse(BaseModel):
    """多项目比较结果。"""

    comparison_id: str

    status: str

    evidence_based: bool

    projects: list[
        ComparisonProjectResponse
    ]

    comparison: dict[str, Any]