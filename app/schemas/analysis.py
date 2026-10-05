"""Analysis API 请求与响应模型。"""

from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


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

    enable_rag: bool | None = Field(
        default=None,
        description=(
            "本次分析是否启用 RAG 语义检索。"
            "留空则跟随服务端 RAG_ENABLED 配置。"
        ),
    )


class AnalysisReplanRequest(BaseModel):
    """在设计闸门修改问题并重新规划。"""

    question: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="修改后的分析问题",
    )


class AnalysisResponse(BaseModel):
    """Analysis Run 当前状态。"""

    run_id: str

    status: str

    repo_url: str

    question: str | None = None

    current_node: str | None = None

    progress: int = 0

    # 分析方案。只在设计闸门等待审批时返回。
    #
    # 以前这个字段不存在，用户被要求「批准分析方案」，
    # 但接口根本不返回方案内容 —— 页面上只能看到一个确认按钮，
    # 等于让人盲签。
    research_plan: dict | None = None

    # 本次 run 是否启用 RAG（跟随配置时为 None）。
    # 前端据此回显开关状态。
    rag_enabled: bool | None = None

    created_at: datetime

    @field_validator(
        "created_at",
        mode="before",
    )
    @classmethod
    def _assume_utc(
        cls,
        value,
    ):
        """
        给 naive 时间戳补上 UTC 时区。

        由来：模型用的是 `datetime.utcnow()`，
        存进 MySQL 的是**不带时区**的 UTC 时间。
        直接序列化出来是 `2026-10-05T08:05:57` ——
        JS 的 `new Date()` 会把它当**本地时间**解析，
        于是在 UTC+8 环境下，"刚刚跑完"的分析
        在页面上显示成「8 小时前」。

        修在这里而不是前端：
        接口本来就不该输出语义不明的时间戳，
        补上时区后所有消费方（前端、curl、脚本）拿到的都是准确时刻。
        """

        if (
            isinstance(value, datetime)
            and value.tzinfo is None
        ):
            return value.replace(
                tzinfo=timezone.utc
            )

        return value


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
