"""文本切片器 - 支持通用切片 + 教培场景定制切片.

策略：
- Markdown 切片：按 ## 章节切分，保留标题上下文
- FAQ 切片：整条 Q&A 作为切片（不切碎）
- 课程切片：按课程名切分（保留完整课程信息）
"""

import re
from dataclasses import dataclass


@dataclass
class TextChunk:
    """文本切片."""

    content: str
    metadata: dict
    chunk_index: int


class MarkdownSectionSplitter:
    """Markdown 按二级标题切片 - 适合课程/师资/SOP 文档."""

    def __init__(self, max_chunk_size: int = 800, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap

    def split(self, text: str, base_metadata: dict | None = None) -> list[TextChunk]:
        """按 ## 二级标题切片，长章节再按段落细分."""
        base_metadata = base_metadata or {}
        chunks: list[TextChunk] = []

        # 切分章节
        sections = re.split(r"\n(?=##\s+)", text)

        chunk_idx = 0
        for section in sections:
            if not section.strip():
                continue

            # 提取章节标题
            title_match = re.match(r"^#+\s+(.+?)$", section, re.MULTILINE)
            section_title = title_match.group(1).strip() if title_match else ""

            # 如果章节太长，按段落切分
            if len(section) > self.max_chunk_size * 2:
                paragraphs = re.split(r"\n\n+", section)
                current_buf: list[str] = []
                current_len = 0

                for para in paragraphs:
                    para_len = len(para)

                    if current_len + para_len > self.max_chunk_size and current_buf:
                        content = "\n\n".join(current_buf)
                        chunks.append(
                            TextChunk(
                                content=content,
                                metadata={
                                    **base_metadata,
                                    "section": section_title,
                                },
                                chunk_index=chunk_idx,
                            )
                        )
                        chunk_idx += 1

                        # 重叠：保留最后一段作为下一 chunk 开头
                        if self.overlap > 0 and current_buf:
                            current_buf = [current_buf[-1]]
                            current_len = len(current_buf[0])
                        else:
                            current_buf = []
                            current_len = 0

                    current_buf.append(para)
                    current_len += para_len

                if current_buf:
                    content = "\n\n".join(current_buf)
                    chunks.append(
                        TextChunk(
                            content=content,
                            metadata={**base_metadata, "section": section_title},
                            chunk_index=chunk_idx,
                        )
                    )
                    chunk_idx += 1
            else:
                chunks.append(
                    TextChunk(
                        content=section.strip(),
                        metadata={**base_metadata, "section": section_title},
                        chunk_index=chunk_idx,
                    )
                )
                chunk_idx += 1

        return chunks


class FAQSplitter:
    """FAQ 专用切片器 - 整条 Q&A 作为切片."""

    def __init__(self):
        self.pattern = re.compile(
            r"^Q\d*[:：]?\s*(.+?)\n+A\d*[:：]?\s*(.+(?:\n(?!Q\d*[:：]?|---).+)*)",
            re.MULTILINE | re.DOTALL,
        )

    def split(self, text: str, base_metadata: dict | None = None) -> list[TextChunk]:
        base_metadata = base_metadata or {}
        chunks: list[TextChunk] = []
        chunk_idx = 0

        for match in self.pattern.finditer(text):
            question = match.group(1).strip()
            answer = match.group(2).strip()
            content = f"Q: {question}\nA: {answer}"

            chunks.append(
                TextChunk(
                    content=content,
                    metadata={
                        **base_metadata,
                        "question": question,
                        "type": "faq",
                    },
                    chunk_index=chunk_idx,
                )
            )
            chunk_idx += 1

        return chunks


class RecursiveSplitter:
    """通用递归切片器 - 兜底方案."""

    def __init__(
        self,
        chunk_size: int = 600,
        chunk_overlap: int = 100,
        separators: list[str] | None = None,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", "。", ".", "；", ";", " ", ""]

    def split(self, text: str, base_metadata: dict | None = None) -> list[TextChunk]:
        base_metadata = base_metadata or {}
        chunks: list[TextChunk] = []
        chunk_idx = 0

        for piece in self._split_recursive(text, self.separators):
            piece = piece.strip()
            if not piece:
                continue
            if len(piece) <= self.chunk_size:
                chunks.append(
                    TextChunk(content=piece, metadata=base_metadata, chunk_index=chunk_idx)
                )
                chunk_idx += 1
            else:
                # 强制切分
                for i in range(0, len(piece), self.chunk_size - self.chunk_overlap):
                    sub = piece[i : i + self.chunk_size]
                    chunks.append(
                        TextChunk(content=sub, metadata=base_metadata, chunk_index=chunk_idx)
                    )
                    chunk_idx += 1

        return chunks

    def _split_recursive(self, text: str, separators: list[str]) -> list[str]:
        if not separators:
            return [text]

        sep = separators[0]
        remaining_seps = separators[1:]

        if sep:
            pieces = text.split(sep)
        else:
            pieces = list(text)

        result: list[str] = []
        for piece in pieces:
            if len(piece) <= self.chunk_size:
                result.append(piece)
            else:
                result.extend(self._split_recursive(piece, remaining_seps))

        return [r for r in result if r.strip()]


def get_splitter(kb_name: str):
    """根据知识库类型返回合适的切片器."""
    if kb_name == "faq":
        return FAQSplitter()
    if kb_name in {"courses", "teachers", "cases", "sop"}:
        return MarkdownSectionSplitter(max_chunk_size=800, overlap=100)
    if kb_name == "scripts":
        return MarkdownSectionSplitter(max_chunk_size=500, overlap=50)
    return RecursiveSplitter(chunk_size=600, chunk_overlap=100)