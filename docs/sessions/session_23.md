# Session 23 — RL3 planiranje: naslov, opseg, i localStorage arhitektura

**Datum:** 29. jul 2026.
**Fokus:** Cela sesija je planiranje i arhitektura za `rl3`, bez ijedne
izmene koda. Krenulo se od skiciranja sadržaja stranice, prešlo kroz
verifikaciju u kodu koja je ispravila pogrešnu raniju pretpostavku, pa u
seriju Flaviovih pitanja koja su otkrila da xpong nema mehanizam da prenese
naučeno između stranica — što je vodilo u odluku da se uvede `localStorage`
perzistencija, sa jasnim principom (Flaviova formulacija) o tome gde se
podaci generišu i kako se koriste na drugim mestima.

## Otvaranje (health snapshot)

- Onboarding: README → poslednja tri session doca (s20, s21, s22) →
  `health_check.py`.
- Sve zeleno: docs i web repo sinhronizovani na s22, HTTPS 200,
  concepts.json validan (6 sekcija).

## Šta je urađeno

### 1. Podsećanje na plan za rl3, i KAKO dokumenti

Flavio je tražio kratak pregled šta je već zapisano za `rl3` (Bellman,
Q-tabela kao vidljiv objekat, telemetrija odluka) i podsetio na postojanje
`KAKO-*.md` recepata za slučaj zastoja. Ponovljeno iz README-a/s22: mehanika
se prenosi iz `rl2.js` skoro nepromenjena, novo je isključivo prikazivanje.

### 2. Naslov stranice odlučen

**"RL 3 — How the agent learns"** — paralelno sa rl1 ("Random walker") i
rl2 ("How the agent sees the world"), ista glagolska porodica naslova.
Levi/desni natpis ("Learning agent" / "Random walker") ostaju nepromenjeni.

### 3. Tri arhitektonske odluke potvrđene

Predložene i prihvaćene u jednom potezu:
- **Segmentirani prekidač grubosti (Coarse/Medium/Fine) se NE prenosi na
  `rl3`** — grid fiksiran na 4.000, bez izbora. Razlog: rl2 već objašnjava
  i odlučuje state space; rl3 ne treba da duplira taj izbor.
- **Beam/Heatmap prekidači OSTAJU** — porodični X-Ray sloj, ne dotiču
  Q-tabelu, ne prave konceptualnu zbrku.
- **Explore/exploit telemetrija — opcija (a), odbačena kao poseban
  mehanizam.** Live-eval je uvek greedy (eps=0), pa nema šta da se vidljivo
  istražuje tokom nje. Epsilon se pominje samo tekstualno u infoboksu
  ("training used epsilon-greedy, decaying from 1.0 to 0.05"), bez nove
  mehanike (odbačena alternativa: poseban headless "peek" sa eps>0).

### 4. Verifikacija u kodu ispravila raniju pretpostavku (Bellman ↔ live-eval)

Pre nego što se pisao ijedan red koda, `grep` kroz `rl2.js` je pokazao da
`qUpdate()` (pravi Bellman update) poziva se **isključivo** unutar
`runEpisode(g, true)` — headless bulk trening, na sopstvenom `st` objektu,
izolovano od vidljivog `state`. `liveStep()` (uživo evaluaciona epizoda)
poziva samo `qAction(si, false)` — čisto čitanje, bez ijednog `qUpdate`
poziva u celoj funkciji.

**Posledica:** raniji plan "sve troje (Bellman, Q-bar, telemetrija) se kači
na live-eval" bio je delimično pogrešan. Ispravljeno na dva odvojena
trenutka:
- **Q-bar panel** (UP/STAY/DOWN za trenutno stanje) → vezan za **live-eval**
  (čisto čitanje, tačno tu radi).
- **Bellman panel** (formula sa upisanim brojevima) → vezan za **headless
  bulk trening**, jer se tu update stvarno dešava — ali headless faza ne
  dodiruje canvas, pa je trebalo posebno rešenje (vidi §8).

### 5. Flaviova pitanja o RL2 ponašanju — provereno u kodu, ne pretpostavljeno

Serija preciznih pitanja ("da li Learning agent uči od tih epizoda", "da li
Random walker koristi trening podatke", "zašto lukavi potezi") razrešena
čitanjem koda, ne opisom:

- **Learning agent uči SAMO tokom headless bulk faze** (`qAction(si, true)`
  + `qUpdate()` posle svakog koraka). U `evaluate()` i `liveStep()` je
  uvek `qAction(si, false)` — greedy, bez `qUpdate` poziva, znači NE uči u
  tim trenucima, samo TESTIRA trenutnu tabelu.
- **Random walker ne uči nikad, nigde** — `agentAction()` ne prima `state`
  ni bilo koji podatak, čist `Math.random()`.
- **Flaviov subjektivni utisak da agent igra sve bolje je tačan i
  objašnjiv:** `Q` niz se pravi JEDNOM (`qReset()`, samo u `trainStart()`)
  i posle toga sve funkcije (`trainTick`, `evaluate`, `liveStep`) rade nad
  ISTIM nizom — nikad se ne pravi ponovo niti briše u međuvremenu.
  Akumulacija kroz treninge je stvarna, ne utisak.
- **"Lukavi potezi" random walkera su čista slučajnost** — `applyAgent()`
  pomera reket ×2 brže od očekivanog ("wider random walk"), pa nasumično
  pokriva širi opseg terena; povremeno se nađe na pravom mestu čistom
  verovatnoćom, bez ikakvog koda koji bi mu davao "sreću".

### 6. Da li trening sa rl2 prelazi u rl3 — ne, nema mehanizma

Provereno `grep`-om kroz `rl2.js`: nema nijednog `localStorage` poziva.
Q-tabela živi isključivo u JS promenljivama dok je stranica otvorena.
Zaključak: `rl3` mora sam da odradi ceo trening ciklus od nule — ista
mehanika (Train, headless bulk, evaluate, live-eval, grafikon) kao rl2,
jer ništa drugo ne postoji da se nasledi. Ovaj nalaz je kasnije doveo do
odluke iz §9–§13.

### 7. Pun grafikon sa krivama na rl3 — izbačen, ostaju tri broja

Flavio je posumnjao da je pun grafikon (poređenje više pokretanja, isto
kao rl2) suvišan kad već postoje Bellman i Q-bar paneli. Odlučeno:
**zadržati samo tri postojeća pokazatelja** (returns/episode, spread,
steps/s) **bez** punog grafikona sa krivama — poređenje više pokretanja je
posao rl2, ne treba se ponavljati (ista logika kao "2× RL1 bespotrebno"
iz s21).

### 8. Human vs Agent / Agent vs Agent — nije planirano za rl3, samo pomenuto ime rl4

Provereno `grep`-om kroz `docs/` i README: `rl4 = EKSPLORACIJA` postoji
SAMO kao ime, na dva mesta (s19, s22), bez ijednog detalja o sadržaju —
nema pomena slobodne igre, Human vs Agent, ni Agent vs Agent nigde.
Odgovoreno Flaviju: nije planirano ni za rl3 ni za rl4, otvoreno pitanje
bez odgovora, ne nešto zaboravljeno.

Dodatno provereno (na Flaviovo pitanje "da li iza rl4 ima još nešto
planirano"): nema M4/M5 milestone-a nigde u README-u. Jedini trag je
aspiraciona rečenica u uvodu README-a ("self-play, DQN, genetski
algoritmi, X-Ray overlay") koja opisuje identitet projekta pozajmljen od
starog Pong projekta, ali nikad razbijena na konkretan plan sa brojem
stranice. `rl4` je trenutno poslednja eksplicitno imenovana stavka.

### 9. Kako je stari Pong rešio trening — localStorage, jedna stranica, zajednički bazen

Na Flaviovo pitanje objašnjeno iz `PongPregledProjekta.md`: stari Pong je
bio JEDNA monolitna stranica (ne porodica kao xpong), sa `localStorage`
perzistencijom po agentu (imenovani `GEN_001` itd.), sparse encoding kad
je broj agenata narastao (~80% ušteda prostora), i Export/Import u
JSON/CSV. Tournament i Evolve su radili nad ZAJEDNIČKIM bazenom sačuvanih
agenata, dostupnim celom UI-ju sa iste stranice — nije bio pipeline
(korak 1 → korak 2), nego deljeno skladište.

### 10. Odluka: uvodimo localStorage — Flaviov princip za masovne podatke

Flavio je formulisao princip eksplicitno: **podaci se generišu na JEDNOM
mestu.** Ako se koriste na drugom mestu:
1. ako podaci ne postoje → ta stranica/regija je deaktivirana, sa linkom
   na stranicu gde se generišu;
2. ako podaci postoje ali ne odgovaraju (npr. pogrešna konfiguracija) →
   isto, deaktivirano + link.

Za masovne/trening podatke: INSERT, DELETE, APPEND treba da postoje, ali
**NE menjanje pojedinačnog sloga** — samo "from scratch" (insert/delete)
ili "append" (produžavanje). Ovo je novo, eksplicitno pravilo koje nije
ranije postojalo u projektu.

### 11. Sopstvena greška uhvaćena i ispravljena u istom razgovoru

Prvi predlog (pre nego što je Flavio jasno formulisao princip) uveo je
"Continue training" dugme NA `rl3` — što bi značilo da `rl3` sama radi
APPEND, tj. postaje DRUGO mesto generisanja. Kad je Flavio postavio pitanje
("zašto se sve ne uradi na rl2, zar to nije mesto gde se podaci
generišu?"), greška je prepoznata i eksplicitno priznata, ne prećutno
ispravljena: **rl3 dobija NULA dugmadi koja treniraju.** Sav INSERT/DELETE/
APPEND ostaje na rl2 (Train = insert, Reset = delete); rl3 je čist
potrošač.

### 12. Rešenje za Bellman panel bez kršenja principa

Flaviovo pitanje "da li su rl3 potrebni podaci kojih nema na rl2, i zašto"
razrešilo je otvoreno pitanje iz §4/§8: Bellman panel treba PRIMERE
konkretnih update-a, koje trenutni `rl2` kod prolazi hiljadama puta u
sekundi ali nigde ne pamti. Rešenje koje ne krši princip "jedno mesto
generisanja": `rl2` (jedino mesto gde se `qUpdate()` poziva) počinje da
**uzgredno hvata** po jedan primer update-a na svakih 500 epizoda (isti
ritam kao postojeći `evaluate()` checkpoint) i čuva taj mali log
(~24 stavke) kao deo istog zapisa. `rl3` samo čita taj log — ne generiše
ga.

### 13. Vidljivost zahtevana — nedokumentovana adaptacija je crna kutija

Flavio je eksplicitno tražio da posetilac VIDI da se nusprodukti generišu
na rl2 i koriste na rl3, ne samo da mehanizam tiho radi. Isti princip kao
`stepsPerSec` samoštimovanje iz s19 ("nedokumentovana adaptacija je crna
kutija"), sad primenjen na deljenje podataka između stranica:
- **rl2** dobija dopunu infoboksa: trening takođe čuva periodične snimke
  Q-update-a, koje koristi rl3.
- **rl3** dobija infobox koji eksplicitno kaže da podaci dolaze sa rl2, sa
  linkom, i da svaka promena (novi trening) mora ići tamo — rl3 nema
  sopstveno dugme za to.

### 14. Konačna shema skladišta (dogovorena, nije implementirana)

- **Ključ:** `xpong_qtable_4000` — vezan za veličinu grida (ne za
  stranicu), pošto rl2 i rl3 dele isti `encodeState()`. rl2 zadržava
  prekidač 300/4.000/12.000 kao i sad; samo trening na 4.000 (Medium)
  upisuje zapis koji rl3 čita.
- **Sadržaj:** Q-tabela (12.000×3 float, 48 KB — već izmereno u README-u,
  ne treba sparse encoding kao stari Pong koji je imao mnogo agenata),
  log od ~24 uhvaćena update-a (stanje, akcija, nagrada, stara/nova Q,
  jedan na svakih 500 epizoda), broj epizoda, vremenska oznaka.
- **Kad se piše:** SAMO kad trening kompletno završi
  (`trainEp >= TRAIN_EPISODES`) — ne usred treninga, ne na svaki
  checkpoint pojedinačno (append semantika je "ceo dodatni prolaz", ne
  "svaki korak").
- **Kad se briše:** Reset na rl2.
- **rl3 pri učitavanju:** proverava zapis. Ne postoji → deaktivirana
  regija (Bellman panel, Q-bar panel) + poruka + link na rl2. Postoji →
  prikazuje oba panela + tri broja (bez punog grafikona, §7).

## Lekcije / ledger

1. **Verifikacija u kodu ispravlja pogrešne pretpostavke i unutar
   planiranja, ne samo unutar debagovanja.** Pretpostavka "Bellman se kači
   na live-eval" delovala je razumno dok se nije proverilo da `qUpdate()`
   tamo nikad ne živi. Isti X-Ray refleks ("instrumentiraj, ne pogađaj")
   važi i pre pisanja koda, ne samo posle neočekivanog rezultata.
2. **Princip za masovne/deljene podatke (Flavio, ova sesija): generisanje
   na jednom mestu; potrošači ili čitaju ili su deaktivirani sa linkom;
   INSERT/DELETE/APPEND da, izmena pojedinačnog sloga ne.** Ovo je opšte
   pravilo, ne specifično za rl2/rl3 — vredi ga zadržati za svaku buduću
   stranicu koja deli podatke sa drugom (npr. rl4).
3. **Čak i kad je princip izrečen, prva primena može da ga prekrši.**
   Predlog "Continue training dugme na rl3" je nastao PRE nego što je
   princip bio eksplicitan, ali bi ga prekršio i posle — potvrđeno tek
   kad je Flavio direktno pitao "zašto ne sve na rl2". Vredi eksplicitno
   proveriti svaki predlog protiv već izrečenog principa, ne pretpostaviti
   usklađenost.
4. **"Nedokumentovana adaptacija je crna kutija" (s19) proteže se i na
   deljenje podataka između stranica**, ne samo na self-tuning mehaniku
   unutar jedne stranice — isti stav, novi domen primene.

## Završno stanje

- **Ništa implementirano u kodu ove sesije.** Web repo nepromenjen, i dalje
  na s22. Cela sesija je planiranje/arhitektura, potvrđena kroz Flaviova
  pitanja i verifikaciju u kodu, ne kroz pisanje.
- Naslov `rl3` odlučen: "RL 3 — How the agent learns".
- Kompletan arhitektonski plan za `localStorage` deljenje podataka između
  rl2 i rl3 dogovoren, uključujući redosled implementacije (§14, Sledeće).
- `rl4` opseg proveren — samo ime "EKSPLORACIJA", bez detalja. Nema
  M4/M5 plana potvrđeno grep-om kroz README.

## Sledeće (s24)

**Korak 1 — izmene na `rl2` (postojeća stranica, dirati pažljivo):**
1. Dodati `localStorage` upis u `xpong_qtable_4000` na kraju kompletnog
   treninga (Q-tabela + log od ~24 uhvaćena update-a, §14).
2. Reset briše taj zapis.
3. Dopuniti infobox tekstom da se ovi podaci generišu i koriste na rl3
   (×5 jezika).
4. **Testirati na rl2 PRE nego što se počne sa rl3** — ne graditi rl3 na
   nečemu što još ne postoji.

**Korak 2 — kreirati `rl3` (posle koraka 1, ne pre):**
1. Klonirati `rl2.html`/`rl2.js` u `rl3.html`/`rl3.js`, identitet: naslov
   "RL 3 — How the agent learns", `data-page="rl3"`, prefiks `r3_`.
2. Ukloniti segmentirani prekidač grubosti (fiksno 4.000, §3).
3. Zadržati beam/heatmap nepromenjeno (§3).
4. Ukloniti sve što trenira (Train dugme, headless bulk logiku,
   `trainTick`) — rl3 nema INSERT/APPEND (§11).
5. Dodati proveru `localStorage['xpong_qtable_4000']` pri učitavanju —
   deaktivirana regija + link na rl2 ako ne postoji (§14).
6. Dodati Bellman panel (prolazi kroz sačuvani log update-a) i Q-bar
   panel (live-eval, čisto čitanje Q-tabele, isti mehanizam kao rl2-ov
   live-eval).
7. Tri broja ispod, BEZ punog grafikona sa krivama (§7).
8. Infobox koji eksplicitno imenuje rl2 kao izvor podataka, sa linkom.
9. Key Concepts za rl3: kandidati Bellman equation, Q-value/Q-function,
   temporal difference learning — tačni pojmovi i Wikipedia slugovi nisu
   još provereni, uraditi po `KAKO-KeyConcepts.md` kad se dođe do te faze.

**Nasleđeno, i dalje otvoreno (nepromenjen prioritet):**
1. `r2_dim_ballx`/`r2_dim_bally`/`r2_dim_leftpad`/`r2_dim_rightpad` i dalje
   samo u EN bloku `app.js` (DE/IT/HR/SR tiho na engleskom).
2. Cache-busting `?v=sNN` na `<link>`/`<script>` (prio 1).
3. *(prio2)* Aktivna provera verzije (`version.json` + banner).
4. *(prio2)* Prekidači bez on/off teksta.
5. *(prio2)* JS benchmark PC/tablet/telefon.
6. Kandidati: `sr.lat` aditivno, Key Concepts iz About eseja.

---

*Flavio & Claude · xpong · session_23.md · 29. jul 2026.*
