# Session 13 — M2 "cigla 3" (dopune telemetrije): zrak na servisu, prsten zrak-ON, broj golova u traci

**Datum:** 03 Jul 2026
**Fokus:** dve Flaviove molbe kao dopuna Telemetrije (praktično "cigla 3" M2, koja
u originalnom planu nikad nije bila definisana — vidi Kontekst). Obe u duhu
senka/metapodaci, bez ikakve inteligencije. Verzije s13.1–s13.4, sve potvrđene
u browseru odmah po deployu.

## Otvaranje (health snapshot)
- xpong (docs) @ `00ffd42` (s13), čisto, u sinhronu.
- xpongweb (web) @ `ab4ce93` (s13), čisto, u sinhronu.
- web: HTTPS 200; `XP_VERSION='s13'` (živo) — README, session docs, kod složni.
- `health_check.py`: i dalje ne postoji (ručni snapshot komandama).

## Kontekst: šta je "cigla 3"
Onboarding je otkrio da "M2 cigla 3+" nikad nije bila konkretizovana. Originalni
plan M2 (zaključan u s09) imao je TRI cigle: (1) zrak, (2) heatmap, (3) parametri
— ali cigla 3 (parametri) je SVESNO izbačena iz M2 na Flaviov zahtev još u s09
(konstante ostaju izolovane u pong-core za kasnije). "Cigla 3+" u kasnijim listama
bila je samo prazna oznaka, ne zaostali plan. Ova sesija je popunjava dopunama
postojeće Telemetrije.

## Šta je urađeno

### Molba #1 — zrak na servisu iz centra + indikator "zrak ON" (s13.1)
- **Bez zraka i markera na servisu iz centra.** `drawRay` rani return kad je
  loptica na centralnoj servisnoj tački: `|ball.x-W/2|<1 && |ball.y-H/2|<1`.
  Prag `<1px` (ne strogo `===`) radi float-otpornosti. Detekcija iz STANJA —
  `resetBall`/`newState` postavljaju lopticu tačno na `W/2,H/2`, prvi `stepBall`
  je pomeri. Bez flaga u pong-core (ne zagađuje čistu deljenu fiziku).
- **Prsten "zrak ON" na loptici.** U `draw()`, posle crtanja loptice, kad `rayOn`:
  tanki prsten (`arc`, `BALL_R+4`, stroke, accent 0.9). Zaseban od `drawRay`, pa
  vidljiv i na servisu gde zraka nema — "sloj je živ" signal, simetričan heatmap
  okvirima. Konstantan (ne prati `dim` zraka) — Flavio potvrdio da tako sedi.
- Marker (kontakt kružić) OSTAJE kako je bio: samo na zid/reket, ne na gol
  (potvrđen dogovor iz s09, bio u header komentaru + kodu — Flavio se nije sećao).

### Molba #2 — broj golova u traci heatmapa (s13.2→s13.4, tri iteracije za vid)
- Broj golova ispisan na traci gde count>0 (senka postaje čitljiv podatak).
- Trake proširene `bw` 14→22 da broj/kontrast lepo stanu.
- **Iteracija boja vođena Flaviovim vidom (visoka dioptrija):**
  - s13.2: beli tekst + tamni obrub, bold 13px → Flaviu "bela fleka" (pretanko za bold).
  - s13.3: crn broj na belom disku (`#fff`/`#000`), 15px normal → čitljivo, ali
    fiksno belo/crno, netematsko.
  - s13.4 (finalno): **opcija 2 — surface disk + text broj** (`colors.bg`/`colors.fg`),
    tematski. Light ≈ s13.3, Dark = taman disk + svetli broj, automatski po temi.
- Izbor boje donet preko HTML **mockup artifakta**: 4 opcije prikazane na traci s
  4 count-a (1/3/5/8) u OBE teme, pravim xpong bojama — Flavio izabrao vizuelno.
  Pristup se pokazao odličnim za dizajnerske odluke gde kontrast/čitljivost bitni.

## Lekcije / ledger
- **Dogovor može biti u KODU, ne samo u sesijama.** Pravilo "marker samo na
  prepreci, ne na golu" nađeno u header komentaru + `drawRay`, ne u arhivu sesija.
  Pre rekonstrukcije "iz glave", grep kod/komentare.
- **Detekcija stanja iz pozicije, bez flaga u core.** Overlay-potreba ("loptica
  na servisu") rešena čitanjem `ball.x/y` u overlay-u, ne dodavanjem polja u čistu
  deljenu fiziku. Prag `<1px` umesto `===` za float-otpornost.
- **Čitljivost > tema (Flaviov vid).** Kad kontrast zakaže, prvo idi na krupnije/
  jače, pa tek onda traži tematsko rešenje koje zadržava kontrast (opcija 2:
  surface/text disk je tematski a čita se kao belo/crno na Light).
- **Mockup u pravim bojama = alat za dizajn-odluke.** Prikaži sve opcije odjednom
  u stvarnim tokenima teme umesto redom deployovati varijante. Vredi ponoviti.

## Telemetrijski rečnik (konvencija za M3 — zabeleženo dok je sveže)
Dva sloja Telemetrije sad dele isti vizuelni jezik, koji M3 stranice nasleđuju:
- **Indikator prisustva sloja** ("ON, ali još bez podataka"): heatmap = prazni
  okviri traka; zrak = prsten na loptici. Isti gest za oba.
- **Metapodatak kao čitljiv broj, ne samo boja**: traka nosi i tačnu vrednost.
- **Presedan boja**: gde čitljivost to traži, broj sme odstupiti od accent i ići
  na surface/text kontrast (opcija 2). Čitljivost pobeđuje temu.

## Završno stanje
- `https://xpong.opik.net/xray.html` (s13): Telemetrija — na servisu iz centra
  nema zraka/markera, loptica nosi prsten "zrak ON"; heatmap trake (bw 22) nose
  broj golova na surface disku s text brojem (tematski, čita se u obe teme).
  Sve potvrđeno u browseru (s13.1→s13.4).
- xpongweb dirnuto: `xray.js` (drawRay rani return, prsten u draw, broj+disk u
  drawHeatmap, bw 22), `app.js` (XP_VERSION, datum).
- M2: cigla 1 ✅, cigla 2 ✅, "cigla 3" (dopune telemetrije) ✅. XP_VERSION s13.
  Bekapi u /tmp/ (brišu se posle commita).

## Sledeće
- M3 (RL faze) — nove stranice, jedna po fazi; uvodi PRAVOG agenta koji uči
  (Q-tabele, trening petlja), koristi postojeći čist `pong-core`. Glavni pravac.
- (kandidat, jeftina zaštita pre M3 ekspanzije) health_check.py kao strukturni čeker.
- (kandidat) Key Concepts iz About eseja: crna kutija, emergencija, neuronska
  mreža, transformer.
- (anticipiran) sr.lat aditivno.
