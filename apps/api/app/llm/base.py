"""LLM 适配器抽象基类."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from app.llm.types import (
    ChatMessage,
    LLMResponse,
    StreamChunk,
    ToolDefinition,
)


class BaseLLMAdapter(ABC):
    """所有 LLM 适配器的统一接口."""

    engine: str = "base"

    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    @abstractmethod
    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: list[ToolDefinition] | None = None,
        **kwargs: object,
    ) -> LLMResponse:
        """普通对话（支持可选工具调用）."""

    @abstractmethod
    def stream_chat(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: list[ToolDefinition] | None = None,
        **kwargs: object,
    ) -> AsyncIterator[StreamChunk]:
        """流式对话."""

    async def close(self) -> None:
        """关闭底层客户端."""