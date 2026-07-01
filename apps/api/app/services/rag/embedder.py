"""Embedding 适配器 - 支持 OpenAI / DeepSeek / 本地 bge / Mock."""

from abc import ABC, abstractmethod

from loguru import logger

from app.core.config import settings


class BaseEmbedder(ABC):
    """Embedding 适配器基类."""

    @abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """批量向量化."""

    @abstractmethod
    async def embed_one(self, text: str) -> list[float]:
        """单条向量化."""

    @property
    @abstractmethod
    def dim(self) -> int:
        """向量维度."""


class OpenAIEmbedder(BaseEmbedder):
    """OpenAI Embedding API - text-embedding-3-small 等."""

    def __init__(self, api_key: str, model: str = "text-embedding-3-small", dim: int = 1536):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self._dim = dim

    async def embed(self, texts: list[str]) -> list[list[float]]:
        # OpenAI 限制每批 ≤ 2048 条；为安全起见分批
        batch_size = 100
        all_embeddings: list[list[float]] = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            response = await self.client.embeddings.create(input=batch, model=self.model)
            all_embeddings.extend([item.embedding for item in response.data])

        return all_embeddings

    async def embed_one(self, text: str) -> list[float]:
        result = await self.embed([text])
        return result[0]

    @property
    def dim(self) -> int:
        return self._dim


class DeepSeekEmbedder(BaseEmbedder):
    """DeepSeek Embedding（如果有提供）- 使用 OpenAI 兼容 API."""

    def __init__(self, api_key: str, model: str = "deepseek-embedding", dim: int = 1536):
        from openai import AsyncOpenAI

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=settings.deepseek_base_url,
        )
        self.model = model
        self._dim = dim

    async def embed(self, texts: list[str]) -> list[list[float]]:
        response = await self.client.embeddings.create(input=texts, model=self.model)
        return [item.embedding for item in response.data]

    async def embed_one(self, text: str) -> list[float]:
        result = await self.embed([text])
        return result[0]

    @property
    def dim(self) -> int:
        return self._dim


class BgeEmbedder(BaseEmbedder):
    """本地 bge 中文 Embedding - 无需 API 调用."""

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        import asyncio
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)
        self._dim = self.model.get_sentence_embedding_dimension()
        self._loop = asyncio.get_event_loop()

    async def embed(self, texts: list[str]) -> list[list[float]]:
        import asyncio

        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(None, self.model.encode, texts)
        return embeddings.tolist()

    async def embed_one(self, text: str) -> list[float]:
        result = await self.embed([text])
        return result[0]

    @property
    def dim(self) -> int:
        return self._dim


class MockEmbedder(BaseEmbedder):
    """Mock Embedder - 用 hash + 字符 n-gram 生成确定性向量.

    用途：
    - 没有 API key 时能跑通流程
    - 单元测试
    - 检索质量低，仅用于演示
    """

    def __init__(self, dim: int = 384):
        self._dim = dim

    async def embed(self, texts: list[str]) -> list[list[float]]:
        import asyncio

        return await asyncio.get_event_loop().run_in_executor(
            None, self._embed_sync, texts
        )

    async def embed_one(self, text: str) -> list[float]:
        result = await self.embed([text])
        return result[0]

    def _embed_sync(self, texts: list[str]) -> list[list[float]]:
        import hashlib
        import math
        import re

        results = []
        for text in texts:
            # 提取字符 n-gram (1-3)
            text_clean = re.sub(r"\s+", " ", text.lower().strip())
            tokens = []
            for n in (1, 2, 3):
                for i in range(len(text_clean) - n + 1):
                    tokens.append(text_clean[i : i + n])

            # Hash 到 dim 维向量
            vec = [0.0] * self._dim
            for tok in tokens:
                h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
                idx = h % self._dim
                vec[idx] += 1.0

            # L2 normalize
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            vec = [x / norm for x in vec]
            results.append(vec)

        return results

    @property
    def dim(self) -> int:
        return self._dim


def get_embedder() -> BaseEmbedder:
    """根据配置返回 Embedder."""
    provider = settings.embedding_provider
    dim = settings.embedding_dim

    if provider == "openai":
        if not settings.openai_api_key:
            logger.warning("OPENAI_API_KEY 未配置，降级到 Mock Embedder")
            return MockEmbedder(dim=384)
        return OpenAIEmbedder(
            api_key=settings.openai_api_key,
            model=settings.embedding_model,
            dim=dim,
        )

    if provider == "deepseek":
        if not settings.deepseek_api_key:
            print("⚠️ DEEPSEEK_API_KEY 未配置，降级到 Mock Embedder")
            return MockEmbedder(dim=384)
        return DeepSeekEmbedder(
            api_key=settings.deepseek_api_key,
            model="deepseek-embedding",
            dim=dim,
        )

    if provider == "bge":
        try:
            return BgeEmbedder()
        except ImportError:
            print("⚠️ sentence-transformers 未安装，降级到 Mock Embedder")
            return MockEmbedder(dim=384)

    print(f"⚠️ 未知 embedding provider: {provider}，降级到 Mock")
    return MockEmbedder(dim=384)