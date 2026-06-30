"""Agent 工具定义与实现.

PRD §3.2.1 招生顾问 Agent 的 5 个工具:
- search_courses: 检索课程库
- search_teachers: 检索师资库
- check_schedule: 查询可预约时段
- book_audition: 预约试听
- send_to_feishu: 推送飞书通知

每个工具有：
- ToolDefinition：LLM Function Calling 的 schema
- handler：实际执行函数
"""

from typing import Any

from loguru import logger

from app.llm.types import ToolDefinition
from app.services.rag.service import get_rag_service


# ===== Tool 1: search_courses =====

SEARCH_COURSES_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "检索关键词或需求描述，例如：'8 岁零基础'、'想打 CSP-J'、'Python 基础'",
        },
        "top_k": {
            "type": "integer",
            "description": "返回几条结果",
            "default": 3,
            "minimum": 1,
            "maximum": 10,
        },
    },
    "required": ["query"],
}


async def _search_courses_handler(query: str, top_k: int = 3) -> dict[str, Any]:
    """检索课程库 - 走 RAG."""
    try:
        rag = get_rag_service()
        citations = await rag.search(query, top_k=top_k, kb_names=["courses"])
        return {
            "status": "ok",
            "query": query,
            "results": [
                {
                    "title": c.title,
                    "score": round(c.score, 3),
                    "content": c.content[:600],  # 截断节省 token
                    "source": c.source,
                }
                for c in citations
            ],
        }
    except Exception as e:
        logger.exception(f"search_courses 失败: {e}")
        return {"status": "error", "message": str(e)}


SEARCH_COURSES_TOOL = ToolDefinition(
    name="search_courses",
    description="检索课程库。基于孩子年龄、基础、目标返回最匹配的课程信息。回复家长关于'有什么课程'、'多少钱'、'哪个适合'等问题时必须使用此工具。",
    parameters=SEARCH_COURSES_SCHEMA,
    handler=_search_courses_handler,
)


# ===== Tool 2: search_teachers =====

SEARCH_TEACHERS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "检索关键词，例如：'Scratch 启蒙老师'、'信奥教练'、'清华背景'",
        },
        "top_k": {
            "type": "integer",
            "default": 3,
            "minimum": 1,
            "maximum": 10,
        },
    },
    "required": ["query"],
}


async def _search_teachers_handler(query: str, top_k: int = 3) -> dict[str, Any]:
    """检索师资库."""
    try:
        rag = get_rag_service()
        citations = await rag.search(query, top_k=top_k, kb_names=["teachers"])
        return {
            "status": "ok",
            "query": query,
            "results": [
                {
                    "title": c.title,
                    "score": round(c.score, 3),
                    "content": c.content[:600],
                    "source": c.source,
                }
                for c in citations
            ],
        }
    except Exception as e:
        logger.exception(f"search_teachers 失败: {e}")
        return {"status": "error", "message": str(e)}


SEARCH_TEACHERS_TOOL = ToolDefinition(
    name="search_teachers",
    description="检索师资库。家长问'老师是什么背景'、'哪个老师教得好'等问题时使用。",
    parameters=SEARCH_TEACHERS_SCHEMA,
    handler=_search_teachers_handler,
)


# ===== Tool 3: check_schedule =====

CHECK_SCHEDULE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "date_range": {
            "type": "string",
            "description": "日期范围，例如：'本周'、'本周末'、'2024-03-15 至 2024-03-17'",
            "default": "本周末",
        },
        "course_type": {
            "type": "string",
            "description": "课程类型（Scratch/Python/C++ 等），None 表示不限",
        },
    },
}


async def _check_schedule_handler(
    date_range: str = "本周末",
    course_type: str | None = None,
) -> dict[str, Any]:
    """查询可预约试听时段 - 演示模式返回 Mock 数据.

    生产实现：连接教务系统 API，查询真实排课.
    """
    # Mock 数据：演示用
    schedule = [
        {
            "date": "2024-03-16",
            "time": "10:00-11:00",
            "course_type": "Scratch 启蒙",
            "teacher": "陈思雨",
            "campus": "春熙路校区",
            "slots_available": 3,
        },
        {
            "date": "2024-03-16",
            "time": "14:00-15:00",
            "course_type": "Python 基础",
            "teacher": "李梦琪",
            "campus": "高新校区",
            "slots_available": 5,
        },
        {
            "date": "2024-03-17",
            "time": "10:00-11:00",
            "course_type": "Scratch 启蒙",
            "teacher": "王晓明",
            "campus": "双流校区",
            "slots_available": 4,
        },
        {
            "date": "2024-03-17",
            "time": "15:00-16:00",
            "course_type": "C++ 算法",
            "teacher": "张子豪",
            "campus": "高新校区",
            "slots_available": 2,
        },
    ]

    if course_type:
        schedule = [s for s in schedule if course_type in s["course_type"]]

    return {
        "status": "ok",
        "date_range": date_range,
        "available_slots": schedule,
        "note": "演示模式返回 Mock 数据，生产环境对接教务系统 API",
    }


CHECK_SCHEDULE_TOOL = ToolDefinition(
    name="check_schedule",
    description="查询可预约的试听课时段。家长表示想试听时调用。",
    parameters=CHECK_SCHEDULE_SCHEMA,
    handler=_check_schedule_handler,
)


# ===== Tool 4: book_audition =====

BOOK_AUDITION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "parent_name": {
            "type": "string",
            "description": "家长称呼，例如'李妈妈'、'王爸爸'",
        },
        "child_name": {
            "type": "string",
            "description": "孩子姓名",
        },
        "child_age": {
            "type": "integer",
            "description": "孩子年龄",
        },
        "phone": {
            "type": "string",
            "description": "家长手机号（11 位）",
        },
        "slot": {
            "type": "string",
            "description": "预约的时段，例如'2024-03-16 10:00 春熙路校区'",
        },
        "course_type": {
            "type": "string",
            "description": "试听课程类型",
        },
    },
    "required": ["parent_name", "child_name", "phone", "slot"],
}


async def _book_audition_handler(
    parent_name: str,
    child_name: str,
    phone: str,
    slot: str,
    child_age: int | None = None,
    course_type: str | None = None,
) -> dict[str, Any]:
    """预约试听 - 演示模式返回 Mock 成功.

    生产实现：
    1. 写入数据库 leads 表
    2. 创建试听记录
    3. 推送飞书通知给招生顾问
    """
    # Mock 成功
    booking_id = f"AUD-{slot.replace(' ', '').replace('-', '')[:8]}-{phone[-4:]}"
    return {
        "status": "ok",
        "booking_id": booking_id,
        "parent_name": parent_name,
        "child_name": child_name,
        "child_age": child_age,
        "phone": phone,
        "slot": slot,
        "course_type": course_type,
        "confirmation_message": f"试听预约成功！{parent_name}，我们会在 {slot} 之前 1 小时给您发送提醒短信。请保持手机畅通。",
        "note": "演示模式，未真正入库",
    }


BOOK_AUDITION_TOOL = ToolDefinition(
    name="book_audition",
    description="预约试听课。需要家长提供称呼、孩子姓名、手机号，并从 check_schedule 返回的时段中选一个。",
    parameters=BOOK_AUDITION_SCHEMA,
    handler=_book_audition_handler,
)


# ===== Tool 5: send_to_feishu =====

SEND_TO_FEISHU_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "message_type": {
            "type": "string",
            "enum": ["new_lead", "audition_booked", "followup_reminder"],
            "description": "消息类型",
        },
        "title": {
            "type": "string",
            "description": "通知标题",
        },
        "content": {
            "type": "string",
            "description": "通知正文（Markdown）",
        },
        "assignee": {
            "type": "string",
            "description": "接收人（招生顾问姓名）",
            "default": "招生顾问",
        },
    },
    "required": ["message_type", "title", "content"],
}


async def _send_to_feishu_handler(
    message_type: str,
    title: str,
    content: str,
    assignee: str = "招生顾问",
) -> dict[str, Any]:
    """发送飞书通知 - 演示模式.

    生产实现：调用飞书群机器人 Webhook 发送 Markdown 卡片.
    """
    # 这里应该是 HTTP POST 到 webhook_url
    # 演示模式仅打印
    logger.info(
        f"📨 [飞书通知] To: {assignee} | Type: {message_type} | Title: {title}"
    )
    return {
        "status": "ok",
        "mode": "demo",
        "message_type": message_type,
        "title": title,
        "would_send_to": assignee,
        "note": "演示模式：未真实推送。生产环境需配置 FEISHU_WEBHOOK_URL",
    }


SEND_TO_FEISHU_TOOL = ToolDefinition(
    name="send_to_feishu",
    description="发送通知给内部招生顾问（飞书群机器人）。新线索入库、试听预约成功、跟进提醒时调用。",
    parameters=SEND_TO_FEISHU_SCHEMA,
    handler=_send_to_feishu_handler,
)


# ===== 工具集字典 =====

AGENT_TOOLS: dict[str, list[ToolDefinition]] = {
    "admission-consultant": [
        SEARCH_COURSES_TOOL,
        SEARCH_TEACHERS_TOOL,
        CHECK_SCHEDULE_TOOL,
        BOOK_AUDITION_TOOL,
        SEND_TO_FEISHU_TOOL,
    ],
    "course-consultant": [
        SEARCH_COURSES_TOOL,
        SEARCH_TEACHERS_TOOL,
    ],
    "academic-teacher": [
        SEARCH_TEACHERS_TOOL,
        SEND_TO_FEISHU_TOOL,
    ],
    "internal-assistant": [
        SEARCH_COURSES_TOOL,
        SEARCH_TEACHERS_TOOL,
    ],
}


def get_agent_tools(slug: str) -> list[ToolDefinition]:
    """获取 Agent 可用的工具列表."""
    return AGENT_TOOLS.get(slug, [])