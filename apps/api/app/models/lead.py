"""线索表模型."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class Lead(UUIDMixin, TimestampMixin, Base):
    """线索表 - 来自各渠道的潜在家长."""

    __tablename__ = "leads"
    __table_args__ = (
        Index("ix_leads_stage", "stage"),
        Index("ix_leads_source", "source"),
        Index("ix_leads_assigned_agent_id", "assigned_agent_id"),
    )

    name: Mapped[str | None] = mapped_column(String(64))
    phone: Mapped[str | None] = mapped_column(String(32))
    wechat: Mapped[str | None] = mapped_column(String(64))
    child_age: Mapped[int | None] = mapped_column()
    interest_subject: Mapped[str | None] = mapped_column(String(128))

    source: Mapped[str] = mapped_column(
        Enum("wechat", "web", "referral", "mock", name="lead_source"),
        default="web",
        nullable=False,
    )
    stage: Mapped[str] = mapped_column(
        Enum(
            "new",
            "contacted",
            "audition",
            "won",
            "lost",
            name="lead_stage",
        ),
        default="new",
        nullable=False,
    )

    extra: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    assigned_agent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("agents.id", ondelete="SET NULL"),
    )

    # 反向关系
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="lead",
        cascade="all, delete-orphan",
    )