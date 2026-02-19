from __future__ import annotations

from dataclasses import dataclass
from rich.console import Console
from rich.table import Table

from .score import MatchResult


@dataclass(frozen=True)
class Report:
    match: MatchResult
    top_resume_keywords: list[tuple[str, int]]
    top_jd_keywords: list[tuple[str, int]]


def print_report(report: Report) -> None:
    console = Console()

    console.print()
    console.print(f"Match score: {report.match.score}/100")

    table = Table(title="Keyword Match")
    table.add_column("Matched", style="green")
    table.add_column("Missing", style="red")

    max_len = max(len(report.match.matched), len(report.match.missing))
    for i in range(max_len):
        m = report.match.matched[i] if i < len(report.match.matched) else ""
        x = report.match.missing[i] if i < len(report.match.missing) else ""
        table.add_row(m, x)

    console.print(table)

    console.print()
    console.print("Top resume keywords:")
    for k, c in report.top_resume_keywords[:15]:
        console.print(f"  {k}, {c}")

    console.print()
    console.print("Top job description keywords:")
    for k, c in report.top_jd_keywords[:15]:
        console.print(f"  {k}, {c}")

    console.print()
