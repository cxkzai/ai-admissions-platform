"""LLM 适配层共享类型."""

from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any, Literal


Role = Literal["system", "user", "assistant", "tool"]


@dataclass
class ChatMessage:
    """统一的消息格式."""

    role: Role
    content: str
    name: str | None = None  # for tool role
    tool_call_id: str | None = None
    tool_calls: list["ToolCall"] | None = None


@dataclass
class ToolDefinition:
    """工具定义 - 适配 OpenAI Function Calling 格式."""

    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema
    handler: Any = None  # 实际执行函数，可选


@dataclass
class ToolCall:
    """LLM 调用的工具."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Usage:
    """Token 使用统计."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass
class LLMResponse:
    """统一的 LLM 响应."""

    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    model: str = ""
    latency_ms: int = 0
    finish_reason: str = "stop"
    raw: dict[str, Any] | None = None  # 原始响应（调试用）


@dataclass
class StreamChunk:
    """流式输出的单个 chunk."""

    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str | None = None
    usage: Usage | None = None


# 引擎类型
EngineType = Literal["claude", "deepseek", "openai"]