# Session 05 — Landing dopune: hero ikona + X-Ray Wikipedia linkovi

**Datum:** 25 Jun 2026
**Fokus:** dve male home-only dopune po buchenberg obrascu — favicon ikona
pored „xpong" naslova u herou, i dva nova Key Concepts linka ka X-Ray temama.
Bez M1.

## Otvaranje (health snapshot)
- xpong @ `11674c9` (s04), čisto, u sinhronu.
- xpongweb @ `31984f3` (s04), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s04'`.
- `health_check.py`: i dalje ne postoji (ručni snapshot komandama).

## Šta je urađeno
1. **Hero ikona (home).** U `.xp-hero-logo` dodat `<img src="favicon.svg"
   class="xp-hero-icon">` ispred „xpong", po buchenberg obrascu. CSS:
   `.xp-hero-logo` dobio `display:flex; align-items:center;
   justify-content:center; gap:16px;`; nova `.xp-hero-icon { 64x64;
   flex-shrink:0 }`. Razmak ikona↔naslov = 16px (identično buchenbergu).
2. **Dva Key Concepts linka (home).** U `data/concepts.json`, ključ `home`,
   dopisana na kraj (4 → 6): 🩻 „X-ray style art" (`X-ray_style_art`) i
   🎸 „Rock Art and the X-Ray Style" (`Rock_Art_and_the_X-Ray_Style`) —
   bajt-identično buchenbergu (ikone, slug-ovi, opisi). Tematski koreni
   X-Ray imena: aboridžinska likovna tradicija + Strummerov album 1999.
3. **Verzija:** `XP_VERSION` s04 → s05; `XP_VERSION_DATE` → 25 Jun 2026.

## Odluka: data/ direktorijum ostaje
Pitanje (Flavio): treba li nam `data/` ubuduće? Provereno na živom
buchenbergu — njegov `data/` je generisani korpus (stotine MB, gitignored).
Naš je drugačiji: `data/concepts.json` se commituje i već ga `app.js:159`
fetcha. `data/` ostaje kao prirodno mesto za kurirane statičke JSON-ove
budućih RL faza (manifesti hiperparametara, opisi agenata, preseti) —
paralela buchenbergovom version.json/books.json, ne generisanom korpusu.

## Lekcije / ledger
- **Atomična multi-fajl izmena.** Sve 4 izmene kroz jednu Python skriptu
  (`/tmp`, van repoa): čita sve → `assert count==1` po zameni + JSON
  re-parse i provera duplikata po `wiki` slug-u → upiše tek kad sve
  asercije prođu. Ako bilo šta padne, ništa se ne piše.
- **Ikona „veća" = optička, ne stvarna.** Oba favicona su 64×64, ista siva
  podloga (`#d8dadd`, rx=14). Razlika je gustina motiva: buchenberg šestougao
  puni ploču (~9px margine), xpong motiv razuđen sa praznim sivim prostorom.
  Okvir identičan — ostavljeno kako jeste (Flaviova odluka).
- **JSON re-serializacija.** `json.dumps(ensure_ascii=False, indent=2)`
  prepisuje ceo concepts.json; ćirilica/emoji ostaju čitljiv UTF-8,
  validnost garantovana parserom.

## Završno stanje
- M0 landing dopunjen na `https://xpong.opik.net` (s05): hero ikona pored
  „xpong" (64×64, gap 16px), Key Concepts grid 6 kartica (4 stara + 2 X-Ray).
  Potvrđeno u brauzeru (hard refresh, footer „s05").
- xpongweb fajlovi dirnuti: `index.html`, `xpong.css`, `app.js`,
  `data/concepts.json`. `favicon.svg` netaknut.
- Igra i dalje neimplementirana (M1 otvoren).

## Sledeće (M1)
- Klasičan Pong: `game.html` — canvas, reketi, lopta, gol L/D, tastatura +
  touch, responzivno; ukloniti `soon` s nav „The Game".
- Popuna landing sadržaja (istorija Ponga + X-Ray okvir) + prevodi de/it/hr/sr.
