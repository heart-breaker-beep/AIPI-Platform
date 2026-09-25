"""Analysis API 的请求和响应数据模型。"""

from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisCreateRequest(BaseModel):
    """创建项目分析任务时的请求参数。"""

    repo_url: str = Field(
        ...,
        min_length=1,
        description="GitHub repository URL",
    )

    question: str | None = Field(
        default=None,
        max_length=5000,
        description="本次项目分析问题，用于 Run Memory 和 Context Manager",
    )


class AnalysisResponse(BaseModel):
    """分析任务的基础响应信息。"""

    run_id: str
    status: str
    repo_url: str
    created_at: datetime