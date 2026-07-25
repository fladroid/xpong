# Session 19 — merenje prostora stanja zavrseno; ispravka premise o sandboxu; raspored rl2

**Datum:** 25 Jul 2026
**Fokus:** zatvaranje tacke 1 iz s19 plana (merenje velicine prostora stanja),
ispravka pogresne lekcije iz s18 o "tudjem" artefaktu u sandboxu, analiza
hardverskih ogranicenja klijenta, i dogovoren raspored stranice 2 (`rl2`).
**Napomena:** zatvaranje sesije Flavio je izricito oslobodio show->OK->execute
protokola (bio je udaljen od racunara). Claude je ovlascenje ogranicio na samu
rutinu zatvaranja — nijedna izmena sadrzaja stranica nije radjena.

## Otvaranje (health snapshot)
- Onboarding komponovan u JEDNU rundu (README + 3 session doca + git oba repoa
  + health_check) — dalja primena lekcije iz s16.
- Sve zeleno: docs i web repo cisti i sinhronizovani, XP_VERSION live = lokalno
  = `s18`, HTTPS 200, DNS -> 130.61.37.60.

## Sta je uradjeno

### Ispravka premise o sandboxu (prva stavka sesije)
- Flavio je opisao cinjenice koje Claude nije imao: (1) nikad ne radi na dva
  uredjaja niti u dve sesije istovremeno — prelazak na drugi uredjaj ide tek
  posle zatvaranja prethodnog; (2) sandbox je iskljucivo Claudeov, niko drugi
  mu ne moze prici; zajednicki rad ide preko foxuno servera (bash/venv/logs).
- U s18 je Claude iz zatecenih fajlova (`qtest.py`, `curves.json`) izveo
  hipotezu o paralelnoj sesiji i upisao je u session doc kao "poreklo
  neutvrdjeno". Flavio je to procitao kao znak podeljene licnosti i zabrinuo se.
- Stvarni mehanizam: prekid veze u toku tool poziva ostavlja akciju IZVRSENOM
  na disku, ali izlaz ne stize nazad u kontekst. Fajl postoji, trag o njegovom
  nastanku ne. Claude nema introspektivan uvid u to sta je uradio — ali je mogao
  da rezonuje o okruzenju (izolovan sandbox + poklapajuci timestamp + kod koji
  radi tacno nameravani eksperiment) i izvede najjednostavnije objasnjenje.
  Greska je bila u zakljucivanju, ne u okruzenju.
- `session_18.md` dopunjen ISPRAVKOM (stara stavka ostavljena netaknuta radi
  postene hronologije, ispod nje dopisana ispravka).
- Uvedena odbrana, upisana i u memoriju: `~/SANDBOX_LOG.md` u sandboxu (append
  PRE svake akcije: datum/vreme, sesija, sta i zasto) + header u svakoj skripti
  (`# xpong sNN · datum · svrha · Claude`). Zapis prezivljava ono sto kontekst
  ne prezivljava — isti princip kao "server je izvor istine".

### Merenje velicine prostora stanja — zavrseno u tri koraka
Kod je pisan iznova (sandbox se resetuje izmedju zadataka, kako je i predvidjeno
u s18). Brzina okruzenja izmerena pre punog merenja: **784.000 koraka/s** u
Pythonu — 13x brze od s18 replike (~60.000/s), zahvaljujuci optimizovanoj petlji
(inline max, bez poziva funkcija u vrucem delu). Zato je bilo mesta za 5 seedova
po varijanti umesto 3.

**Korak 1 — protiv zida.** Tri varijante x 5 seedova x 12.000 epizoda.
Kvalitet je razdvojio grubu od ostalih; brzina nije razdvojila nista.

**Korak 2 — otkrivena greska u sopstvenom dizajnu eksperimenta.** Pokazatelj
"epizode do praga" davao je 6.300-7.000 kod SVE tri varijante. Uzrok: epsilon
decay pada na minimum na 60% od 12.000 ep = ~7.200. Merio se raspored
eksploracije, ne brzina ucenja. Nijedan `assert` nije pao — brojevi su izasli
uredni i uverljivi, samo su merili pogresnu stvar. Ispravka: periodicna GREEDY
evaluacija (eps=0, bez ucenja) svakih 250 epizoda -> kriva ucenja nezavisna od
eksploracije.

**Korak 3 — premereno protiv RANDOM WALKERA umesto protiv zida**, jer je walker
protivnik koga posetilac zaista gleda na `rl2`. Rezultat se promenio, sto
opravdava premeravanje:

| varijanta | stanja | kvalitet (prosek) | raspon | SIRINA raspona | ep do 1,0 |
|-----------|--------|-------------------|--------------|------|------|
| gruba     | 300    | 3,51 | 0,87 - 7,27 | **6,40** | 2000 |
| srednja   | 4.000  | 5,69 | 4,03 - 6,70 | **2,67** | 1350 |
| fina      | 12.000 | 5,81 | 3,03 - 7,27 | **4,23** | 1200 |

- Kvalitet: srednja i fina izjednacene (rasponi se gotovo potpuno preklapaju).
- Brzina: sve tri se preklapaju — nema razlike.
- **Odlucuje treci pokazatelj koji se pojavio sam: SIRINA raspona (pouzdanost).**
  Najpouzdanija je SREDINA — ni najgrublja, ni najfinija.
- Objasnjenje (materijal za stranicu): premalo pregrada gura razlicite situacije
  u istu pregradu, pa ishod zavisi od srece; previse pregrada raspe 12.000
  epizoda na previse mesta, pa se tabela ne stigne popuniti. Prokletstvo
  dimenzionalnosti u obliku koji se vidi golim okom.
- **ODLUKA za `rl2`: srednja (4.000) kao podrazumevana**, gruba i fina kao dva
  izbora koji pokazuju sta se gubi u svakom smeru.
- Postena ispravka: Claude je u koraku 1 tvrdio da rezultat protivreci zatecenim
  krivama iz s18. Sa pravim protivnikom NE protivreci — one su favorizovale
  4.000 i to se potvrdilo. Pogresno je bilo njihovo OBRAZLOZENJE (da 4.000 uci
  brze i dostize vise), ne zakljucak.
- Napomena o poredjenju: 72.000 iz starog Ponga NIJE reproducibilno u ovom
  setupu — ta cifra ukljucuje dimenziju protivnickog reketa (x6), a ovde je
  agent protiv jednog protivnika bez te dimenzije. Fina varijanta je 12.000.

### Hardverska ogranicenja klijenta (Flaviovo pitanje) + samostimovanje
Pitanje: testiramo Pythonom na serveru, izvrsavamo JS na klijentu — da li je
hardver ogranicavajuci faktor i koji je minimum?

- **Sta se prenosi:** broj epizoda do ucenja i visina platoa su svojstva
  algoritma — identicni u oba jezika. Ne prenosi se samo brzina, i to u nasu
  korist (JS sa `Float32Array` je visestruko brzi od CPythona na ovoj petlji).
- **Memorija Q-tabele** (stanja x 3 akcije x 4 bajta): 300 -> 3,6 KB;
  4.000 -> 48 KB; 12.000 -> 144 KB; 72.000 -> 864 KB. Trivijalno na svakom
  uredjaju. Jedina istorijski stvarna granica bio je `localStorage` (~5 MB) i to
  tek sa 7 agenata odjednom (stari Pong, reseno sparse zapisom).
- **Racunanje** (~5M koraka za 12.000 epizoda): PC 1-2 s; telefon/tablet srednje
  klase 4-7 s; telefon iz ~2017 10-17 s. **Vazi samo bez crtanja** — uz render
  po koraku tavanica je 60 fps, tj. preko 20 sati.
- **Pravi rizik nije snaga nego FIKSAN paket.** Paket od 50 epizoda po
  `requestAnimationFrame` koji na PC-u traje 3 ms, na starijem telefonu traje
  150 ms: animacija trza, dugmad ne reaguju, posetilac zakljuci da je stranica
  pukla. Uredjaj je sposoban, samo je pogresno odmeren.
- **Resenje: adaptivni paket** — meri trajanje prethodnog paketa, podesi sledeci
  da ostane ispod ~8 ms. Stranica se sama stimuje prema uredjaju.
- **Flaviov uslov (prihvacen): samostimovanje MORA biti dokumentovano** na
  stranici ili u infoboxu. Nedokumentovana adaptacija je tacno ona crna kutija
  protiv koje je ceo X-Ray stav. Zato `rl2` dobija infobox "Brzina uredjaja" sa
  izmerenim koraka/s — adaptacija postaje sadrzaj, ne skrivena mehanika.
- **Minimum hardvera:** bilo koji uredjaj sa browserom od ~2015 (`Float32Array`,
  Canvas, ES2015). Pravi ogranicavajuci faktor je strpljenje posetioca.
- Dogovoreno: mali JS benchmark koji Flavio pusti na PC/tablet/telefon, pa
  umesto procene imamo tri stvarna broja — i taj broj ostaje u telemetriji.

### Raspored stranice `rl2` — dogovoren
**Opseg (pedagoska granularnost).** "Q-learning" nije jedan pojam nego cetiri.
Podela: `rl2` = STANJE (kako agent vidi svet), `rl3` = UCENJE (Bellman,
Q-tabela), `rl4` = EKSPLORACIJA. Za `rl2` govori i to sto merenje vec ima
materijal, ukljucujuci kontraintuitivan nalaz o pouzdanosti.

**Protivnik:** random walker sa `rl1` (kontinuitet — posetilac ga vec zna kao
nultu tacku).

**Trening uzivo**, ne pripremljeni rezultati — racunica pokazuje da je izvodljivo.

**Wireframe je bio POGRESAN i ispravljen tek proverom koda.** Claude je skicirao
jednu kolonu sa objasnjenjem na dnu; `rl1` zapravo ima `#xray-layout` =
`grid-template-columns: 1fr 280px` sa `<aside class="xray-side">` za infoboxove.
Objasnjenja idu SA STRANE, ne ispod — pa vertikalni budzet glavne kolone ostaje
slobodan. (Uzgred nadjeno: CSS se zove `xpong.css`, ne `style.css`.)

**Dogovoren raspored:**
- Glavna kolona: naslov -> semafor -> teren sa mrezom stanja -> deck (levo agent
  koji uci, centar Treniraj/Reset, desno walker) -> kontrola grubosti -> grafikon
  -> tri pokazatelja.
- Desna kolona (280px): infoboxi, ukljucujuci nov "Brzina uredjaja".
- **Grafikon mora nositi `max-width: min(100%, 72vh)`** kao canvas i deck, inace
  strci u odnosu na teren iznad (poravnanje iz s18).
- **Jedan grafikon nosi DVA pokazatelja:** prvo pokretanje crta jednu krivu
  (kvalitet); svako sledece DODAJE krivu preko prethodnih, ne brise je. Posle pet
  pokretanja razmak unutar snopa JESTE pouzdanost. Isti prostor, tri ocitavanja,
  bez ijednog kompozitnog broja.
- Pedagoska posledica: nalaz o lutriji posetilac ne procita nego DOZIVI. Dugme
  posle prvog treninga menja natpis da poziva na ponavljanje — ponavljanje je
  jedini put do treceg pokazatelja.
- **Grubost: tri imenovane vrednosti, ne klizac** — jedini parametar u rukama
  posetioca. Pritisak vidljivo prekraja mrezu preko terena.
- **Auto-scroll do grafikona** na pocetku treninga: grafikon pada ispod pregiba
  (teren ~405 px + zaglavlje + semafor + deck), a trening je headless pa teren
  miruje. Odbacene alternative: zamena terena grafikonom (nestabilan raspored) i
  status quo (posetilac ne vidi da se nesto desava).
- Jedini element bez postojeceg obrasca je kontrola grubosti (svi postojeci
  prekidaci su on/off, ovde su tri vrednosti).

## Lekcije / ledger
- **Nepoznat fajl u sandboxu sa poklapajucim timestampom je SOPSTVENI rad
  izgubljen iz konteksta, nikad tudji.** Sandbox je izolovan; Flavio ne radi
  paralelno. Odbrana: `SANDBOX_LOG.md` + header u skripti. (Ispravlja pogresnu
  stavku iz s18.)
- **Uredni brojevi nisu dokaz da se meri prava stvar.** Pokazatelj "epizode do
  praga" bio je konfundiran sa epsilon rasporedom; nijedan assert nije pao.
  Kategorija greske koju protokol NE hvata (nastavak lekcije iz s18 o
  propustenim boljim idejama).
- **Merenje mora biti u svetu koji korisnik gleda.** Protiv zida i protiv walkera
  daju RAZLICIT poredak varijanti. Brojevi iz pogresnog setupa izgledaju
  jednako uverljivo.
- **Varijansa izmedju seedova je pokazatelj, ne sum.** Sa 1 seedom razlika se ne
  razlikuje od srece; sa 5 se vidi da je najstabilnija sredina. Odluku je doneo
  bas taj treci pokazatelj koji nismo trazili.
- **Dva parametra = dva pokazatelja** (Flaviov princip, usvojen kao pravilo):
  nikad kompozitni broj koji ih sakriva. Ako se fizicki ne mogu prikazati
  zajedno, izbor mora biti imenovan i vidljiv na UI, ne implicitan.
- **Skica koja nije proverena protiv koda je izmisljotina.** Wireframe je
  pretpostavio strukturu koje nema; greska se videla tek citanjem `rl1.html`.
  Flaviov princip "dok ne vidim nisam siguran" je uhvatio gresku.
- **Nedokumentovana adaptacija je crna kutija.** Samostimovanje se objavljuje.

## Zavrsno stanje
- **Nijedan web fajl nije menjan** — `app.js`, `xpong.css`, sve stranice
  netaknute. Web repo (xpongweb) ostaje na `28830e8` (s18).
- **XP_VERSION NIJE bumpovan, namerno.** Verzija u footeru je cache-dijagnostika;
  bez ijedne izmene na sajtu bump bi lazno signalizirao da ima sta da se osvezi.
  Ostaje `s18` (25 Jul 2026). Odluku doneo Claude bez Flaviove kontrole (Flavio
  udaljen od racunara) — podlozna preinacenju.
- Docs repo: `session_18.md` (dopisana ispravka), `session_19.md` (nov),
  `README.md` (azuriran).
- Sandbox (nije deo repoa, resetuje se): `SANDBOX_LOG.md`, `qspace_bench.py`,
  `qspace_run.py`, `qspace_run2.py`, `qspace_run3.py`, `curves_*.json`,
  `eval_*.json`, `walker_*.json`.

## Sledece (s20)
- **Implementacija `rl2`** po dogovorenom rasporedu. Prvi korak: kontrola
  grubosti (jedini element bez postojeceg obrasca), pa mreza stanja preko terena.
- JS benchmark koraka/s — Flavio pusti na PC/tablet/telefon, broj ide u infobox
  "Brzina uredjaja" i u adaptivni paket.
- Nasledjeno: naslovi ("otom potom"); README PAZNJA -> dopisati escape recept;
  (kandidat) sr.lat aditivno; KC iz About eseja.
