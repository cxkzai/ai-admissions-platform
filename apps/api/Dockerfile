# ===== AI-Admissions Platform · FastAPI Dockerfile =====

FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy

# 安装 uv
RUN pip install uv

WORKDIR /app

# 先拷贝依赖文件，利用 Docker 缓存
COPY pyproject.toml ./

# 安装依赖
RUN uv sync --no-dev

# 拷贝源代码
COPY app ./app
COPY scripts ./scripts
COPY alembic ./alembic
COPY alembic.ini ./
COPY data ./data

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]