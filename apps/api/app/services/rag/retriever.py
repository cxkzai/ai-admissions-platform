"""检索器 - Query 改写 + 向量检索 + 重排序.

RAG 核心：把用户问题变成高质量的检索 query。
"""

import re
from dataclasses import dataclass

from app.services.rag.embedder import BaseEmbedder, get_embedder
from app.services.rag.vector_store import ChromaVectorStore, SearchResult, get_vector_store


@dataclass
class RetrievalConfig:
    """检索配置."""

    top_k: int = 5
    score_threshold: float = 0.3
    kb_names: list[str] | None = None  # None = 全部库
    use_query_rewrite: bool = True


class Retriever:
    """统一检索器."""

    def __init__(
        self,
        embedder: BaseEmbedder | None = None,
        vector_store: ChromaVectorStore | None = None,
    ):
        self.embedder = embedder or get_embedder()
        self.vector_store = vector_store or get_vector_store()

    async def retrieve(
        self,
        query: str,
        config: RetrievalConfig | None = None,
    ) -> list[SearchResult]:
        """主检索流程."""
        config = config or RetrievalConfig()

        # 1. Query 改写（去除口语化、补全关键词）
        if config.use_query_rewrite:
            query = self._rewrite_query(query)

        # 2. 向量化
        query_embedding = await self.embedder.embed_one(query)

        # 3. 向量检索
        where: dict | None = None
        if config.kb_names:
            where = {"kb_name": {"$in": config.kb_names}}

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=config.top_k * 2,  # 多取一些用于重排
            where=where,
        )

        # 4. 重排序：基于关键词匹配度 + LLM 评分
        results = self._rerank(query, results, top_k=config.top_k)

        # 5. 阈值过滤
        results = [r for r in results if r.score >= config.score_threshold]

        return results

    @staticmethod
    def _rewrite_query(query: str) -> str:
        """简单的 Query 改写：去除口语词、补全关键词."""
        # 去除常见停用词
        stopwords = ["那个", "这个", "请问", "您好", "你好", "麻烦", "想问一下", "我想", "就是", "咋", "怎么", "什么", "啊", "吗", "呢"]
        cleaned = query
        for sw in stopwords:
            cleaned = cleaned.replace(sw, " ")

        # 多余空白
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned or query

    @staticmethod
    def _rerank(
        query: str,
        results: list[SearchResult],
        top_k: int = 5,
    ) -> list[SearchResult]:
        """简单重排序：结合向量相似度 + 关键词匹配度.

        score_final = 0.7 * vector_score + 0.3 * keyword_score
        """
        query_keywords = set(_tokenize(query))

        for r in results:
            content_keywords = set(_tokenize(r.content))
            if query_keywords:
                overlap = len(query_keywords & content_keywords)
                keyword_score = overlap / len(query_keywords)
            else:
                keyword_score = 0.0

            r.score = 0.7 * r.score + 0.3 * keyword_score

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]


def _tokenize(text: str) -> list[str]:
    """简单中文分词 - 按字符 + 2-gram.

    注意：生产环境应该用 jieba 等专业分词。
    这里用 character + 2-gram 简化处理。
    """
    text = re.sub(r"[^\w一-鿿]+", " ", text.lower())
    chars = [c for c in text if c.strip()]
    tokens = chars + [chars[i] + chars[i + 1] for i in range(len(chars) - 1)]
    return [t for t in tokens if len(t) > 0]