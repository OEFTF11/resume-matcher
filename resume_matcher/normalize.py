from __future__ import annotations

import re


_BULLETS = ["•", "◦", "▪", "●", "‣", "∙", "·"]


def normalize_text(text: str) -> str:
    if not text:
        return ""

    t = text

    for b in _BULLETS:
        t = t.replace(b, " ")

    t = t.replace("\u00a0", " ")
    t = t.replace("\t", " ")
    t = t.replace("\r", "\n")

    t = re.sub(r"[ ]{2,}", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)

    return t.strip()


def tokenize_words(text: str) -> list[str]:
    if not text:
        return []

    lower = text.lower()

    words = re.findall(r"[a-z0-9\+\#\.]{2,}", lower)
    return words
