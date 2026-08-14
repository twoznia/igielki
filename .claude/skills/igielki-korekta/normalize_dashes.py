#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Normalizacja myślników w rozdziałach IGIEŁEK do polskiego standardu (półpauza „–").

Zamienia:
  - początek kwestii dialogowej „- " → „– "  (inaczej Markdown robi listę punktowaną),
  - pauzę w narracji ze spacjami „ - " → „ – ",
  - amerykańską pauzę „—" (em dash) → „–" (półpauza).

NIE rusza:
  - wiersza `# tytuł` (pierwszy nagłówek rozdziału),
  - separatorów sceny (samodzielne `---`),
  - łączników w złożeniach bez spacji (tik-tak, sześć-siedem, biało-czarny),
  - list punktowanych w plikach `_dodatek.md` (to nie dialog, punktory zostają).

Użycie:
  python normalize_dashes.py                 # wszystkie rozdziały opowiadania/**/NN - *.md
  python normalize_dashes.py <plik> [<plik>] # wskazane pliki
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
STORIES_DIR = REPO / "opowiadania"

DASH = "–"       # –  półpauza (en dash)
EMDASH = "—"     # —  pauza (em dash)


def normalize_line(line):
    stripped = line.strip()
    # nie ruszaj tytułu ani separatora sceny
    if stripped.startswith("# ") or stripped == "---":
        return line
    # em dash → półpauza (w każdej pozycji)
    line = line.replace(EMDASH, DASH)
    # początek kwestii dialogowej: „- " (albo z wcięciem) → „– "
    line = re.sub(r"^(\s*)-(\s)", r"\1" + DASH + r"\2", line)
    # pauza ze spacjami w środku zdania: „ - " → „ – " (pojedynczy łącznik)
    line = re.sub(r"(?<=\S) -(\s)", r" " + DASH + r"\1", line)
    return line


def normalize_text(text):
    return "\n".join(normalize_line(l) for l in text.split("\n"))


def process(path):
    path = Path(path)
    if path.name.startswith("_"):
        return False  # meta (_tom/_czesc/_dodatek) — pomijamy
    orig = path.read_text(encoding="utf-8")
    new = normalize_text(orig)
    if new != orig:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def all_chapter_files():
    return sorted(p for p in STORIES_DIR.glob("tom-*/czesc-*/*.md")
                  if not p.name.startswith("_"))


def main():
    args = sys.argv[1:]
    files = [Path(a) for a in args] if args else all_chapter_files()
    changed = 0
    for f in files:
        if process(f):
            changed += 1
            print(f"znormalizowano: {f.relative_to(REPO) if REPO in f.resolve().parents else f}")
    print(f"Zmienione pliki: {changed}/{len(files)}")


if __name__ == "__main__":
    main()
