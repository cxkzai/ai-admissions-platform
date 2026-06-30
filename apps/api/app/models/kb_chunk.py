"""知识库切片表模型."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector  # type: ignore[import-not-found]

from app.models.base import Base, TimestampMixin, UUIDMixin
from app.models.kb_document import KbDocument
from app.core.config import settings

if TYPE_CHECKING:
    pass


class KBChunk(UUIDMixin, TimestampMixin, Base):
    """知识库切片表 - 文档切片及向量."""

    __tablename__ = "kb_chunks"
    __table_args__ = (
        Index("ix_kb_chunks_doc_id", "doc_id"),
        Index("ix_kb_chunks_doc_id_chunk_index", "doc_id", "chunk_index"),
    )

    doc_id: Mapped[UUID] = mapped_column(
        ForeignKey("kb_documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 向量字段（pgvector），开发期也保留以便迁移
    embedding = mapped_column(
        Vector(settings.embedding_dim),
        nullable=True,
    )

    metadata_: Mapped[dict] = mapped_column(
        "metadata",
        JSONB,
        default=dict,
        nullable=False,
    )

    # 反向关系
    document: Mapped[KbDocument] = relationship(back_populates="chunks")