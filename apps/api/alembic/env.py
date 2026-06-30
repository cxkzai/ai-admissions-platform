"""Alembic 环境配置."""

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# 导入配置与模型
from app.core.config import settings
from app.models.base import Base

# 自动导入所有模型（让 Alembic 能检测到 schema 变化）
from app.models import (  # noqa: F401
    lead,
    conversation,
    message,
    agent,
    kb_document,
    kb_chunk,
    prompt_template,
)

config = context.config

# 用 settings 覆盖 alembic.ini 中的 url
config.set_main_option("sqlalchemy.url", settings.database_url_sync)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """离线模式（生成 SQL 脚本）."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """在线模式（直接连接数据库）."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()