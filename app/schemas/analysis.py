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


class AnalysisDeepDiveResponse(BaseModel):
    """
    单个模块的深挖报告。

    默认报告每章只给要点；
    这一份是某个模块的实现细节展开。
    """

    run_id: str

    module: str

    title: str | None = None

    # 写入磁盘的报告文件信息（path / format）。
    report: dict | None = None

    # 报告正文，便于调用方直接展示。
    content: str | None = None

    # 本次深挖读取了哪些文件。
    # 是「比默认报告看得多」的证据，
    # 也让读者知道结论的覆盖面。
    files_read: list[str] = []

    # 展开了多少项实现明细。
    details: int = 0

class AnalysisJsonReportResponse(BaseModel):
    """
    结构化报告（Phase 14.2）。

    markdown 是给人读的排版结果；
    这一份是同一份数据的结构化形态，
    字段含义与 schema_version 见
    ReportService.build_document()。
    """

    run_id: str

    status: str

    document: dict | None = None


class LearningPathResponse(BaseModel):
    """
    项目的学习路线（Phase 14.1）。

    基于已有分析结果生成，
    不重新采集数据。
    """

    run_id: str

    available: bool = False

    reason: str | None = None

    # 五个小节：学习顺序 / 需要掌握的技术 /
    # 核心源码 / 推荐阅读路径 / 改造建议
    sections: dict = {}

    report: dict | None = None

    content: str = ""
