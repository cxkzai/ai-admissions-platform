"""Anthropic Claude 适配器."""

import time
from collections.abc import AsyncIterator
from typing import Any

from anthropic import AsyncAnthropic
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


class ClaudeAdapter(BaseLLMAdapter):
    """Claude 3.5 Sonnet 适配器."""

    engine = "claude"

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-5-sonnet-20241022",
        base_url: str | None = None,
    ):
        super().__init__(api_key, model, base_url)
        client_kwargs: dict[str, Any] = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = AsyncAnthropic(**client_kwargs)

    @staticmethod
    def _to_anthropic_messages(
        messages: list[ChatMessage],
    ) -> tuple[str | None, list[dict[str, Any]]]:
        """分离 system 消息与其他消息."""
        system = None
        converted = []
        for m in messages:
            if m.role == "system":
                system = m.content
                continue
            if m.role == "tool":
                converted.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": m.tool_call_id,
                                "content": m.content,
                            }
                        ],
                    }
                )
                continue

            msg: dict[str, Any] = {"role": m.role, "content": m.content}

            if m.tool_calls:
                msg["content"] = [
                    {"type": "text", "text": m.content},
                    *[
                        {
                            "type": "tool_use",
                            "id": tc.id,
                            "name": tc.name,
                            "input": tc.arguments,
                        }
                        for tc in m.tool_calls
                    ],
                ]
            converted.append(msg)
        return system, converted

    @staticmethod
    def _to_anthropic_tools(tools: list[ToolDefinition]) -> list[dict[str, Any]]:
        """转换为 Anthropic 工具格式."""
        return [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.parameters,
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
        system, converted = self._to_anthropic_messages(messages)
        start = time.perf_counter()

        params: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": converted,
        }
        if system:
            params["system"] = system
        if tools:
            params["tools"] = self._to_anthropic_tools(tools)

        response = await self.client.messages.create(**params)
        latency_ms = int((time.perf_counter() - start) * 1000)

        # 解析响应
        content_text = ""
        tool_calls: list[ToolCall] = []
        for block in response.content:
            if block.type == "text":
                content_text += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        arguments=block.input,
                    )
                )

        usage = Usage(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens,
        )

        return LLMResponse(
            content=content_text,
            tool_calls=tool_calls,
            usage=usage,
            model=response.model,
            latency_ms=latency_ms,
            finish_reason=response.stop_reason or "stop",
            raw=response.model_dump() if hasattr(response, "model_dump") else None,
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
        system, converted = self._to_anthropic_messages(messages)

        params: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": converted,
        }
        if system:
            params["system"] = system
        if tools:
            params["tools"] = self._to_anthropic_tools(tools)

        async with self.client.messages.stream(**params) as stream:
            async for text in stream.text_stream:
                yield StreamChunk(content=text)

            # 结束时获取 usage
            final = await stream.get_final_message()
            yield StreamChunk(
                content="",
                finish_reason=final.stop_reason or "stop",
                usage=Usage(
                    prompt_tokens=final.usage.input_tokens,
                    completion_tokens=final.usage.output_tokens,
                    total_tokens=final.usage.input_tokens + final.usage.output_tokens,
                ),
            )

    async def close(self) -> None:
        await self.client.close()