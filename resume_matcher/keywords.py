from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re

from .normalize import tokenize_words


_STOPWORDS = {
    "and","or","the","a","an","to","of","in","on","for","with","as","at","by",
    "from","is","are","was","were","be","been","being","this","that","these","those",
    "it","its","you","your","we","our","they","their","i","me","my",
    "will","can","could","should","would","may","might","must",
    "experience","years","year","work","worked","working","responsible","responsibilities",
    "skills","skill","ability","abilities","team","teams","including","plus",
}

_CANONICAL_MAP = {
    "js": "javascript",
    "node": "nodejs",
    "node.js": "nodejs",
    "ts": "typescript",
    "py": "python",
    "c sharp": "c#",
    "csharp": "c#",
    "dotnet": ".net",
    "aspnet": "asp.net",
    "postgres": "postgresql",
    "postgre": "postgresql",
    "k8s": "kubernetes",
    "ci cd": "ci/cd",
    "cicd": "ci/cd",
}


_MULTIWORD_SKILLS = [
    "machine learning",
    "deep learning",
    "data structures",
    "unit testing",
    "integration testing",
    "test driven",
    "object oriented",
    "system design",
    "rest api",
    "restful api",
    "computer science",
    "amazon web services",
    "microsoft azure",
    "google cloud",
]


@dataclass(frozen=True)
class KeywordSet:
    keywords: set[str]
    counts: Counter[str]


def _canonicalize(token: str) -> str:
    t = token.strip().lower()
    t = t.replace("–", "-")
    t = re.sub(r"\s{2,}", " ", t)
    return _CANONICAL_MAP.get(t, t)


def extract_keywords(text: str, top_n: int = 60) -> KeywordSet:
    words = tokenize_words(text)
    canon = [_canonicalize(w) for w in words]
    filtered = [w for w in canon if w not in _STOPWORDS and len(w) >= 2]

    counts: Counter[str] = Counter(filtered)

    lower_text = text.lower()
    for phrase in _MULTIWORD_SKILLS:
        if phrase in lower_text:
            counts[_canonicalize(phrase)] += 3

    common = counts.most_common(top_n)
    keywords = {k for k, _ in common}

    return KeywordSet(keywords=keywords, counts=counts)
