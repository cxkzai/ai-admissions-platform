"""Chat API 路由.

POST /api/v1/chat/message  - 发送消息给智能体
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.agents.service import AgentRunRequest, get_agent_service
from app.llm.types import ChatMessage

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessageRequest(BaseModel):
    """对话消息请求."""

    conversation_id: str | None = None
    agent_slug: str = Field(..., description="Agent 标识")
    message: str = Field(..., min_length=1, max_length=4000)
    history: list[dict] | None = Field(
        default=None,
        description="历史消息 [{role, content, ...}]",
    )
    metadata: dict | None = None


class CitationResponse(BaseModel):
    """RAG 引用."""

    title: str
    score: float
    source: str


class ChatMessageResponse(BaseModel):
    """对话消息响应."""

    conversation_id: str
    message_id: str
    content: str
    tool_calls: list[dict] = []
    citations: list[CitationResponse] = []
    latency_ms: int
    rounds: int


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(req: ChatMessageRequest) -> ChatMessageResponse:
    """发送消息给智能体并返回回复."""
    try:
        service = get_agent_service()

        # 转换 history
        history: list[ChatMessage] = []
        if req.history:
            for m in req.history:
                history.append(
                    ChatMessage(
                        role=m.get("role", "user"),
                        content=m.get("content", ""),
                    )
                )

        run_req = AgentRunRequest(
            agent_slug=req.agent_slug,
            user_message=req.message,
            conversation_history=history,
            metadata=req.metadata,
        )

        result = await service.run(run_req)

        # 提取 citations（从工具调用的 search_courses / search_teachers 结果）
        citations = _extract_citations(result.tool_calls)

        import uuid

        return ChatMessageResponse(
            conversation_id=req.conversation_id or str(uuid.uuid4()),
            message_id=str(uuid.uuid4()),
            content=result.content,
            tool_calls=result.tool_calls,
            citations=citations,
            latency_ms=result.latency_ms,
            rounds=result.rounds,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def _extract_citations(tool_calls: list[dict]) -> list[CitationResponse]:
    """从工具调用结果中提取 RAG 引用."""
    citations: list[CitationResponse] = []

    for tc in tool_calls:
        if tc.get("name") not in ("search_courses", "search_teachers", "search_cases"):
            continue
        result = tc.get("result", {})
        if not isinstance(result, dict):
            continue
        for r in result.get("results", []):
            citations.append(
                CitationResponse(
                    title=r.get("title", "未知"),
                    score=r.get("score", 0.0),
                    source=r.get("source", ""),
                )
            )

    return citations