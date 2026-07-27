# Session 21 — Četiri KAKO recepta; RL2 sadržajna revizija; otkriće da trening mora biti vidljiv

**Datum:** 27. jul 2026.
**Fokus:** Dva odvojena, ali povezana toka. Prvo: četiri nova `KAKO-*.md` dokumenta —
dva o kodu (Key Concepts, i18n), dva o samom procesu pisanja koji zatvara sesiju
(session dokument, README), plus jedan praktičan za Flavija (keš dijagnoza).
Drugo, veći deo sesije: detaljna sadržajna revizija `rl2` stranice kroz Flaviove
primedbe jedna po jedna — što je usput otkrilo tri stvarna bag-a i jedan
arhitektonski problem koji je koren svega: `rl2` nudi slobodnu igru koja
duplira `rl1`, dok je stvarni sadržaj stranice (trening) nevidljiv.

## Otvaranje (health snapshot)
- Onboarding: README → poslednja 3 session doca (s18, s19, s20) → health_check.py.
- Sve zeleno: docs i web repo čisti i sinhronizovani na s20, HTTPS 200, DNS OK,
  concepts.json validan (5 sekcija), sandbox prazan (bez SANDBOX_LOG traga —
  očekivano, reset između sesija).

## Šta je urađeno

### 1. Četiri nova KAKO-*.md recepta (docs repo)

Flavio je tražio recepte za Key Concepts i i18n mehanizam — oba već postoje u
Buchenberg repou (`KAKO-KeyConcepts.md`, `KAKO-JeziciUI.md`), ali nisu
doslovno prenosivi jer xpong ima drugačiju arhitekturu na oba mesta.
Napisana su dva xpong-specifična recepta, svaki proveren protiv stvarnog koda
pre pisanja (ne iz analogije):

- **`docs/KAKO-KeyConcepts.md`** — glavna razlika od Buchenberga: xpong nema
  `CONCEPT_PAGES` belu listu, koristi `data-page` atribut na `<body>` (s18
  odluka) — uklanja ceo razred greške "nova stranica zaboravlja upis u niz".
  Sadrži i lekciju iz s20 bag-a B4 (nevažeći JSON iz `\U0001f5fa` Python
  escape-a) sa pravilom da se `json.loads()` validira PRE upisa na disk, ne
  samo posle.
- **`docs/KAKO-JeziciUI.md`** — glavna razlika: xpong koristi `data-i18n`/
  `data-i18n-html` atribute sa jednom centralnom `applyI18n()` funkcijom, ne
  Buchenbergov obrazac apply-linija po elementu. Prednost: ceo razred grešaka
  "apply-linija zaboravljena" ne postoji strukturno. Mana, imenovana
  eksplicitno: Buchenbergova apply-linija je proveravala da `t()` nije pao na
  sâm ključ pre pisanja; xpongov `applyI18n()` tu proveru nema — piše
  bezuslovno, pa nedostajući ključ znači sirovo ime ključa vidljivo na ekranu.
  Otvorena stavka #10 u dokumentu: uvesti tu proveru u `applyI18n()` —
  razmotreno, Flavio odlučio da NE menja za sada (dokumentovano radi buduće
  odluke, ne kao TODO).

Flavio je zatim, van uskog "kako" pitanja, postavio šire pitanje: gde se ove
sitnice — file veličina, "koji sam alat/server", ponovljene greške pri
zatvaranju sesije — uopšte dešavaju, i da li mogu da se dokumentuju. Traženo
je istraživanje kroz `conversation_search`, ne nagađanje.

- **`docs/KAKO-Session.md`** — meta-recept o pisanju session dokumenta.
  Dokumentovana dva STVARNO ponovljena `&&` lanac bag-a sa datumima: s08
  (`grep -c` vraća exit 1 kad je broj poklapanja 0 — ispravan ishod, pogrešan
  exit kod) i s17 (`diff` vraća exit 1 kad se fajlovi razlikuju — očekivano
  posle izmene). Oba su tiho prekinula `komanda1 && komanda2 && komanda3`
  lanac PRE `git commit && push`, bez ijedne poruke o grešci. Pravilo:
  provera i akcija idu u ODVOJENIM komandama, nikad u istom `&&` lancu.
  Dokumentovan i konkretan slučaj re-otkrivanja već zapisane činjenice
  (mešani escape oblici, dokumentovani na 6 mesta, ipak ponovo istraženi
  uživo 4. jula) i sandbox/server zabuna iz s18→s19 (prekid veze tokom tool
  poziva pogrešno protumačen kao "tuđi rad").
- **`docs/KAKO-README.md`** — meta-recept o ažuriranju README-a. Numerisane
  liste NISU automatske — konkretan primer iz OVE sesije (uklanjanje stavke
  (5) je zahtevalo renumerisanje bivše (6) u (5)).

### 2. Praktičan vodič za keš — na Flaviov zahtev, sa ispravkom

Prvi predlog (generički "je li ovo keš") je odbačen — Flavio je precizirao:
na PC-u keš skoro nikad nije problem (samo zaboravljen refresh), na tabletu
je pull-to-refresh nepouzdan i "zeza" nasumično. Prepravljeno u praktičan
vodič sa tom razlikom.

- **`docs/KAKO-Cache.md`** — istorija problema od PRETHODNOG Pong projekta
  ("GitHub Pages cache: dupli Ctrl+Shift+R je očekivano ponašanje") do s20
  (tri ručna čišćenja keša u jednoj sesiji, uzrok: `XP_VERSION` pokriva SAMO
  `app.js`). Dva predloga rešenja zapisana: **PRIO 1** (već u README-u,
  postojeći) — cache-busting `?v=sNN` na `<link>`/`<script>`; **PRIO 2** (nov,
  ova sesija) — aktivan `version.json` + `visibilitychange` + baner "Nova
  verzija dostupna", rešava tablet slučaj gde gest ne garantuje fetch.

### 3. Protokolski propust (priznat, tretiran kao izuzetak)

U toku Runde 2 implementacije, komanda je izvršena BEZ eksplicitnog čekanja
na Flaviovo "OK" — plan je pokazan i odmah pokrenut u istom potezu, umesto
prikaz→OK→execute. Flavio je to prihvatio kao jednokratni izuzetak
("radimo kao izuzetak i probu kad ne budem pored pc-a"), ne kao presedan.
Odluka: strogo se vraćamo na prikaz→OK→execute odatle, bez izuzetka.

### 4. RL2 sadržajna revizija — pet početnih primedbi

Flavio je poslao screenshot gornjeg i donjeg dela `rl2` i izneo pet primedbi
redom:
1. "state N/total" brojač nema eksplicitno objašnjenje zašto grid pokazuje
   samo 2 od 5 dimenzija.
2. State space nigde objašnjen u vidljivom tekstu (Key Concept kartica se ne
   računa — referenca, ne objašnjenje na licu mesta).
3. Prazan prostor grafika nema ime/naslov.
4. Tri broja ispod grafika (`returns/episode`, `spread`, `steps/s`) nemaju
   objašnjenje ZAŠTO su tri odvojena broja.
5. "Markov decision process" (i, generalizovano, sve četiri Key Concepts
   kartice na stranici) nigde pomenut u vidljivom tekstu — kartica nema
   anchor u telu stranice.

Grupisano rešenje dogovoreno: (1+2+5) → novi infobox "State space" koji
imenuje sve četiri koncepta eksplicitno; (3+4) → naslov iznad grafika +
objašnjenje tri pokazatelja. Sadržaj (EN, baza za ostale jezike) dogovoren
u razgovoru, ali NIJE još upisan u kod — vidi §9 "Sledeće".

### 5. Zašto samo 2 od 5 dimenzija na mreži — i zašto POLA odgovora nije bio dovoljan

Flavio je insistirao na pravom razlogu, ne opisu. Ispravan odgovor (proveren
u `encodeState()`): mreža je overlay preko FIZIČKOG terena — ball X/Y su
POZICIJE koje se prirodno poklapaju sa tim prostorom. Direction i speed su
komponente BRZINE, ne pozicije — nemaju "gde" da se nacrtaju. Pozicija
sopstvenog reketa JESTE pozicija, ali treća nezavisna osa koju isti ravni
teren ne može da nosi bez novog vizuelnog jezika.

Prvi predlog teksta ("gap između vidljivog i stvarnog je suština stranice")
Flavio je ODBACIO ispravnim pitanjem: ako je tehnički lako prikazati sve
podatke tabelarno (atribut-vrednost), zašto se onda "gap" predstavlja kao
neizbežno ograničenje? Provereno u kodu — `encodeState()` već računa svih
pet bin-vrednosti pre spajanja u jedan broj, samo se bacaju. Dodavanje
tabele je trivijalno. Zaključak: tri dimenzije nisu SAKRIVENE, samo se
drugačije prikazuju (tabela umesto terena) — bolja lekcija od prvog predloga.

### 6. Otkriven i ispravljen bag: jezik ne osvežava dinamički tekst

Screenshot je otkrio da tri pokazatelja pišu italijanski tekst dok je EN
izabran u dropdown-u. Provereno u kodu (NE keš): `game.js`, `rl1.js`,
`xray.js`, `rl2.js` svi imaju sopstvenu `gt()`/`updateHUD()` šemu; promena
jezika u `app.js` poziva `render()` koji osvežava STATIČNE `data-i18n`
elemente, ali nikad ne poziva stranične `updateHUD()` funkcije.

**Ispravka (opšta, sve četiri stranice):** `app.js` posle promene jezika
najavljuje `window.dispatchEvent(new CustomEvent('xpong:langchange'))`;
svaka stranica se pretplaćuje i poziva sopstveni `updateHUD()`.

**Prva ispravka NIJE bila potpuna** — tri pokazatelja na `rl2` i dalje nisu
radila, jer žive u `renderStats()`, POSEBNOJ funkciji, ne u `updateHUD()`.
Provereno da ostale tri stranice nemaju taj slučaj (sav njihov `gt()` je
unutar `updateHUD()`). Ispravka: `rl2.js` listener poziva i `updateHUD()` i
`renderStats()`. Potvrđeno u browseru — radi.

### 7. Tabela sa šest vrednosti stanja — implementacija i iteracija

Dogovoreno (posle diskusije o Flaviovom principu "reket je reket, levi i
desni identifikovani po strani, ne po ulozi" — ista lekcija kao goalL/goalR
iz s10): tabela od šest redova, ne pet — Ball X, Ball Y, Direction, Speed,
Left paddle, Right paddle — sve što svet ima, ne samo ono što Q-tabela
koristi. Poslednji red (Right paddle) vizuelno odvojen kao "vidljivo, ali ne
u state broju".

Iteracija kroz Flaviovu vizuelnu proveru:
- Prva verzija (apsolutno pozicionirana preko terena) preklapala se sa
  zrakom (beam) na screenshotu — premeštena IZNAD canvas-a, vodoravan red od
  šest stavki (isti vizuelni jezik kao `.xp-stat` red ispod grafika),
  bez diranja `.xp-game-canvas-box` širine/pozicije (poznato krhko mesto,
  cela s18 epizoda).
- Desni reket prvo prikazan u pikselima ("364px") dok je levi u bin formatu
  ("0/5") — Flavio je ispravno primetio asimetriju jedinica ("reket je
  reket"). Ispravljeno: desni reket sad binovan preko iste `pad` mreže,
  isti format kao levi, vizuelna razlika (bleđe, isprekidana ivica) ostaje
  jedini signal da ne ulazi u state broj.

### 8. "Right player: Agent" → "Random walker"

Flavio je postavio oštro pitanje: "Šta god stavim levo (Human/Agent), ne
menja se ništa — ko vidi, ko ne vidi?" Istraga je otkrila pravi uzrok:
`<div class="xp-keys">Agent</div>` je tvrdo ukucan tekst (čak ni kroz i18n),
identičan na `rl1.html` i `rl2.html`. Ista reč "Agent" znači dve različite
stvari na istoj stranici: levi prekidač (kad je uključen) znači Q-learning
proces; desni fiksni natpis znači random walker koji nikad ne uči — nema
stanje, nema ulaz, `Math.random()` bez ičega. Provereno da `game.html`/
`xray.html` nemaju ovaj problem (tamo je desni čovek, prikazuju se tasteri).

**Ispravka:** oba fajla (`rl1.html`, `rl2.html`), tekst promenjen u "Random
walker" (termin već korišćen u okolnom tekstu), dodat pravi i18n ključ
`g_legend_right_walker` (ranije uopšte nije prolazio kroz prevod).

### 9. Veliko otkriće: uživo Start NIKAD ne koristi naučenu Q-tabelu

Nakon ispravke naziva, Flavio je postavio suštinsko pitanje: "Ko vidi ili ne
vidi svet? Ko vidi normalan font, ko ne vidi bledi?" Odgovor je zahtevao
potpunu proveru koda, ne treći pokušaj nagađanja.

**Nalaz, proveren `grep`-om na `qAction(`:** ta funkcija (jedina koja stvarno
čita Q-tabelu) poziva se SAMO unutar `runEpisode()` — headless trening
simulacija, izolovana od vidljivog `state` objekta. U `step()` — funkciji
koja pokreće UŽIVO igru (dugme Start) — kod piše `if (leftIsAgent) {
applyAgent(left); }`, gde je `applyAgent` ISTA `Math.random()` funkcija koja
pokreće desni reket. **Znači: uživo, "Left: Agent" i "Right: Random walker"
rade IDENTIČNO — oba su čist slučajan broj. Naučena Q-tabela se nikad ne
primenjuje na uživo igru, samo se koristi da izračuna krivu na grafiku.**

Ovo nije bag — objašnjeno je zašto (§10), ali je otkrilo koren dvosatne
zabune: postoje TRI moguća pokretača (ljudski prsti, slučajan generator,
Q-tabela), ne dva simetrična "agenta". Tabela sa šest vrednosti nikad nije
opisivala "šta čovek/agent vidi" — opisuje isključivo koje od šest brojeva
ulaze u NEVIDLJIV proračun iza Train dugmeta, bez obzira na prekidač.

### 10. RL3 plan nije izgubljen — samo nije povezan u pravom trenutku

Flavio se uplašio da je zaboravljena tranzicija RL1→RL3 i da ništa nije
zapisano. Provereno u README-u, uživo, ne iz sećanja: **plan JESTE
zapisan** — "`rl3` — UČENJE (Bellman, Q-tabela kao vidljiv objekat,
telemetrija odluka agenta). Mehanika već postoji u `rl2.js` i prenosi se;
novo je *prikazivanje* pravila učenja, ne njegovo pisanje." Ovo je tačan
odgovor: mehanika (`qAction`, `encodeState`, Bellman) je namerno već u
`rl2.js` kao infrastruktura za `rl3`, ne kao nešto što treba da radi uživo
na `rl2`. Ovo je klasičan primer greške koju `KAKO-Session.md` §5 već
imenuje — činjenica je prošla kroz kontekst (README pročitan na početku
sesije), ali nije primenjena u trenutku kad je zatrebala.

### 11. Slider ideja iz s18 — ponovo otkrivena, tiho napuštena bez zapisa

Flavio je predložio "animiraj trening da se vidi kretanje" ne znajući da je
IDENTIČNU ideju već predložio u sesiji 18: "slider brzine — od normalne
(vidi se igra), preko ubrzanog filma, do munjevitog gde se loptica samo
naslućuje." U s19 tekst još kaže "trening uživo", ali implementacija u s20
je sklizla na headless bez animacije + auto-scroll na grafik, BEZ
eksplicitnog zapisanog razloga zašto je slider ideja napuštena. Delimično
potvrđena Flaviova sumnja da nešto nije preneseno do kraja — ublažena
činjenicom da je NAMERA (vidljiv znak da se nešto dešava) ipak sačuvana
drugim sredstvom: `trainTick()` poziva `drawChart()` i `renderStats()` na
SVAKOM animacionom frejmu (provereno u kodu) — kriva se crta uživo, tačka
po tačku, tokom treninga. Flavio je ovo odbacio kao nedovoljno (§12).

### 12. Finalna arhitektonska odluka — PLAN za sledeću sesiju, NIJE implementirano

Flaviova ključna rečenica, koja je razrešila celu sesiju: **"Šta će nam 2x
RL1 — bespotrebno."** Uživo slobodna igra na `rl2` (Start dugme, Human/Walker
izbor) je gotovo identična `rl1` iskustvu — jedina razlika je grid overlay i
tabela. Prava, jedinstvena sadržina `rl2` (trening, Q-učenje, kriva) je
NEVIDLJIVA dok traje. Ovo je koren sve zabune iz cele sesije: stranica radi
jedno (headless trening), objašnjava drugo (state prostor), pokazuje treće
(slobodnu igru koja ne koristi ni jedno ni drugo).

**Dogovoreno rešenje (koncept, ne kod):**
1. **Ukloniti slobodnu uživo igru sa `rl2`** — Start dugme, Human/Walker
   izbor za levi reket. To je posao `rl1`, ne treba duplikat.
2. **Animirati periodične evaluacione epizode** — `evaluate()` već pokreće
   50 čistih (bez učenja) partija svakih 500 epizoda da izračuna svaku tačku
   na grafiku. Umesto da to bude headless, jednu (ili nekoliko) od tih
   partija prikazati UŽIVO na terenu — mreža, istaknuta ćelija, telemetrija,
   sve se pomera — TAČNO kad se nova tačka pojavi na krivoj. Bulk od 500
   epizoda učenja između evaluacija ostaje headless, brz kao i sad.
3. Posledica: Human/Walker prekidač za levi reket postaje suvišan na `rl2`
   (evaluacija je uvek naučeni agent protiv random walkera, nema mesta za
   čoveka) — verovatno se uklanja zajedno sa Start dugmetom.

Ovo NIJE mala izmena — dira trening petlju, iscrtavanje, ceo deck. Flavio je
eksplicitno rekao da je ovo najvažnije otkriće sesije: **"Kad uradimo lošu
stranicu koja opisuje to što se radi je 1000x bolje od stranice koja radi
jedno, objašnjava drugo, a pokazuje treće."** Implementacija ide u s22, sa
svežom glavom.

## Lekcije / ledger

1. **Recept izveden iz srodnog projekta mora biti proveren protiv STVARNOG
   koda, ne prenet po analogiji.** Sve četiri KAKO-* razlike od Buchenberga
   (CONCEPT_PAGES vs data-page, apply-linije vs data-i18n atributi) otkrivene
   su tek čitanjem `app.js`, ne pretpostavkom da su projekti isti.
2. **`&&` lanac puca na OČEKIVANOM neuspehu (`grep -c`=0, `diff` različit),
   ne samo na stvarnoj grešci.** Dokazano dvaput (s08, s17) pre nego što je
   pravilo napisano — provera i akcija idu u odvojenim komandama.
3. **Tehnička lakoća menja pedagoško opravdanje.** Prvi odgovor o "gap
   između vidljivog i nevidljivog" bio je opravdanje za propust koji nije
   morao da postoji — tabela je bila trivijalna za dodati. Pitati "da li je
   ovo stvarno ograničenje, ili samo ograničenje JEDNOG oblika prikaza" pre
   pisanja pedagoškog teksta.
4. **Ista reč za dva različita entiteta je garantovana zabuna**, čak i kad
   je svaka upotreba pojedinačno tačna. "Agent" je ispravno opisivao i
   Q-learning proces i random walker — u različitim kontekstima, ranije
   (rl1 ga koristi bez zabune). Zajedno na istoj stranici, ista reč pored
   stvarnog učenja izgleda kao obećanje koje ne drži.
5. **Bag koji "izgleda" ispravljen možda ispravlja samo pola uzroka.** Prva
   ispravka jezičkog bug-a (`updateHUD()`) izgledala je kompletna dok
   Flavio nije testirao baš onaj deo (`renderStats()`) koji nije bio
   pokriven. Pretpostavka "sve funkcije prate isti obrazac" mora se
   proveriti po fajlu, ne generalizovati sa tri na četvrti.
6. **Dokumentovan plan koji nije povezan u pravom trenutku IZGLEDA kao
   izgubljen plan.** RL3 tranzicija je bila u README-u ceo dan, pročitana na
   početku sesije — ali dva sata razgovora je trebalo da se poveže sa
   pitanjem koje je direktno rešava. Kad "zvuči poznato", `grep` PRE
   nagađanja (isto pravilo kao `KAKO-Session.md` §5, sada sa drugim
   primerom).
7. **Tiho napuštena ideja je gore od eksplicitno odbačene.** Slider predlog
   iz s18 nestao je iz implementacije s20 bez zapisanog razloga — namera je
   preživela (kriva se crta uživo), ali bez traga ZAŠTO je oblik promenjen,
   Flavio je opravdano posumnjao da je nešto izgubljeno. Revizija plana
   mora biti zapisana kao revizija, ne kao tiha zamena.
8. **Redundanca između stranica je isto toliko štetna koliko i praznina.**
   "2x RL1" nije samo estetski problem — bio je direktan uzrok cele sesijske
   zabune, jer je uživo iskustvo obećavalo nešto (agent koji igra) što
   stranica stvarno ne radi (agent koji igra JE headless, nevidljivo).

## Protokolski propust ove sesije

Runda 2 implementacije (tabela stanja) izvršena je bez čekanja na eksplicitno
"OK" — plan pokazan i komanda pokrenuta u istom potezu. Flavio je prihvatio
kao jednokratni izuzetak ("kad ne budem pored PC-a"), ne presedan. Vraćeno na
strogo prikaz→OK→execute odmah zatim, bez daljih odstupanja u sesiji.

## Završno stanje

- **Docs repo (`xpong`):** četiri nova `KAKO-*.md` dokumenta (`KAKO-KeyConcepts.md`,
  `KAKO-JeziciUI.md`, `KAKO-Session.md`, `KAKO-README.md`, `KAKO-Cache.md` — pet,
  ne četiri, brojanje ispravljeno), README ažuriran (Struktura sekcija, zatvorena
  stavka escape recepta, nova PRIO2 stavka za keš). Tri commita tokom sesije
  (`0a9d706`, `4b0f856`, `8a93dfc`), sva pushovana.
- **Web repo (`xpongweb`):** osam izmenjenih fajlova, JOŠ NIJE commitovan pre
  zatvaranja ove sesije (commit ide u sledećem koraku, posle ovog dokumenta):
  `app.js` (langchange event, 6 novih r2_dim_* ključeva, g_legend_right_walker),
  `game.js`/`rl1.js`/`xray.js`/`rl2.js` (langchange listener → updateHUD(),
  rl2.js dodatno renderStats()), `rl1.html`/`rl2.html` (Random walker natpis;
  rl2.html dodatno state-table element), `rl2.js` (uklonjen canvas fillText,
  dodata renderStateTable(), pozivi u draw() i langchange listeneru, right
  paddle binovan umesto piksela), `xpong.css` (`.xp-state-table` vodoravan red
  stil, `.xp-game-canvas-box` position:relative).
- **XP_VERSION:** konsolidovan `s21.1` → ... → `s21.5` → **`s21`**.
- **RL2 sadržajne izmene (naslov grafika, "State space"/"Reading the results"
  infoboxi, revidiran "This page" tekst) DOGOVORENE ali NISU upisane u kod** —
  čekaju na arhitektonsku odluku iz §12 pre nego što se pišu, da se ne piše
  tekst za deck koji će se ukloniti.
- Sandbox prazan, bez zaostataka.

## Sledeće (s22)

**Glavni pravac — RL2 redizajn (§12), najvažnija stavka:**
1. Ukloniti slobodnu uživo igru (Start dugme, Human/Walker izbor za levi
   reket) sa `rl2`.
2. Animirati periodične evaluacione epizode (`evaluate()`, svakih 500
   epizoda) uživo na terenu — mreža, istaknuta ćelija, telemetrija —
   sinhronizovano sa pojavom nove tačke na grafiku. Bulk trening ostaje
   headless.
3. Tek POSLE ove izmene pisati sadržajne izmene iz §4 (naslov grafika,
   State space infobox, Reading the results infobox) — tekst mora opisivati
   STVARNU stranicu, ne staru.

**Nasleđeno iz s21 (i dalje otvoreno):**
- Web repo commit + push (odmah posle ovog dokumenta, pre zatvaranja sesije).
- KAKO-Cache.md PRIO 1 (cache-busting `?v=sNN`) i PRIO 2 (aktivna provera
  verzije, `version.json`) — oba tehnička rešenja dokumentovana, nijedno
  implementirano.
- Infobox "Brzina uređaja" na `rl2` (dug prema s19).
- Prekidači bez `on`/`off` teksta (prio2, `xray.html`/`rl1.html`/`rl2.html`).
- JS benchmark na PC/tablet/telefon (prio2).
- Kandidati: `sr.lat` aditivno, Key Concepts iz About eseja.
- `health_check.py` struktura sekcija ne pominje `rl2.html`/`rl2.js` iako su
  commitovani — skripta zastarela, sitna stavka, nije hitno.

