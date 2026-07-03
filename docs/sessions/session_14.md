# Session 14 — M3 otvoren: pravilo pedagoške granularnosti + rl1 cigla 1 (random-walker agent)

**Datum:** 03 Jul 2026
**Fokus:** otvaranje M3 (RL faze). Najpre duga konceptualna diskusija koja je
iznedrila trajno pravilo o pedagoškoj granularnosti (upisano u README), zatim
dekompozicija M3 i izgradnja prve fizičke stranice s agentom — `rl1`,
random-walker agent koji igra ali NE uči. Cigla 1: skelet + agent + porodični
layout; i18n/nav/naslovi odloženi za s15.

## Otvaranje (health snapshot)
- xpong (docs) @ `e379d38` (s13), čisto, u sinhronu.
- xpongweb (web) @ `7a428de` (s13), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s13'` (živo); DNS @8.8.8.8/@1.1.1.1 → 130.61.37.60.
- Memorija je kasnila celu s13 (mislila „početak s13"); server = izvor istine ispravio.
- `health_check.py`: i dalje ne postoji (ručni snapshot).

## Konceptualni rad: pravilo pedagoške granularnosti (ključno)
Duga diskusija pre koda, jer M3 unutrašnjost nikad nije bila zaključana (samo
„M2+ X-Ray i RL faze" iz s03). Zaključeno pravilo (README, sekcija „Pedagoška
granularnost (pravilo M3+)"):
- **Granica pojma je obavezna**: pojmovno/istorijski odvojeno mora biti odvojeno prikazano.
- **Forma (stranica vs switch) bira se prema korisniku, ne prema nama.** Za publiku
  van struke switch je „još jedan feature" i granica se percepcijski gubi; nova
  stranica tera novost da se opazi. Pojmovi s pedagoškom težinom (Q-learning, DQN)
  → default zasebna stranica; ponavljanje konteksta je namerno (pozadina za novost).
- **Implementacioni koraci** (skelet, telemetrija, i18n, KC) nisu pojmovi → nemaju svoje mesto.
- **Switch je ravnopravan sa stranicom** (porodica deli look & feel, switch reciklira);
  ali switch s pojmovnom granicom mora biti eksplicitno uokviren, inače je briše.
- Posledica: „agent koji ne uči" i „agent koji uči" su DVE stranice, ne dva stanja jedne.

## Dekompozicija M3 (dogovoreno)
M3 = više stranica, jedna po RL fazi; prva je random baseline → kasnije Q-learning.
„Cigle" su koraci gradnje unutar stranice. Prva stranica: `rl1` = random-walker baseline.

## Odluka: random walker, ne „Q bez učenja"
Za „agent koji ne uči" razmatrane 3 opcije; izabran **random walker** (čist nasumičan
agent). Razlog: random walk je zaseban pojam s imenom/istorijom/Wiki (zaslužuje mesto
po pravilu), dok je „Q bez update-a" implementaciona faza maskirana u stranicu.
Flaviov argument presudan (arhetip početka svake simulacione biblioteke).

## Tehnički identitet (zaključan)
`rl1.html`/`rl1.js`, `data-page="rl1"`, prefiks `r1_` — redni, neutralan,
faza-agnostičan (s12 pouka: ne vezuj vidljivo ime za tehnički identitet).

## Šta je urađeno (rl1 cigla 1)

### Pogrešna pa ispravljena osnova
Prvo `rl1` kloniran iz `game.html` (gola igra) → Flavio (i „njegov prijatelj":
gde je zrak?) uočio da ne liči na porodicu. **Rebazirano na `xray.*`** — porodični
šablon: sidebar, Beam + Heatmap switchevi, infoboxi, auto Key Concepts. Pouka niže.

### Agent (nad pong-core, bez diranja jezgra)
- `pong-core` kretanje reketa je u consumeru → agent je samo drugi izvor `vy`.
- `agentAction()` vraća -1/0/+1 (random walker); `applyAgent(p){ p.y += action*PADDLE_SPEED*2 }`.
  Faktor ×2 na Flaviov zahtev (vidljivije lutanje, ista priroda).
- `step()`: desni reket UVEK agent; levi = čovek (W/S/touch) ili agent, po mode-switchu.
- Zrak/heatmap nasleđeni iz xray netaknuti — čitaju SVET (putanja, golovi), ne agenta.

### Layout / UI
- Naslov h1 „RL 1 — Random walker" (statičan, bez data-i18n — r1_ ključevi ne postoje još).
- Desni deck: „Agent" umesto O/L; levi deck: mode-toggle iznad W/S.
- Mode-prekidač: prvo goli checkbox (brzo za skelet) → na Flaviovu primedbu pretvoren u
  `.xp-toggle` (isti kao Beam/Heatmap). Direktna primena README pravila: switch s
  pojmovnom granicom (čovek⇄agent) mora biti uokviren kao ravnopravan, ne uzgredan.
- „This page — RL 1" infobox (prvi u sidebaru): objašnjava agenta koji ne uči,
  random walker baseline, i izričito „Beam/Heatmap čitaju svet, ne um — uma ovde još
  nema; učeći agent i telemetrija odluka dolaze na sledećoj stranici". Nav infobox
  prilagođen (desni = agent). Oba statična EN (i18n zaseban korak).
- Key Concepts: `concepts.json` sekcija `rl1` sa 1 karticom — 🎲 Random walk (Wiki).
  Auto-pokupljen preko `data-page="rl1"` (renderConcepts).

## Lekcije / ledger
- **Kloniraj iz porodičnog šablona, ne iz najbližeg fajla.** rl1 pripada xray porodici
  (sidebar, telemetrija), ne game porodici. Pogrešna osnova = stranica „ne liči";
  „gde je zrak?" bio je signal da fali ceo porodični kontekst, ne kozmetika.
- **Zrak/heatmap = telemetrija SVETA, ne UMA.** Rade nad pong-core nezavisno od toga
  ko vodi reket → pripadaju svakoj porodičnoj stranici uključujući random-walker.
  Telemetrija UMA (Q-vrednosti) je zaseban sloj, dolazi sa učećim agentom.
- **README pravilo odmah presuđuje UI.** Goli checkbox za pojmovnu granicu prekršio je
  tek upisano pravilo; Flavio uhvatio. Pravilo nije dekor — koristi se isti čas.
- **JSON izmena: json.loads + strukturni assert PRE upisa** (s12 obrazac, ponovljen).

## Završno stanje
- `https://xpong.opik.net/rl1.html` (s14): porodična stranica (xray layout) —
  desni reket random-walker agent (×2), levi čovek⇄agent preko `.xp-toggle`;
  Beam + Heatmap switchevi rade (svet, ne um); „This page" + Navigation infoboxi
  (statični EN); 1 Key Concept (Random walk). Potvrđeno u browseru kroz iteracije.
- Novi fajlovi: `rl1.html`, `rl1.js` (klon xray + agent). Dirnuto: `data/concepts.json`
  (rl1 sekcija), `README.md` (pravilo granularnosti + stanje), `app.js` (XP_VERSION s14).
- M3: stranica 1 (rl1) cigla 1 ✅. XP_VERSION s14.

## Sledeće (paket za s15)
- **i18n `r1_*` ×5** za rl1 (This page, Navigation, mode-label, h1 naslov) — mešani
  escape u app.js, `cat -A` pre svakog sidra.
- **Nav-stavka** za rl1 u meniju (sad direktan URL); gde u niz (pre Stabilization?).
- **Naslovi** — Flavio „otom potom".
- Dopuna Key Concepts rl1 (kandidati: Reinforcement learning, Agent).
- Stranica 2: „agent koji uči" (Q-learning) — uvodi telemetriju UMA.
- (kandidat) health_check.py pre daljeg širenja.
