"""应用配置加载.

使用 pydantic-settings 从环境变量与 .env 文件加载配置.
"""

import json
from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """应用全局配置."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ===== 应用基础 =====
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    app_name: str = "AI-Admissions Platform"
    app_version: str = "0.1.0"
    app_secret_key: str = "change-me"

    # ===== API 服务 =====
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_base_url: str = "http://localhost:8000"
    # NoDecode 禁用 pydantic-settings 内置的 json.loads 解析（它会拒绝逗号分隔）
    # 由下面的 _parse_cors_origins 自定义处理：接受逗号分隔或 JSON 数组
    api_cors_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"],
    )

    @field_validator("api_cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v: object) -> object:
        """允许 .env 写逗号分隔字符串或 JSON 数组两种格式."""
        if isinstance(v, str):
            s = v.strip()
            if s.startswith("["):
                return json.loads(s)
            return [item.strip() for item in s.split(",") if item.strip()]
        return v

    # ===== 数据库 =====
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/edu_admissions"
    )
    database_url_sync: str = (
        "postgresql://postgres:postgres@localhost:5432/edu_admissions"
    )

    # ===== Redis =====
    redis_url: str = "redis://localhost:6379/0"

    # ===== LLM 引擎 =====
    # 主力 = DeepSeek（中文好、价格低、面试官有代入感）
    # 备选 = claude（演示效果最佳）、openai（兼容性强）
    llm_default_engine: Literal["claude", "deepseek", "openai"] = "deepseek"

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    anthropic_base_url: str = "https://api.anthropic.com"

    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    deepseek_base_url: str = "https://api.deepseek.com"

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # ===== Embedding =====
    embedding_provider: Literal["openai", "bge"] = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # ===== 向量库 =====
    vector_store: Literal["chroma", "pgvector"] = "chroma"
    chroma_persist_dir: str = "./chroma_data"

    # ===== IM Webhook =====
    feishu_webhook_url: str = ""
    feishu_webhook_secret: str = ""
    wecom_webhook_url: str = ""

    # ===== 日志 =====
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """获取单例配置."""
    return Settings()


settings = get_settings()