# Session 22 — RL2 redizajn zatvoren: live evaluacija, sadržaj, imenovanje

**Datum:** 27. jul 2026.
**Fokus:** Zatvaranje trotačkastog plana iz s21 (§12): uklanjanje slobodne
igre sa `rl2`, uživo animirana evaluaciona epizoda svakih 500 epizoda, i
sadržajne izmene koje su na to čekale. Sve tri tačke gotove. Usput: podešena
brzina prikaza po Flaviovom zahtevu, uhvaćen i ispravljen pravi sintaksni bag
pre deploya, i detaljna rasprava o preciznom imenovanju state-tabele koja je
otkrila da je pola njenih redova godinama bilo samo na engleskom za sve
ostale jezike.

## Otvaranje (health snapshot)

- Onboarding: README → poslednja tri session doca (s19, s20, s21) → git
  status oba repoa → `health_check.py`.
- Sve zeleno: docs i web repo čisti i sinhronizovani na s21, HTTPS 200,
  concepts.json validan (6 sekcija).

## Šta je urađeno

### 1. Tačka 1+2 iz s21 plana — uklonjena slobodna igra, dodata live evaluacija (s22.1)

`rl2.html`: uklonjen scorebar (`xp-score-l/r`, `xp-winner`), `Start` dugme,
`Left: Human/Agent` prekidač (`rl1-left-mode`). Levi reket trajno "Learning
agent" (novi ključ `r2_legend_left_agent` ×5 jezika), simetrično sa desnim
"Random walker".

`rl2.js`: potpuno prepisan. Uklonjeno: tastatura (w/s/o/l), touch unos,
stara `step()`/`afterPoint()`/`toggleRun()`, scoreboard/winner HUD, mode
switch, `gameOver`/`WIN_SCORE`. Novo stanje: `trainRun` (headless bulk) i
`liveEval` (uživo epizoda). Na svakih 500 epizoda: `evaluate()` i dalje
računa broj za grafik headless (statistika nepromenjena), zatim JEDNA
epizoda se odigra UŽIVO na terenu — `qAction(si, false)` (greedy) za levi
reket, isti `applyAgent()` (random) za desni, mreža/tabela/beam/heatmap se
pomeraju u realnom vremenu. Granica 900 frejmova (~15s) sprečava da dobar
agent zarobi prikaz. `Reset` sad resetuje CEO trening (Q-tabela, krive,
grafikon), ne samo jednu partiju — gasi i Beam/Heatmap. Grid kontrole i
`Train` dugme onemogućeni dok je trening aktivan — ovo usput ispravlja
latentan bag: `trainTick()` je čitao `gridKey` uživo, pa bi promena mreže
usred treninga pokvarila indeksiranje Q-tabele.

Verifikacija pre deploya: zagrade/zagrade/uglaste zagrade balansirane,
svih 34 funkcije definisane tačno jednom, svi HTML ID-jevi na koje se JS
oslanja postoje tačno jednom.

### 2. Brzina live epizode (s22.2)

Flavio: epizoda "normalna" ali traje duže od 15s, hteo je brže bez novog
prekidača/slajdera (setio se starog predloga o više brzina, odlučio protiv
njega zbog UI zagušenja). Rešenje: frakcioni akumulator umesto tačno 1
fizičkog koraka po `rAF` frejmu — `LIVE_SPEED = 1.125`, svaki ~8. frejm radi
dva koraka. Ista fizika (verna naučenoj politici), ~12.5% kraće stvarno
trajanje, bez nove kontrole na stranici.

### 3. Sadržajne izmene — naslov grafika, split infoboksa (s22.3)

Iznad grafikona: naslov (`r2_chart_title`, "Evaluation quality across
training"). Ispod: natpis (`r2_chart_caption`) koji eksplicitno imenuje X/Y
osu i vezuje Y osu za isti broj kao stat "returns / episode" ispod — Flavio
je primetio da veza grafik↔statistika nije bila vidljiva, ovo je direktan
odgovor. Stara jedinstvena infobox kutija ("This page", naslov greškom i
dalje pisao "RL 1" u HTML fallback-u, tekst opisivao ukinutu slobodnu igru)
podeljena na dve: **"State space"** (mreža/dimenzije) i nova **"Reading the
results"** (šta Train/Reset sad rade, kako čitati krive i raspon). Kutija
"Navigation" (`r2_nav_text`) uklonjena sa `rl2.html` — sadržaj utopljen u
"Reading the results"; deljeni ključ `x_nav_title` NIJE dirnut jer ga
`rl1`/`xray` i dalje koriste (proverio `grep -l` pre brisanja). Dve nove CSS
klase (`.xp-chart-title`, `.xp-chart-caption`).

**Bag uhvaćen pre deploya, ne posle:** nekoliko novih EN/IT rečenica je
koristilo prave apostrofe unutar single-quote JS stringova (`agent's`,
`l'agente`, `dell'agente`, `un'esecuzione`...) — to bi slomilo `app.js`
sintaksu u potpunosti. Uhvaćeno rutinskom post-write proverom (`grep -nP`
za apostrof između slova unutar novih ključeva), ne balansom zagrada koji
ovu klasu greške ne vidi. Ispravljeno kovrdžavim apostrofom (`\u2019`),
isti stil koji IT blok već koristi na starijim linijama.

### 4. Imenovanje state-tabele — Direction/Speed → Horizontal/Vertical move (s22.4)

Flavio je tražio objašnjenje brojeva u tabeli (Direction/Speed/Paddle),
pa preciznije objašnjenje `<n1>/<n2>` formata (n2 = broj pregrada za
trenutnu mrežu, n1 = indeks od nule u kom se vrednost nalazi sad). Zatim
postavio konceptualno pitanje: "Direction" implicira busolsku kategoriju,
"Speed" implicira bezpredznačni skalar sa stvarnom jedinicom — ni jedno ni
drugo ne opisuje ono što `dx`/`dy` stvarno jesu (predznačena binovana
komponenta brzine). Pretražene prošle sesije (`conversation_search`) —
pitanje nije ranije postavljano u ovom obliku, samo tangencijalna ranija
napomena o imenovanju "own paddle" reda. Preimenovano u "Horizontal move" /
"Vertical move" (isti ključevi `r2_dim_dir`/`r2_dim_speed`, samo nova
vrednost) za svih 5 jezika.

**Usput otkriveno:** svih šest `r2_dim_*` ključeva je od postanka postojalo
SAMO u EN bloku — DE/IT/HR/SR stranice su ceo taj red tiho prikazivale na
engleskom (fallback mehanizam `t()` radi tačno kako treba, ali niko nije
primetio da prevodi nikad nisu ni napisani). Popravljeno za `dir`/`speed`
(sad ×5 jezika); `ballx`/`bally`/`leftpad`/`rightpad` OSTAJU na EN fallback-u
— van dogovorenog opsega ove sesije, zapisano kao otvorena stavka niže.

Na kraju, Flavio je pojasnio da je pitanje "da li je ovo negde obrađeno"
mislilo na internet, van projekta — pretraga (`web_search`) pokazala da RL
literatura o diskretizaciji (MountainCar, CartPole primeri) imenuje ose
sirovom fizičkom veličinom ("velocity") jer je njihova brzina 1D; naš
problem (2D brzina razdvojena u dve odvojeno objašnjene UI vrednosti za
laika) je pedagoško-prezentacioni problem koji akademska literatura
uglavnom ne mora da reši. "Horizontal move"/"Vertical move" je potvrđeno
legitimno originalno rešenje, ne propušteno tuđe.

### 5. Verzija

`s21` → `s22.1` → `s22.2` → `s22.3` → `s22.4` → konsolidovano na **`s22`**
pri zatvaranju ove sesije.

## Lekcije / ledger

- **Apostrof unutar single-quote JS stringa je poseban rizik klase teksta
  sa kontrakcijama** (engleski posesiv `'s`, italijanski `l'`/`dell'`/`un'`).
  Balans zagrada/parenteza NE hvata ovu grešku. Pravilo ubuduće: posle
  pisanja bilo kog novog i18n sadržaja na EN ili IT, obavezan
  `grep -nP "r2_ključ:.*[a-zA-Z]'[a-zA-Z]"` (slovo-apostrof-slovo unutar
  vrednosti) PRE nego što se sesija smatra završenom za taj fajl — ne
  osloniti se samo na `count('{')==count('}')`.
- **Klonirani fajlovi nose stare naslove i tekst dok se eksplicitno ne
  provere.** `rl2.js` header je i dalje govorio "rl1.js" i opisivao
  free-play kontrole (kopiran iz `rl1.js` pri kloniranju, nikad ažuriran);
  `rl2.html` infobox naslov je hardkodovano pisao "This page — RL 1".
  Oboje ispravljeno ove sesije, ali oba su postojala neopaženo kroz više
  prethodnih sesija. Kad se klonira fajl kao polazna tačka, header komentar
  i svaki hardkodovan fallback tekst treba eksplicitno pregledati, ne samo
  logiku.
- **"Tiho na engleskom" je sopstvena klasa buga, različita od slomljene
  i18n mehanike.** `r2_dim_*` ključevi rade TAČNO kako je fallback
  projektovan (`t()` → `T.en[key]` kad prevod ne postoji) — nema greške u
  mehanizmu. Greška je što niko nije primetio da prevod nikad nije NI
  NAPISAN za 4 od 5 jezika, jer je fallback nevidljiv dok neko doslovno ne
  pročita stranicu na tom jeziku i primeti engleske reči usred prevoda.
  Vredi periodično proveriti (`grep -c "ključ:" app.js`, treba da vrati 5)
  za svaku grupu ključeva koja se pamti kao "odavno gotova".
- **Verifikacija "srodne verifikacije komponovati, protokol ne žrtvovati"
  (s16/s20 pravilo) i dalje drži** — čitava sesija urađena u ~5 pisanja na
  server (HTML, app.js ×2, rl2.js, CSS), svako sa punim planom prikazanim
  pre izvršenja i sopstvenom post-write verifikacijom, bez usitnjavanja na
  desetine mikro-koraka.

## Završno stanje

- **Web repo (`xpongweb`):** četiri fajla izmenjena — `rl2.html`, `rl2.js`
  (potpuno prepisan), `app.js`, `xpong.css`. Četiri commita tokom sesije
  (`c55b0cc` s22.1, `4b65663` s22.2, `7f94b32` s22.3, `aafe634` s22.4), sva
  pushovana. `XP_VERSION` konsolidovan na `s22`, ide u peti commit ove
  sesije (posle ovog dokumenta).
- **Docs repo (`xpong`):** ovaj dokument, `README.md` ažuriran (posle ovog
  upisa) — commit i push u sledećem koraku.
- `rl2` originalni trotačkasti plan iz s21 (§12) — **sve tri tačke
  zatvorene.** Stranica demonstrira ono što treba: state space + trening +
  vidljiva evaluacija naučene politike, na sva 5 jezika, bez slobodne igre
  koja je dupliranje `rl1`.
- Sandbox bez zaostataka relevantnih za ovu sesiju.

## Sledeće (s23)

**GLAVNI PRAVAC — `rl3`, UČENJE.** Bellman jednačina, Q-tabela kao vidljiv
objekat, telemetrija agentovih odluka. Mehanika (Q-jezgro, `encodeState`,
trening petlja, `evaluate`/live-eval obrazac) već postoji u `rl2.js` i
prenosi se skoro nepromenjena — novo je *prikazivanje* pravila učenja
(Q-vrednosti po akciji, kako se ažuriraju, šta agent "misli" u datom
trenutku), ne pisanje nove mehanike učenja. Opseg dalje ostaje uzak: `rl3` =
UČENJE, `rl4` = EKSPLORACIJA (već razgraničeno u README-u, ne menjati bez
razloga). **Ovo je stavka koja ne sme biti zaboravljena ili preskočena na
početku sledeće sesije** — Flavio je to eksplicitno naglasio pri zatvaranju
s22.

**Ostavljeno iz `rl2` (manje, ne blokira `rl3`, ali ne zaboraviti):**
1. `r2_dim_ballx` / `r2_dim_bally` / `r2_dim_leftpad` / `r2_dim_rightpad` —
   i dalje SAMO u EN bloku `app.js`; DE/IT/HR/SR i dalje tiho padaju na
   engleski za te četiri vrednosti u state-tabeli (isti bug klasa kao
   `r2_dim_dir`/`r2_dim_speed` koji je OVE sesije ispravljen — ostala
   polovina table još čeka).
2. Infobox "Brzina uređaja" na `rl2` — `stepsPerSec` se meri i prikazuje u
   statistici, ali sama adaptacija paketa po `rAF` frejmu (s19 dogovor)
   nije objašnjena tekstom na stranici; s19 uslov je da adaptacija mora
   biti dokumentovana, ne ostati crna kutija. Nasleđeno iz README-a, i dalje
   otvoreno.

**Nasleđeno iz README-a, i dalje otvoreno (nepromenjen prioritet):**
1. Cache-busting `?v=sNN` na `<link>`/`<script>`, bumpovan sa `XP_VERSION` —
   `XP_VERSION` trenutno pokriva samo `app.js`, ne i `xpong.css`/HTML; uzrok
   tri ranija ručna čišćenja keša (s20).
2. *(prio2)* Aktivna provera verzije (`version.json` + `visibilitychange` +
   baner) — rešava tablet slučaj gde pull-to-refresh nije pouzdan.
3. *(prio2)* Prekidači (Beam/Heatmap) nose ime bez on/off stanja u tekstu.
4. *(prio2)* JS benchmark na PC/tablet/telefonu.
5. Kandidati: `sr.lat` (dodatna latinična srpska varijanta), Key Concepts
   iz About eseja.

---

*Flavio & Claude · xpong · session_22.md · 27. jul 2026.*
