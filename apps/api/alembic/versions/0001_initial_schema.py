"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-06-30

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector  # type: ignore[import-not-found]


# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """创建初始 schema."""
    # ===== 启用 pgvector 扩展 =====
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # ===== agents 智能体配置 =====
    op.create_table(
        "agents",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "slug",
            sa.Enum(
                "admission-consultant",
                "course-consultant",
                "academic-teacher",
                "internal-assistant",
                name="agent_slug",
            ),
            nullable=False,
        ),
        sa.Column("name", sa.String(64), nullable=False),
        sa.Column("description", sa.Text, nullable=False),
        sa.Column("system_prompt", sa.Text, nullable=False),
        sa.Column("tools", sa.dialects.postgresql.ARRAY(sa.String), nullable=False, server_default="{}"),
        sa.Column("tool_configs", sa.dialects.postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("model", sa.String(64), nullable=False, server_default="claude-3-5-sonnet-20241022"),
        sa.Column("temperature", sa.Float, nullable=False, server_default="0.7"),
        sa.Column("max_tokens", sa.Integer, nullable=False, server_default="2000"),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("kb_names", sa.dialects.postgresql.ARRAY(sa.String), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("slug", "version", name="uq_agent_slug_version"),
    )

    # ===== leads 线索 =====
    op.create_table(
        "leads",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(64)),
        sa.Column("phone", sa.String(32)),
        sa.Column("wechat", sa.String(64)),
        sa.Column("child_age", sa.Integer),
        sa.Column("interest_subject", sa.String(128)),
        sa.Column(
            "source",
            sa.Enum("wechat", "web", "referral", "mock", name="lead_source"),
            nullable=False,
            server_default="web",
        ),
        sa.Column(
            "stage",
            sa.Enum("new", "contacted", "audition", "won", "lost", name="lead_stage"),
            nullable=False,
            server_default="new",
        ),
        sa.Column("extra", sa.dialects.postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("notes", sa.Text),
        sa.Column("assigned_agent_id", sa.dialects.postgresql.UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["assigned_agent_id"], ["agents.id"], ondelete="SET NULL",
        ),
    )
    op.create_index("ix_leads_stage", "leads", ["stage"])
    op.create_index("ix_leads_source", "leads", ["source"])
    op.create_index("ix_leads_assigned_agent_id", "leads", ["assigned_agent_id"])

    # ===== conversations 会话 =====
    op.create_table(
        "conversations",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lead_id", sa.dialects.postgresql.UUID(as_uuid=True)),
        sa.Column("agent_id", sa.dialects.postgresql.UUID(as_uuid=True)),
        sa.Column(
            "channel",
            sa.Enum("web", "wechat", "feishu", "mock", name="conversation_channel"),
            nullable=False,
            server_default="web",
        ),
        sa.Column(
            "status",
            sa.Enum("active", "closed", name="conversation_status"),
            nullable=False,
            server_default="active",
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"], ondelete="SET NULL"),
    )
    op.create_index("ix_conversations_lead_id", "conversations", ["lead_id"])
    op.create_index("ix_conversations_agent_id", "conversations", ["agent_id"])
    op.create_index("ix_conversations_status", "conversations", ["status"])

    # ===== messages 消息 =====
    op.create_table(
        "messages",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "role",
            sa.Enum("user", "assistant", "tool", "system", name="message_role"),
            nullable=False,
        ),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("tool_calls", sa.dialects.postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("citations", sa.dialects.postgresql.JSONB, nullable=False, server_default="[]"),
        sa.Column("extra", sa.dialects.postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("latency_ms", sa.Integer),
        sa.Column("prompt_tokens", sa.Integer),
        sa.Column("completion_tokens", sa.Integer),
        sa.Column("model", sa.Text),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"])
    op.create_index("ix_messages_created_at", "messages", ["created_at"])

    # ===== kb_documents 知识库文档 =====
    op.create_table(
        "kb_documents",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "kb_name",
            sa.Enum(
                "courses", "teachers", "cases", "faq", "scripts", "sop",
                name="kb_name",
            ),
            nullable=False,
        ),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("source_path", sa.String(512), nullable=False),
        sa.Column("file_type", sa.String(16), nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "processing", "indexed", "failed", name="kb_doc_status"),
            nullable=False,
            server_default="pending",
        ),
        sa.Column("chunk_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error_message", sa.String(512)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_kb_documents_kb_name", "kb_documents", ["kb_name"])
    op.create_index("ix_kb_documents_status", "kb_documents", ["status"])

    # ===== kb_chunks 知识库切片 =====
    op.create_table(
        "kb_chunks",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("doc_id", sa.dialects.postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chunk_index", sa.Integer, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("embedding", Vector(1536), nullable=True),
        sa.Column("metadata", sa.dialects.postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["doc_id"], ["kb_documents.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_kb_chunks_doc_id", "kb_chunks", ["doc_id"])
    op.create_index("ix_kb_chunks_doc_id_chunk_index", "kb_chunks", ["doc_id", "chunk_index"])

    # ===== prompt_templates 提示词模板 =====
    op.create_table(
        "prompt_templates",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("category", sa.String(32), nullable=False),
        sa.Column("scenario", sa.String(32), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("variables", sa.dialects.postgresql.ARRAY(sa.String), nullable=False, server_default="{}"),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
        sa.Column("usage_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("success_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("tags", sa.dialects.postgresql.ARRAY(sa.String), nullable=False, server_default="{}"),
        sa.Column("extra", sa.dialects.postgresql.JSONB, nullable=False, server_default="{}"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_prompt_templates_category", "prompt_templates", ["category"])
    op.create_index("ix_prompt_templates_scenario", "prompt_templates", ["scenario"])


def downgrade() -> None:
    """删除所有表."""
    op.drop_table("prompt_templates")
    op.drop_table("kb_chunks")
    op.drop_table("kb_documents")
    op.drop_table("messages")
    op.drop_table("conversations")
    op.drop_table("leads")
    op.drop_table("agents")
    op.execute("DROP EXTENSION IF EXISTS vector")