"""知识库导入脚本.

用法：
    uv run python -m scripts.ingest_kb                  # 导入全部 6 个库
    uv run python -m scripts.ingest_kb --kb courses     # 只导入课程库
    uv run python -m scripts.ingest_kb --reset          # 清空再导入

导入数据位置：data/knowledge_base/{kb_name}/
"""

import argparse
import asyncio
from pathlib import Path

from loguru import logger
from rich.console import Console
from rich.table import Table

from app.services.rag.service import RAGService, get_rag_service

console = Console()

# 知识库映射
KB_DIRS = {
    "courses": "data/knowledge_base/courses",
    "teachers": "data/knowledge_base/teachers",
    "cases": "data/knowledge_base/cases",
    "faq": "data/knowledge_base/faq",
    "scripts": "data/knowledge_base/scripts",
    "sop": "data/knowledge_base/sop",
}


async def ingest_all(reset: bool = False) -> None:
    """导入全部知识库."""
    service = get_rag_service()

    if reset:
        console.print("[yellow]⚠️  Resetting vector store...[/yellow]")
        service.vector_store.delete_by_filter({})
        console.print("[green]✓ Cleared all chunks[/green]")

    table = Table(title="📥 Knowledge Base Ingestion", show_header=True)
    table.add_column("Library", style="cyan")
    table.add_column("Docs", justify="right", style="green")
    table.add_column("Chunks", justify="right", style="green")
    table.add_column("Time", justify="right", style="yellow")
    table.add_column("Status", style="bold")

    total_chunks = 0
    for kb_name, dir_path in KB_DIRS.items():
        full_path = Path(dir_path)
        if not full_path.exists():
            table.add_row(kb_name, "—", "—", "—", "[red]dir not found[/red]")
            continue

        try:
            result = await service.ingest_directory(str(full_path), kb_name)
            total_chunks += result.chunk_count
            table.add_row(
                kb_name,
                str(result.document_count),
                str(result.chunk_count),
                f"{result.elapsed_seconds:.2f}s",
                "[green]✓ ok[/green]",
            )
        except Exception as e:
            logger.exception(f"Ingestion failed for {kb_name}")
            table.add_row(kb_name, "—", "—", "—", f"[red]✗ {e}[/red]")

    console.print(table)
    console.print(f"\n[bold green]✓ Total chunks indexed: {total_chunks}[/bold green]")

    # 统计
    stats = service.stats()
    console.print(f"[dim]Embedder: {stats['embedder_type']} (dim={stats['embedder_dim']})[/dim]")
    console.print(f"[dim]Vector store: {stats['vector_store_type']} ({stats['total_chunks']} total chunks)[/dim]")


async def ingest_one(kb_name: str, reset: bool = False) -> None:
    """导入单个知识库."""
    if kb_name not in KB_DIRS:
        console.print(f"[red]✗ Unknown KB: {kb_name}[/red]")
        console.print(f"[yellow]Available: {list(KB_DIRS.keys())}[/yellow]")
        return

    service = get_rag_service()
    if reset:
        service.vector_store.delete_by_filter({"kb_name": kb_name})

    result = await service.ingest_directory(KB_DIRS[kb_name], kb_name)
    console.print(
        f"[green]✓ {kb_name}: {result.document_count} docs, {result.chunk_count} chunks in {result.elapsed_seconds:.2f}s[/green]"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="知识库导入脚本")
    parser.add_argument("--kb", choices=list(KB_DIRS.keys()), help="指定单个知识库")
    parser.add_argument("--reset", action="store_true", help="导入前清空向量库")
    args = parser.parse_args()

    if args.kb:
        asyncio.run(ingest_one(args.kb, reset=args.reset))
    else:
        asyncio.run(ingest_all(reset=args.reset))


if __name__ == "__main__":
    main()