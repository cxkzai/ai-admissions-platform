"""LLM 适配层测试."""

import os
from unittest.mock import patch

import pytest

from app.llm.base import BaseLLMAdapter
from app.llm.claude import ClaudeAdapter
from app.llm.deepseek import DeepSeekAdapter
from app.llm.factory import get_llm_adapter
from app.llm.openai import OpenAIAdapter
from app.llm.types import ChatMessage, ToolDefinition


class TestLLMTypes:
    """类型测试（不需要 API key）."""

    def test_chat_message_creation(self) -> None:
        msg = ChatMessage(role="user", content="你好")
        assert msg.role == "user"
        assert msg.content == "你好"

    def test_tool_definition_creation(self) -> None:
        tool = ToolDefinition(
            name="search_courses",
            description="检索课程",
            parameters={
                "type": "object",
                "properties": {"keyword": {"type": "string"}},
            },
        )
        assert tool.name == "search_courses"
        assert "keyword" in tool.parameters["properties"]


class TestLLMFactory:
    """工厂测试."""

    def setup_method(self) -> None:
        """每个测试前清缓存."""
        from app.llm.factory import reset_llm_adapter_cache
        reset_llm_adapter_cache()

    def test_factory_claude(self) -> None:
        with patch.dict(
            os.environ,
            {
                "ANTHROPIC_API_KEY": "test-key",
                "LLM_DEFAULT_ENGINE": "claude",
            },
        ):
            from app.llm.factory import reset_llm_adapter_cache
            reset_llm_adapter_cache()
            adapter = get_llm_adapter("claude")
            assert isinstance(adapter, ClaudeAdapter)
            assert adapter.engine == "claude"

    def test_factory_deepseek(self) -> None:
        with patch.dict(
            os.environ,
            {
                "DEEPSEEK_API_KEY": "test-key",
                "LLM_DEFAULT_ENGINE": "deepseek",
            },
        ):
            from app.llm.factory import reset_llm_adapter_cache
            reset_llm_adapter_cache()
            adapter = get_llm_adapter("deepseek")
            assert isinstance(adapter, DeepSeekAdapter)
            assert adapter.engine == "deepseek"

    def test_factory_openai(self) -> None:
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "test-key",
                "LLM_DEFAULT_ENGINE": "openai",
            },
        ):
            from app.llm.factory import reset_llm_adapter_cache
            reset_llm_adapter_cache()
            adapter = get_llm_adapter("openai")
            assert isinstance(adapter, OpenAIAdapter)

    def test_factory_invalid_engine(self) -> None:
        with pytest.raises(ValueError, match="Unknown LLM engine"):
            get_llm_adapter("invalid")


@pytest.mark.skip(reason="需要真实 API key，仅在 CI 集成测试中运行")
class TestRealAPI:
    """真实 API 集成测试（默认跳过）."""

    async def test_claude_chat(self) -> None:
        adapter = get_llm_adapter("claude")
        response = await adapter.chat(
            [ChatMessage(role="user", content="用一句话介绍你自己")],
            max_tokens=100,
        )
        assert response.content
        assert response.usage.total_tokens > 0

    async def test_deepseek_chat(self) -> None:
        adapter = get_llm_adapter("deepseek")
        response = await adapter.chat(
            [ChatMessage(role="user", content="用一句话介绍你自己")],
            max_tokens=100,
        )
        assert response.content
        assert response.usage.total_tokens > 0