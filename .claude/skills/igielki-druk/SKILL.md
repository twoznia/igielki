---
name: igielki-druk
description: Buduje wersję do druku (PDF/DOCX) powieści IGIEŁKI z hierarchią TOM → CZĘŚĆ → ROZDZIAŁ. Domyślnie PDF całości (cztery tomy). Parametry typ (pdf/docx/oba) i tom (N/calosc/wszystko). PDF powstaje CZYSTO w Pythonie (reportlab) — bez MS Word i bez drukarki; ma klikalny spis treści i zakładki (tom→część→rozdział). Użyj, gdy użytkownik prosi o "wersję do druku", "pdf", "docx", "plik do wydruku tomu N".
---

# igielki-druk — wersja do druku (PDF/DOCX)

Składasz powieść z `opowiadania/` (struktura TOM → CZĘŚĆ → ROZDZIAŁ) do pliku do druku.
Silnik: [`build_pdf.py`](build_pdf.py). Rozbicie źródeł na pliki: [`split_source.py`](split_source.py).

> **NIGDY nie używaj MS Word do konwersji.** Word przy starcie budzi domyślną drukarkę.
> PDF robimy **czysto w Pythonie (reportlab)** — bez Worda, bez drukarki. Nie zmieniaj tego
> na ścieżkę przez Worda/`docx2pdf`.

## Struktura źródeł (widoczna hierarchia)

```
opowiadania/
  tom-1-wielka-ksiega/
    _tom.md                       # tytuł tomu
    czesc-1-ksiega/
      _czesc.md                   # tytuł części
      01 - Kolce.md               # rozdział (# tytuł + treść)
      ...
    czesc-2-ucieczka/
    czesc-3-mchowo-gorne/
    _dodatek.md                   # posłowie / "co zostało na tom" (opcjonalne)
  tom-2-... / tom-3-... / tom-4-...
```

- Każdy **tom** = jeden plik źródłowy `info/powiesc{1..4}.md`.
- Każdy tom ma **3 części** (rozdziały 1–7, 8–14, 15–20) i **20 rozdziałów**.
- Podział na tomy/części jest **taki, jak w powieści** (sekcja „PLAN CAŁOŚCI"), a nie na równe kawałki.
- Aby (od)tworzyć `opowiadania/` ze źródeł: `python ".claude/skills/igielki-druk/split_source.py"`.

## Jak uruchomić

```bash
# DOMYŚLNIE: PDF całości (cztery tomy)
python ".claude/skills/igielki-druk/build_pdf.py"

# konkretny tom (PDF)
python ".claude/skills/igielki-druk/build_pdf.py" --tom 2

# każdy tom osobno + całość
python ".claude/skills/igielki-druk/build_pdf.py" --tom wszystko

# format: pdf (domyślnie) | docx | oba
python ".claude/skills/igielki-druk/build_pdf.py" --tom 3 --typ oba
```

- **`--typ`**: `pdf` (domyślnie) · `docx` · `oba`.
- **`--tom`**: `N` · `calosc` · `wszystko`. Brak = **całość**.
- Pliki lądują w `druk/` (na żądanie, nieśledzone w repo).
- Wymaga `reportlab` (PDF) i `python-docx` (DOCX): `python -m pip install reportlab python-docx`.

## Co dostajesz w PDF (reportlab)

- **Klikalny spis treści** (Tom → Część → Rozdział) z numerami stron.
- **Zakładki/outline po lewej: Tom → Część → Rozdział** — klikalne.
- Tekst 12 pt (justowany, wcięcie akapitu), rozdział 15, część 20, tom 26; każdy tom, każda część
  i każdy rozdział od nowej strony; numeracja stron; separator sceny `---` jako wyśrodkowana gwiazdka.
- **Czcionka Montserrat**, jeśli TTF jest w `fonts/` albo w `C:\Windows\Fonts`; inaczej **Arial**
  (polskie znaki OK). Aby mieć Montserrat: wrzuć `Montserrat-Regular.ttf` i `Montserrat-Bold.ttf`
  (opcjonalnie -Italic/-BoldItalic) do folderu `fonts/` w repo.

## DOCX (opcjonalnie, `--typ docx`/`oba`)

- python-docx; nagłówki jako style Word (Heading 1=Tom, 2=Część, 3=Rozdział) → panel nawigacji.
- Wstawione **pole spisu treści** (klikalne po aktualizacji: w Wordzie Ctrl+A, potem F9).
- Generowanie DOCX **nie uruchamia Worda** (to zwykły plik).

## Parametry

Czcionka, rozmiary, marginesy, tytuł serii — stałe na górze `build_pdf.py`.
Tytuły tomów i części oraz podział rozdziałów na części — w `split_source.py` (`TOMS`, `PART_RANGES`).
