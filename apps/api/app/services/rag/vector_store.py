"""向量库适配层 - 当前实现 Chroma，未来可平滑迁移 pgvector."""

from dataclasses import dataclass
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings


@dataclass
class SearchResult:
    """检索结果."""

    chunk_id: str
    content: str
    score: float
    metadata: dict
    source: str = ""


class ChromaVectorStore:
    """Chroma 向量库封装."""

    def __init__(self, persist_dir: str = "./chroma_data", collection_name: str = "edu_admissions"):
        path = Path(persist_dir)
        path.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(path),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            ),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict] | None = None,
    ) -> None:
        """批量添加."""
        kwargs: dict = {
            "ids": ids,
            "documents": documents,
            "embeddings": embeddings,
        }
        if metadatas:
            kwargs["metadatas"] = metadatas
        self.collection.add(**kwargs)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """检索 Top-K."""
        kwargs: dict = {
            "query_embeddings": [query_embedding],
            "n_results": top_k,
        }
        if where:
            kwargs["where"] = where

        results = self.collection.query(**kwargs)

        search_results: list[SearchResult] = []
        if not results or not results.get("ids"):
            return search_results

        ids = results["ids"][0]
        docs = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results.get("metadatas", [[{}] * len(ids)])[0]

        for i, chunk_id in enumerate(ids):
            # Chroma 用 cosine distance，转换为 score = 1 - distance
            score = 1.0 - distances[i] if distances else 0.0
            search_results.append(
                SearchResult(
                    chunk_id=chunk_id,
                    content=docs[i],
                    score=score,
                    metadata=metadatas[i] if metadatas else {},
                    source=metadatas[i].get("source", "") if metadatas else "",
                )
            )

        return search_results

    def delete(self, ids: list[str]) -> None:
        self.collection.delete(ids=ids)

    def delete_by_filter(self, where: dict) -> None:
        self.collection.delete(where=where)

    def count(self) -> int:
        return self.collection.count()


_singleton: ChromaVectorStore | None = None


def get_vector_store() -> ChromaVectorStore:
    """获取向量库单例."""
    global _singleton
    if _singleton is None:
        from app.core.config import settings

        _singleton = ChromaVectorStore(
            persist_dir=settings.chroma_persist_dir,
            collection_name="edu_admissions",
        )
    return _singleton