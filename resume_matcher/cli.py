from __future__ import annotations

from pathlib import Path
import typer
from rich.console import Console

from .extract import extract_text_from_pdf
from .normalize import normalize_text
from .keywords import extract_keywords
from .score import score_match
from .report import Report, print_report

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def match(
    resume_pdf: Path = typer.Argument(..., help="Path to resume PDF"),
    jd_file: Path | None = typer.Option(None, help="Path to a text file containing the job description"),
    jd_text: str | None = typer.Option(None, help="Job description pasted as text"),
    top_n: int = typer.Option(60, help="How many keywords to consider from each side"),
    fuzzy_threshold: int = typer.Option(90, help="Fuzzy match threshold, 100 is exact only"),
) -> None:
    if (jd_file is None and jd_text is None) or (jd_file is not None and jd_text is not None):
        raise typer.BadParameter("Provide exactly one of jd_file or jd_text")

    resume_raw = extract_text_from_pdf(resume_pdf)
    resume = normalize_text(resume_raw)

    if jd_file is not None:
        if not jd_file.exists():
            raise FileNotFoundError(f"File not found: {jd_file}")
        jd_raw = jd_file.read_text(encoding="utf-8", errors="ignore")
    else:
        jd_raw = jd_text or ""

    jd = normalize_text(jd_raw)

    resume_kw = extract_keywords(resume, top_n=top_n)
    jd_kw = extract_keywords(jd, top_n=top_n)

    match_result = score_match(
        resume_keywords=resume_kw.keywords,
        jd_keywords=jd_kw.keywords,
        fuzzy_threshold=fuzzy_threshold,
    )

    report = Report(
        match=match_result,
        top_resume_keywords=resume_kw.counts.most_common(25),
        top_jd_keywords=jd_kw.counts.most_common(25),
    )

    print_report(report)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
