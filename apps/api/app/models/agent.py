"""智能体配置表模型."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Enum, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class Agent(UUIDMixin, TimestampMixin, Base):
    """智能体配置表 - 4 类角色 Agent 的配置."""

    __tablename__ = "agents"
    __table_args__ = (
        UniqueConstraint("slug", "version", name="uq_agent_slug_version"),
    )

    slug: Mapped[str] = mapped_column(
        Enum(
            "admission-consultant",
            "course-consultant",
            "academic-teacher",
            "internal-assistant",
            name="agent_slug",
        ),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)

    tools: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    tool_configs: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    model: Mapped[str] = mapped_column(String(64), default="claude-3-5-sonnet-20241022")
    temperature: Mapped[float] = mapped_column(Float, default=0.7, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, default=2000, nullable=False)

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # 知识库绑定（Agent 可访问的知识库）
    kb_names: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
    )

    # 反向关系
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="agent")