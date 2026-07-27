# xpong

Treći pokušaj naslednika projekta **Pong** — browser-based platforma za
treniranje AI agenata (self-play, DQN, genetski algoritmi, X-Ray overlay),
predstavljena kao višestranični **X-Ray sajt**: svaka stranica je prozor u
jednu fazu razvoja.

> Kanonski README: drži SAMO trenutno stanje. Uvek čitaj poslednju verziju.
> Hronologija je u `docs/sessions/`.

## Trenutno stanje
- **Faza:** M3 (RL faze) otvoren — stranica 1 `rl1` ✅, stranica 2 `rl2` ✅ (vidi ispod). M2 kompletan: cigla 1 (zrak) ✅, cigla 2 (heatmap golova) ✅.
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
  ne agenta — uma još nema. Infobox „This page — RL 1" + Navigacija (i18n `r1_*` ožičen ×5, s16). Key Concepts ×3: 🧠 Reinforcement learning, 🤖 Agent, 🎲 Random walk (`concepts.json` sekcija `rl1`).
  U navu ("RL 1" / "РЛ 1", između Telemetrije i Stabilization) — s17.
- **M3 stranica 2 — `rl2`** (`rl2.html`/`rl2.js`, `data-page="rl2"`, prefiks `r2_`;
  naslov „RL 2 — How the agent sees the world"): tema je **STANJE**, ne učenje.
  Levi reket je agent koji uči (tabelarni Q), desni je random walker s prethodne stranice.
  **Mreža stanja** preko terena crta X×Y — dve od pet dimenzija; smer, brzina i položaj
  sopstvenog reketa ulaze u broj stanja ali nemaju mesto na terenu (to je poenta, ne propust).
  Pregrada s lopticom se ističe; gore levo `state N / ukupno` — ceo svet agenta kao jedan ceo broj.
  **Grubost** = segmentirani prekidač s tri imenovane vrednosti (ime iznad, broj ispod),
  `4000` podrazumevano u markupu. **Trening** je headless, adaptivni paket po `rAF` (cilj < 8 ms),
  greedy evaluacija odvojena od treninga. **Grafikon**: svako pokretanje DODAJE krivu;
  tri pokazatelja — kvalitet, rasejanje (std. devijacija), koraka/s. `Start` zadržan pored
  `Train` jer je igra uživo jedino mesto gde se mreža i telemetrija vide.
  Key Concepts ×4: 🗺️ State space, 🔲 Discretization, 🌌 Curse of dimensionality,
  ⛓️ Markov decision process. U navu „RL 2" / „РЛ 2" — s20.
- **Prostor stanja — definicija (s20).** s19 je zapisao rezultate merenja ali NE i parametre;
  sandbox je resetovan pa je recept izgubljen. Rastavi su definisani iznova (fina je
  rekonstruisana pouzdano: 10×10×3×5×8 = stari Pong minus dimenzija protivničkog reketa):
  gruba `5×5×2×3×2 = 300`, srednja `10×8×2×5×5 = 4.000`, fina `10×10×3×5×8 = 12.000`.
  Apsolutni brojevi iz s19 tabele NISU uporedivi sa današnjim bez poznatih uslova merenja;
  **uporediv je poredak**, i on je reprodukovan u browseru (s20, n=10): srednja 4,56 (dev 1,10),
  fina 4,02 (dev 1,32) — po kvalitetu izjednačene, fina raspršenija.
- **Web:** `https://xpong.opik.net` živ (apache2 + Let's Encrypt, auto-renew).
  Portal verzija u footeru: **s20** (`XP_VERSION` u `app.js` — cache-dijagnostika;
  sufiks `sNN.M` se koristi u toku sesije za razlučivanje keša od kvara).
  PAŽNJA: `XP_VERSION` pokriva SAMO `app.js`. `xpong.css` i `<page>.js` idu bez oznake
  verzije, pa svež footer NE znači svež CSS/JS — otvorena stavka `?v=sNN` (s21, prio 1).
- **Layout:** sve stranice dele okvir od 1200px (`#xp-page` /
  `#xp-header-inner`), pa su poravnate s nav-redom; igra je dodatno
  ograničena na `min(100%, 72vh)` (canvas je 800×500 sa `width:100%` i
  `height:auto`, pa širina diktira visinu) — s18.
- **Stack:** statički, bez builda — vanilla JS + HTML5 canvas. Look & feel
  pozajmljen iz buchenberga (`xpong.css`). i18n: en (baza), de, it, hr, sr
  (ćirilica; struktura `sr.cyr` — latinica se može dodati aditivno).
  PAŽNJA: escape oblici u `app.js` su MEŠANI i unutar istog bloka (`\uXXXX`,
  `\xNN`, sirov UTF-8) — pre svakog sidrenja proveriti stvarni bajt-oblik.
- **Merenje prostora stanja (završeno s19):** protiv random walkera,
  3 varijante × 5 seedova × 12.000 epizoda, sa greedy evaluacijom odvojenom od
  treninga. Kvalitet: srednja (4.000) 5,69 i fina (12.000) 5,81 izjednačene,
  gruba (300) 3,51. Brzina: sve tri se preklapaju — nema razlike. **Odlučuje
  pouzdanost, tj. širina raspona između seedova: srednja 2,67, fina 4,23,
  gruba 6,40 — najpouzdanija je SREDINA.** Premalo pregrada meša različite
  situacije, previše pregrada raspe iskustvo na previše mesta (prokletstvo
  dimenzionalnosti). **Odluka: 4.000 podrazumevana na `rl2`**, gruba i fina kao
  izbori koji pokazuju šta se gubi u svakom smeru. Napomena: 72.000 iz starog
  Ponga nije reproducibilno bez dimenzije protivničkog reketa — fina je 12.000.
- **Sledeće (s21):** **`rl3` — UČENJE** (Bellman, Q-tabela kao vidljiv objekat,
  telemetrija odluka agenta). Mehanika već postoji u `rl2.js` i prenosi se; novo je
  *prikazivanje* pravila učenja, ne njegovo pisanje. Opseg dalje ostaje uzak:
  `rl3` = UČENJE, `rl4` = EKSPLORACIJA.
  **Otvorene stavke po prioritetu:** (1) cache-busting `?v=sNN` na `<link>`/`<script>`,
  bumpuje se sa `XP_VERSION` — uzrok tri ručna čišćenja keša u s20; (2) infobox „Brzina
  uređaja" na `rl2` — `stepsPerSec` se meri i prikazuje, ali adaptacija nije objašnjena,
  a s19 uslov je da mora biti dokumentovana; (3) prio2: prekidači nose ime bez `on`/`off`
  (Material/Apple/W3C — stanje čita položaj, tekst duplira signal), uz jače vizuelno
  stanje; (4) prio2: JS benchmark na PC/tablet/telefon; (5) kandidati: `sr.lat` aditivno,
  Key Concepts iz About eseja.
- **Samoštimovanje (dogovoreno s19):** trening u browseru koristi adaptivni
  paket epizoda po `requestAnimationFrame` (meri prethodni, drži ispod ~8 ms) —
  fiksan paket koji je na PC-u 3 ms na starijem telefonu traje 150 ms i zamrzava
  UI. **Uslov: adaptacija mora biti dokumentovana** na stranici (infobox „Brzina
  uređaja" sa izmerenim koraka/s); nedokumentovana adaptacija je crna kutija
  protiv koje je ceo X-Ray stav. Minimum hardvera je browser od ~2015; Q-tabela
  je 48 KB na 4.000 stanja. Sledi JS benchmark na PC/tablet/telefon.
- **Nasleđeno:** kandidati sr.lat aditivno; Key Concepts iz About eseja (crna
  kutija, emergencija, neuronska mreža, transformer). Zatvoreno u s21: escape
  recept dokumentovan u `docs/KAKO-JeziciUI.md` §4.

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
        ├── KAKO-KeyConcepts.md      # recept: Key Concepts/Wikipedia kartice (izveden iz buchenberga, s21)
        ├── KAKO-JeziciUI.md         # recept: višejezični UI, data-i18n mehanizam (izveden iz buchenberga, s21)
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
    ├── rl2.html             # M3 str.2 Prostor stanja (mreza, grubost, grafikon)
    ├── rl2.js               # M3 str.2: GRIDS, encodeState, Q-jezgro, trening, grafikon
    ├── xpong.css            # deljeni stil (adaptiran iz buchenberg.css)
    ├── app.js               # i18n + chrome + teme; XP_VERSION; renderConcepts
    ├── favicon.svg          # Pong motiv (injektuje se iz app.js)
    ├── data/
    │   └── concepts.json    # Key Concepts po stranici (commituje se)
    └── .gitignore
