# KAKO-KeyConcepts.md — Kako se dodaju, menjaju i brišu Key Concepts / Wikipedia kartice u xpongu

Konsolidovana referenca za xpong, izvedena iz Buchenberg recepta
(`KAKO-KeyConcepts.md`, buchenberg repo) i proverena protiv stvarnog koda
`app.js` i `data/concepts.json` (sesija 21, 27. jul 2026). Mehanizam je isti
duh kao u Buchenbergu, sa jednom namernom arhitekturnom razlikom zapisanom
u s18.

**Nastalo:** sesija 21, 27. jul 2026.

---

## 1. Arhitektura — izvor istine

- Podaci: `/var/www/xpong/data/concepts.json` — poseban fajl, pod git
  kontrolom, deo `xpongweb` repoa (ceo `data/` folder ide u git, bez
  Buchenbergovog `.gitignore` izuzetka).
- Jednojezične su — `name`/`description` postoje SAMO na engleskom, ne
  menjaju se promenom UI jezika.
- Naslov sekcije je hardkodovan string `'Key Concepts'` u `renderConcepts()`
  (`app.js`) — ne ide kroz `t()`, nikad se ne prevodi. xpong (za razliku od
  Buchenberga) NEMA `CONCEPT_TITLES` override mapu — nijedna stranica
  trenutno ne treba drugačiji naslov sekcije.
- Renderovanje je centralizovano u `app.js`, funkcija `renderConcepts()`
  (poziva se iz `render()` na svakoj stranici).

## 2. Ključna razlika od Buchenberga: nema CONCEPT_PAGES

Buchenberg drži belu listu `CONCEPT_PAGES` — svaka nova stranica mora se
ručno upisati u taj niz ili se kartice nikad ne prikazuju. xpong tu listu
nema: stranica se prepoznaje preko `data-page` atributa na `<body>`. Ovo je
namerna izmena iz sesije 18 — uklanja ceo razred greške ("nova stranica
zaboravlja upis u niz").

Tačan mehanizam (`app.js`, funkcija `renderConcepts()`):

    function renderConcepts() {
      var page = document.body.getAttribute('data-page');
      if (!page) return;
      var footer = document.getElementById('xp-footer');
      if (!footer) return;
      var existing = document.getElementById('xp-key-concepts');
      if (existing) existing.remove();
      fetch('data/concepts.json?t=' + Date.now())
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var concepts = data[page];
          if (!concepts || !concepts.length) return;
          // ... gradi <section id="xp-key-concepts">, insertuje pre #xp-footer
        })
        .catch(function () {});
    }

Šta ovo znači praktično:
- **`data-page="X"` na `<body>`** — jedini uslov da se kartice pokušaju
  učitati. Nova stranica automatski radi čim ima taj atribut.
- **Page key** = vrednost `data-page` atributa — mora se poklapati sa
  ključem u `concepts.json`.
- **`<div id="xp-footer">` mora postojati** — insertion point. Bez njega:
  tiho ništa, bez greške.
- **`data[page]` ne postoji ili prazan niz** → tiho ništa, bez greške.
- **Fetch cache-bust je AUTOMATSKI** (`?t=Date.now()`) — nema potrebe za
  `XP_VERSION` bump kad se menja SAMO `concepts.json` (potvrđeno u s18).
- Postojeća sekcija se uklanja pre ponovnog crtanja (`existing.remove()`).

## 3. Struktura concepts.json

    {
      "xray": [
        { "icon": "🩻", "name": "Telemetry", "description": "...", "wiki": "Telemetry" },
        ...
      ],
      "rl1": [ ... ],
      "rl2": [ ... ]
    }

- Grupisano po stranici (ključ = `data-page` vrednost).
- Svaka kartica: `{icon, name, description, wiki}`.
  - `name` — kratko, BEZ zagrada.
  - `wiki` — pun Wikipedia slug, uključujući disambiguation zagrade gde su
    deo stvarnog naslova.
  - `description` — prost tekst na engleskom (ubacuje se kao `innerHTML`).
  - Link se auto-gradi: `https://en.wikipedia.org/wiki/{wiki}`.

## 4. Pravilo sadržaja

Isto kao Buchenberg: samo pojmovi koji STVARNO imaju članak na engleskoj
Wikipediji. Broj kartica po stranici nema minimum ni maksimum — kriterijum
je stvarna relevantnost (trenutno: xray 4, rl1 3, rl2 4).

## 5. Kako DODATI karticu

1. Proveri da stranica ima `data-page="X"` na `<body>` i `#xp-footer`
   element (nema niz koji treba ažurirati).
2. Proveri da pojam STVARNO ima Wikipedia članak (web pretraga prvo).
3. Potvrdi tačan slug: `curl -sS -o /dev/null -w "%{http_code} %{url_effective}" -L https://en.wikipedia.org/wiki/SLUG`.
4. Odaberi icon koji se ne poklapa sa postojećim na ISTOJ stranici.
5. Dodaj JSON objekat na KRAJ niza za tu stranicu.
6. Validiraj JSON PRE i POSLE upisa (§7) — obavezno.
7. Browser test — jedina prava potvrda.

## 6. Kako IZMENITI ili OBRISATI karticu

Izmena: pronađi karticu po `name` ili `wiki`
(`grep -n '"wiki": "TAČAN_SLUG"' concepts.json`), izmeni `str.replace` +
`assert count==1`. Validiraj posle.

Brisanje: ukloni ceo `{...}` objekat kartice. Pažnja na zareze — brisanje
prvog ili poslednjeg elementa niza čest je izvor slomljenog JSON-a.
Validiraj ODMAH posle brisanja.

## 7. Validacija JSON-a — PRE pisanja na disk, ne samo posle

    python3 -c "import json; json.load(open('/var/www/xpong/data/concepts.json')); print('JSON OK')"

**Lekcija iz sesije 20 (bag B4):** upisan je `\U0001f5fa` (Python escape)
direktno u JSON string, koji poznaje samo `\uXXXX`. Fajl je pisan pre
validacije stringa, pa je nevažeći JSON završio na disku. `.catch(function(){})`
u `app.js` guta grešku bez traga — nevažeći JSON znači **tiho nestajanje Key
Concepts kartica na SVIM stranicama, svim jezicima, bez ikakvog vizuelnog
znaka.**

**Pravilo (strože od Buchenberg recepta):** validiraj `json.loads(s)` na
stringu PRE upisa na disk, ne samo `json.load` na fajlu posle.

## 8. Tehnička metoda izmene

    cd /var/www/xpong && python3 - << 'PYEOF'
    import json
    f = "data/concepts.json"
    s = open(f, encoding="utf-8").read()

    old = '<TAČAN POSTOJEĆI JSON FRAGMENT — anchor>'
    new = '<NOVI JSON FRAGMENT>'

    assert s.count(old) == 1, f"anchor count = {s.count(old)}"
    new_s = s.replace(old, new)

    json.loads(new_s)  # validacija PRE pisanja na disk (lekcija s20 B4)
    open(f, "w", encoding="utf-8").write(new_s)
    json.load(open(f, encoding="utf-8"))  # provera posle pisanja
    print("OK — JSON valid pre i posle")
    PYEOF

## 9. Git

`concepts.json` je pod git kontrolom u `xpongweb` repou, commituje se
normalno.

## 10. Poznati slučajevi — ledger

| Slučaj | Sesija | Detalj |
|---|---|---|
| `\U0001f5fa` Python escape upisan direktno u JSON | s20 (bag B4) | Nevažeći JSON na disku, kartice tiho nestale na svim stranicama; ispravljeno vraćanjem backupa + validacija pre pisanja |

## 11. Poreklo

Recept izveden iz Buchenberg `KAKO-KeyConcepts.md` (sesije 90, 96, 108) i
prilagođen stvarnom xpong kodu. Glavna razlika: `data-page` atribut umesto
`CONCEPT_PAGES` niza (s18 odluka).

---

*Flavio & Claude · xpong · KAKO-KeyConcepts.md · 27. jul 2026.*
