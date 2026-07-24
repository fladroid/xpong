# xpong

Treći pokušaj naslednika projekta **Pong** — browser-based platforma za
treniranje AI agenata (self-play, DQN, genetski algoritmi, X-Ray overlay),
predstavljena kao višestranični **X-Ray sajt**: svaka stranica je prozor u
jednu fazu razvoja.

> Kanonski README: drži SAMO trenutno stanje. Uvek čitaj poslednju verziju.
> Hronologija je u `docs/sessions/`.

## Trenutno stanje
- **Faza:** M3 (RL faze) otvoren — stranica 1 `rl1` cigla 1 ✅ (vidi ispod). M2 kompletan: cigla 1 (zrak) ✅, cigla 2 (heatmap golova) ✅.
  Landing (M0) + About (esej, sidebar, Key Concepts) + favicon + **The Game**
  (`game.html`/`game.js`: klasičan Pong za 2 igrača, w/s vs o/l + touch) +
  **Telemetrija** (`xray.html`/`xray.js` — fajlovi i i18n prefiks `x_` zadržani
  kao tehnički identitet; stranica se ZOVE Telemetry/Telemetrie/Telemetria/
  Telemetrija/Телеметрија jer X-Ray je stav nad celim projektom, ne feature
  jedne stranice — stav pomenut u intro s uputom na About): (1) **zrak** —
  trajektorija čistom fizikom do prve prepreke, bleđi (×0.55) dok igra ne
  teče; na servisu iz centra nema zraka/markera, loptica tada nosi prsten
  zrak-ON (znak da je sloj aktivan, simetrično heatmap okvirima); (2) **heatmap golova** — 4 trake uz svaki zid, tanki okviri traka
  vidljivi čim se uključi (i pre golova), ispune po frekvenciji + broj golova
  u traci (surface disk + text broj, tematski, čita se u obe teme), akumulira
  kroz sesiju. Oba su **switchevi** (Buchenberg `.xp-toggle`; checkbox = izvor
  istine, tasteri `x`/`h` sinhronizuju); switch imenovan po sloju: Zrak/Beam,
  Heatmap. Kontrole u dva reda: akcije (Start/Reset) gore, switchevi dole.
  Tri infoboxa: **Zrak** (opis zraka + X-Ray stav), **Heatmap** (senka/
  metapodaci, pun opis), **Navigacija** (tastatura + touch). Bočne kutije =
  bold `W / S`, `O / L`. Pobednik seta (do 11) ispod brojača; Reset čisti sve.
  **Key Concepts x4**: Pong, Telemetry, Light beam, Heat map (EN + EN
  Wikipedia, `data/concepts.json` sekcija `xray`). Fizika u deljenom
  `pong-core.js`.
- **M3 stranica 1 — `rl1`** (`rl1.html`/`rl1.js`, `data-page="rl1"`, prefiks
  `r1_`; naslov „RL 1 — Random walker"): klon Telemetrije (isti porodični layout —
  sidebar, Zrak/Heatmap switchevi, infoboxi). Desni reket je **random-walker agent**
  (gore/stoj/dole nasumično, ×2 korak, BEZ učenja); levi je čovek (W/S/touch) ili
  agent preko `.xp-toggle` mode-prekidača. Zrak/heatmap čitaju SVET (putanja, golovi),
  ne agenta — uma još nema. Infobox „This page — RL 1" + Navigacija (i18n `r1_*` ožičen ×5, s16). Key Concept: 🎲 Random walk (`concepts.json` sekcija `rl1`).
  U navu ("RL 1" / "РЛ 1", između Telemetrije i Stabilization) — s17.
- **Web:** `https://xpong.opik.net` živ (apache2 + Let's Encrypt, auto-renew).
  Portal verzija u footeru: **s17** (`XP_VERSION` u `app.js` — cache-dijagnostika;
  sufiks `sNN.M` se koristi u toku sesije za razlučivanje keša od kvara).
- **Stack:** statički, bez builda — vanilla JS + HTML5 canvas. Look & feel
  pozajmljen iz buchenberga (`xpong.css`). i18n: en (baza), de, it, hr, sr
  (ćirilica; struktura `sr.cyr` — latinica se može dodati aditivno).
  PAŽNJA: escape oblici u `app.js` su MEŠANI i unutar istog bloka (`\uXXXX`,
  `\xNN`, sirov UTF-8) — pre svakog sidrenja proveriti stvarni bajt-oblik.
- **Sledeće (s18):** dopuna Key Concepts rl1 (RL, Agent); naslovi
  („otom potom"). Zatim **stranica 2 — agent
  koji UČI (Q-learning)**: uvodi telemetriju UMA (Q-vrednosti) nad pong-core.
  Ostali kandidati: Key Concepts iz About eseja (crna kutija,
  emergencija, neuronska mreža, transformer); sr.lat aditivno.

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
komandi; sirovi izlaz prvo; fiksno otvaranje/zatvaranje sesije (`health_check.py` za health
snapshot); server/repo je izvor istine, ne pamćenje.

## Pedagoška granularnost (pravilo M3+)
Granica pojma je obavezna: ono što je pojmovno ili istorijski odvojeno mora i kod nas biti odvojeno prikazano. Forma odvajanja (zasebna stranica ili switch na istoj stranici) bira se prema profilu korisnika, ne prema nama — za publiku van struke switch se percipira kao još jedan feature i pojmovna granica se gubi, dok nova stranica tera novost da se opazi. Kod pojmova s pedagoškom težinom (Q-learning, DQN…) default naginje ka zasebnoj stranici; ponavljanje zajedničkog konteksta među stranicama je namerno — pozadina naspram koje se ističe ono novo. Implementacioni koraci (skelet, telemetrija, i18n, Key Concepts) nisu pojmovi i ne dobijaju svoje mesto — oni su faze gradnje unutar stranice. Posledica za M3: „agent koji ne uči“ i „agent koji uči“ su dve stranice, ne dva stanja jedne. Switch je ravnopravan sa zasebnom stranicom (porodica stranica deli look & feel, pa switch reciklira umesto da duplira); kad switch nosi pojmovnu granicu, mora biti eksplicitno uokviren (naslov + objašnjenje), inače je briše.

## Struktura
    xpong/                   # backend/docs repo (/home/balsam/xpong)
    ├── README.md            # ovaj fajl — kanonsko stanje
    ├── health_check.py      # health snapshot (git, struktura, concepts.json, DNS, live site, apache)
    └── docs/
        ├── PongPregledProjekta.md   # retrospektiva prethodnog Pong projekta
        └── sessions/                # hronološki zapisi (session_NN.md)

    xpongweb/                # web repo (/var/www/xpong)
    ├── index.html           # landing (M0)
    ├── about.html           # esej + sidebar (5 jezika)
    ├── game.html            # M1 klasičan Pong (2 igrača, touch)
    ├── game.js              # M1 Pong: input/render/HUD (zove pong-core)
    ├── pong-core.js         # deljena čista fizika (PongCore, castRay) — bez DOM
    ├── xray.html            # M2 Telemetrija stranica (zrak + heatmap + infoboxi)
    ├── xray.js              # M2 Telemetrija: render, drawRay, drawHeatmap
    ├── rl1.html             # M3 str.1 Random walker (klon xray + agent)
    ├── rl1.js               # M3 str.1: random-walker agent nad pong-core
    ├── xpong.css            # deljeni stil (adaptiran iz buchenberg.css)
    ├── app.js               # i18n + chrome + teme; XP_VERSION; renderConcepts
    ├── favicon.svg          # Pong motiv (injektuje se iz app.js)
    ├── data/
    │   └── concepts.json    # Key Concepts po stranici (commituje se)
    └── .gitignore
