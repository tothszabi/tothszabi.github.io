#!/usr/bin/env python3
"""
Scan shipped content for unqualified medical/curative claims.

Chakra work is a wellbeing service, not healthcare. Hungarian and EU consumer
law limits health claims for non-medical services, so copy must not promise to
cure, treat, or diagnose anything.

A line-based grep cannot do this job: HTML wraps prose across lines, so a
sentence's negation ("nem helyettesíti...") often sits on a different line from
its claim word ("kezelést"). This script strips tags, normalises whitespace,
splits into sentences, and only flags a sentence that contains a claim word
with NO qualifier in the same sentence.

Usage: python3 tools/claims-check.py [paths...]   (default: repo root)
Exit:  0 = clean, 1 = review needed
"""

import html
import re
import sys
from pathlib import Path

# Words that describe medical action. Present in a sentence without a
# qualifier, they read as a health claim.
CLAIM = re.compile(
    r"gyógyít|meggyógy|gyógyul|kezel[éi]|betegség|diagnó|tünet",
    re.IGNORECASE,
)

# A qualifier turns the sentence into a disclaimer rather than a claim.
QUALIFIER = re.compile(
    r"\bnem\b|\bsem\b|\bne\b|helyettesít|nincs|kiegészítő|adatkezel",
    re.IGNORECASE,
)

SKIP_DIRS = {"tasks", "reports", "node_modules", ".git", "tools"}
SUFFIXES = {".html", ".md"}

TAG = re.compile(r"<[^>]+>")
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
# Markdown tables document the placeholder tokens; not prose.
MD_TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n\n+")


def sentences(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    text = COMMENT.sub(" ", text)
    text = MD_TABLE_ROW.sub(" ", text)
    text = TAG.sub(" ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    return [s.strip() for s in SENTENCE_SPLIT.split(text) if s.strip()]


def collect(roots: list[str]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        p = Path(root)
        if p.is_file():
            files.append(p)
            continue
        for f in sorted(p.rglob("*")):
            if f.suffix not in SUFFIXES:
                continue
            if SKIP_DIRS & set(f.parts):
                continue
            files.append(f)
    return files


def main() -> int:
    roots = sys.argv[1:] or ["."]
    findings = []

    for path in collect(roots):
        for sentence in sentences(path):
            claim = CLAIM.search(sentence)
            if claim and not QUALIFIER.search(sentence):
                findings.append((path, claim.group(0), sentence))

    if not findings:
        print("✓ No unqualified medical claims found.")
        return 0

    print(f"✗ {len(findings)} sentence(s) need review:\n")
    for path, word, sentence in findings:
        snippet = sentence if len(sentence) <= 160 else sentence[:157] + "..."
        print(f"  {path}")
        print(f"    claim word: {word!r}")
        print(f"    sentence:   {snippet}\n")
    print("Rephrase, or qualify the sentence (e.g. 'nem helyettesíti az orvosi kezelést').")
    return 1


if __name__ == "__main__":
    sys.exit(main())
