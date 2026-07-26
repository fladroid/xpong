# Sesija 20 — 26. jul 2026.

## Fokus
Implementacija stranice **`rl2` — agent koji uči**, po rasporedu dogovorenom u s19.
Stranica je završena i živa. Uz to: pročitana dva `KAKO-*` recepta iz Buchenberga,
zatvorena jedna nasleđena stavka, i otkrivena tri stvarna baga u sopstvenoj
implementaciji — dva algoritamska, jedan u pokazatelju.

## Health snapshot (početak)
- docs `s19`, web `s18` (namerno nesinhronizovano — s19 nije dirao web fajlove)
- live `xpong.opik.net` 200, `concepts.json` validan, 5 sekcija
- sandbox (Claudeov container) **prazan** — skripte i JSON rezultati merenja iz s19 nestali

## Šta je urađeno

### 1. Zatvorena nasleđena stavka „naslovi (otom potom)"
Živela od s14 do s19 kao naslov bez sadržaja. `grep` kroz sve sesije potvrdio je da
predmet nikad nije zapisan — samo Flaviova napomena da se odlaže. **Nerekonstruktibilna,
zatvorena bez izvršenja.** Pokušaj čitanja iz starih razgovora odbačen: alat vraća
fragmente u kontekst (ne fajl na disk), pa nije grep-abilan i nije izvor istine.

### 2. `rl2` — podloga
Klon `rl1.html`/`rl1.js` uz četiri izmene identiteta (`<title>`, `data-page`,
`r1_title`→`r2_title`, `<script src>`). Naslov: **„RL 2 — How the agent sees the world"**
(potvrdio Flavio; opseg stranice je STANJE, ne učenje).

### 3. Kontrola grubosti — segmentirani prekidač
Prvi element u projektu bez postojećeg obrasca (svi dotadašnji prekidači su on/off).
Forma: tri polja u jednom okviru, skriveni `radio` kao izvor istine (isti odnos kao
checkbox kod `.xp-toggle`). Ime **i** broj jedan iznad drugog — ime nosi značenje,
broj nosi meru. `4000` je `checked` u markupu, ne iz JS-a: podrazumevana vrednost je
odluka iz merenja i treba da stoji tamo gde se vidi.
CSS bez `:has()` — projekat cilja browser od ~2015.

### 4. Definicija prostora stanja (`GRIDS`)
s19 je zapisao **rezultate** merenja, ali ne i **parametre**. Sandbox je resetovan, pa
je recept izgubljen. Fina varijanta je rekonstruisana pouzdano (`10×10×3×5×8 = 12.000`
= stari Pong minus dimenzija protivničkog reketa); ostale dve su **definisane iznova**
uz uslov da se mreža na terenu vidljivo menja na sve tri:

| | loptica X×Y | smer | brzina | reket | ukupno |
|---|---|---|---|---|---|
| gruba | 5×5 | 2 | 3 | 2 | 300 |
| srednja | 10×8 | 2 | 5 | 5 | 4.000 |
| fina | 10×10 | 3 | 5 | 8 | 12.000 |

Kodiranje provereno računski: maksimalni indeks je tačno `N−1` za sve tri (299 / 3999 / 11999).

### 5. Mreža stanja, istaknuta ćelija, telemetrija
`drawGrid()` crta X×Y preko terena — **dve od pet dimenzija**; ostale tri nemaju mesto
na terenu i to je pedagoška poenta, ne propust. Pregrada u kojoj je loptica dobija blagu
ispunu (ispod linija mreže). Gore levo: `state N / ukupno` — ceo svet agenta sveden na
jedan ceo broj. Broj se menja i kad loptica miruje, jer se menja peta dimenzija (reket).
Mreža je najdublji sloj — ispod heatmapa, jer je koordinatni sistem, a ne podatak nad njim.

### 6. Q-jezgro i trening
`Float32Array` (12.000 stanja = 144 KB), `LR 0.15`, `GAMMA 0.95`, epsilon 1.0→0.05
(`decay 0.9995`). Headless epizoda, greedy evaluacija **odvojena** od treninga (po lekciji
iz s19 — merenje tokom treninga meri raspored eksploracije, ne učenje).
Adaptivni paket epizoda po `requestAnimationFrame`: meri prethodni prolaz, cilja ispod 8 ms.
Izmereni koraka/s objavljen u pokazateljima — **adaptacija mora biti vidljiva**.

### 7. Grafikon i tri pokazatelja
Svako pokretanje **dodaje** krivu preko prethodnih (poslednja puna, ranije bleđe).
Bez kompozitnog broja: kvalitet, rasejanje, brzina — tri zasebna broja.
Auto-scroll do grafikona pri pokretanju treninga (pada ispod pregiba, a trening je headless).

### 8. Tekstovi i Key Concepts
`r2_page_title`, `r2_page_text`, `r2_nav_text`, `r2_train`, `r2_stat_*`, `r2_grid_*`,
`nav_rl2` — svi × 5 jezika. Nav-stavka „RL 2" / „РЛ 2" između RL 1 i Stabilization.
Key Concepts sekcija `rl2` × 4 kartice: 🗺️ State space, 🔲 Discretization,
🌌 Curse of dimensionality, ⛓️ Markov decision process. Svi slugovi provereni `curl`-om (HTTP 200).

## Bagovi otkriveni i ispravljeni (svi u kodu pisanom danas)

### B1 — fiksni tie-break pinovao reket uz gornju ivicu
`if (a0 >= a1 && a0 >= a2) return 0;` — sa nula-inicijalizovanom tabelom **svako**
stanje je izjednačeno, uslov je uvek tačan, i agent u svakom neposećenom stanju bira
akciju 0 („gore"). Greedy evaluacija (eps=0) nikad ne izađe iz tog izbora → reket na
vrhu → stabilnih 0,25 odbijanja kroz 11 pokretanja.
Komentar uz tu liniju opisivao je grešku kao osobinu („deterministic, not random").
**Ispravka:** nasumičan izbor među akcijama sa maksimalnom vrednošću.

### B2 — pogrešna definicija epizode (glavni uzrok)
Epizoda se prekidala na **bilo koji** gol. Kad slab protivnik (walker) primi gol,
epizoda se završava bez obzira koliko je agent dobar — plafon je bio ugrađen u merenje,
ne u agenta. Izmereno u izolovanoj Python replici: **0,40 vs 1,35 pri inače identičnom
algoritmu (faktor 3,4)**.
**Ispravka:** epizoda traje dok **agent** ne primi gol; gol koji agent da samo re-servira
lopticu. Posle ispravke: 4,56 (srednja) i 4,02 (fina) — isti red veličine kao s19 tabela,
što potvrđuje da je s19 koristio istu definiciju.

### B3 — `max − min` kao mera pouzdanosti
Raspon sistematski raste sa brojem uzoraka, pa je merio **koliko puta je dugme
pritisnuto**, ne koliko je metoda pouzdana (Fine 4,45 pri n=4 vs Medium 5,25 pri n=10 —
lažno je izgledalo da je Medium gori). **Ispravka:** standardna devijacija.
Uz to `EVAL_N` 20→50, jer je 20 epizoda merilo šum a ne kvalitet.

### B4 — slomljen `concepts.json` (moja greška, odmah vraćena)
Upisan `\U0001f5fa` (Python escape) u JSON, koji poznaje samo `\uXXXX`. Fajl je pisan
pre validacije, pa je nevalidan JSON završio na disku — a `.catch(function(){})` u
`app.js` guta grešku, što znači **tiho nestajanje kartica na SVIM stranicama**.
Vraćen backup, upisano ponovo sa sirovim UTF-8 emoji znakovima (kako postojeće kartice
već rade) i `json.loads(s)` **pre** dodirivanja diska.

## Rezultat merenja u browseru (Flavio, s20.8, n=10 po varijanti)

| grubost | kvalitet | devijacija |
|---|---|---|
| srednja 4.000 | 4,56 | **1,10** |
| fina 12.000 | 4,02 | **1,32** |

Razlika u kvalitetu (0,54) manja je od same devijacije → po kvalitetu **izjednačene**;
fina je **raspršenija**. Nalaz iz s19 reprodukovan uživo, u browseru, korisnikovim rukama.
Stranica sada nosi tvrdnju koju posetilac može sam da obori za dva minuta.

## Lekcije (ledger)

1. **Stavka bez zapisanog sadržaja nije stavka.** „Otom potom" je legitimno odlaganje, ali
   mora nositi rečenicu o čemu se radi — inače preživi pet sesija kao trošak pažnje bez
   ijednog bita informacije.
2. **Merenje mora zapisati ULAZ, ne samo izlaz.** s19 je dao brojeve bez parametara; kad
   se sandbox resetovao, recept je nestao a broj ostao — i postao nereproducibilan.
   Definicija epizode je deo eksperimenta jednako kao broj epizoda.
3. **`data-i18n` atribut i ključ u rečniku ulaze ISTOVREMENO.** `applyI18n()` bezuslovno
   radi `textContent = t(key)` — nema provere postojanja, pa se fallback iz HTML-a nikad
   ne vidi. Atribut pre ključa = sirovo ime ključa na ekranu. (Isto piše u
   `KAKO-JeziciUI.md` §1 — pročitati recept pre nego što se dijagnostikuje.)
4. **`XP_VERSION` je cache-dijagnostika SAMO za `app.js`.** `xpong.css` i `rl2.js` idu bez
   oznake verzije, pa svež footer NE znači svež CSS. Uzrok tri ručna čišćenja keša danas.
   → stavka: `?v=sNN` na `<link>`/`<script>`.
5. **JSON: validirati string PRE pisanja**, ne samo fajl posle. `KAKO-KeyConcepts.md` §8
   validira posle upisa — nedovoljno, jer je slomljen fajl već na disku i tiho briše
   kartice sajt-široko.
6. **`max − min` nije mera rasejanja kad se n razlikuje.** Standardna devijacija jeste.
7. **Fiksni tie-break + nula-inicijalizacija = sistemska pristrasnost**, ne neutralnost.
8. **Sopstveni komentar u kodu nije dokaz.** B1 je nosio komentar koji je grešku
   opisivao kao namernu odluku.
9. **Ne nagađati treći put — instrumentirati.** Posle dve promašene dijagnoze, izolovana
   Python replika dala je broj (3,4×) umesto pretpostavke, bez trošenja Flaviovog vremena
   na još jedan „probaj pa vidi".
10. **Onboarding mora obuhvatiti `KAKO-*` dokumente.** Nisu u project knowledge ovog
    projekta nego u buchenberg repou — a sadrže recepte koji su danas dvaput bili potrebni.

## Pravila potvrđena/zapisana ove sesije

- **Key Concepts — ponavljanje između stranica je NAMERNO.** Princip je pozajmljen iz
  YouTube predavanja: kad god se pojam pojavi u izlaganju, link ka Wikipediji se pokaže
  ponovo. Zabrana duplikata važi **samo unutar jedne stranice**. Sve kartice — naslov i
  opis — su na engleskom, na svim UI jezicima. (Ranije dogovoreno, nigde zapisano.)
- **Oprez ≠ usitnjenost** (iz s16, primenjeno danas): srodne provere kompozirane u manji
  broj rundi, bez žrtvovanja show → OK → execute protokola.
- **Dokumentovana odluka nije predmet ponovnog glasanja.** Kad Claude nema razlog za
  odstupanje, izvršava zapisano umesto da nudi opcije; ponuda opcije signalizira da je
  odluka otvorena i obesmišljava trud oko dokumentacije.

## Završno stanje

- **`rl2` živ i kompletan** po s19 rasporedu: mreža stanja, istaknuta ćelija, telemetrija
  indeksa, segmentirani prekidač grubosti, Q-učenje, headless trening sa adaptivnim
  paketom, grafikon sa snopom krivih, tri pokazatelja, tekstovi ×5 jezika, Key Concepts ×4,
  nav-stavka.
- **Odstupanje od s19 rasporeda (namerno):** `Start` zadržan pored novog `Train`. s19 kaže
  „centar Treniraj/Reset", ali ne kaže da Start ide napolje — a igra uživo je jedino mesto
  gde se vidi mreža, istaknuta ćelija i telemetrija. Trening je headless i teren miruje.
- Verzija konsolidovana `s20.9` → **`s20`**; web i docs sinhronizovani na s20.

## Sledeće (s21)

**Glavni pravac: `rl3` — UČENJE** (Bellman, Q-tabela kao vidljiv objekat, telemetrija
odluka agenta). Mehanika već postoji u `rl2.js` i može se preneti; novo je *prikazivanje*
pravila učenja, ne njegovo pisanje.

**Otvorene stavke, po prioritetu:**
1. **Cache-busting `?v=sNN`** na `<link>`/`<script>` u svim stranicama, bumpuje se zajedno
   sa `XP_VERSION`. Rešava uzrok tri ručna čišćenja keša u s20. (prio 1 — infrastrukturno)
2. **Infobox „Brzina uređaja"** na `rl2` — `stepsPerSec` se već meri i prikazuje u
   pokazateljima, ali nema objašnjenja šta adaptacija radi. s19 uslov: adaptacija mora biti
   dokumentovana, inače je crna kutija. (prio 1 — dug prema s19)
3. **Prekidači bez `on`/`off` u tekstu** (prio 2) — Material/Apple/W3C se slažu: uz prekidač
   ide ime onoga što kontroliše, stanje čita položaj. Trenutno „Beam: off" duplira signal.
   Dira `xray.html`, `rl1.html`, `rl2.html` + `x_ray_on/off`, `x_heat_on/off`.
   Uz to: pojačati vizuelnu razliku aktivnog stanja (bold na imenu).
4. **JS benchmark** na PC/tablet/telefon (prio 2) — svi Android uređaji posle 2015
   odgovaraju, a samoštimovanje ne zavisi od njega; benchmark bi samo dao broj za infobox.
5. **README PAŽNJA → dopisati escape recept**: `grep -n "target" app.js | cat -A` pre
   svakog sidrenja. Upozorenje bez postupka je pola dokumentacije.
6. **Kandidati:** `sr.lat` aditivno; Key Concepts iz About eseja (crna kutija, emergencija,
   neuronska mreža, transformer).

**Zatvoreno u s20:** „naslovi (otom potom)" — nerekonstruktibilna, uklonjena iz nasleđenog.
