# Session 07 — M1: klasičan Pong (2 igrača, tastatura + touch), i18n, Key Concept

**Datum:** 26 Jun 2026
**Fokus:** M1 — `game.html` + `game.js`, klasičan Pong za dva igrača (w/s vs o/l,
+ touch), responzivan canvas koji prati temu; aktivacija nav stavke „The Game";
i18n HUD-a u svih 5 jezika; jedan Key Concept (Pong) na game stranici.

## Otvaranje (health snapshot)
- xpong @ `9419c25` (s06), čisto, u sinhronu.
- xpongweb @ `b82e928` (s06), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s06'` (živo) — README je pokazivao s04 (zaostao
  dve sesije; s05/s06 nisu menjale „trajno stanje" pa ga nisu ažurirale).
- `health_check.py`: i dalje ne postoji.

## Odluke pre koda (rendgenisane, ne refleksne)
- **health_check.py — ODLOŽEN do M1+.** Buchenbergov ima suštinu (živi brojevi
  korpusa iz baze); naš bi danas bio tanak wrapper oko git/curl koji ionako
  prikazujemo i OK-ujemo. Loš health check (zastari, vraća lažno zeleno) gori je
  od nijednog. Vredeće kad poraste struktura — kao STRUKTURNI čeker (paritet
  i18n ključeva među jezicima, validnost concepts.json, postojanje nav stranica),
  ne kao wrapper. Odloženo svesno.
- **Python venv — NE sada.** xpong nema nijednu pip zavisnost; sve sesijske
  /tmp skripte koriste samo stdlib. Venv bez requirements.txt ne izoluje ništa.
  Venv (u `/home/balsam/xpong/venv`, s requirements.txt) tek kad se pojavi prva
  stvarna zavisnost (npr. Pillow za sprite-ove). Provereno: venv ne postoji,
  nijedan .gitignore ga ne pominje — ništa da truli.

## Šta je urađeno
1. **`game.js`** (nov, ~300 linija) — Pong engine, čist vanilla, bez zavisnosti.
   Logički koord. sistem 800×500, skalira CSS-om, devicePixelRatio za oštrinu.
   Boje čitane iz CSS varijabli (`getComputedStyle`) → prati svetlu/tamnu temu;
   MutationObserver na `<html>` (data-theme + lang) re-čita boje i osveži HUD.
   Fizika: lopta odbija od zidova/reketa, ubrzava na udarcu (cap), ugao zavisi
   od mesta pogotka; gol L/D; do 11 → pobednik.
2. **`game.html`** (nov) — prati about.html obrazac (head, header injektovan,
   footer, app.js + game.js na kraju). Scorebar, canvas, status, Start/Reset,
   legenda kontrola. HUD elementi s ID-jevima koje game.js traži.
3. **Kontrole — 2 igrača, ravnopravno:** levi w/s, desni **o/l** (prvobitno
   strelice; promenjeno na o/l radi simetrije — slova kao slova, i strelice
   skroluju stranicu). Touch: svaka polovina canvasa upravlja svojim reketom
   (`touch-action: none` da povlačenje ne skroluje). Space = start/pauza.
4. **Nav aktivacija** — uklonjen `soon: true` s game stavke (app.js); nav_game
   ključ već postojao u 5 jezika iz ranije.
5. **i18n HUD** — 16 `g_*` ključeva × 5 jezika (EN/DE/IT/HR/SR-ćir). Statika
   kroz `data-i18n` (app.js applyI18n je prevodi); dinamičke poruke
   (Start/Pause/Play again, status, pobednik) kroz `window.xpong.t()` s EN
   fallback-om — hook koji app.js VEĆ izvozi (`window.xpong`, ne moj
   pretpostavljeni `window.XP`).
6. **Key Concept (game)** — `concepts.json` dobio `game` sekciju: 1 kartica
   (Pong, kopija home kartice). renderConcepts je sam ubacuje (data-page=game).
7. **CSS** — `.xp-game-*` blok (scorebar mono, canvas-box, dugmad, legenda s
   `<kbd>`), + game-mobile @media. Sve boje preko CSS varijabli (prati temu).
8. **Verzija** — s06 → s07.

## Lekcije / ledger
- **`node` ne postoji na foxuno.** `node --check` dao exit 127 (command not
  found), a moj `&& OK || FAIL` omotač to prijavio kao „SYNTAX FAIL" — lažni
  alarm koji sam sam proizveo. Sintaksu JS-a potvrđujemo u BRAUZERU (konzola),
  nema lokalnog lintera. Pravilo: sirovi izlaz/exit kod prvo, ne omotač.
- **`grep -c` broji LINIJE, ne pojave.** data-i18n provera dala 11 umesto 13
  jer se g_up/g_down javljaju dvaput u istom redu. Za pojave: `grep -o | wc -l`.
- **Proveri postojeći hook pre nego što ga praviš.** app.js već izvozi
  `window.xpong = {t, getLang, render}`. Pretpostavio sam `window.XP` i hteo da
  ga „dodam" — nije trebalo dirati app.js. (Isti nauk kao node: proveri, ne
  pretpostavi.)
- **Jezik u letu se NE zamrzava (opcija 1).** Promena UI jezika usred igre ne
  kvari simulaciju (jezik ne dira nijedan broj) → nema šta da se popravlja.
  Config→start disciplina pripada PRAVIM parametrima (brzina lopte, win-score),
  ne prikazu. Ne gradi mehanizam dok problem koji rešava ne postoji stvarno —
  ista X-Ray disciplina primenjena na „kantu" i na zrak.

## Odbačeno / odloženo (svesno)
- **„Kanta"/meta-igra solo mod** — odbačeno za M1. Nije ni Pong ni AI; nazvati
  je „AI" bi lagalo igrača o unutrašnjosti, suprotno X-Ray stavu. Pravi AI
  protivnik pripada RL stranici (Q-learning), gde ima šta da osvetli.
- **X-Ray zrak (predviđena putanja lopte s odbijanjima)** — odložen za sledeću
  stranicu, NE na klasičnu igru. Odluka: putanja s odbijanjima (istinita), ne
  prosta strelica (laže čim dođe do zida). Prva cigla M2.
- **Settings panel (podesivi parametri pre igre)** — `UPPER_CASE` konstante na
  vrhu game.js (PADDLE_SPEED, BALL_SPEED0, WIN_SCORE…) namerno izdvojene kao
  budući podesivi parametri. Pripada sledećoj stranici, s config→start
  disciplinom.
- **Space-pauza kao M2 oslonac** — pauza zamrzne `step()` ali nastavlja `draw()`
  → slika stoji. Svestan dizajn-oslonac za X-Ray overlay (zamrzneš trenutak,
  nakačiš prozor iznutra).

## Završno stanje
- M1 živ na `https://xpong.opik.net/game.html` (s07): klasičan Pong 2 igrača
  (w/s vs o/l + touch), responzivno, prati temu, 5 jezika, Pong Key Concept.
  Potvrđeno u brauzeru (desktop + tablet Chrome): igra, jezici, ćirilica,
  dvoigračka kontrola, Key Concept kartica.
- xpongweb dirnuto: `app.js`, `xpong.css`, `data/concepts.json` (M);
  `game.html`, `game.js` (novi).
- Nav: „The Game" više nije „coming soon".

## Sledeće
- **M2 — X-Ray overlay** (zrak/predviđena putanja, na zasebnoj stranici, ne na
  klasičnoj igri); settings panel s podesivim parametrima (config→start).
- (kandidat, i dalje otvoren) Proširenje Key Concepts iz About teksta (crna
  kutija, emergencija, neuronska mreža, transformer).
- (kandidat) health_check.py kao strukturni čeker kad struktura poraste.
