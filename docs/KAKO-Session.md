# KAKO-Session.md — Kako se piše i zatvara sesijski dokument (session_NN.md) u xpongu

Meta-recept — ne o kodu xponga, nego o samom procesu pisanja koji zatvara
svaku sesiju. Sastavljen posle ponovljenih, imenovanih grešaka u tom procesu
(sesija 21, 27. jul 2026), na zahtev Flavija koji je primetio da se iste
sitnice ponavljaju nezavisno od broja odrađenih sesija.

**Nastalo:** sesija 21, 27. jul 2026.

---

## 1. Svrha i mesto

Session dokument je **hronološki, nepromenljiv trag** onog što se desilo i
zašto — piše se na kraju SVAKE sesije, jednom, i posle se ne prepisuje (za
razliku od README-a, koji se prepisuje). Odgovara na pitanje "kako smo došli
dovde". Detaljno obrazloženje u METHOD §4 (project knowledge).

## 2. Mehanika pisanja — prag veličine

Session dokumenti u xpongu su odavno prerasli veličinu koja staje u jedan
bezbedan heredoc upis. Stvarni brojevi (27. jul 2026):

| Fajl | Veličina |
|---|---|
| session_18.md | 9.742 znakova |
| session_19.md | 11.988 znakova |
| session_20.md | 11.618 znakova |

Prag posle kog heredoc upis treba deliti na blokove je **~3.900 znakova**
(recept rođen u s08/s09 za `xray.js`, prenosiv na bilo koji veliki fajl).
Sva tri fajla iznad su 2,5–3× iznad tog praga.

**Pravilo:** ako je sesija bila obimna (više od jedne veće teme), pretpostavi
da će session dokument preći prag PRE nego što počneš pisanje, ne posle
prvog neuspelog pokušaja. Deli pisanje na 2–3 `cat >>` bloka (prvi `cat >`,
ostali `cat >>`, isti fajl), svaki prikazan i OK-ovan kao zasebna komanda po
protokolu — ne kao jedan džinovski heredoc.

## 3. Verifikacija posle pisanja

Posle svakog bloka: `wc -l` (raste li fajl kako se očekuje) i na kraju
`grep -c "^## "` (broj sekcija — potvrđuje da nijedan blok nije duplirao ili
progutao sadržaj). Ne pretpostaviti da je upis prošao samo zato što komanda
nije vratila grešku — heredoc koji je isečen usred puta (bag s08) prošao je
bez ijedne poruke o grešci.

## 4. Poznat rizik: `&&` lanac i "očekivan" nenulti exit kod

**Najčešća, ponovo dokazana greška.** Neke komande vraćaju exit kod 1 kad je
ISHOD potpuno u redu — samo forma odgovora izgleda kao "neuspeh":
- `grep -c "uzorak" fajl` vraća **exit 1 kad je broj poklapanja 0** — čak i
  kad je "0 poklapanja" tačno ono što se nadalo (npr. potvrda da je stari
  string potpuno uklonjen).
- `diff stari novi` vraća **exit 1 kad se fajlovi razlikuju** — što je
  očekivano posle svake namerne izmene.

Oba tiho prekidaju `komanda1 && komanda2 && komanda3` lanac na tom mestu.
Naredni koraci u istom lancu (tipično `git commit && git push`) se **uopšte
ne izvrše**, a izlaz do te tačke izgleda potpuno uredan — nema poruke o
grešci, samo lanac stane.

**Dokazano se desilo dvaput:**
- s08 (27. jun): `grep -c` u proveri (broj poklapanja 0, ispravno) prekinuo
  lanac pre nego što su ostale provere stigle da se izvrše.
- s17 (24. jul): `diff` pre/posle izmene (fajlovi različiti, ispravno)
  prekinuo lanac pre `git commit && git push` — commit/push su morali da se
  ponove ručno kad se primetilo da working tree nije čist.

**Pravilo:** komande koje SLUŽE ZA PROVERU (grep -c, diff, test) ne stavljati
u isti `&&` lanac sa komandama koje IZVRŠAVAJU akciju (commit, push, upis).
Razdvojiti sa `;` ili u posebne pozive — svaki deo ide bez obzira na exit
kod prethodnog. Provera i akcija idu u odvojenim, pojedinačno OK-ovanim
komandama.

## 5. Poznat rizik: re-otkrivanje već dokumentovane činjenice

Onboarding (čitanje README-a i poslednjih sesija) garantuje da je činjenica
PROŠLA kroz kontekst — ne garantuje da će biti PRIMENJENA u trenutku kad
zatreba. Konkretan primer (4. jul): mešani escape oblici u `app.js`
dokumentovani su na šest mesta (README + s06, s09, s10, s11, s12). Ipak je,
u kasnijoj sesiji, pokrenuto `cat -A` istraživanje uživo "da se vidi kako", i
predloženo Flaviju da se zajedno odluči pristup — kao da odluka nije već
doneta.

**Pravilo:** kad se naiđe na problem koji "zvuči poznato", PRVI korak je
`grep` kroz README i `docs/sessions/` za ključne reči problema — PRE
predlaganja istraživanja uživo ili traženja nove odluke od Flavija. Ako grep
pogodi postojeću odluku, primeni je i navedi izvor (npr. "po s11, radim X").
Ne nuditi opcije za nešto što je već rešeno — to obesmišljava dokumentaciju
(princip potvrđen u s20: "dokumentovana odluka nije predmet ponovnog
glasanja").

## 6. Poznat rizik: sandbox/server zabuna posle prekida veze

Ako se tool poziv prekine usred dugog zadatka (npr. dugačak test skript),
akcija može biti IZVRŠENA na disku iako se izlaz nije vratio u kontekst.
Fajl postoji; trag o njegovom nastanku ne postoji u tekućem razgovoru.

**Pravilo:** prva pretpostavka mora biti NAJJEDNOSTAVNIJE objašnjenje —
sopstveni rad izgubljen iz konteksta usled prekida — nikad egzotična
hipoteza (npr. paralelna sesija, tuđi rad, "druga ličnost"). Flavio nikad ne
radi paralelno na dva uređaja; sandbox je isključivo Claudeov. Odbrana već
uspostavljena: `~/SANDBOX_LOG.md` (append PRE svake akcije) + header u
svakoj skripti (`# xpong sNN · datum · svrha · Claude`). Ova greška se
jednom dogodila (s18→ispravljeno u s19) i zabrinula je Flavija — zapisano
ovde da se rezonovanje, ne samo odbrana, ponovo primeni ako se okolnosti
ponove.

## 7. Redosled zatvaranja sesije (checklist)

1. Napiši `session_NN.md` (§2–3), verifikuj.
2. Ažuriraj README ako se nešto trajno promenilo (videti `KAKO-README.md`).
3. `git add` + `git commit` + `git push` — kao ODVOJENA komanda od bilo koje
   provere (§4), za oba repoa ako je oba diran.
4. Sveži `git status` na kraju (ne inferisati čistoću iz izlaza prethodnog
   koraka).
5. Obriši privremene bekape u `/tmp/`.

## 8. Poznati slučajevi — ledger

| Slučaj | Sesija | Uzrok | Pravilo |
|---|---|---|---|
| `grep -c` prekinuo `&&` lanac pre ostatka provere | s08 | Exit 1 na broju poklapanja 0 (ispravan ishod) | §4 — provera i akcija u odvojenim komandama |
| `diff` prekinuo `&&` lanac pre commit/push | s17 | Exit 1 na razlici fajlova (očekivano posle izmene) | §4 — isto |
| Re-otkrivanje mešanih escape oblika uživo, uprkos 6 zapisa | s16→dijagnostikovano 4. jul | Onboarding pročitan, ali činjenica nije primenjena u trenutku odluke | §5 — grep pre predlaganja istraživanja |
| Sandbox fajlovi proglašeni "tuđim" umesto sopstvenim izgubljenim radom | s18→ispravljeno s19 | Prekid veze u tool pozivu; posegnuto za egzotičnom hipotezom | §6 — najjednostavnije objašnjenje prvo |

---

*Flavio & Claude · xpong · KAKO-Session.md · 27. jul 2026.*
