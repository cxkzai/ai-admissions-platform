"""会话表模型."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.lead import Lead

if TYPE_CHECKING:
    from app.models.agent import Agent
    from app.models.message import Message


class Conversation(UUIDMixin, TimestampMixin, Base):
    """会话表 - 一个会话包含多轮对话."""

    __tablename__ = "conversations"
    __table_args__ = (
        Index("ix_conversations_lead_id", "lead_id"),
        Index("ix_conversations_agent_id", "agent_id"),
        Index("ix_conversations_status", "status"),
    )

    lead_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
    )
    agent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("agents.id", ondelete="SET NULL"),
    )

    channel: Mapped[str] = mapped_column(
        Enum("web", "wechat", "feishu", "mock", name="conversation_channel"),
        default="web",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        Enum("active", "closed", name="conversation_status"),
        default="active",
        nullable=False,
    )

    # 反向关系
    lead: Mapped[Lead | None] = relationship(back_populates="conversations")
    agent: Mapped["Agent | None"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )