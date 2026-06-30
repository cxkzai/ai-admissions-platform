"""DeepSeek 适配器（OpenAI 兼容协议）."""

import time
from collections.abc import AsyncIterator
from typing import Any

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from app.llm.base import BaseLLMAdapter
from app.llm.types import (
    ChatMessage,
    LLMResponse,
    StreamChunk,
    ToolCall,
    ToolDefinition,
    Usage,
)


class DeepSeekAdapter(BaseLLMAdapter):
    """DeepSeek 适配器 - 使用 OpenAI 兼容协议."""

    engine = "deepseek"

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
    ):
        super().__init__(api_key, model, base_url)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    @staticmethod
    def _to_openai_messages(messages: list[ChatMessage]) -> list[dict[str, Any]]:
        """转换为 OpenAI Chat 格式."""
        converted = []
        for m in messages:
            msg: dict[str, Any] = {"role": m.role, "content": m.content}
            if m.role == "tool":
                msg["tool_call_id"] = m.tool_call_id
                msg["name"] = m.name or "tool"
            if m.tool_calls:
                msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": _json_dumps(tc.arguments),
                        },
                    }
                    for tc in m.tool_calls
                ]
                # OpenAI 要求 assistant 有 tool_calls 时 content 可为空
                if not msg["content"]:
                    msg["content"] = None
            converted.append(msg)
        return converted

    @staticmethod
    def _to_openai_tools(tools: list[ToolDefinition]) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.parameters,
                },
            }
            for t in tools
        ]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
    )
    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: list[ToolDefinition] | None = None,
        **kwargs: object,
    ) -> LLMResponse:
        converted = self._to_openai_messages(messages)
        start = time.perf_counter()

        params: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": converted,
        }
        if tools:
            params["tools"] = self._to_openai_tools(tools)

        response = await self.client.chat.completions.create(**params)
        latency_ms = int((time.perf_counter() - start) * 1000)

        choice = response.choices[0]
        content = choice.message.content or ""
        tool_calls: list[ToolCall] = []
        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                import json
                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        name=tc.function.name,
                        arguments=json.loads(tc.function.arguments or "{}"),
                    )
                )

        usage = Usage(
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=response.usage.completion_tokens if response.usage else 0,
            total_tokens=response.usage.total_tokens if response.usage else 0,
        )

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            latency_ms=latency_ms,
            finish_reason=choice.finish_reason or "stop",
        )

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: list[ToolDefinition] | None = None,
        **kwargs: object,
    ) -> AsyncIterator[StreamChunk]:
        converted = self._to_openai_messages(messages)

        params: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": converted,
            "stream": True,
            "stream_options": {"include_usage": True},
        }
        if tools:
            params["tools"] = self._to_openai_tools(tools)

        stream = await self.client.chat.completions.create(**params)
        async for chunk in stream:
            if chunk.choices:
                delta = chunk.choices[0].delta
                content = delta.content or ""
                yield StreamChunk(content=content)
            elif chunk.usage:
                yield StreamChunk(
                    content="",
                    finish_reason="stop",
                    usage=Usage(
                        prompt_tokens=chunk.usage.prompt_tokens,
                        completion_tokens=chunk.usage.completion_tokens,
                        total_tokens=chunk.usage.total_tokens,
                    ),
                )

    async def close(self) -> None:
        await self.client.close()


def _json_dumps(obj: object) -> str:
    import json
    return json.dumps(obj, ensure_ascii=False)