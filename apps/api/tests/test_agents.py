"""智能体服务测试.

- 单元测试：不调用 LLM，验证 Prompt / Tools 配置
- 集成测试：默认跳过，需要真实 LLM API key
"""

import pytest

from app.agents.prompts import (
    ADMISSION_CONSULTANT_PROMPT,
    AGENT_PROMPTS,
    get_agent_prompt,
)
from app.agents.tools import (
    AGENT_TOOLS,
    BOOK_AUDITION_TOOL,
    CHECK_SCHEDULE_TOOL,
    SEARCH_COURSES_TOOL,
    SEARCH_TEACHERS_TOOL,
    SEND_TO_FEISHU_TOOL,
    get_agent_tools,
)


class TestAgentPrompts:
    """Prompt 测试."""

    def test_all_prompts_defined(self) -> None:
        assert len(AGENT_PROMPTS) == 4
        assert "admission-consultant" in AGENT_PROMPTS
        assert "course-consultant" in AGENT_PROMPTS
        assert "academic-teacher" in AGENT_PROMPTS
        assert "internal-assistant" in AGENT_PROMPTS

    def test_admission_consultant_prompt_completeness(self) -> None:
        prompt = ADMISSION_CONSULTANT_PROMPT
        # 必备要素
        assert "角色定位" in prompt or "角色" in prompt
        assert "沟通风格" in prompt or "Tone" in prompt
        assert "边界" in prompt or "Guardrails" in prompt or "禁止" in prompt
        # 必须提到工具
        assert "search_courses" in prompt
        assert "search_teachers" in prompt
        assert "book_audition" in prompt

    def test_get_agent_prompt_unknown_fallback(self) -> None:
        # 未知 slug 应该返回默认 prompt
        prompt = get_agent_prompt("unknown-agent")
        assert prompt == ADMISSION_CONSULTANT_PROMPT

    def test_all_prompts_have_minimum_length(self) -> None:
        # 每个 prompt 至少 500 字（保证质量）
        for slug, prompt in AGENT_PROMPTS.items():
            assert len(prompt) > 500, f"{slug} prompt too short: {len(prompt)}"


class TestAgentTools:
    """工具测试."""

    def test_admission_consultant_has_all_5_tools(self) -> None:
        tools = get_agent_tools("admission-consultant")
        assert len(tools) == 5

        tool_names = {t.name for t in tools}
        assert "search_courses" in tool_names
        assert "search_teachers" in tool_names
        assert "check_schedule" in tool_names
        assert "book_audition" in tool_names
        assert "send_to_feishu" in tool_names

    def test_tools_have_required_fields(self) -> None:
        for slug, tools in AGENT_TOOLS.items():
            for tool in tools:
                assert tool.name, f"{slug} tool missing name"
                assert tool.description, f"{slug} tool missing description"
                assert tool.parameters, f"{slug} tool missing parameters"
                assert "type" in tool.parameters, f"{slug} {tool.name} parameters missing 'type'"
                assert tool.parameters["type"] == "object", f"{slug} {tool.name} must be object schema"

    def test_unknown_agent_returns_empty_tools(self) -> None:
        assert get_agent_tools("unknown") == []


class TestToolSchemas:
    """工具 schema 细节测试."""

    def test_search_courses_schema(self) -> None:
        schema = SEARCH_COURSES_TOOL.parameters
        assert "query" in schema["properties"]
        assert schema["required"] == ["query"]

    def test_book_audition_schema(self) -> None:
        schema = BOOK_AUDITION_TOOL.parameters
        required = schema["required"]
        assert "parent_name" in required
        assert "phone" in required
        assert "slot" in required

    def test_send_to_feishu_schema(self) -> None:
        schema = SEND_TO_FEISHU_TOOL.parameters
        assert "message_type" in schema["properties"]
        assert "enum" in schema["properties"]["message_type"]


class TestToolHandlers:
    """工具 handler 单元测试（不依赖 LLM）."""

    @pytest.mark.asyncio
    async def test_check_schedule_returns_mock_data(self) -> None:
        result = await CHECK_SCHEDULE_TOOL.handler(date_range="本周末")
        assert result["status"] == "ok"
        assert len(result["available_slots"]) > 0

    @pytest.mark.asyncio
    async def test_book_audition_returns_booking_id(self) -> None:
        result = await BOOK_AUDITION_TOOL.handler(
            parent_name="李妈妈",
            child_name="小明",
            phone="13800138000",
            slot="2024-03-16 10:00 春熙路校区",
        )
        assert result["status"] == "ok"
        assert "booking_id" in result
        assert result["parent_name"] == "李妈妈"

    @pytest.mark.asyncio
    async def test_send_to_feishu_demo_mode(self) -> None:
        result = await SEND_TO_FEISHU_TOOL.handler(
            message_type="new_lead",
            title="新线索",
            content="测试内容",
        )
        assert result["status"] == "ok"
        assert result["mode"] == "demo"


@pytest.mark.skip(reason="需要真实 LLM API key，仅在集成测试中运行")
class TestAgentIntegration:
    """集成测试."""

    async def test_admission_agent_run(self) -> None:
        from app.agents.service import AgentRunRequest, get_agent_service

        service = get_agent_service()
        result = await service.run(
            AgentRunRequest(
                agent_slug="admission-consultant",
                user_message="我家孩子 8 岁想学编程，有什么课程？",
            )
        )
        assert result.content
        assert result.rounds >= 1

    async def test_tool_call_flow(self) -> None:
        from app.agents.service import AgentRunRequest, get_agent_service

        service = get_agent_service()
        result = await service.run(
            AgentRunRequest(
                agent_slug="admission-consultant",
                user_message="我想了解 Scratch 和 Python 的区别",
            )
        )
        # 应该触发 search_courses 工具
        tool_names = [t["name"] for t in result.tool_calls]
        assert "search_courses" in tool_names