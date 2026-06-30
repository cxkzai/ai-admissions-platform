"""RAG 服务测试."""

import pytest

from app.services.rag.embedder import MockEmbedder, get_embedder
from app.services.rag.text_splitter import (
    FAQSplitter,
    MarkdownSectionSplitter,
    RecursiveSplitter,
    get_splitter,
)
from app.services.rag.vector_store import ChromaVectorStore


class TestSplitters:
    """切片器测试（不依赖外部资源）."""

    def test_markdown_section_splitter(self) -> None:
        text = """# 总标题

## 章节 1

这是章节 1 的内容。

## 章节 2

这是章节 2 的内容。

## 章节 3

这是章节 3 的内容。
"""
        splitter = MarkdownSectionSplitter()
        chunks = splitter.split(text)
        assert len(chunks) >= 3
        assert any("章节 1" in c.content for c in chunks)
        assert any("章节 2" in c.content for c in chunks)

    def test_faq_splitter(self) -> None:
        text = """Q1: 孩子几岁学编程？
A1: 建议 8 岁开始接触 Scratch。

Q2: 学费多少？
A2: Scratch ¥5,800 起，Python ¥7,800 起。
"""
        splitter = FAQSplitter()
        chunks = splitter.split(text)
        assert len(chunks) == 2
        assert "8 岁" in chunks[0].content
        assert "Scratch" in chunks[0].content

    def test_recursive_splitter(self) -> None:
        text = "这是一个测试文本。" * 50  # 较长文本
        splitter = RecursiveSplitter(chunk_size=100, chunk_overlap=20)
        chunks = splitter.split(text)
        assert len(chunks) > 1
        # 每个 chunk 不超过 chunk_size（考虑边界）
        for c in chunks:
            assert len(c.content) <= 200

    def test_get_splitter_returns_correct_type(self) -> None:
        assert isinstance(get_splitter("faq"), FAQSplitter)
        assert isinstance(get_splitter("courses"), MarkdownSectionSplitter)
        assert isinstance(get_splitter("unknown"), RecursiveSplitter)


class TestMockEmbedder:
    """Mock Embedder 测试."""

    @pytest.mark.asyncio
    async def test_embed_deterministic(self) -> None:
        embedder = MockEmbedder(dim=128)
        text = "测试文本"
        vec1 = await embedder.embed_one(text)
        vec2 = await embedder.embed_one(text)
        # 同一文本应产生相同向量
        assert vec1 == vec2

    @pytest.mark.asyncio
    async def test_embed_different_texts_differ(self) -> None:
        embedder = MockEmbedder(dim=128)
        vec1 = await embedder.embed_one("Python 编程")
        vec2 = await embedder.embed_one("学费多少")
        # 不同文本向量不同
        assert vec1 != vec2

    @pytest.mark.asyncio
    async def test_embed_batch(self) -> None:
        embedder = MockEmbedder(dim=128)
        vecs = await embedder.embed(["文本 A", "文本 B", "文本 C"])
        assert len(vecs) == 3
        for v in vecs:
            assert len(v) == 128

    def test_dim_property(self) -> None:
        assert MockEmbedder(dim=256).dim == 256


class TestEmbedderFactory:
    """Embedder 工厂测试."""

    def test_factory_returns_instance(self) -> None:
        embedder = get_embedder()
        assert embedder is not None
        assert hasattr(embedder, "embed")
        assert hasattr(embedder, "embed_one")
        assert hasattr(embedder, "dim")


@pytest.mark.skip(reason="需要 chromadb 服务，仅在集成测试中运行")
class TestChromaVectorStore:
    """Chroma 向量库测试."""

    def setup_method(self) -> None:
        self.store = ChromaVectorStore(
            persist_dir="./test_chroma",
            collection_name="test",
        )

    def teardown_method(self) -> None:
        import shutil
        from pathlib import Path

        path = Path("./test_chroma")
        if path.exists():
            shutil.rmtree(path)

    def test_add_and_search(self) -> None:
        ids = ["1", "2", "3"]
        docs = ["Python 编程基础", "Scratch 启蒙课", "C++ 算法进阶"]
        embeddings = [[0.1] * 384, [0.2] * 384, [0.3] * 384]

        self.store.add(ids, docs, embeddings)

        results = self.store.search([0.1] * 384, top_k=2)
        assert len(results) > 0
        assert results[0].content in docs