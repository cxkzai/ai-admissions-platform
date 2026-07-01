"""FastAPI 应用入口.

启动方式:
    uv run uvicorn app.main:app --reload --port 8000

或:
    uv run python -m app.main
"""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期."""
    # 启动
    logger.info(f"[startup] {settings.app_name} v{settings.app_version}")
    logger.info(f"[startup] API: http://{settings.api_host}:{settings.api_port}")
    logger.info(f"[startup] Docs: http://{settings.api_host}:{settings.api_port}/docs")
    logger.info(f"[startup] LLM Engine: {settings.llm_default_engine}")
    yield
    # 关闭
    logger.info("[shutdown] Shutting down...")


app = FastAPI(
    title=settings.app_name,
    description="教培机构 AI 招生顾问平台 - 多智能体 + RAG + 工作流",
    version=settings.app_version,
    debug=settings.app_debug,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, Any]:
    """根路由."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "env": settings.app_env,
        "docs": "/docs",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    """健康检查."""
    return {"status": "ok"}


@app.get("/api/v1/health", include_in_schema=False)
async def api_v1_health() -> dict[str, str]:
    """v1 路径下的健康检查（与 /health 相同，供前端 Vite proxy 调用）。"""
    return {"status": "ok"}


# ===== 路由（Phase 1 已接入） =====
from app.api.v1 import chat as chat_router

app.include_router(chat_router.router, prefix="/api/v1")


def run() -> None:
    """脚本入口."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_debug,
    )


if __name__ == "__main__":
    run()