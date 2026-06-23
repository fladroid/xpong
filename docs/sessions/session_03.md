# Session 03 — Stack odluka + M0 web skelet

**Datum:** 23 Jun 2026
**Fokus:** odluka o stacku i prvom milestone-u; M0 (chrome + i18n + teme).

## Otvaranje (health snapshot)
- xpong @ `c8fc0cf` (s02), čisto, u sinhronu.
- xpongweb @ `cd20c9e`, čisto, u sinhronu.
- `health_check.py`: ne postoji.
- web: 200.

## Šta je urađeno
1. Retrospektiva prethodnog Ponga → `docs/PongPregledProjekta.md` (bajt-identično
   preko gzip+base64, md5 `9d5e1ce5…`), i u project files. Commit `7ac4b6b`.
2. **Stack odluka:** statički, bez builda — vanilla JS + HTML5 canvas; look & feel
   iz buchenberga; i18n en/de/it/hr/sr(ćir). Backend = kasnije.
3. **Milestone ladder:** M0 skelet/landing → M1 klasičan Pong → M2+ X-Ray overlay
   i RL faze (po stranica po fazi).
4. **M0 implementiran** u `/var/www/xpong`:
   - `xpong.css` — kopija `buchenberg.css`, `bb-`→`xp-` (106 zamena).
   - `app.js` — i18n engine + chrome (header/nav/footer) + theme + burger;
     `T` rečnik 5 lokala; `sr.cyr` struktura; `XP_VERSION='s03'`.
   - `index.html` — landing skelet (hero), prepisuje s02 placeholder.
   - Footer: čist tekst `… · sNN (datum)`, kao buchenberg.
5. README prepisan na novo stanje.

## Lekcije
- **Kurirska mašinerija (heredoc/base64/md5) opravdana samo kad je Claude izvor
  bajtova.** Kad je Flavio izvor + ima git pristup → ide direktno, bez posrednika.
- **Grep je senka, ne original.** Dva promašaja: (1) zaključeno da buchenberg nema
  sr-ćirilicu iz odsečenog grepa — Flavio ispravio slikom; sr je pun ćirilični blok
  (linije 1127+). Pravilo: kad se Flaviov iskaz sukobi s plitkim nalazom — pitaj,
  ne nadglasavaj (METHOD §1/§2). (2) „split" loga iz CSS pravila — optički ga nema.
- **i18n sr: pismo kao podključ (`sr.cyr`)** od starta → latinica/transliterator
  kasnije aditivni, ne refaktor.
- **Verzija u footeru = self-dijagnostika keša** (ispisana iz `app.js`).
- `node` nedostupan na foxuno → JS validacija preko brauzera, ne CLI.

## Završno stanje
- M0 živ na `https://xpong.opik.net` (s03): chrome, i18n (5 lokala, SR ćirilica),
  teme (light/dark, pamti se), responsive + burger — sve potvrđeno u brauzeru.
- Repos: xpongweb (M0, 3 fajla), xpong (README + retrospektiva + ovaj doc).

## Sledeće (M1)
- Klasičan Pong: `game.html` — canvas, reketi, lopta, gol L/D, tastatura + touch,
  responzivno; ukloniti `soon` s nav „The Game".
- Popuna landing sadržaja (istorija Ponga + X-Ray okvir) + prevodi de/it/hr/sr.
