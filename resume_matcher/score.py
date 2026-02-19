from __future__ import annotations

from dataclasses import dataclass
from rapidfuzz import fuzz


@dataclass(frozen=True)
class MatchResult:
    score: int
    matched: list[str]
    missing: list[str]


def _best_fuzzy_match(term: str, candidates: set[str], threshold: int) -> bool:
    if term in candidates:
        return True

    best = 0
    for c in candidates:
        s = fuzz.ratio(term, c)
        if s > best:
            best = s
            if best >= threshold:
                return True
    return False


def score_match(
    resume_keywords: set[str],
    jd_keywords: set[str],
    fuzzy_threshold: int = 90,
) -> MatchResult:
    if not jd_keywords:
        return MatchResult(score=0, matched=[], missing=[])

    matched: list[str] = []
    missing: list[str] = []

    for term in sorted(jd_keywords):
        if _best_fuzzy_match(term, resume_keywords, fuzzy_threshold):
            matched.append(term)
        else:
            missing.append(term)

    score_float = (len(matched) / len(jd_keywords)) * 100.0
    score = int(round(score_float))

    return MatchResult(score=score, matched=matched, missing=missing)
