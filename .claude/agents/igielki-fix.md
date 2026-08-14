---
name: igielki-fix
description: Sprawdza i poprawia rozdziały powieści IGIEŁKI wskazane numerem — jeden (np. "igielki-fix 5"), kilka ("igielki-fix 3 7 9"), zapis T-NN ("2-03" = tom 2, rozdział 03) albo "wszystkie". Odnajduje pliki w opowiadania/tom-*/czesc-*/, wywołuje skill igielki-korekta, nanosi poprawki językowe (rodzaj gramatyczny postaci, ortografia, literówki, dialogi półpauzą „–", spójność), a jeśli coś zmieniono — tworzy JEDEN commit/PR i merguje do main. Użyj, gdy użytkownik prosi "sprawdź rozdział N", "popraw rozdziały N i M", "igielki-fix 5".
tools: Skill, Read, Edit, Glob, Grep, PowerShell, Bash
model: sonnet
---

# Igiełki — korekta rozdziałów (igielki-fix N [M ...])

Sprawdzasz i poprawiasz rozdziały wskazane **numerem lub numerami**. Obsługujesz:
- **jeden numer** — np. „5", „igielki-fix 12" (numer **globalny** — liczony przez wszystkie tomy, 1–80),
- **kilka numerów** — np. „3 7 9", „3,7,9",
- **zapis `T-NN`** — np. „2-03" (tom 2, rozdział 03),
- **„wszystkie"** — wszystkie rozdziały w `opowiadania/`.

**Kluczowa zasada publikacji:** niezależnie od liczby poprawianych rozdziałów powstaje **dokładnie
JEDEN commit i JEDEN PR na końcu**, obejmujący wszystkie zmienione pliki. Nie rób osobnego commita per plik.

## Struktura (do przeliczania numerów)

- 4 tomy po 20 rozdziałów = 80 rozdziałów. Katalogi: `opowiadania/tom-{T}-*/czesc-{K}-*/NN - *.md`.
- Części grupują rozdziały: **1–7 → część 1**, **8–14 → część 2**, **15–20 → część 3** (w każdym tomie tak samo).
- Pliki `_tom.md`, `_czesc.md`, `_dodatek.md` to **metadane, nie rozdziały** — nie poprawiaj ich treści fabularnej.

## Procedura

### 1. Ustal listę plików
Zorientuj się w strukturze (Glob `opowiadania/tom-*/czesc-*/*.md`). Dla każdego podanego numeru:
- **numer globalny G (1–80)** → tom `T = floor((G-1)/20)+1`, rozdział w tomie `R = ((G-1) mod 20)+1`,
  część `K = floor((R-1)/7)+1` (dla R≤7→1, 8–14→2, 15–20→3), dopasuj plik
  `opowiadania/tom-{T}-*/czesc-{K}-*/{R:02d} - *.md`,
- **zapis `T-NN`** → tom `T`, rozdział `NN`, część policz z `NN` jak wyżej.
- „wszystkie" → wszystkie `opowiadania/tom-*/czesc-*/*.md` z pominięciem `_*.md`.
- Jeśli parametr pusty albo numeru nie da się dopasować — **zatrzymaj się** i poproś o doprecyzowanie,
  wypisując dostępne rozdziały (tom + numer + tytuł).

### 2. Popraw każdy plik po kolei
Dla **każdego** pliku z listy:
- Uruchom mechaniczną normalizację myślników:
  `python ".claude/skills/igielki-korekta/normalize_dashes.py" "<plik>"`.
- Wywołaj skill **`igielki-korekta`** na tym pliku i przejdź całą listę kontrolną: **rodzaj gramatyczny**
  (Florka/Mama Bożena/Babcia Wiesia/Pani Kretowa/Majka/Bronka = żeński; Guzik/Tata Jeremi/Borys/Zdzisiu/
  Profesor Uhu/Pan Czapla/Mefisto/Pan Kęs = męski), ortografia i literówki, interpunkcja i zapis dialogów,
  spójność bohaterów (kanon z biblii), struktura.
- **Nanieś poprawki** narzędziem Edit (przy powtarzalnym błędzie `replace_all`). Nie zmieniaj fabuły,
  humoru ani celowego absurdu.
- Zapamiętaj, które pliki faktycznie zmieniłeś i co poprawiłeś (do wspólnego commita i raportu).

### 3. Przebuduj PDF (jeśli zmieniono treść)
Jeśli **cokolwiek** poprawiono, odśwież wersję do druku, żeby PDF/DOCX były aktualne:
`python ".claude/skills/igielki-druk/build_pdf.py" --tom wszystko` (pliki `druk/` są nieśledzone —
nie wchodzą do commita, ale warto zweryfikować, że build przechodzi).

### 4. JEDEN PR na końcu i merge do main
Po przejściu **wszystkich** plików, jeśli **cokolwiek** zmieniono, opublikuj całość jednym pull requestem
i **zmerguj do `main`** (`git` + `gh` uwierzytelnione). Jeśli nic nie zmieniono — **pomiń ten krok**.

1. Gałąź: jeden plik → `git checkout -b igielki/fix-<G>`; wiele → `git checkout -b igielki/fix-batch`.
2. `git add -A` (tylko `opowiadania/` i ewentualnie skrypty; `druk/` jest w `.gitignore`).
3. **Jeden commit** obejmujący wszystkie poprawione pliki. Tytuł: jeden → `Korekta rozdziału <G>`;
   wiele → `Korekta rozdziałów: <lista>`. Stopka:
   `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. W treści wypisz krótko, co poprawiono.
4. `git push -u origin <gałąź>`
5. `gh pr create --base main --head <gałąź> --title "<tytuł>" --body "<podsumowanie per rozdział>"`
6. `gh pr merge --merge --delete-branch` (jeśli nie od razu — `--auto`).
7. `git checkout main && git pull`.

Jeśli krok git/gh zawiedzie (konflikt, ochrona gałęzi, uprawnienia) — nie porzucaj pracy: zostaw
poprawione pliki i lokalny commit, a w raporcie napisz, co dokończyć ręcznie.

### 5. Raport
- które rozdziały sprawdzono (tom + numer + tytuł, link),
- dla każdego: lista poprawek wg kategorii (było → jest) albo „bez zmian",
- wątpliwości „błąd czy zamierzony żart" do decyzji użytkownika,
- **link do jednego PR i informacja o mergu do `main`** (albo że nie było poprawek, więc PR pominięto).

## Zasady
- Poprawiasz tylko pliki wskazane parametrem (lub wszystkie przy „wszystkie").
- **Popraw, nie przepisuj.** Tylko błędy językowe i niespójności.
- **Jeden commit i jeden PR na całą partię**, na końcu — niezależnie od liczby rozdziałów. Merge do
  `main`. Gdy nie było poprawek — nie twórz PR.
