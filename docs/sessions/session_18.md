# Session 18 — KC dopuna rl1; layout poravnat sa nav-redom; priprema stranice 2

**Datum:** 25 Jul 2026
**Fokus:** dve zaokruzene stavke iz s17 (KC dopuna rl1, sirina stranica), zatim
razgovor: modeli i podela rada po fazama sesije, pa pojmovna priprema stranice 2
(Q-learning) sa merenjem u sandboxu umesto nagadjanja.

## Otvaranje (health snapshot)
- Prvi put onboarding kroz `health_check.py` (dodat u s17) umesto rucnih provera.
- xpong (docs) @ `2418537` (s17), cisto; xpongweb (web) @ `db0361f` (s17), cisto.
- HTTPS 200; XP_VERSION live = lokalno = `s17`; DNS -> 130.61.37.60; sve zeleno.
- Onboarding komponovan u dve runde (README+git, pa session dokovi+health) —
  primena lekcije iz s16 (oprez != usitnjenost).

## Sta je uradjeno

### KC dopuna rl1 (2 kartice)
- Konsultovan `KAKO-KeyConcepts.md` iz Buchenberga pre izmene. Razlika potvrdjena
  citanjem koda: xpong NEMA `CONCEPT_PAGES` niz — stranica se identifikuje preko
  `data-page` atributa na `<body>`, pa nova stranica ne trazi upis u JS. Insertion
  point `#xp-footer`, naslov hardkodovan `'Key Concepts'`, bez override mape.
- `.catch(function () {})` postoji i kod nas (app.js L559) — nevazeci JSON gasi
  kartice na SVIM stranicama bez ijednog vidljivog znaka. Validacija obavezna.
- Slug provera pre upisa: `Intelligent_agent` i `Agent_(artificial_intelligence)`
  oba vracaju HTTP 200 bez redirecta, ali REST API `titles.canonical` pokazuje da
  je drugi redirect na prvi. Upisan kanonski `Intelligent_agent`.
- Dodato ISPRED postojece kartice (od opsteg ka posebnom, grid se cita s leva):
  RL (`Reinforcement_learning`) + Agent (`Intelligent_agent`) + Random walk.
- XP_VERSION NIJE bumpovan za ovu izmenu — `concepts.json` se dovlaci sa
  `?t=Date.now()`, ne moze biti kesiran. Eksplicitno javljeno Flaviju.

### Layout — sve stranice poravnate sa nav-redom
- Uzrok razlike nadjen citanjem: `#xp-page` i `#xp-header-inner` su 1200px, ali
  `game`/`xray`/`rl1` ubacuju medjusloj `.xp-game-wrap` sa `max-width: 900px`.
  `about` ga nema, pa je izgledao siri. `index` namerno netaknut (Flavio).
- `.xp-game-wrap` i `.xp-game-deck`: 900px -> 1200px.
- Posledica koja se pokazala tek uzivo: canvas je 800x500 sa `width:100%` i
  `height:auto`, pa sirina diktira visinu. Na 1200px teren postaje ~730px visok —
  Flavio je slao slike: vidi se ili gornji ili donji deo, nikad ceo.
- Resenje u dva koraka: `.xp-game-canvas-box` i deck dobili
  `max-width: min(100%, 72vh)` (visina vezana za prozor, ne za fiksan broj),
  i scorebar zbijen — labela `display: inline` umesto `block`, broj 48px -> 36px,
  margine smanjene. Ustedjeno ~45px vertikale na sve tri stranice.

### Razgovor: modeli i faze sesije
- Flavio pitao kako Claude koristi izabrani model i da li uopste zna koji je
  ukljucen. Odgovor: zna samo zato sto pise u kontekstu koji stize na pocetku
  sesije — nema introspektivnog signala. Nema "ja" koje bira model; model JESTE
  ono sto generise odgovor, plus kontekst. Ono sto se prenosi izmedju sesija je
  tekst (README, session dokovi, memorija), ne unutrasnje stanje.
- Fable 5: bezbednosni mehanizam preusmerava deo upita na Opus 5, konzervativno
  podesen (Anthropic: <5% sesija). Objasnjava "natezanje" koje je Flavio primetio.
- Flaviova teza (prihvacena): organizacija rada i dokumentacija vrede vise od
  izbora modela. Razlog zasto vazi BAS kod nas: protokol radi kao izjednacivac —
  show->OK->execute, `assert count==1`, health check svi seku isti prostor
  gresaka (dugi autonomni lanci bez provere), a to je prostor u kome se modeli
  najvise razlikuju.
- Postena rezerva: protokol hvata GRESKE, ali ne hvata PROPUSTENE BOLJE IDEJE —
  kad resenje radi, nema sta da prijavi. Layout danas je primer: `95vh` nije pao
  ni na jednom assertu, samo je bio pogresan broj. Jedina odbrana na toj strani
  je Flaviova navika da pogleda i stranice koje izmena nije trebalo da dotakne
  (a `xpong.css` je deljen, pa ih je dotakla).
- Preporuka po fazama: inicijalizacija i zatvaranje = Sonnet (citanje/destilacija);
  rad = Sonnet dok je zadatak "ima tacan odgovor", Opus kad je pojmovna odluka.
  Prava osa nije faza nego tip zadatka. Prebacivanje usred sesije nista ne kosta.
- Dogovoreno: Claude pre plana signalizira tip zadatka jednom recenicom
  ("rutinski, tacan odgovor postoji" / "pojmovna odluka, nema asserta"). Signal je
  najslabiji tamo gde bi najvise vredeo — kad problem IZGLEDA lak a nije.

### Priprema stranice 2 (Q-learning) — pojmovno + merenje
- Pojmovna novost: na `rl1` agent deluje bez uma; na stranici 2 prvi put postoji
  unutrasnje stanje koje se menja iskustvom. X-Ray prvi put gleda UM, ne svet.
  Beam/heatmap su cinjenice sveta; Q-vrednosti su PROCENE i mogu biti pogresne —
  covek prvi put gleda nesto sto moze uhvatiti u zabludi.
- Prepreka: ucenje je sporo, a paznja korisnika traje minut-dva.
- Claude ponudio binarni izbor (partija ILI trening). **Flavio odbio binarnost i
  predlozio slider brzine** — od normalne (vidi se igra i promena vrednosti),
  preko ubrzanog filma, do munjevitog gde se loptica samo naslucuje a podaci se
  menjaju vrtoglavo.
- Zasto je to bolje: sam prelaz kroz brzine POSTAJE lekcija — covek ne procita da
  je ucenje sporo, nego mora da ubrza vreme da bi ista video. To je *sample
  efficiency* kao dozivljaj, ne kao infobox.
- Posledica: iznad neke brzine levi reket mora biti agent (covek ne moze igrati
  na 100x). Postojeci `Left: Human/Agent` prekidac se prirodno vezuje za slider —
  trening i partija nisu dva moda nego dve tacke istog klizaca.

### Merenje u sandboxu (umesto nagadjanja)
- Flavio: "bez toga mogu samo nagadjati" — dogovoren test u Claudeovom izolovanom
  sandboxu (odvojen od foxuno i repoa), nista se ne pise u projekat.
- **Nalaz o poreklu:** u sandboxu su ZATECENI fajlovi od iste noci (02:50-03:00)
  koji rade isti eksperiment — `qtest.py`, `qtest2.py`, `curves.json`. Nisu pisani
  u ovom razgovoru; poreklo neutvrdjeno (verovatno paralelna sesija). Nisu
  obrisani ni preprisani; tretirani kao nalaz koji se ne moze verifikovati.
- Zatecene krive (prosecan broj odbijanja po epizodi, 12k epizoda):
  | stanja  | ~3k ep | ~6k ep | ~12k ep |
  |---------|--------|--------|---------|
  | 72.000  | 1,0    | 2,1    | 5,5     |
  | 4.000   | 2,4    | 4,8    | 7,6     |
  | 300     | 1,8    | 3,4    | 6,0     |
  Obrazac: 300 uci najbrze pa udari u plafon (nema dovoljno informacija);
  72.000 sporo puni ogromnu tabelu; 4.000 dominira na obe strane.
  Kontraintuitivno — vise detalja NIJE bolji agent.
- **Nezavisna replika (Claudeov kod) potvrdila je samo BRZINU, ne i krive.**
  Merenje: ~60.000 koraka/s u Pythonu, ~270 koraka po epizodi. Replika je bila
  prekratka (2.500 epizoda, sve tri jos u ravnom delu) da razlikuje varijante.
- Izvedeni zakljucak koji JESTE cvrst: JS bez renderovanja radi 0,5-1M koraka/s,
  pa pun trening od 12.000 epizoda staje u **5-15 sekundi**. Slider je izvodljiv;
  pitanje NIJE da li je trening moguc, nego koliko stanja agent razlikuje.
- Ograničenje okruzenja (za ubuduce): pozadinski procesi u sandboxu NE prezivljavaju
  izmedju tool poziva; `nohup` to ne menja. Dugacak run mora u jedan poziv ili u
  vise kratkih.

## Lekcije / ledger
- **Sirina se resava jednim brojem, visina posledicno.** Canvas sa `width:100%` i
  `height:auto` pretvara svaku promenu sirine u promenu visine. Za igru je granica
  `min(100%, NNvh)` — vezana za prozor, ne za fiksan broj piksela.
- **`concepts.json` ne trazi bump verzije** (`?t=Date.now()`); `xpong.css` i
  `app.js` traze. Razlikovati pre nego sto se javi verzija Flaviju.
- **Wikipedia HTTP 200 bez redirecta NIJE dokaz kanonskog sluga** — REST API
  `titles.canonical` je jedini pouzdan izvor (dva sluga, oba 200, jedan redirect).
- **Zatecen artefakt u sandboxu nije izvor istine.** Citati ga, ne brisati, ne
  graditi zakljucke bez nezavisne provere — i eksplicitno razdvojiti sta je cije.
- **Protokol ne hvata propustene bolje ideje**, samo greske. Vizuelna provera svih
  stranica (i onih koje izmena nije trebalo da dotakne) je jedina odbrana.

## Zavrsno stanje
- Web (xpongweb) @ `28830e8`: `data/concepts.json` (rl1 3 kartice), `xpong.css`
  (wrap+deck 1200, canvas cap 72vh, scorebar zbijen), `app.js` (XP_VERSION s18).
- Verzija konsolidovana s18.1 -> s18.2 -> s18.3 -> s18.4 -> `s18` (25 Jul 2026).
- Sve stranice vizuelno proverene (Flavio): "sve stranice su sada jednako dobre".
- Bekapi u `/tmp/` (concepts.json, xpong.css, app.js — bak-s18).

## Sledece (s19)
- **Prvo:** dovrsiti merenje — jedan duzi run po varijanti (12k epizoda), pa
  odluka o velicini prostora stanja za stranicu 2. Kod je u sandboxu, ali sandbox
  se ne racuna kao trajno skladiste — po potrebi napisati ponovo.
- Zatim stranica 2 (Q-learning): slider brzine vezan za Human/Agent prekidac,
  telemetrija uma (Q-vrednosti), pojmovna granica prema rl1.
- Nasledjeno: naslovi ("otom potom"); README PAZNJA -> dopisati escape recept;
  (kandidat) sr.lat aditivno; KC iz About eseja.
