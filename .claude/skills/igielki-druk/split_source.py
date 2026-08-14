#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Rozbija powieść IGIEŁKI (info/powiesc1..4.md) na strukturę plików:

    opowiadania/
      tom-N-slug/
        _tom.md                      (# Tytuł tomu)
        czesc-K-slug/
          _czesc.md                  (# Tytuł części)
          NN - Tytuł rozdziału.md    (# Tytuł rozdziału  + treść)
        _dodatek.md                  (opcjonalne posłowie / "co zostało")

Hierarchia TOM → CZĘŚĆ → ROZDZIAŁ jest widoczna w drzewie katalogów.
Każdy plik rozdziału zaczyna się od `# <tytuł>`, dalej idzie treść
(separator sceny `---` zachowany). Numer rozdziału bierze się z nazwy pliku.

Uruchom raz, żeby (od)tworzyć `opowiadania/` ze źródeł w `info/`.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "info"
OUT = REPO / "opowiadania"

# Podział na części jest w każdym tomie taki sam: 1-7, 8-14, 15-20.
PART_RANGES = [(1, 7), (8, 14), (15, 20)]

TOMS = [
    dict(file="powiesc1.md", num=1,
         slug="tom-1-wielka-ksiega",
         title="Tom pierwszy: Wielka Księga Mchowa Dolnego",
         parts=[("Księga", "ksiega"),
                ("Ucieczka", "ucieczka"),
                ("Mchowo Górne", "mchowo-gorne")]),
    dict(file="powiesc2.md", num=2,
         slug="tom-2-napis-na-okladce",
         title="Tom drugi: Napis na okładce",
         parts=[("Nowi", "nowi"),
                ("Okładka", "okladka"),
                ("Oddanie", "oddanie")]),
    dict(file="powiesc3.md", num=3,
         slug="tom-3-zima-ktorej-nie-widzialam",
         title="Tom trzeci: Zima, której nie widziałam",
         parts=[("Przed snem", "przed-snem"),
                ("Zima", "zima"),
                ("Wiosna", "wiosna")]),
    dict(file="powiesc4.md", num=4,
         slug="tom-4-dwiescie-metrow",
         title="Tom czwarty: Dwieście metrów",
         parts=[("Sto siedemdziesiąt dni", "sto-siedemdziesiat-dni"),
                ("Dwieście metrów", "dwiescie-metrow"),
                ("Dwie kroniki", "dwie-kroniki")]),
]

CHAPTER_RE = re.compile(r"^#\s+ROZDZIAŁ\b", re.IGNORECASE)


def sanitize_filename(name):
    """Bezpieczna nazwa pliku na Windows (zachowuje polskie znaki i spacje)."""
    name = re.sub(r'[\\/:*?"<>|]', "", name)
    return name.strip().rstrip(".")


def part_index_for(chapter_no):
    for i, (lo, hi) in enumerate(PART_RANGES):
        if lo <= chapter_no <= hi:
            return i
    raise ValueError(f"Rozdział {chapter_no} poza zakresem części")


def clean_body(lines):
    """Usuwa puste linie i osamotnione '---' z początku i końca bloku treści."""
    def strip_edge(seq):
        while seq and (not seq[0].strip() or seq[0].strip() == "---"):
            seq.pop(0)
        return seq
    lines = strip_edge(lines)
    lines.reverse()
    lines = strip_edge(lines)
    lines.reverse()
    return lines


def parse_tom(path):
    """Zwraca (lista_rozdzialow, dodatek).

    rozdzial = dict(no, title, body_lines)
    dodatek  = dict(title, body_lines) albo None (materiał po ostatnim rozdziale).
    """
    raw = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, l in enumerate(raw) if CHAPTER_RE.match(l)]
    starts.append(len(raw))
    chapters, appendix = [], None

    for idx in range(len(starts) - 1):
        block = raw[starts[idx]:starts[idx + 1]]
        # pierwszy '## ' to tytuł rozdziału
        title, body_start = None, 1
        for j in range(1, len(block)):
            m = re.match(r"^##\s+(.*)$", block[j])
            if m:
                title = m.group(1).strip()
                body_start = j + 1
                break
        body = block[body_start:]

        # w ostatnim rozdziale może wisieć dodatek zaczynający się od '## '
        for j, l in enumerate(body):
            m = re.match(r"^##\s+(.*)$", l)
            if m:
                appendix = dict(title=m.group(1).strip(),
                                body_lines=clean_body(body[j + 1:]))
                body = body[:j]
                break

        chapters.append(dict(no=idx + 1, title=title,
                             body_lines=clean_body(body)))
    return chapters, appendix


def write_file(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main():
    if OUT.exists():
        import shutil
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    total_ch = 0
    for tom in TOMS:
        chapters, appendix = parse_tom(SRC / tom["file"])
        assert len(chapters) == 20, f'{tom["file"]}: {len(chapters)} rozdziałów'
        tom_dir = OUT / tom["slug"]
        write_file(tom_dir / "_tom.md", f'# {tom["title"]}')

        for part_i, (pname, pslug) in enumerate(tom["parts"]):
            part_dir = tom_dir / f"czesc-{part_i + 1}-{pslug}"
            write_file(part_dir / "_czesc.md",
                       f'# Część {["pierwsza", "druga", "trzecia"][part_i]} – {pname}')

        for ch in chapters:
            pi = part_index_for(ch["no"])
            pname, pslug = tom["parts"][pi]
            part_dir = tom_dir / f"czesc-{pi + 1}-{pslug}"
            fname = f'{ch["no"]:02d} - {sanitize_filename(ch["title"])}.md'
            body = "\n".join(ch["body_lines"])
            write_file(part_dir / fname, f'# {ch["title"]}\n\n{body}')
            total_ch += 1

        if appendix:
            write_file(tom_dir / "_dodatek.md",
                       f'# {appendix["title"]}\n\n' + "\n".join(appendix["body_lines"]))

    print(f"Utworzono {total_ch} rozdziałów w {OUT}")


if __name__ == "__main__":
    main()
