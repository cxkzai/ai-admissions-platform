"""提示词模板表模型."""

from sqlalchemy import Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class PromptTemplate(UUIDMixin, TimestampMixin, Base):
    """提示词模板表 - 可复用的 Prompt 模板."""

    __tablename__ = "prompt_templates"
    __table_args__ = (
        Index("ix_prompt_templates_category", "category"),
        Index("ix_prompt_templates_scenario", "scenario"),
    )

    category: Mapped[str] = mapped_column(String(32), nullable=False)
    # 场景：admission / renewal / refund / activity / etc.
    scenario: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    content: Mapped[str] = mapped_column(Text, nullable=False)
    variables: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
    )

    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    usage_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    success_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list, nullable=False)
    extra: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)