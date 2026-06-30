"""RAG Service - 高级 API.

封装 RAG 全流程：
- 知识库导入（从文件）
- 检索 + 引用构建
- 评测
"""

import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from loguru import logger

from app.services.rag.document_loader import DocumentLoader, LoadedDocument
from app.services.rag.embedder import BaseEmbedder, get_embedder
from app.services.rag.retriever import Retriever, RetrievalConfig
from app.services.rag.text_splitter import get_splitter
from app.services.rag.vector_store import ChromaVectorStore, SearchResult, get_vector_store


@dataclass
class Citation:
    """RAG 引用."""

    title: str
    score: float
    source: str
    content: str = ""


@dataclass
class IngestResult:
    """导入结果."""

    kb_name: str
    document_count: int
    chunk_count: int
    elapsed_seconds: float
    failed_files: list[str]


class RAGService:
    """RAG 服务 - 高层 API."""

    def __init__(
        self,
        embedder: BaseEmbedder | None = None,
        vector_store: ChromaVectorStore | None = None,
        retriever: Retriever | None = None,
    ):
        self.embedder = embedder or get_embedder()
        self.vector_store = vector_store or get_vector_store()
        self.retriever = retriever or Retriever(
            embedder=self.embedder,
            vector_store=self.vector_store,
        )
        self.loader = DocumentLoader()

    # ===== 知识库导入 =====

    async def ingest_file(
        self,
        file_path: str,
        kb_name: str,
        title: str | None = None,
    ) -> IngestResult:
        """导入单个文件到指定知识库."""
        import time

        start = time.perf_counter()

        doc = await self.loader.load(file_path)
        title = title or Path(file_path).stem

        chunks = self._split_doc(doc, kb_name)
        await self._index_chunks(chunks, kb_name, title, doc.source_path)

        elapsed = time.perf_counter() - start
        logger.info(
            f"📥 Ingested {file_path} → {len(chunks)} chunks in {elapsed:.2f}s"
        )

        return IngestResult(
            kb_name=kb_name,
            document_count=1,
            chunk_count=len(chunks),
            elapsed_seconds=elapsed,
            failed_files=[],
        )

    async def ingest_directory(
        self,
        dir_path: str,
        kb_name: str,
    ) -> IngestResult:
        """批量导入目录所有文件到指定知识库."""
        import time

        start = time.perf_counter()
        docs = await self.loader.load_directory(dir_path)

        total_chunks = 0
        failed: list[str] = []

        for doc in docs:
            try:
                chunks = self._split_doc(doc, kb_name)
                title = Path(doc.source_path).stem
                await self._index_chunks(chunks, kb_name, title, doc.source_path)
                total_chunks += len(chunks)
            except Exception as e:
                logger.error(f"❌ Failed to ingest {doc.source_path}: {e}")
                failed.append(doc.source_path)

        elapsed = time.perf_counter() - start
        logger.info(
            f"📥 Ingested directory {dir_path}: {len(docs)} docs, {total_chunks} chunks in {elapsed:.2f}s"
        )

        return IngestResult(
            kb_name=kb_name,
            document_count=len(docs),
            chunk_count=total_chunks,
            elapsed_seconds=elapsed,
            failed_files=failed,
        )

    def _split_doc(self, doc: LoadedDocument, kb_name: str) -> list[Any]:
        """根据知识库类型切片."""
        splitter = get_splitter(kb_name)
        return splitter.split(doc.content, base_metadata={"source": doc.source_path})

    async def _index_chunks(
        self,
        chunks: list[Any],
        kb_name: str,
        doc_title: str,
        source_path: str,
    ) -> None:
        """将切片向量化并入库."""
        if not chunks:
            return

        texts = [c.content for c in chunks]
        embeddings = await self.embedder.embed(texts)

        ids = [str(uuid.uuid4()) for _ in chunks]
        metadatas = [
            {
                "kb_name": kb_name,
                "doc_title": doc_title,
                "source": source_path,
                "chunk_index": c.chunk_index,
                **c.metadata,
            }
            for c in chunks
        ]

        self.vector_store.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    # ===== 检索 =====

    async def search(
        self,
        query: str,
        top_k: int = 5,
        kb_names: list[str] | None = None,
    ) -> list[Citation]:
        """高层检索接口：返回 Citations."""
        config = RetrievalConfig(top_k=top_k, kb_names=kb_names)
        results = await self.retriever.retrieve(query, config)

        return [
            Citation(
                title=r.metadata.get("doc_title", "未知"),
                score=r.score,
                source=r.metadata.get("source", ""),
                content=r.content,
            )
            for r in results
        ]

    # ===== 统计 =====

    def stats(self) -> dict[str, Any]:
        """获取向量库统计信息."""
        total = self.vector_store.count()
        return {
            "total_chunks": total,
            "embedder_type": type(self.embedder).__name__,
            "embedder_dim": self.embedder.dim,
            "vector_store_type": type(self.vector_store).__name__,
        }


# 单例
_service: RAGService | None = None


def get_rag_service() -> RAGService:
    """获取 RAG Service 单例."""
    global _service
    if _service is None:
        _service = RAGService()
    return _service