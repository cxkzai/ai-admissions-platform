"""Agent Service - 高级 API.

负责：
- 加载 Agent 配置（System Prompt + Tools）
- 管理对话循环（user → LLM → tools → LLM → ...）
- 持久化消息历史（DB）
- 返回最终回复 + 工具调用记录
"""

import time
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

from loguru import logger

from app.agents.prompts import get_agent_prompt
from app.agents.tools import get_agent_tools
from app.core.config import settings
from app.llm.factory import get_llm_adapter
from app.llm.types import ChatMessage, LLMResponse, ToolCall, ToolDefinition


@dataclass
class AgentRunResult:
    """Agent 一次运行的结果."""

    content: str
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    citations: list[dict[str, Any]] = field(default_factory=list)
    latency_ms: int = 0
    total_tokens: int = 0
    rounds: int = 1  # LLM 调用轮次（含工具调用循环）


@dataclass
class AgentRunRequest:
    """Agent 运行请求."""

    agent_slug: str
    user_message: str
    conversation_history: list[ChatMessage] | None = None
    metadata: dict[str, Any] | None = None
    max_tool_rounds: int = 5


class AgentService:
    """Agent 服务."""

    def __init__(self, llm_engine: str | None = None):
        self.llm_engine = llm_engine or settings.llm_default_engine
        self.llm = get_llm_adapter(self.llm_engine)

    async def run(self, req: AgentRunRequest) -> AgentRunResult:
        """运行 Agent 完成一轮对话."""

        system_prompt = get_agent_prompt(req.agent_slug)
        tools = get_agent_tools(req.agent_slug)

        # 构造 messages
        messages: list[ChatMessage] = [
            ChatMessage(role="system", content=system_prompt),
            *(req.conversation_history or []),
            ChatMessage(role="user", content=req.user_message),
        ]

        start = time.perf_counter()
        all_tool_calls: list[dict[str, Any]] = []
        rounds = 0

        # 工具调用循环
        for _ in range(req.max_tool_rounds):
            rounds += 1

            response: LLMResponse = await self.llm.chat(
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
                tools=tools if tools else None,
            )

            # 没有工具调用 → 直接返回
            if not response.tool_calls:
                latency_ms = int((time.perf_counter() - start) * 1000)
                return AgentRunResult(
                    content=response.content,
                    tool_calls=all_tool_calls,
                    citations=[],
                    latency_ms=latency_ms,
                    total_tokens=response.usage.total_tokens,
                    rounds=rounds,
                )

            # 有工具调用 → 执行工具
            # 1. 把 LLM 的回复（含 tool_calls）加到 messages
            messages.append(
                ChatMessage(
                    role="assistant",
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )

            # 2. 执行每个工具
            for tool_call in response.tool_calls:
                tool_result = await self._execute_tool(tool_call, tools)
                all_tool_calls.append(
                    {
                        "id": tool_call.id,
                        "name": tool_call.name,
                        "arguments": tool_call.arguments,
                        "result": tool_result,
                    }
                )
                # 3. 把工具结果回填给 LLM
                messages.append(
                    ChatMessage(
                        role="tool",
                        content=_format_tool_result(tool_result),
                        name=tool_call.name,
                        tool_call_id=tool_call.id,
                    )
                )

        # 超过最大轮次
        latency_ms = int((time.perf_counter() - start) * 1000)
        logger.warning(
            f"⚠️ Agent {req.agent_slug} 达到最大工具轮次 {req.max_tool_rounds}"
        )
        return AgentRunResult(
            content="抱歉，我需要更多时间来处理这个问题，请稍后再试。",
            tool_calls=all_tool_calls,
            citations=[],
            latency_ms=latency_ms,
            total_tokens=0,
            rounds=rounds,
        )

    async def stream(self, req: AgentRunRequest) -> AsyncIterator[str]:
        """流式运行（仅返回最终回复文本，不处理工具循环）.

        工具调用循环本身是阻塞的，所以流式仅对最后一轮 LLM 输出有效.
        """
        # 先完整跑一遍（处理工具调用）
        result = await self.run(req)

        # 把结果按字符 yield 模拟流式
        for char in result.content:
            yield char
            await _noop_sleep(0.005)

    async def _execute_tool(
        self, tool_call: ToolCall, tools: list[ToolDefinition]
    ) -> dict[str, Any]:
        """执行单个工具调用."""
        tool = next((t for t in tools if t.name == tool_call.name), None)
        if not tool or not tool.handler:
            return {"status": "error", "message": f"Tool {tool_call.name} not found"}

        try:
            logger.info(
                f"🔧 Tool call: {tool_call.name}({tool_call.arguments})"
            )
            result = await tool.handler(**tool_call.arguments)
            return result
        except Exception as e:
            logger.exception(f"Tool {tool_call.name} failed")
            return {"status": "error", "message": str(e)}


def _format_tool_result(result: dict[str, Any]) -> str:
    """把工具结果格式化为 LLM 可消费的文本."""
    import json

    return json.dumps(result, ensure_ascii=False)


async def _noop_sleep(seconds: float) -> None:
    import asyncio

    await asyncio.sleep(seconds)


# ===== 单例 =====

_service: AgentService | None = None


def get_agent_service() -> AgentService:
    """获取 Agent Service 单例."""
    global _service
    if _service is None:
        _service = AgentService()
    return _service