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
    LLM_PROVIDER: str = "deepseek"
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "deepseek-chat"

    # Embedding
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"

    EMBEDDING_PROVIDER: str = "ollama"
    EMBEDDING_MODEL: str = "bge-m3"

    # GitHub
    GITHUB_TOKEN: str = ""

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