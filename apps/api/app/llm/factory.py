"""LLM 适配器工厂."""

from functools import lru_cache

from app.core.config import settings
from app.llm.base import BaseLLMAdapter
from app.llm.claude import ClaudeAdapter
from app.llm.deepseek import DeepSeekAdapter
from app.llm.openai import OpenAIAdapter


@lru_cache(maxsize=4)
def get_llm_adapter(engine: str | None = None) -> BaseLLMAdapter:
    """获取 LLM 适配器单例.

    Args:
        engine: 'claude' | 'deepseek' | 'openai'，None 则用配置默认引擎
    """
    engine = engine or settings.llm_default_engine

    if engine == "claude":
        return ClaudeAdapter(
            api_key=settings.anthropic_api_key,
            model=settings.anthropic_model,
            base_url=settings.anthropic_base_url,
        )
    if engine == "deepseek":
        return DeepSeekAdapter(
            api_key=settings.deepseek_api_key,
            model=settings.deepseek_model,
            base_url=settings.deepseek_base_url,
        )
    if engine == "openai":
        return OpenAIAdapter(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
        )

    raise ValueError(
        f"Unknown LLM engine: {engine}. Choose from: claude / deepseek / openai"
    )


def reset_llm_adapter_cache() -> None:
    """清空适配器缓存（用于测试或重载配置）."""
    get_llm_adapter.cache_clear()