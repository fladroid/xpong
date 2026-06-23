# PONG AI Training Lab — Pregled projekta

**Repozitorij:** https://github.com/fladroid/pong
**Hosting:** https://fladroid.github.io/pong/
**Autori:** Flavio & Claude
**Period:** Mart 2026 (Sesije 1–3)
**Trenutna verzija:** v3.0 (deployovana)

---

## 1. Šta je projekat i zašto postoji

PONG AI Training Lab je edukativni projekat koji koristi klasičnu igru Pong kao **sandbox** za demonstraciju Reinforcement Learning-a u browseru. Motivacija nije produkcijski ishod nego učenje kroz praksu — korisnik kreira AI agente, trenira ih i prati kako hyperparametri utječu na kvalitet igrača.

Projekat je istovremeno bio i prvi zajednički zadatak u saradnji Flavio–Claude: test infrastrukture (MCP balsam-server), metodologije zajedničkog razvoja, i self-play treninga u browserskom okruženju.

**Koncepti koji se demonstriraju:**

- Q-Learning — model-free RL algoritam (Watkins & Dayan, 1992; Bellman, 1957)
- Self-play — agent trenira igrajući protiv kopije sebe (AlphaGo / AlphaZero tehnika)
- Exploration vs Exploitation — kontrolisano epsilon (ε) parametrom
- Osjetljivost na hyperparametre — poređenje agenata s različitim parametrima
- Elo-like rating sistem — penalizuje brute-force trening
- Genetski algoritam — evolucija hyperparametara kroz crossover i mutaciju
- DQN tehnike — experience replay i target network, adaptirane na tabelarni Q-learning

---

## 2. Gdje i kako radimo (infrastruktura i metodologija)

| Komponenta | Detalji |
| --- | --- |
| Dev server | Ubuntu 24.04 LTS — Strato.de, user: `balsam` |
| Pristup | MCP balsam-server — sve operacije s fajlovima i gitom |
| Putanja projekta | `/home/balsam/pong/` |
| Verzioniranje | Git / GitHub — `github.com/fladroid/pong` |
| Hosting | GitHub Pages — `fladroid.github.io/pong/` |
| Editor | `vi` na serveru + Python skripte za precizne modifikacije |
| Lokalni razvoj | **Nema** — nijedna linija koda nije pisana lokalno |

**Metodološka napomena:** umjesto ručnog kopiranja velikih blokova koda, izmjene su rađene Python skriptama (regex matching / string replacement via `python3 << PYEOF` heredoc). Time se izbjegavaju shell escaping problemi s JS template literalima i navodnicima, te ručne greške pri ekstrakciji.

---

## 3. Hronologija — šta je urađeno po sesijama

### Sesija 1 — Osnova (28. mart 2026)

Inicijalna igra i kompletna baza funkcionalnosti.

| Verzija | Sadržaj |
| --- | --- |
| v1.0 | Kompletna igra, Q-learning, self-play, 4 game moda, višejezičnost (EN/DE/HR/SR/SR-ćirilica), localStorage persistencija |
| v1.0 fix | Score display styling — veći brojevi, border oko panela |
| v1.1 | Accessibility bar (font A/A+/A++, kontrast jaki/normalni/slabi), About modal, User Guide modal, footer |
| v1.1 fix | i18n za footer u svim jezicima |
| v1.3 | Export/Import JSON i CSV, IO bar |

Na kraju sesije aplikacija je bila monolitni `index.html` (~2127 linija, ~76KB) sa svim CSS-om, HTML-om, i18n-om i JS-om u jednom fajlu.

### Sesija 2 — Refaktoracija + edukacija (28. mart 2026)

Dva cilja: čistija arhitektura i edukativni uvod u algoritam.

**Refaktoracija** (commit `9f6b89c`):

| Fajl | Prije | Poslije | Sadržaj |
| --- | --- | --- | --- |
| `index.html` | 2127 | 1484 | HTML, i18n, game loop, UI funkcije |
| `style.css` | inline | 536 | Sav CSS — varijable, layout, kontrast |
| `qlearning.js` | inline | 340 | Konstante + `QLearningAgent` klasa s detaljnim komentarima |

Inline `<style>` blok zamijenjen s `<link>` i `<script>` referencama; sve reference na konstante ostaju validne jer se `qlearning.js` učitava prije ostatka JS-a.

**Edukacija:** prošli smo Bellmanovu jednadžbu, epsilon-greedy politiku, self-play, konvergenciju. Diskutovano je **zašto tabelarni Q-learning nije dovoljan za La Briscolu** (parcijalna observabilnost, eksplozija state space-a) i zašto je DQN prirodan sljedeći korak.

### Sesija 3 — Najobimnija (29. mart 2026)

Tri major feature sloja u jednoj sesiji, 10 git commitova.

| Feature | Verzija | Opis |
| --- | --- | --- |
| X-Ray overlay | v1.4 | Heatmap (10×10), ball telemetry tag, paddle Q-bars |
| Experience Replay Buffer | v2.0 | Circular buffer 5000, mini-batch 32, Int32Array |
| Target Network | v2.0 | Frozen Q-table, hard sync svakih 300 ep. |
| Sparse Q-table storage | fix | ~80% uštede u localStorage, backward compatible |
| Auto-Generate | v3.0 | Nasumični hyperparametri, GEN_001+ naming |
| Tournament | v3.0 | Round-robin svih treniranih agenata, live log |
| Evolve | v3.0 | Crossover + Gaussian mutacija, 3 potomka, callback chain |

Sesija je zaključena teorijskim prijedlozima za v3.1.

**Commit log sesije 3:**

| Commit | Sadržaj |
| --- | --- |
| `103c308` | v2.0 X-Ray: heatmap, ball tag, paddle Q-bars |
| `82a9475` | fix: heatmap opacity, right paddle, mirror-state |
| `d1bba82` | v2.0: experience replay + target network |
| `2d36151` | fix: sparse Q-table storage |
| `3066861` | v3.0-step1: auto-generate agent |
| `bdc7294` | v3.0-step2: tournament mode |
| `4504e39` | v3.0-step3: evolve — crossover + mutation |
| `015a74a` | fix: evolve callback chain |
| `45c2489` | fix: startTrainingAgent rewrite |
| `0cd3aa4` | fix: evolve clears callback on finish |

---

## 4. Kako algoritam radi (tehnička jezgra)

### 4.1 State space

Tabelarni Q-Learning zahtijeva konačan prostor stanja, pa su kontinualne vrijednosti diskretizovane u binove:

| Dimenzija | Konstanta | Binovi |
| --- | --- | --- |
| Pozicija loptice X | `BALL_X_BINS` | 10 |
| Pozicija loptice Y | `BALL_Y_BINS` | 10 |
| Smjer loptice dX | `BALL_DX_BINS` | 3 |
| Brzina loptice dY | `BALL_DY_BINS` | 5 |
| Vlastiti paddle | `PADDLE_Y_BINS` | 8 |
| Protivnički paddle | `OPP_Y_BINS` | 6 |
| **UKUPNO** | `STATE_SIZE` | **72.000** |

10 × 10 × 3 × 5 × 8 × 6 = 72.000 stanja × 3 akcije (gore/stoj/dolje) = **216.000 vrijednosti**, implementirano kao `Float32Array` (~864 KB po agentu).

### 4.2 Ključne metode `QLearningAgent`

- `encodeState(...)` — mixed-radix encoding 6 parametara u jedan integer indeks (analogno kako sat kodira h/m/s u jedan broj)
- `getAction(state, explore)` — epsilon-greedy: s vjerovatnoćom ε nasumična akcija (eksploracija), inače max-Q akcija (eksploatacija)
- `update(s, a, r, s2)` — jedino mjesto gdje agent uči, Bellmanova jednadžba:

```
Q(s,a) ← Q(s,a) + α·[r + γ·maxQ(s',a') − Q(s,a)]
```

### 4.3 Trening (self-play)

Headless loop bez renderinga. Batch od 50 epizoda po `requestAnimationFrame` tiku drži UI responzivnim. Agent igra protiv kopije sebe (mirror state za desnu stranu) — uči iz oba ugla. Epsilon decay postepeno smanjuje eksploraciju.

### 4.4 Rating sistem

```
rating_faktor = max(0.2, 1.5 − log10(episodes) × 0.15)
```

Više treniran agent zarađuje manje poena pri pobjedi — sprečava da brute-force trening dominira ljestvicu.

---

## 5. v2.0 — Stabilizacija (DQN tehnike na tabelarnom Q-learningu)

Dvije ključne DQN ideje (DeepMind 2013/2015), adaptirane i backward compatible.

**Experience Replay Buffer** (Lin, 1992) — iskustva se čuvaju u circular bufferu pa nasumično uzorkuju:

| Parametar | Vrijednost |
| --- | --- |
| bufferSize | 5000 (circular) |
| batchSize | 32 po koraku učenja |
| format | (s, a, r, s') — `Int32Array` |
| efekt | slomljena vremenska korelacija, stabilniji trening |

Novi metodi: `pushReplay(s,a,r,s2)`, `learnFromReplay()`.

**Target Network** (Mnih et al., 2015) — dvije Q-tabele: online (uči se svaki korak) i target (zamrznuta kopija). Bellman koristi target Q za `maxQ(s',a')`, čime se sprečava "pomicanje cilja":

| Parametar | Vrijednost |
| --- | --- |
| targetSyncInterval | 300 epizoda (hard update) |
| targetQ | `Float32Array` ~864 KB |
| sync | `Float32Array.set()` — O(n) memcpy |

---

## 6. v3.0 — Genetski algoritam (evolucija agenata)

Tri komponente evolutivnog pristupa optimizaciji hyperparametara.

**Auto-Generate (⚙)** — agent s nasumičnim hyperparametrima, odmah treniran:

| Parametar | Raspon |
| --- | --- |
| lr (α) | 0.05 – 0.5 |
| discount (γ) | 0.90 – 0.999 |
| epsilon | 1.0 (uvijek pun na početku) |
| epsilonDecay | 0.999 – 0.9999 |
| trainSpeed | 4 – 8 |
| ime | GEN_001+ |

**Tournament (⚑)** — round-robin svih treniranih agenata, n×(n−1)/2 parova, svaki headless meč (max 8000 koraka, 7 poena), live log, rang lista s medaljama.

**Evolve (⚗)** — top 2 agenta po ratingu kao roditelji → 3 potomka:

- *Crossover:* `param = random() < 0.5 ? parentA : parentB`
- *Mutacija (Gaussian, Box-Muller):* `param = clamp(param + gaussian(0,sigma)·sigma·param, min, max)`

| Parametar | Sigma |
| --- | --- |
| lr | 5% |
| discount | 2% |
| epsilonDecay | 1% |
| trainSpeed | 5% |
| epsilon | ne mutira (1.0) |

Potomci: EVO_001+, treniraju se sekvencijalno.

---

## 7. X-Ray overlay (v1.4)

Vizualizacija šta agent "misli" u realnom vremenu, inspirisana X-Ray filozofijom iz manifesta. Toggle dugme ✦ X-RAY, radi u svim modovima i tokom treninga.

| Sloj | Opis |
| --- | --- |
| Heatmap (10×10) | Semi-transparentan overlay, boje plava→cijan→žuta→crvena, projekcija Q-vrijednosti po poziciji loptice |
| Ball telemetry tag | Floating panel uz lopticu: X/Y bin, smjer, brzina, connector linija |
| Paddle Q-bars | Bar chart UP/ST/DN relativnih Q-vrijednosti uz svaki AI paddle, aktivna akcija istaknuta |

U Human vs Human modu prikazuje se samo telemetry tag (heatmap/Q-bars nemaju smisla bez agenta).

---

## 8. Naučene lekcije (key learnings)

- **Sparse Q-table encoding:** localStorage limit (~5MB) je s 7+ agenata (svaki ~864KB) davao `QuotaExceededError`. Rješenje — čuvanje samo nenultih vrijednosti kao `{i:[indeksi], v:[vrijednosti]}`, ~80% uštede. Dense JSON export zadržan za analizu; `fromJSON` čita oba formata.
- **Stale closure u EVOLVE:** `onTrainingComplete` callback se mora eksplicitno nullirati između EVOLVE poziva; UI dugme se disablea tokom async procesa da se spriječe race conditions (drugi EVOLVE je radio samo 1×).
- **Dizajn za oporavak, ne savršenstvo:** tihi failure ovisan o redoslijedu akcija (TOURNAMENT → EVOLVE) postao je školski primjer za "Resilience" pillar X-Ray manifesta.
- **GitHub Pages cache:** dupli `Ctrl+Shift+R` je očekivano ponašanje, nije deployment greška.
- **Uređivanje na serveru:** Python string replacement (heredoc) umjesto `sed`/ručno za JS s template literalima.

---

## 9. Stanje repozitorija (trenutno)

| Fajl | Linija | Sadržaj |
| --- | --- | --- |
| `index.html` | ~1484 | HTML, i18n (5 jezika), game loop, UI, v3.0 genetski algoritam |
| `style.css` | 536 | Sav CSS — varijable, layout, dark theme, kontrast |
| `qlearning.js` | 340 | Konstante, `QLearningAgent`, ExperienceReplay, TargetNetwork |

**Technology stack:** Vanilla JS (ES2022+), HTML5 Canvas, Google Fonts (Share Tech Mono, Orbitron), localStorage, GitHub Pages, Git, MCP balsam-server.

---

## 10. Šta je sve bilo planirano

### Planirano i još neimplementirano

| Verzija | Plan |
| --- | --- |
| **v1.4 (API)** | REST endpoint za mrežnog protivnika; bodovanje skalirano mrežnim faktorom (obrnuto proporcionalno treningu); prikaz latencije i statusa konekcije *— napomena: oznaka v1.4 kasnije je iskorištena za X-Ray overlay; mrežni igrač kao ideja ostaje otvoren* |
| **v3.1** | Fitness-proportionate selection (roulette wheel) umjesto determinističkog top 2 |
| **v3.1** | Threshold-based discrete mutation (prag ~10%) umjesto Gaussian |
| **v3.1** | Progress indicator tokom dugih turnira (21+ mečeva) |
| **v3.2** | Vizualizacija evolucije — graf ratinga po generacijama |
| **DQN / La Briscola** | Deep Q-Network, Python/PyTorch, Google Colab (GPU); LSTM/Transformer za pamćenje karata (parcijalna observabilnost) |

### Detaljnije — v3.1 prijedlozi (Flaviovi, sa kraja sesije 3)

**Fitness-proportionate selection (roulette wheel)** — klasični GA (Holland, 1975).
*Problem trenutne implementacije:* deterministički top 2 vodi u preuranjenu konvergenciju — populacija degenerira u kopije jednog dominantnog agenta.
*Rješenje:* probabilistička selekcija proporcionalna udjelu u ukupnom ratingu — najbolji ima najveću šansu, najlošiji nenultu, diversitet očuvan.
```
udio_i = rating_i / Σ rating
```

**Threshold-based discrete mutation.**
*Problem Gaussian mutacije:* "creep" — svaki parametar se uvijek malo pomjera, postepeno gurajući sve prema sredini raspona.
*Rješenje:* za svaki parametar random [0,1]; ako < threshold (npr. 0.10) parametar se zamjenjuje nasumičnim iz skupa, inače ostaje od roditelja. Stabilno većinom, povremeni veći skokovi — bliže biološkoj mutaciji, bolje istražuje prostor.

### Šire planirano oko Pong ekosistema

- **La Briscola DQN** kao prirodan sljedeći projekat: dovoljno kompleksna za DQN, dovoljno mala (40 karata) da je izvediva. Infrastruktura već postoji (Python, Colab, self-play metodologija iz Ponga).
- **X-Ray** filozofski manifest (BHS/EN/DE/SR) razvio se iz diskusija u ovom projektu; primjeri iz Pong rada (npr. silent failure → "Resilience") koriste se kao ilustracije.

---

*Generisano iz Pong sesija 1–3. Flavio & Claude, mart 2026.*
