"""RAG 评测脚本.

评测数据集格式（data/eval/rag_eval.jsonl）：
    {"query": "...", "relevant_docs": ["title1", "title2"], "expected_answer": "..."}

评测指标：
- Recall@K：相关文档是否在前 K 个检索结果中
- MRR (Mean Reciprocal Rank)：第一个相关文档的排名倒数
- Hit Rate：命中率
- Avg Latency：平均检索耗时

用法：
    uv run python -m scripts.eval_rag
"""

import asyncio
import json
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table

from app.services.rag.service import get_rag_service

console = Console()

DEFAULT_EVAL_FILE = "data/eval/rag_eval.jsonl"


async def run_eval(eval_file: str = DEFAULT_EVAL_FILE, top_k: int = 5) -> None:
    """运行 RAG 评测."""
    eval_path = Path(eval_file)
    if not eval_path.exists():
        console.print(f"[red]✗ 评测文件不存在: {eval_file}[/red]")
        console.print("[yellow]提示：先创建评测数据集[/yellow]")
        return

    # 加载评测集
    eval_cases: list[dict] = []
    with eval_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            eval_cases.append(json.loads(line))

    console.print(f"[bold]📊 Running RAG evaluation on {len(eval_cases)} cases[/bold]")
    console.print(f"[dim]Top-K: {top_k}[/dim]\n")

    service = get_rag_service()

    table = Table(show_header=True)
    table.add_column("Case", style="cyan")
    table.add_column("Recall@5", justify="right")
    table.add_column("Hit", justify="right")
    table.add_column("Rank", justify="right")
    table.add_column("Latency", justify="right", style="yellow")

    total_recall = 0.0
    total_hit = 0
    total_mrr = 0.0
    total_latency = 0.0

    for i, case in enumerate(eval_cases, 1):
        query = case["query"]
        relevant = set(case.get("relevant_docs", []))

        start = time.perf_counter()
        results = await service.search(query, top_k=top_k)
        latency_ms = (time.perf_counter() - start) * 1000

        retrieved_titles = [r.title for r in results]
        retrieved_set = set(retrieved_titles)

        # Recall@K = 检索到的相关文档数 / 总相关文档数
        if relevant:
            recall = len(retrieved_set & relevant) / len(relevant)
        else:
            recall = 1.0

        # Hit Rate = 是否有任意一个相关文档被检索到
        hit = 1 if (retrieved_set & relevant) else 0

        # MRR = 第一个相关文档的排名倒数
        mrr = 0.0
        for rank, title in enumerate(retrieved_titles, 1):
            if title in relevant:
                mrr = 1.0 / rank
                break

        total_recall += recall
        total_hit += hit
        total_mrr += mrr
        total_latency += latency_ms

        table.add_row(
            f"#{i} {query[:30]}...",
            f"{recall:.2f}",
            "✓" if hit else "✗",
            f"{mrr:.2f}",
            f"{latency_ms:.0f}ms",
        )

    n = len(eval_cases) or 1
    console.print(table)
    console.print("\n[bold green]📈 Summary[/bold green]")
    console.print(f"  Recall@5  : {total_recall / n:.3f}")
    console.print(f"  Hit Rate  : {total_hit / n:.3f}")
    console.print(f"  MRR       : {total_mrr / n:.3f}")
    console.print(f"  Avg Latency: {total_latency / n:.1f}ms")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="RAG 评测脚本")
    parser.add_argument("--file", default=DEFAULT_EVAL_FILE, help="评测数据集路径")
    parser.add_argument("--top-k", type=int, default=5, help="Top-K 数量")
    args = parser.parse_args()

    asyncio.run(run_eval(args.file, args.top_k))


if __name__ == "__main__":
    main()