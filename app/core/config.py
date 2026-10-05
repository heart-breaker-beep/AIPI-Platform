"""项目统一配置：负责从环境变量和 .env 加载应用、数据库和 AI 服务配置。"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用全局配置，统一管理项目运行所需的环境参数。"""

    # Application
    APP_NAME: str = "AI Agent GitHub Project Intelligence Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # MySQL
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "agent_intelligence"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # LLM
    #
    # DeepSeek 提供 OpenAI 兼容接口，
    # 因此 openai SDK 直连该 base_url 即可。
    LLM_PROVIDER: str = "deepseek"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "deepseek-chat"
    LLM_BASE_URL: str = "https://api.deepseek.com"
    LLM_TIMEOUT: float = 120.0

    # 单次回复的最大 token 数。
    #
    # 必须显式设置：综合分析要输出
    # 六个维度的判断段落 + 摘要，
    # 用 API 默认值会被截断，
    # 截断的 JSON 解析必然失败，
    # 报告就会退化成「综合分析不可用」。
    LLM_MAX_TOKENS: int = 8192

    # Embedding
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"

    EMBEDDING_PROVIDER: str = "ollama"
    EMBEDDING_MODEL: str = "bge-m3"

    # GitHub
    GITHUB_TOKEN: str = ""

    # RAG（语义检索）
    #
    # 默认关闭。
    #
    # 打开后，证据环节会先把仓库源码索引进 Qdrant，
    # 再按六个维度分别做语义检索，把命中的代码片段
    # 叠加进证据清单（而不是替换掉结构分析产出的证据）。
    #
    # 为什么默认关：
    #
    # 1. 索引要额外读 GitHub 文件、调 Ollama 嵌入，
    #    每次分析会多等一分钟左右；
    # 2. 它的增益是否为正，取决于仓库规模与提问方式，
    #    需要实测对照才能判断 —— 默认开会让所有分析
    #    都承担这个未经检验的成本。
    #
    # 打开方式：.env 里设 RAG_ENABLED=true
    RAG_ENABLED: bool = False

    # 单次索引最多收录多少个 .py 文件。
    #
    # 已读文件（约 20 个，正文已在内存里）不额外花钱，
    # 其余按剩余名额去 GitHub 补读 —— 补读是串行的，
    # 每个约 0.9 秒，所以这个值直接决定额外耗时。
    # 80 ≈ 已读 20 + 补读 60 ≈ 多等 70 秒。
    RAG_INDEX_MAX_FILES: int = 80

    # 每个维度取前几条检索结果。
    #
    # 六个维度 × 3 条 = 最多 18 条候选，
    # 再去重、按相似度截断到 RAG_MAX_EVIDENCE。
    RAG_LIMIT_PER_DIMENSION: int = 3

    # 检索证据并入证据清单后的总上限。
    #
    # 与 ReportSynthesisSkill.MAX_EVIDENCE 一致：
    # 超出部分进不了综合分析，等于白检索。
    RAG_MAX_EVIDENCE: int = 12

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        """生成 SQLAlchemy 异步 MySQL 连接地址。"""
        return (
            f"mysql+asyncmy://"
            f"{self.MYSQL_USER}:"
            f"{self.MYSQL_PASSWORD}@"
            f"{self.MYSQL_HOST}:"
            f"{self.MYSQL_PORT}/"
            f"{self.MYSQL_DATABASE}"
        )


@lru_cache
def get_settings() -> Settings:
    """获取全局配置实例，整个应用复用同一个 Settings 对象。"""
    return Settings()