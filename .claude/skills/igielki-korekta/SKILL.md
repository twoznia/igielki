---
name: igielki-korekta
description: Sprawdza i POPRAWIA tekst rozdziału powieści IGIEŁKI — poprawność językową (ortografia, literówki, interpunkcja), rodzaj gramatyczny postaci (Florka, Mama Bożena, Babcia Wiesia, Pani Kretowa, Majka, Bronka = żeński; Guzik, Tata Jeremi, Borys, Zdzisiu, Profesor Uhu, Pan Czapla, Mefisto, Pan Kęs = męski), zapis dialogów półpauzą „–" oraz spójność bohaterów i stylu. Nie zmienia fabuły. Użyj, gdy użytkownik prosi "sprawdź/popraw rozdział", "korekta", "literówki". Do sprawdzenia konkretnego pliku po numerze użyj agenta igielki-fix.
---

# Igiełki — korekta i poprawa tekstu

Sprawdzasz rozdział powieści „Igiełki" pod kątem **poprawności językowej i spójności**, a potem
**nanosisz poprawki** (Edit). Poprawiasz język — **nie przepisujesz fabuły**, nie zmieniasz stylu,
humoru ani celowego absurdu.

Mechaniczną normalizację myślników robi skrypt [`normalize_dashes.py`](normalize_dashes.py)
(dialogi i pauzy → półpauza „–", z pominięciem list punktowanych w `_dodatek.md`).
Resztę (rodzaj, ortografia, spójność) sprawdzasz czytając.

## Jak działać

1. **Wczytaj** wskazany plik (Read). Jeśli nie podano — zapytaj który albo weź plik z rozmowy.
2. **Znormalizuj myślniki**: `python ".claude/skills/igielki-korekta/normalize_dashes.py" <plik>`
   (albo bez argumentu = wszystkie rozdziały). Nie dotyka `# tytułu` ani separatorów sceny `---`.
3. **Przejrzyj** tekst wg listy kontrolnej i wypisz usterki (cytat → propozycja).
4. **Popraw** przez Edit (przy powtarzalnym błędzie `replace_all`).
5. **Raport**: lista zmian (było → jest) wg kategorii. Jeśli nic — napisz wprost.

## Lista kontrolna

### 1. Rodzaj gramatyczny (najważniejsze)
Gatunek to nie to samo co rodzaj postaci. *Jeż, kret, żółw, nietoperz, ślimak* są męskie,
*sowa, kaczka, wiewiórka* żeńskie — ale **odmieniaj postać wg jej rodzaju**, nie wg gatunku:

- **Rodzaj męski:** **Guzik**, **Tata Jeremi**, **Borys** (borsuk), **Zdzisiu** (ślimak),
  **Profesor Uhu** (sowa!), **Pan Czapla**, **Mefisto** (kot), **Pan Kęs** (bóbr), **Patyk**.
  Formy męskie: *Guzik powiedział, zwinął się, poszedł; Uhu udawał, że tak miało być*
  (NIE „Uhu udawała", mimo że „sowa").
- **Rodzaj żeński:** **Florka**, **Mama Bożena**, **Babcia Wiesia**, **Ciocia Genowefa**,
  **Pani Kretowa** (kret!), **Majka** (wiewiórka), **Jola** (kaczka), **Bronka** (nietoperz),
  **Pani Puszczyk** (żółw!). Formy żeńskie: *Florka powiedziała, była, poszła; Kretowa wiedziała*.
- **Plakusy** — liczba mnoga (*Plakusy przyszły, zbudowały, negocjowały*).
- Uwaga na Panią Kretową, Profesora Uhu, Panią Puszczyk i Bronkę — tam gatunek myli rodzaj
  najłatwiej. Sprawdź też zaimki i końcówki: *ten/ta, sam/sama, cały/cała, gotów/gotowa*.

### 2. Składnia: przypadki i przyimki
- **Orzecznik po „być" w NARZĘDNIKU:** *„będę kronikarka"* → **„będę kronikarką"**,
  *„jest teraz kot"* → zależnie od konstrukcji (*„to jest kot"* OK; *„był kotem"* — narzędnik).
- **Rekcja przyimków:** sprawdź, czy przyimek i przypadek pasują (*„do terminu"* → **„w terminie"/„na czas"**).
- Zgoda przydawki z rzeczownikiem: *„z wielkim, ciężką łapą"* → *„z wielką, ciężką łapą"*.

### 3. Naturalność / kalki językowe
- Wyłapuj sformułowania nienaturalne po polsku i zamień na naturalny odpowiednik — **bez zmiany
  sensu i żartu**. Czytaj każde zdanie „na głos w głowie": to książka do czytania na głos.
- **Nie** ruszaj celowych żartów, zawołań i powtórzeń bohaterów.

### 4. Ortografia i literówki
- **ó/u, rz/ż, ch/h, ą/ę, ś/sz, ci/ć** (np. *jeż, mchowo, wróć, chrupać, spłuczka, żołądek*).
- Przestawione/zgubione/podwojone litery, sklejone lub rozdzielone wyrazy.
- Wielkie litery w nazwach własnych: **Mchowo Dolne, Mchowo Górne, Wielka Księga, Plakusy,
  Igiełkowie**, imiona postaci. „**Patyk**" jako imię — wielką literą.

### 5. Interpunkcja i zapis dialogów
- **Dialogi półpauzą „–" (U+2013)** na początku kwestii, spacja po niej. **Zwykły „-" na początku
  kwestii → „–"** (inaczej Markdown robi listę punktowaną). Atrybucja w kwestii też „–"
  (*„– Wiem – powiedziała Florka."*). To robi `normalize_dashes.py`.
- **Myślnik/pauza w narracji → „–"** (półpauza ze spacjami). **Nie** ruszaj **łączników w złożeniach**
  bez spacji: *tik-tak, sześć-siedem, biało-czarny*.
- **Em-dash „—" → „–"** (polski standard to półpauza, nie pauza amerykańska).
- **Listy punktowane w `_dodatek.md`** (posłowie / „co zostało") **zostają punktorami `- `** —
  to nie dialog. Skrypt ich nie rusza.
- Zdania pytające/wykrzyknikowe z `?`/`!`; wielokropek `...`; brak podwójnych spacji;
  cudzysłowy polskie „…".

### 6. Spójność bohaterów (kanon)
- **Florka Igiełka** — 6 lat, mówi dużo i szybko, kronikarka Mchowa, pisze koszmarnie, uczy się
  czytać; **główna bohaterka**. Ma poczucie sprawiedliwości „wielkości szafy".
- **Guzik Igiełka** — 4 lata, mówi mało (często jedno celne zdanie), **nosi Patyk**, **je tylko
  rzeczy okrągłe**, zwija się w kulkę.
- **Mama Bożena** — weterynarka owadów; jej **kawa nigdy nie jest dopita** (bieżący gag).
- **Tata Jeremi** — „pracuje w tabelkach", wchodzi w każdą zabawę za głęboko.
- **Babcia Wiesia** — twierdzi, że była **traktorem** (nigdy nierozstrzygnięte); miesza prawdę z bujdą.
- **Borys** — borsuk, kolega Florki, zawsze „**prawie**" (prawie wygrał, prawie widział).
- **Pani Kretowa** — nauczycielka kret, prawie nic nie widzi, a wie wszystko.
- **Zdzisiu** — listonosz ślimak, **nigdy nie zdąża** (długi lont zaległej poczty).
- **Mefisto** — kot; wygłasza filozoficzne monologi, **które słyszy tylko czytelnik** (bohaterowie: „miau").
- **Profesor Uhu** — sowa, strażnik alfabetu, kiepski w tym, ma świetne wymówki.
- **Bronka Nietoperz** — śpi w dzień, czyta najlepiej w klasie (tomy 2–4).
- **Zasada świata:** nikt nie jest złoczyńcą; konflikt bierze się z tego, że ktoś nie wie,
  nie zapytał albo się wstydzi. Dorośli też popełniają błędy i je naprawiają.
- Sprawdź, czy nie pomylono imion (Florka/Guzik, Borys/Zdzisiu) i czy cechy się zgadzają
  (np. Guzik je coś nieokrągłego bez powodu — zgłoś).

### 7. Struktura i styl (lekko)
- Plik rozdziału zaczyna się od **`# Tytuł`** (sam tytuł, **bez** prefiksu „Rozdział N:" — numer jest
  w nazwie pliku). Jeśli natrafisz na taki prefiks w treści, usuń go.
- **Separator sceny to samodzielna linia `---`** — zostaw (skrypt jej nie rusza).
- Krótkie akapity (dorosły czytający musi mieć gdzie wziąć oddech); zdanie-puenta na końcu akapitu.
- **Bez morałów do kamery** i **bez zakończeń typu „Dobranoc"/spanie** — jeśli trafisz na doklejony
  morał, zgłoś. Rozdział domyka **zmiana zachowania**, nie deklaracja.
- **Nie** poprawiaj celowych efektów i powtórzeń (np. jedenastokrotne słowo Florki) — to część stylu.

## Zasady
- **Popraw, nie przepisuj.** Zmieniasz błędy językowe i niespójności, nie fabułę ani humor.
- Przy wątpliwości „błąd czy zamierzony żart" — zostaw, ale **wypisz w raporcie** jako pytanie.
- Po skończeniu zwięzły raport (było → jest). **Nie commituj ani nie pushuj** (to zadanie agenta
  `igielki-fix`).
