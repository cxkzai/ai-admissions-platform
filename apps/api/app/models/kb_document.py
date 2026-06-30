"""知识库文档表模型."""

from typing import TYPE_CHECKING

from sqlalchemy import Enum, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.kb_chunk import KBChunk


class KbDocument(UUIDMixin, TimestampMixin, Base):
    """知识库文档表 - 原始文档元数据."""

    __tablename__ = "kb_documents"
    __table_args__ = (
        Index("ix_kb_documents_kb_name", "kb_name"),
        Index("ix_kb_documents_status", "status"),
    )

    kb_name: Mapped[str] = mapped_column(
        Enum(
            "courses",
            "teachers",
            "cases",
            "faq",
            "scripts",
            "sop",
            name="kb_name",
        ),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    source_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_type: Mapped[str] = mapped_column(String(16), nullable=False)

    status: Mapped[str] = mapped_column(
        Enum(
            "pending",
            "processing",
            "indexed",
            "failed",
            name="kb_doc_status",
        ),
        default="pending",
        nullable=False,
    )
    chunk_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_message: Mapped[str | None] = mapped_column(String(512))

    # 反向关系
    chunks: Mapped[list["KBChunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )