"""Analysis API 请求与响应模型。"""

from datetime import datetime

from pydantic import BaseModel, Field


class AnalysisCreateRequest(BaseModel):
    """创建项目分析任务。"""

    repo_url: str = Field(
        ...,
        min_length=1,
        description="GitHub repository URL",
    )

    question: str | None = Field(
        default=None,
        max_length=5000,
        description="本次项目分析问题",
    )


class AnalysisResponse(BaseModel):
    """Analysis Run 当前状态。"""

    run_id: str

    status: str

    repo_url: str

    question: str | None = None

    current_node: str | None = None

    progress: int = 0

    created_at: datetime


class AnalysisReportResponse(BaseModel):
    """最终项目分析报告。"""

    run_id: str

    status: str

    report: dict | None = None