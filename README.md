# xpong

Treći pokušaj naslednika projekta **Pong** — browser-based platforma za
treniranje AI agenata (self-play, DQN, genetski algoritmi, X-Ray overlay),
predstavljena kao višestranični **X-Ray sajt**: svaka stranica je prozor u
jednu fazu razvoja.

> Kanonski README: drži SAMO trenutno stanje. Uvek čitaj poslednju verziju.
> Hronologija je u `docs/sessions/`.

## Trenutno stanje
- **Faza:** M2 u toku — cigla 1 (X-Ray zrak) dovršena; cigla 2 (heatmap golova)
  **suštinski dovršena** (mehanika + kontrole + i18n) — ostaje samo pun opis heatmapa
  u infoboxu (za sada jedna rečenica u X-Ray boxu). Landing (M0) + About (esej,
  sidebar, Key Concepts) + favicon + **The Game** (`game.html`/`game.js`: klasičan
  Pong za 2 igrača, w/s vs o/l + touch) + **X-Ray** (`xray.html`/`xray.js`): (1)
  trajektorni zrak čistom fizikom do prve prepreke; (2) **heatmap golova** — uske
  trake uz zid gde lopta fizički ulazi u gol, gruba granularnost 4 trake, akumulira
  kroz sesiju. X-Ray i Heatmap su **switchevi** (Buchenberg `.xp-toggle`; checkbox =
  izvor istine, tasteri `x`/`h` sinhronizuju). Kontrole u dva reda: akcije
  (Start/Reset) gore, switchevi dole. Bočne kutije = brza referenca tastera (bold
  `W / S`, `O / L`); infobox **Navigacija** nosi pun opis kretanja (tastatura + touch).
  Pobednik seta (do 11) ispod brojača; Reset čisti sve (brojači na nulu, switchevi off).
  Fizika u deljenom `pong-core.js` (izvor za game.js i xray.js).
- **Web:** `https://xpong.opik.net` živ (apache2 + Let's Encrypt, auto-renew).
  Portal verzija u footeru: **s12** (`XP_VERSION` u `app.js` — cache-dijagnostika;
  sufiks `sNN.M` se koristi u toku sesije za razlučivanje keša od kvara).
- **Stack:** statički, bez builda — vanilla JS + HTML5 canvas. Look & feel
  pozajmljen iz buchenberga (`xpong.css`). i18n: en (baza), de, it, hr, sr
  (ćirilica; struktura `sr.cyr` — latinica se može dodati aditivno).
- **Sledeće:** pun opis heatmapa u infoboxu (senka/metapodaci okvir, granularnost) —
  kad Flavio odluči granularnost gledajući golove uživo (zasad gruba, 4 trake).
  Kandidati: Key Concept kartica za xray; Key Concepts iz About eseja (crna kutija,
  emergencija, neuronska mreža, transformer); health_check.py; sr.lat aditivno.
  M2 nema inteligenciju ikad; pravi agent pripada budućim RL stranicama.

## Infrastruktura
- **Server:** `foxuno.dynu.net` (Ubuntu), javni IP `130.61.37.60`, user `balsam`.
  Sudo kod Flavija (root komande: Claude priprema, Flavio izvršava).
- **Repo (backend/docs):** `git@github.com:fladroid/xpong.git`, grana `main`,
  home `/home/balsam/xpong`.
- **Repo (web):** `git@github.com:fladroid/xpongweb.git`, grana `main`,
  docroot `/var/www/xpong` (vlasnik `balsam`).
- **Web:** domen `xpong.opik.net` (dynu) → foxuno; apache2 vhost-ovi
  `xpong.opik.net.conf` (:80, redirect) i `xpong.opik.net-le-ssl.conf` (:443).
- **Baza / drugi server:** ne koristi se.
- **Alat:** `foxuno:run_command` za sve na foxuno. Web fajlovi se pišu
  heredoc-om direktno u docroot, pa commit u xpongweb.

## Metoda
Radimo po METHOD dokumentu (project knowledge): show → OK → execute na svakoj
komandi; sirovi izlaz prvo; fiksno otvaranje/zatvaranje sesije; server/repo je
izvor istine, ne pamćenje.

## Struktura
    xpong/                   # backend/docs repo (/home/balsam/xpong)
    ├── README.md            # ovaj fajl — kanonsko stanje
    └── docs/
        ├── PongPregledProjekta.md   # retrospektiva prethodnog Pong projekta
        └── sessions/                # hronološki zapisi (session_NN.md)

    xpongweb/                # web repo (/var/www/xpong)
    ├── index.html           # landing (M0)
    ├── about.html           # esej + sidebar (5 jezika)
    ├── game.html            # M1 klasičan Pong (2 igrača, touch)
    ├── game.js              # M1 Pong: input/render/HUD (zove pong-core)
    ├── pong-core.js         # deljena čista fizika (PongCore, castRay) — bez DOM
    ├── xray.html            # M2 X-Ray stranica (zrak + sidebar infobox)
    ├── xray.js              # M2 X-Ray: render + drawRay (PongCore consumer)
    ├── xpong.css            # deljeni stil (adaptiran iz buchenberg.css)
    ├── app.js               # i18n + chrome + teme; XP_VERSION; renderConcepts
    ├── favicon.svg          # Pong motiv (injektuje se iz app.js)
    ├── data/
    │   └── concepts.json    # Key Concepts po stranici (commituje se)
    └── .gitignore
